"""Capstone runner used by the demo and the eval gate's building blocks."""

from __future__ import annotations

from collections.abc import Sequence

from workshop.agent.loop import run_agent
from workshop.evalkit.cases import HAPPY_FINAL, HAPPY_QUESTION, happy_turns
from workshop.models import Approval, ModelTurn, RunResult
from workshop.providers.fake import FakeProvider


def run_shift_assistant(
    question: str,
    turns: Sequence[ModelTurn],
    *,
    cap_usd: float = 0.01,
    max_steps: int = 6,
    approval: Approval | None = None,
    latency_cap_ms: int = 60_000,
) -> RunResult:
    return run_agent(
        provider=FakeProvider(turns),
        question=question,
        cap_usd=cap_usd,
        max_steps=max_steps,
        approval=approval,
        latency_cap_ms=latency_cap_ms,
    )


def demo_result() -> RunResult:
    return run_shift_assistant(HAPPY_QUESTION, happy_turns())


__all__ = ["HAPPY_FINAL", "HAPPY_QUESTION", "demo_result", "run_shift_assistant"]
