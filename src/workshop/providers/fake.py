"""Deterministic provider. It replays a script and does not read the prompt."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from workshop.models import ModelTurn
from workshop.providers.base import ProviderExhausted


class FakeProvider:
    def __init__(self, turns: Sequence[ModelTurn]) -> None:
        self._turns = list(turns)
        self.calls = 0

    def complete(self, messages: Sequence[Mapping[str, str]]) -> ModelTurn:
        del messages
        if self.calls >= len(self._turns):
            raise ProviderExhausted("fake provider script has no further turn")
        turn = self._turns[self.calls]
        self.calls += 1
        return turn
