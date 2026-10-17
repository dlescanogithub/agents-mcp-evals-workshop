"""Cassette files store a fake-provider script. They are not vendor recordings."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path

from workshop.models import ModelTurn
from workshop.providers.fake import FakeProvider


def _arguments(raw: object) -> dict[str, object]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("cassette arguments must be an object")
    return {str(key): value for key, value in raw.items()}


def _int_field(raw: Mapping[str, object], name: str, default: int) -> int:
    value = raw.get(name, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"cassette field {name} must be an integer")
    return value


def turns_from_payload(payload: Mapping[str, object]) -> tuple[ModelTurn, ...]:
    raw_turns = payload.get("turns")
    if not isinstance(raw_turns, list):
        raise ValueError("cassette must contain a turns list")
    turns: list[ModelTurn] = []
    for item in raw_turns:
        if not isinstance(item, dict):
            raise ValueError("each cassette turn must be an object")
        kind = item.get("kind")
        if kind not in {"tool", "final"}:
            raise ValueError("cassette turn kind must be tool or final")
        turns.append(
            ModelTurn(
                kind=kind,
                tool_name=str(item.get("tool_name", "")),
                arguments=_arguments(item.get("arguments")),
                text=str(item.get("text", "")),
                simulated_input_tokens=_int_field(item, "simulated_input_tokens", 12),
                simulated_output_tokens=_int_field(item, "simulated_output_tokens", 8),
                simulated_latency_ms=_int_field(item, "simulated_latency_ms", 5),
            )
        )
    return tuple(turns)


def load_cassette(path: Path) -> FakeProvider:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("cassette root must be an object")
    return FakeProvider(turns_from_payload({str(key): value for key, value in raw.items()}))


def dump_turns(turns: Sequence[ModelTurn]) -> dict[str, object]:
    return {
        "provider": "fake",
        "note": "simulated script, not a recorded vendor response",
        "turns": [
            {
                "kind": turn.kind,
                "tool_name": turn.tool_name,
                "arguments": dict(turn.arguments),
                "text": turn.text,
                "simulated_input_tokens": turn.simulated_input_tokens,
                "simulated_output_tokens": turn.simulated_output_tokens,
                "simulated_latency_ms": turn.simulated_latency_ms,
            }
            for turn in turns
        ],
    }


def save_cassette(path: Path, turns: Sequence[ModelTurn]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dump_turns(turns), indent=2, sort_keys=True) + "\n", encoding="utf-8")
