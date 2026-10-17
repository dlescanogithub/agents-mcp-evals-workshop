"""Reference stop policy for the module 1 exercise.

The production loop applies the step cap before a call. This function classifies
a turn the loop already received, which is what the exercise asks for.
"""

from __future__ import annotations

from workshop.models import ModelTurn


def choose_stop_reason(turn: ModelTurn, steps: int, max_steps: int) -> str | None:
    """Return "final", "max_steps", or None to keep going.

    A final answer wins even when the step count is also at the cap.
    """

    if turn.kind == "final":
        return "final"
    if steps >= max_steps:
        return "max_steps"
    return None
