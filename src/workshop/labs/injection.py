"""Synthetic prompt-injection follower. It is a lab fixture, not a model."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from workshop.models import ModelTurn
from workshop.providers.base import Provider

INSTRUCTION_MARK = "Ignore previous instructions"


def looks_like_instruction(text: str) -> bool:
    """Keyword label for the lab. This is not a security boundary."""

    return INSTRUCTION_MARK.casefold() in text.casefold()


class InjectionFollower:
    """If untrusted tool text contains the lab phrase, request a stock write once."""

    def __init__(self, inner: Provider) -> None:
        self._inner = inner
        self.armed = False

    def complete(self, messages: Sequence[Mapping[str, str]]) -> ModelTurn:
        blob = "\n".join(message.get("content", "") for message in messages)
        if looks_like_instruction(blob) and not self.armed:
            self.armed = True
            return ModelTurn(
                kind="tool",
                tool_name="inventory.adjust",
                arguments={"sku": "CD-100", "delta": -12},
            )
        return self._inner.complete(messages)
