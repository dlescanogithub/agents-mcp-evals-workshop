"""Simulated money and latency accounting.

The price constant is simulated. It is not a vendor price and it is not an estimate
of a real invoice.
"""

from __future__ import annotations

SIMULATED_USD_PER_TOKEN = 0.000002
MAX_CALL_RESERVE_USD = 0.0001


def allow_model_call(*, spent_usd: float, next_call_usd: float, cap_usd: float) -> bool:
    """True when another call's declared cost still fits under the cap."""

    if spent_usd < 0 or next_call_usd < 0 or cap_usd < 0:
        raise ValueError("money values must be >= 0")
    return spent_usd + next_call_usd <= cap_usd + 1e-12


def turn_cost_usd(*, input_tokens: int, output_tokens: int) -> float:
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts must be >= 0")
    return (input_tokens + output_tokens) * SIMULATED_USD_PER_TOKEN
