"""Bounded retries. Attempts have a ceiling and the backoff delay has a cap."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class RetryableError(Exception):
    """A caller may try again. Anything else propagates immediately."""


def delay_seconds(attempt: int, *, base: float, backoff_cap: float) -> float:
    """Delay after a failed attempt. `attempt` is 1-based. Never above `backoff_cap`."""

    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    if base < 0 or backoff_cap < 0:
        raise ValueError("delays must be >= 0")
    growth = base * (2 ** (attempt - 1))
    return float(min(growth, backoff_cap))


def call_with_retry(
    fn: Callable[[], T],
    *,
    max_attempts: int,
    base_delay_s: float,
    backoff_cap_s: float,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[T, int]:
    """Return (value, attempts). Retry only RetryableError, at most max_attempts."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    last: RetryableError | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(), attempt
        except RetryableError as exc:
            last = exc
            if attempt == max_attempts:
                break
            sleep(delay_seconds(attempt, base=base_delay_s, backoff_cap=backoff_cap_s))
    assert last is not None
    raise last
