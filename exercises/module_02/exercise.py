"""Module 2 exercise. Typed arguments and a human grant for writes."""

from __future__ import annotations

from collections.abc import Mapping

from workshop.models import Approval
from workshop.tools.auth import Decision
from workshop.tools.specs import ToolSpec


def authorize_tool(spec: ToolSpec, arguments: Mapping[str, object], approval: Approval) -> Decision:
    """Reason codes: ok, missing_argument, unknown_argument, bad_type, needs_human_approval.

    A bool is not an integer. A grant for a different tool does not authorize this one.
    """

    raise NotImplementedError("module 2: validate arguments and the human gate")
