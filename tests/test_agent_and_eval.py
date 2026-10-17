"""Agent loop, tool gate, golden eval, and the forced red regression."""

from __future__ import annotations

from pathlib import Path

import pytest

from workshop.agent.loop import run_agent
from workshop.agent.stopping import choose_stop_reason
from workshop.domain import fresh_state
from workshop.evalkit.cases import cassette_path, happy_turns
from workshop.evalkit.gate import run_gate, run_regression
from workshop.evalkit.invariants import failed_invariants
from workshop.evalkit.judge import calibrate, literal_judge
from workshop.models import Approval, Effect, ModelTurn, RunResult
from workshop.providers.base import ProviderExhausted
from workshop.providers.fake import FakeProvider
from workshop.retries import RetryableError
from workshop.tools.execute import execute
from workshop.tools.specs import INVENTORY_ADJUST, INVENTORY_LOOKUP
from workshop.tracing import MemoryTrace


def test_reference_stop_policy() -> None:
    assert choose_stop_reason(ModelTurn(kind="final", text="x"), 4, 4) == "final"
    assert (
        choose_stop_reason(
            ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"}),
            1,
            4,
        )
        is None
    )


def test_unapproved_write_does_not_change_stock() -> None:
    state = fresh_state()
    before = state.items["CD-100"].on_hand
    state, effect, text = execute(
        state,
        "inventory.adjust",
        {"sku": "CD-100", "delta": -1},
        Approval(frozenset(), ""),
    )
    assert effect.kind == "blocked"
    assert state.items["CD-100"].on_hand == before
    assert "needs_human_approval" in text
    state, effect, _text = execute(
        state,
        "inventory.adjust",
        {"sku": "CD-100", "delta": -1},
        Approval(frozenset({"inventory.adjust"}), "shift-lead"),
    )
    assert effect.kind == "write"
    assert state.items["CD-100"].on_hand == before - 1


def test_bad_arguments_do_not_run() -> None:
    state = fresh_state()
    state, effect, _text = execute(state, "inventory.lookup", {"sku": 1}, Approval(frozenset(), ""))
    assert effect.kind == "blocked"
    state, effect, _text = execute(state, "notify.email", {"to": "x"}, Approval(frozenset(), ""))
    assert effect.detail == "unknown_tool"
    state, effect, text = execute(state, "inventory.lookup", {"sku": "CD-999"}, Approval(frozenset(), ""))
    assert effect.kind == "read"
    assert "unknown sku" in text
    state, effect, text = execute(state, "notes.search", {"query": "no-such"}, Approval(frozenset(), ""))
    assert "no notes matched" in text


def test_bool_delta_is_rejected_even_with_a_grant() -> None:
    _state, effect, _text = execute(
        fresh_state(),
        "inventory.adjust",
        {"sku": "CD-100", "delta": True},
        Approval(frozenset({"inventory.adjust"}), "shift-lead"),
    )
    assert effect.detail == "bad_type"


def test_happy_path_trace_and_budget_stop() -> None:
    trace = MemoryTrace()
    result = run_agent(
        provider=FakeProvider(happy_turns()),
        question="Where is CD-240?",
        trace=trace,
    )
    assert result.stop_reason == "final"
    assert result.stock_unchanged
    assert result.model_calls == 3
    assert len(trace.events) == 3
    assert result.spent_usd > 0
    starved = run_agent(
        provider=FakeProvider(happy_turns()),
        question="Where is CD-240?",
        cap_usd=0,
    )
    assert starved.stop_reason == "budget"
    assert starved.model_calls == 0


def test_max_steps_and_provider_errors() -> None:
    tools = tuple(
        ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"}) for _ in range(5)
    )
    capped = run_agent(provider=FakeProvider(tools), question="loop", max_steps=2)
    assert capped.stop_reason == "max_steps"
    assert capped.model_calls == 2

    class Endless:
        def complete(self, messages: object) -> ModelTurn:
            del messages
            return ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"})

    ceiling = run_agent(provider=Endless(), question="loop", max_steps=10_000)
    assert ceiling.stop_reason == "safety_ceiling"

    exhausted = run_agent(provider=FakeProvider(()), question="empty")
    assert exhausted.stop_reason == "provider_exhausted"

    class AlwaysRetry:
        def complete(self, messages: object) -> ModelTurn:
            del messages
            raise RetryableError("still down")

    slept: list[float] = []
    failed = run_agent(
        provider=AlwaysRetry(),
        question="retry",
        max_attempts=3,
        sleep=slept.append,
    )
    assert failed.stop_reason == "provider_error"
    assert slept == [0.01, 0.02]


def test_flaky_provider_recovers_inside_the_loop() -> None:
    class Flaky:
        def __init__(self) -> None:
            self.calls = 0

        def complete(self, messages: object) -> ModelTurn:
            del messages
            self.calls += 1
            if self.calls == 1:
                raise RetryableError("once")
            return ModelTurn(kind="final", text="recovered")

    result = run_agent(provider=Flaky(), question="retry", sleep=lambda _delay: None)
    assert result.final_text == "recovered"
    assert result.model_calls == 1


def test_gate_is_green_and_regression_is_red() -> None:
    report = run_gate()
    assert report.failed == 0
    assert {item.case_id for item in report.results} == {
        "shift_lookup",
        "shift_lookup_swapped",
        "missing_sku",
        "unapproved_adjust",
        "injection_blocked",
        "budget_stop",
    }
    case_result, run = run_regression()
    assert case_result.passed is False
    assert run.stock_unchanged is False
    assert "no_harmful_effect" in case_result.failed_invariants
    names = failed_invariants(
        RunResult(
            final_text="bin B-1",
            stop_reason="provider_exhausted",
            steps=1,
            model_calls=1,
            effects=[Effect("notify.email", "read", "sent")],
            spent_usd=2,
            latency_ms=10,
            latency_cap_ms=1,
            stock_unchanged=True,
        ),
        required_facts=("missing",),
        cap_usd=0.01,
        forbid_writes=True,
    )
    assert "cost_within_cap" in names
    assert "latency_within_cap" in names
    assert "facts_present" in names
    assert "no_unapproved_external" in names
    assert "stopped" in names


def test_claim_mismatch_and_calibration() -> None:
    lied = RunResult(
        final_text="stock updated",
        stop_reason="final",
        steps=1,
        model_calls=1,
        effects=[],
        spent_usd=0,
        latency_ms=0,
        latency_cap_ms=10,
        stock_unchanged=True,
    )
    assert "claim_mismatch" in failed_invariants(lied, required_facts=(), cap_usd=1, forbid_writes=True)
    report = calibrate()
    assert report.items == 6
    assert report.agreements == 5
    assert report.disagreements == 1
    assert literal_judge("located in B-1", "bin B-1") is False
    assert cassette_path().is_file()
    assert happy_turns()[0].tool_name == "inventory.lookup"


def test_specs_are_the_ones_the_lesson_names() -> None:
    assert INVENTORY_LOOKUP.effect == "read"
    assert INVENTORY_ADJUST.effect == "write"


def test_bad_cassette(tmp_path: Path) -> None:
    from workshop.providers.cassette import load_cassette

    path = tmp_path / "bad.json"
    path.write_text('{"turns": [{"kind": "nope"}]}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_cassette(path)
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError):
        load_cassette(path)


def test_provider_exhausted_type() -> None:
    with pytest.raises(ProviderExhausted):
        FakeProvider(()).complete(())
