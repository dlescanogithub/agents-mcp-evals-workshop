"""Block network sockets for the whole suite. Subprocess pipes stay allowed."""

from __future__ import annotations

import socket

import pytest


def _refuse(*args: object, **kwargs: object) -> object:
    del kwargs
    raise RuntimeError(f"network disabled in tests: {args}")


@pytest.fixture(autouse=True)
def block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket.socket, "connect", _refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", _refuse)
    monkeypatch.setattr(socket, "create_connection", _refuse)
