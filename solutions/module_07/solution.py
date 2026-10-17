"""Module 7 answer. Fake provider, human gate, simulated budget. Live stays off."""

from __future__ import annotations

from collections.abc import Sequence

from workshop.agent.loop import run_agent
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
