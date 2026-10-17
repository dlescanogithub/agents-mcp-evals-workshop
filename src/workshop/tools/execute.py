"""Run a tool against a depot copy. A denied call does not touch stock."""

from __future__ import annotations

from collections.abc import Mapping

from workshop.domain import DepotState
from workshop.models import Approval, Effect
from workshop.tools.auth import authorize_tool
from workshop.tools.specs import CATALOG


def _lookup(state: DepotState, sku: str) -> tuple[str, bool]:
    item = state.items.get(sku)
    if item is None:
        return f"unknown sku {sku}", True
    return f"{item.sku} {item.name} on_hand={item.on_hand} bin={item.bin}", False


def _search(state: DepotState, query: str) -> str:
    needle = query.casefold()
    hits = [
        note
        for note in state.notes
        if needle in note.sku.casefold() or needle in note.text.casefold() or needle in note.id.casefold()
    ]
    if not hits:
        return "no notes matched"
    return "\n".join(f"{note.id} {note.sku}: {note.text}" for note in hits)


def execute(
    state: DepotState,
    tool_name: str,
    arguments: Mapping[str, object],
    approval: Approval,
    *,
    trust_writes: bool = False,
) -> tuple[DepotState, Effect, str]:
    """Return the next state, the effect, and text that can be shown to the model.

    `trust_writes` exists for the injection lab. The default path never sets it.
    """

    spec = CATALOG.get(tool_name)
    if spec is None:
        effect = Effect(tool=tool_name, kind="blocked", detail="unknown_tool")
        return state, effect, f"blocked: unknown_tool {tool_name}"
    decision = authorize_tool(spec, arguments, approval)
    if trust_writes and spec.effect == "write" and decision.reason == "needs_human_approval":
        decision_allowed = True
        reason = "trusted_model"
    else:
        decision_allowed = decision.allowed
        reason = decision.reason
    if not decision_allowed:
        effect = Effect(tool=tool_name, kind="blocked", detail=reason)
        return state, effect, f"blocked: {reason}"
    if spec.name == "inventory.lookup":
        sku = arguments["sku"]
        if not isinstance(sku, str):
            effect = Effect(tool=tool_name, kind="blocked", detail="bad_type")
            return state, effect, "blocked: bad_type"
        text, missing = _lookup(state, sku)
        detail = "missing" if missing else "found"
        return state, Effect(tool=tool_name, kind="read", detail=detail), text
    if spec.name == "notes.search":
        query = arguments["query"]
        if not isinstance(query, str):
            effect = Effect(tool=tool_name, kind="blocked", detail="bad_type")
            return state, effect, "blocked: bad_type"
        return state, Effect(tool=tool_name, kind="read", detail="notes"), _search(state, query)
    sku = arguments["sku"]
    delta = arguments["delta"]
    if not isinstance(sku, str) or isinstance(delta, bool) or not isinstance(delta, int):
        effect = Effect(tool=tool_name, kind="blocked", detail="bad_type")
        return state, effect, "blocked: bad_type"
    item = state.items.get(sku)
    if item is None:
        effect = Effect(tool=tool_name, kind="blocked", detail="unknown_sku")
        return state, effect, f"blocked: unknown sku {sku}"
    item.on_hand += delta
    text = f"adjusted {sku} by {delta}; on_hand={item.on_hand}"
    return state, Effect(tool=tool_name, kind="write", detail=text), text
