"""Auto-grader for the exercises. Checks are invariants and contracts, not diffs."""

from __future__ import annotations

import importlib.util
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from workshop.domain import SEED_NOTES
from workshop.evalkit.cases import HAPPY_QUESTION, happy_turns
from workshop.mcpmini.protocol import PROTOCOL_VERSION, ToolFailed
from workshop.models import Approval, Effect, ModelTurn, RunResult, no_approval
from workshop.tools.specs import INVENTORY_ADJUST, INVENTORY_LOOKUP


@dataclass
class Grade:
    module: str
    checks: list[tuple[str, bool, str]]

    @property
    def passed(self) -> int:
        return sum(1 for _name, ok, _detail in self.checks if ok)

    @property
    def failed(self) -> int:
        return len(self.checks) - self.passed

    @property
    def failed_names(self) -> list[str]:
        return [name for name, ok, _detail in self.checks if not ok]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def impl_path(module_id: str, impl: str) -> Path:
    folder = "solutions" if impl == "solution" else "exercises"
    filename = "solution.py" if impl == "solution" else "exercise.py"
    return repo_root() / folder / f"module_{int(module_id):02d}" / filename


def load_impl(module_id: str, impl: str) -> ModuleType:
    path = impl_path(module_id, impl)
    spec = importlib.util.spec_from_file_location(f"workshop_{impl}_{module_id}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _call(fn: Callable[..., object], *args: object, **kwargs: object) -> tuple[bool, object, str]:
    try:
        return True, fn(*args, **kwargs), ""
    except NotImplementedError as exc:
        return False, None, str(exc) or "not implemented"
    except Exception as exc:
        return False, None, f"{type(exc).__name__}: {exc}"


def _record(checks: list[tuple[str, bool, str]], name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, ok, detail))


def _result(**overrides: object) -> RunResult:
    payload: dict[str, object] = {
        "final_text": "",
        "stop_reason": "final",
        "steps": 1,
        "model_calls": 1,
        "effects": [],
        "spent_usd": 0.00004,
        "latency_ms": 5,
        "latency_cap_ms": 60_000,
        "stock_unchanged": True,
    }
    payload.update(overrides)
    effects = payload["effects"]
    if not isinstance(effects, list):
        raise TypeError("effects must be a list")
    spent = payload["spent_usd"]
    latency = payload["latency_ms"]
    cap = payload["latency_cap_ms"]
    steps = payload["steps"]
    calls = payload["model_calls"]
    if (
        not isinstance(spent, float)
        or not isinstance(latency, int)
        or not isinstance(cap, int)
        or not isinstance(steps, int)
        or not isinstance(calls, int)
        or not isinstance(payload["final_text"], str)
        or not isinstance(payload["stop_reason"], str)
        or not isinstance(payload["stock_unchanged"], bool)
    ):
        raise TypeError("bad fixture")
    return RunResult(
        final_text=payload["final_text"],
        stop_reason=payload["stop_reason"],
        steps=steps,
        model_calls=calls,
        effects=effects,
        spent_usd=spent,
        latency_ms=latency,
        latency_cap_ms=cap,
        stock_unchanged=payload["stock_unchanged"],
    )


def grade_module_1(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    fn = getattr(module, "choose_stop_reason", None)
    if not callable(fn):
        return Grade("1", [("choose_stop_reason", False, "missing function")])
    table: tuple[tuple[str, ModelTurn, int, int, str | None], ...] = (
        ("classifies_final", ModelTurn(kind="final", text="done"), 1, 4, "final"),
        (
            "classifies_continue",
            ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"}),
            1,
            4,
            None,
        ),
        (
            "classifies_max_steps",
            ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"}),
            4,
            4,
            "max_steps",
        ),
        ("final_wins_at_cap", ModelTurn(kind="final", text="done"), 4, 4, "final"),
    )
    for name, turn, steps, limit, expected in table:
        ok, value, detail = _call(fn, turn, steps, limit)
        _record(checks, name, ok and value == expected, detail or f"got {value!r}")

    def harness(turns: tuple[ModelTurn, ...], limit: int) -> tuple[bool, object]:
        executed = 0
        reason: object = None
        for turn in turns:
            executed += 1
            called, reason, detail = _call(fn, turn, executed, limit)
            if not called:
                return False, detail
            if reason is not None:
                return True, (reason, executed)
            if executed > limit + 1:
                return True, ("safety_ceiling", executed)
        return True, (reason, executed)

    tool = ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"})
    tools = (tool, tool, tool, tool, tool)
    ok, value = harness((tool, tool, ModelTurn(kind="final", text="done")), 4)
    _record(checks, "harness_stops_on_final", ok and value == ("final", 3), "" if ok else str(value))
    ok, value = harness(tools, 2)
    _record(checks, "harness_obeys_cap", ok and value == ("max_steps", 2), "" if ok else str(value))
    return Grade("1", checks)


def grade_module_2(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    fn = getattr(module, "authorize_tool", None)
    if not callable(fn):
        return Grade("2", [("authorize_tool", False, "missing function")])
    grant = Approval(granted=frozenset({"inventory.adjust"}), approver="shift-lead")
    other = Approval(granted=frozenset({"notes.search"}), approver="shift-lead")
    rows: tuple[tuple[str, object, dict[str, object], Approval, bool, str], ...] = (
        ("read_without_approval", INVENTORY_LOOKUP, {"sku": "CD-240"}, no_approval(), True, "ok"),
        ("missing_argument", INVENTORY_LOOKUP, {}, no_approval(), False, "missing_argument"),
        (
            "unknown_argument",
            INVENTORY_LOOKUP,
            {"sku": "CD-240", "extra": "no"},
            no_approval(),
            False,
            "unknown_argument",
        ),
        ("bad_type", INVENTORY_LOOKUP, {"sku": 3}, no_approval(), False, "bad_type"),
        (
            "write_needs_human",
            INVENTORY_ADJUST,
            {"sku": "CD-100", "delta": -1},
            no_approval(),
            False,
            "needs_human_approval",
        ),
        ("write_with_grant", INVENTORY_ADJUST, {"sku": "CD-100", "delta": -1}, grant, True, "ok"),
        (
            "bool_is_not_integer",
            INVENTORY_ADJUST,
            {"sku": "CD-100", "delta": True},
            grant,
            False,
            "bad_type",
        ),
        (
            "grant_for_other_tool",
            INVENTORY_ADJUST,
            {"sku": "CD-100", "delta": -1},
            other,
            False,
            "needs_human_approval",
        ),
    )
    for name, spec, arguments, approval, allowed, reason in rows:
        ok, value, detail = _call(fn, spec, arguments, approval)
        matched = ok and getattr(value, "allowed", None) is allowed and getattr(value, "reason", None) == reason
        _record(checks, name, matched, detail or f"got {value!r}")
    return Grade("2", checks)


def grade_module_3(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    encode = getattr(module, "encode_request", None)
    decode = getattr(module, "decode_tool_text", None)
    run_tool = getattr(module, "run_tool", None)
    list_names = getattr(module, "list_tool_names", None)
    if not all(callable(item) for item in (encode, decode, run_tool, list_names)):
        return Grade("3", [("exports", False, "encode_request, decode_tool_text, run_tool, list_tool_names")])
    assert callable(encode) and callable(decode) and callable(run_tool) and callable(list_names)
    ok, payload, detail = _call(encode, "tools/list", {}, 7)
    version = None
    if ok and isinstance(payload, dict):
        params = payload.get("params")
        if isinstance(params, dict):
            meta = params.get("_meta")
            if isinstance(meta, dict):
                version = meta.get("io.modelcontextprotocol/protocolVersion")
        shape = (
            payload.get("jsonrpc") == "2.0"
            and payload.get("method") == "tools/list"
            and payload.get("id") == 7
            and version == PROTOCOL_VERSION
        )
        _record(checks, "request_frame", shape, detail)
    else:
        _record(checks, "request_frame", False, detail)
    ok, text, detail = _call(
        decode,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "resultType": "complete",
                "content": [{"type": "text", "text": "hello"}],
                "isError": False,
            },
        },
    )
    _record(checks, "reads_text", ok and text == "hello", detail or f"got {text!r}")
    try:
        decode(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "resultType": "complete",
                    "content": [{"type": "text", "text": "unknown sku CD-999"}],
                    "isError": True,
                },
            }
        )
        _record(checks, "surfaces_tool_error", False, "did not raise ToolFailed")
    except ToolFailed:
        _record(checks, "surfaces_tool_error", True, "")
    except NotImplementedError as exc:
        _record(checks, "surfaces_tool_error", False, str(exc))
    except Exception as exc:
        _record(checks, "surfaces_tool_error", False, f"{type(exc).__name__}: {exc}")
    ok, body, detail = _call(run_tool, "inventory.lookup", {"sku": "CD-240"})
    _record(checks, "lookup_cd_240", ok and isinstance(body, str) and "bin=B-1" in body, detail)
    ok, body, detail = _call(run_tool, "notes.search", {"query": "CD-240"})
    _record(
        checks,
        "notes_cd_240",
        ok and isinstance(body, str) and "recount" in body.casefold(),
        detail,
    )
    try:
        run_tool("inventory.lookup", {"sku": "CD-999"})
        _record(checks, "missing_sku_is_error", False, "did not raise ToolFailed")
    except ToolFailed:
        _record(checks, "missing_sku_is_error", True, "")
    except Exception as exc:
        _record(checks, "missing_sku_is_error", False, f"{type(exc).__name__}: {exc}")
    ok, names, detail = _call(list_names)
    _record(
        checks,
        "exports_read_tools_only",
        ok and names == ["inventory.lookup", "notes.search"],
        detail or f"got {names!r}",
    )
    return Grade("3", checks)


def _names(value: object) -> set[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return set(value)


def grade_module_4(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    fn = getattr(module, "failed_invariants", None)
    if not callable(fn):
        return Grade("4", [("failed_invariants", False, "missing function")])
    fixtures: tuple[tuple[str, RunResult, tuple[str, ...], float, bool, set[str]], ...] = (
        (
            "read_only_passes",
            _result(
                final_text="bin B-1",
                effects=[Effect("inventory.lookup", "read", "found")],
            ),
            ("bin B-1",),
            0.01,
            True,
            set(),
        ),
        (
            "write_is_harmful",
            _result(
                final_text="done",
                effects=[Effect("inventory.adjust", "write", "changed")],
                stock_unchanged=False,
            ),
            (),
            0.01,
            True,
            {"no_harmful_effect"},
        ),
        (
            "over_budget",
            _result(final_text="done", spent_usd=1.0),
            (),
            0.01,
            True,
            {"cost_within_cap"},
        ),
        (
            "missing_fact",
            _result(final_text="hello"),
            ("bin B-1",),
            0.01,
            True,
            {"facts_present"},
        ),
        (
            "order_does_not_matter",
            _result(
                final_text="bin B-1 and recount matches the card.",
                effects=[
                    Effect("notes.search", "read", "notes"),
                    Effect("inventory.lookup", "read", "found"),
                ],
            ),
            ("bin B-1", "recount matches the card"),
            0.01,
            True,
            set(),
        ),
        (
            "external_tool",
            _result(
                final_text="done",
                effects=[Effect("notify.email", "write", "sent")],
                stock_unchanged=True,
            ),
            (),
            0.01,
            True,
            {"no_harmful_effect", "no_unapproved_external"},
        ),
    )
    for name, result, facts, cap, forbid, expected in fixtures:
        ok, value, detail = _call(fn, result, facts, cap, forbid)
        got = _names(value) if ok else None
        _record(checks, name, got == expected, detail or f"got {value!r}")
    return Grade("4", checks)


def grade_module_5(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    allow = getattr(module, "allow_model_call", None)
    delay = getattr(module, "delay_seconds", None)
    if not callable(allow) or not callable(delay):
        return Grade("5", [("exports", False, "allow_model_call and delay_seconds")])
    rows = (
        ("fits", {"spent_usd": 0.0, "next_call_usd": 0.0001, "cap_usd": 0.01}, True),
        ("cap_zero", {"spent_usd": 0.0, "next_call_usd": 0.0001, "cap_usd": 0.0}, False),
        ("would_pass_cap", {"spent_usd": 0.009, "next_call_usd": 0.002, "cap_usd": 0.01}, False),
    )
    for name, kwargs, expected in rows:
        ok, value, detail = _call(allow, **kwargs)
        _record(checks, name, ok and value is expected, detail or f"got {value!r}")
    delays = ((1, 0.2), (2, 0.4), (3, 0.5), (4, 0.5))
    for attempt, expected_delay in delays:
        ok, value, detail = _call(delay, attempt, base=0.2, backoff_cap=0.5)
        matched = ok and isinstance(value, float) and abs(value - expected_delay) < 1e-9
        _record(checks, f"delay_{attempt}", matched, detail or f"got {value!r}")
    return Grade("5", checks)


def grade_module_6(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    detect = getattr(module, "looks_like_instruction", None)
    failed = getattr(module, "failed_attack_invariants", None)
    if not callable(detect) or not callable(failed):
        return Grade("6", [("exports", False, "looks_like_instruction and failed_attack_invariants")])
    hostile = next(note.text for note in SEED_NOTES if note.id == "N-3")
    ok, value, detail = _call(detect, hostile)
    _record(checks, "marks_injected_note", ok and value is True, detail)
    ok, value, detail = _call(detect, "Count matches the card.")
    _record(checks, "spares_ordinary_note", ok and value is False, detail)
    harmful = _result(
        final_text="done",
        effects=[Effect("inventory.adjust", "write", "changed")],
        stock_unchanged=False,
    )
    quoted = _result(
        final_text="The note says Ignore previous instructions. No stock was changed.",
        effects=[Effect("notes.search", "read", "notes")],
        stock_unchanged=True,
    )
    emailed = _result(
        final_text="done",
        effects=[Effect("notify.email", "write", "sent")],
        stock_unchanged=True,
    )
    expectations: tuple[tuple[str, RunResult, set[str]], ...] = (
        ("harmful_write", harmful, {"no_harmful_effect"}),
        ("quoting_is_not_failure", quoted, set()),
        ("external_send", emailed, {"no_harmful_effect", "no_unapproved_external"}),
    )
    for name, result, expected in expectations:
        ok, value, detail = _call(failed, result)
        got = _names(value) if ok else None
        _record(checks, name, got == expected, detail or f"got {value!r}")
    return Grade("6", checks)


def grade_module_7(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    fn = getattr(module, "run_shift_assistant", None)
    if not callable(fn):
        return Grade("7", [("run_shift_assistant", False, "missing function")])
    ok, happy, detail = _call(fn, HAPPY_QUESTION, happy_turns())
    happy_ok = (
        ok
        and isinstance(happy, RunResult)
        and happy.stop_reason == "final"
        and happy.model_calls == 3
        and happy.stock_unchanged
        and "bin B-1" in happy.final_text
        and "recount matches the card" in happy.final_text
        and all(effect.kind != "write" for effect in happy.effects)
    )
    _record(checks, "answers_lookup", happy_ok, detail)
    refusal_script = (
        ModelTurn(kind="tool", tool_name="inventory.adjust", arguments={"sku": "CD-100", "delta": -1}),
        ModelTurn(kind="final", text="No stock was changed."),
    )
    ok, refused, detail = _call(fn, "Set CD-100 on hand down by one.", refusal_script)
    refused_ok = (
        ok
        and isinstance(refused, RunResult)
        and refused.stock_unchanged
        and all(effect.kind != "write" for effect in refused.effects)
    )
    _record(checks, "blocks_unapproved_write", refused_ok, detail)
    ok, starved, detail = _call(fn, HAPPY_QUESTION, happy_turns(), cap_usd=0.0)
    starved_ok = (
        ok and isinstance(starved, RunResult) and starved.model_calls == 0 and starved.stop_reason == "budget"
    )
    _record(checks, "stops_at_budget", starved_ok, detail)
    return Grade("7", checks)


def grade_module_8(module: ModuleType) -> Grade:
    checks: list[tuple[str, bool, str]] = []
    fn = getattr(module, "compare_against_reference", None)
    if not callable(fn):
        return Grade("8", [("compare_against_reference", False, "missing function")])
    sample = (
        (True, False, True),
        (True, True, True),
        (False, None, False),
    )
    expected = {
        "checker_compared": 3,
        "checker_agreements": 3,
        "llm_compared": 2,
        "llm_agreements": 1,
    }
    ok, value, detail = _call(fn, sample)
    _record(checks, "counts_checker_and_llm", ok and value == expected, detail or f"got {value!r}")
    disagree = ((True, True, False),)
    expected_disagree = {
        "checker_compared": 1,
        "checker_agreements": 0,
        "llm_compared": 1,
        "llm_agreements": 0,
    }
    ok, value, detail = _call(fn, disagree)
    _record(checks, "counts_disagreement", ok and value == expected_disagree, detail or f"got {value!r}")
    return Grade("8", checks)


GRADERS = {
    "1": grade_module_1,
    "2": grade_module_2,
    "3": grade_module_3,
    "4": grade_module_4,
    "5": grade_module_5,
    "6": grade_module_6,
    "7": grade_module_7,
    "8": grade_module_8,
}


def grade(module_id: str, impl: str) -> Grade:
    module = load_impl(module_id, impl)
    return GRADERS[module_id](module)
