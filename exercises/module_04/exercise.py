"""Module 4 exercise. Score a finished run by invariants, not by tool order."""

from __future__ import annotations

from collections.abc import Sequence

from workshop.models import RunResult


def failed_invariants(
    result: RunResult,
    required_facts: Sequence[str],
    cap_usd: float,
    forbid_writes: bool,
) -> list[str]:
    """Return the ids that failed. Use only these ids:

    no_harmful_effect, cost_within_cap, facts_present, no_unapproved_external.

    A different tool order with the same facts and the same effects passes.
    """

    raise NotImplementedError("module 4: check invariants")
