"""Module 5 answer. The next call has to fit, and the delay cannot grow without a cap."""

from __future__ import annotations


def allow_model_call(*, spent_usd: float, next_call_usd: float, cap_usd: float) -> bool:
    if spent_usd < 0 or next_call_usd < 0 or cap_usd < 0:
        raise ValueError("money values must be >= 0")
    return spent_usd + next_call_usd <= cap_usd + 1e-12


def delay_seconds(attempt: int, *, base: float, backoff_cap: float) -> float:
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    if base < 0 or backoff_cap < 0:
        raise ValueError("delays must be >= 0")
    return float(min(base * (2 ** (attempt - 1)), backoff_cap))
