"""Module 7 exercise. Wire the shift assistant to the fake provider and the tool gate."""

from __future__ import annotations

from collections.abc import Sequence

from workshop.models import Approval, ModelTurn, RunResult


def run_shift_assistant(
    question: str,
    turns: Sequence[ModelTurn],
    *,
    cap_usd: float = 0.01,
    max_steps: int = 6,
    approval: Approval | None = None,
    latency_cap_ms: int = 60_000,
) -> RunResult:
    """Run the scripted assistant. Do not enable a live provider."""

    raise NotImplementedError("module 7: wire the shift assistant")
