"""Module 5 exercise. Admit a model call only if it fits, and cap the backoff."""

from __future__ import annotations


def allow_model_call(*, spent_usd: float, next_call_usd: float, cap_usd: float) -> bool:
    """True when spent + next still fits under the cap."""

    raise NotImplementedError("module 5: enforce the budget")


def delay_seconds(attempt: int, *, base: float, backoff_cap: float) -> float:
    """Delay after a 1-based failed attempt. Double each time. Never above backoff_cap."""

    raise NotImplementedError("module 5: cap the backoff")
