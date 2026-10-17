"""Module 1 answer. Stop on a final answer, otherwise on the step cap."""

from __future__ import annotations

from workshop.models import ModelTurn


def choose_stop_reason(turn: ModelTurn, steps: int, max_steps: int) -> str | None:
    if turn.kind == "final":
        return "final"
    if steps >= max_steps:
        return "max_steps"
    return None
