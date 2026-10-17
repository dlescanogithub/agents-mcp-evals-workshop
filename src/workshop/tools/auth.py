"""Argument checks and the human gate. Approval is a set of tool names, not a prompt line."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from workshop.models import Approval
from workshop.tools.specs import ToolSpec


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def _type_ok(type_name: str, value: object) -> bool:
    if type_name == "string":
        return isinstance(value, str)
    if type_name == "integer":
        return not isinstance(value, bool) and isinstance(value, int)
    return False


def authorize_tool(spec: ToolSpec, arguments: Mapping[str, object], approval: Approval) -> Decision:
    """Validate arguments, then require a human grant for write tools.

    Reason codes: ok, missing_argument, unknown_argument, bad_type, needs_human_approval.
    """

    known = {field.name for field in spec.fields}
    if any(key not in known for key in arguments):
        return Decision(False, "unknown_argument")
    for field in spec.fields:
        if field.name not in arguments:
            if field.required:
                return Decision(False, "missing_argument")
            continue
        if not _type_ok(field.type_name, arguments[field.name]):
            return Decision(False, "bad_type")
    if spec.effect == "write" and spec.name not in approval.granted:
        return Decision(False, "needs_human_approval")
    return Decision(True, "ok")
