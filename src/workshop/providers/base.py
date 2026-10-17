"""Provider protocol. Implementations must be synchronous and side-effect free unless live."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from workshop.models import ModelTurn


class ProviderExhausted(RuntimeError):
    """The script or cassette has no further turn."""


class Provider(Protocol):
    def complete(self, messages: Sequence[Mapping[str, str]]) -> ModelTurn:
        """Return the next scripted or generated turn."""
