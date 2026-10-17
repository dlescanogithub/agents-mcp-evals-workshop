"""Shared run records. Effects are what the eval gate looks at."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class ModelTurn:
    kind: Literal["tool", "final"]
    tool_name: str = ""
    arguments: Mapping[str, object] = field(default_factory=dict)
    text: str = ""
    simulated_input_tokens: int = 12
    simulated_output_tokens: int = 8
    simulated_latency_ms: int = 5


@dataclass(frozen=True)
class Effect:
    tool: str
    kind: Literal["read", "write", "blocked"]
    detail: str


@dataclass(frozen=True)
class Approval:
    granted: frozenset[str]
    approver: str


def no_approval() -> Approval:
    return Approval(granted=frozenset(), approver="")


@dataclass
class RunResult:
    final_text: str
    stop_reason: str
    steps: int
    model_calls: int
    effects: list[Effect]
    spent_usd: float
    latency_ms: int
    latency_cap_ms: int
    stock_unchanged: bool
    error: str = ""
