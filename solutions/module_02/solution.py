"""Module 2 answer. Writes do not run unless the tool name is in the human grant."""

from __future__ import annotations

from collections.abc import Mapping

from workshop.models import Approval
from workshop.tools.auth import Decision
from workshop.tools.specs import ToolSpec


def _type_ok(type_name: str, value: object) -> bool:
    if type_name == "string":
        return isinstance(value, str)
    if type_name == "integer":
        return not isinstance(value, bool) and isinstance(value, int)
    return False


def authorize_tool(spec: ToolSpec, arguments: Mapping[str, object], approval: Approval) -> Decision:
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
