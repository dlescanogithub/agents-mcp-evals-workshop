"""JSONL traces. One JSON object per line. Callers choose the path."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol


class Trace(Protocol):
    def write(self, event: Mapping[str, object]) -> None:
        """Append one event."""


class MemoryTrace:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def write(self, event: Mapping[str, object]) -> None:
        self.events.append(dict(event))


class JsonlTrace:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, event: Mapping[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(dict(event), sort_keys=True, default=str)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        if not isinstance(raw, dict):
            raise ValueError("trace line must be a JSON object")
        events.append({str(key): value for key, value in raw.items()})
    return events
