"""Module 1 exercise. Decide when the agent loop stops."""

from __future__ import annotations

from workshop.models import ModelTurn


def choose_stop_reason(turn: ModelTurn, steps: int, max_steps: int) -> str | None:
    """Return "final", "max_steps", or None.

    A final answer wins when the step count is also at the cap.
    The grader calls this with a turn the loop has already received.
    """

    raise NotImplementedError("module 1: decide when the loop stops")
