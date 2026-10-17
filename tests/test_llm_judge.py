"""Optional LLM judge. The HTTP layer is fake. No live endpoint is called."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from workshop.cli import main
from workshop.evalkit.checker import compare_checker_to_reference, deterministic_checker
from workshop.evalkit.labels import HEADER, summarize_label_csv
from workshop.evalkit.llm_judge import (
    LiveJudgeSettings,
    chat_completions_url,
    load_live_judge_settings,
    public_settings,
    run_llm_judge,
    token_cost,
    urllib_transport,
)

ROOT = Path(__file__).resolve().parents[1]


def _env(**overrides: str) -> dict[str, str]:
    base = {
        "LIVE_MODE": "1",
        "LLM_BASE_URL": "http://llm.example",
        "LLM_MODEL": "example-model",
        "LLM_API_KEY": "test-key",
        "MAX_LIVE_SPEND_USD": "1",
        "LLM_INPUT_USD_PER_TOKEN": "0.000001",
        "LLM_OUTPUT_USD_PER_TOKEN": "0.000002",
        "LLM_PRICE_DATE": "2026-10-17",
    }
    base.update(overrides)
    return base


def _settings() -> LiveJudgeSettings:
    loaded = load_live_judge_settings(_env())
    assert loaded is not None
    return loaded


def test_checker_matches_author_reference_labels() -> None:
    report = compare_checker_to_reference()
    assert report.items == 6
    assert report.agreements == 5
    assert report.disagreements == 1
    assert report.ratio == 5 / 6
    assert deterministic_checker("located in B-1", "bin B-1") is False
    empty = compare_checker_to_reference(())
    assert empty.ratio == 0.0


def test_live_judge_settings_require_every_field() -> None:
    assert load_live_judge_settings({}) is None
    assert load_live_judge_settings(_env(LIVE_MODE="0")) is None
    assert load_live_judge_settings(_env(LLM_API_KEY="")) is None
    assert load_live_judge_settings(_env(MAX_LIVE_SPEND_USD="nope")) is None
    assert load_live_judge_settings(_env(LLM_INPUT_USD_PER_TOKEN="-1")) is None
    loaded = _settings()
    assert loaded.model == "example-model"
    assert loaded.price_date == "2026-10-17"
    shown = public_settings(loaded)
    assert shown["api_key_set"] is True
    assert "test-key" not in str(shown["redacted"])
    assert chat_completions_url("http://llm.example/") == "http://llm.example/chat/completions"


def test_run_llm_judge_uses_the_injected_transport() -> None:
    seen: list[tuple[str, object]] = []

    def transport(url: str, headers: object, payload: object) -> dict[str, object]:
        seen.append((url, payload))
        assert isinstance(headers, dict)
        assert str(headers["authorization"]).startswith("Bearer ")
        return {
            "choices": [{"message": {"content": "pass"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }

    outcome = run_llm_judge("CD-240 is in bin B-1.", "bin B-1", _settings(), transport)
    assert outcome.label == "pass"
    assert outcome.skipped == ""
    assert outcome.spent_usd == pytest.approx(token_cost(_settings(), 10, 5))
    assert seen[0][0] == "http://llm.example/chat/completions"
    body = seen[0][1]
    assert isinstance(body, dict)
    assert body["model"] == "example-model"


def test_zero_cap_does_not_call_transport_and_bad_payloads_are_skipped() -> None:
    def boom(url: str, headers: object, payload: object) -> dict[str, object]:
        raise AssertionError("transport should not be called")

    capped = load_live_judge_settings(_env(MAX_LIVE_SPEND_USD="0"))
    assert capped is not None
    skipped = run_llm_judge("text", "phrase", capped, boom)
    assert skipped.skipped == "spend_cap"
    assert skipped.label is None

    def reply(content: str, usage: object | None = None) -> dict[str, object]:
        payload: dict[str, object] = {"choices": [{"message": {"content": content}}]}
        if usage is not None:
            payload["usage"] = usage
        return payload

    settings = _settings()
    unparsed = run_llm_judge("text", "phrase", settings, lambda _u, _h, _p: reply("maybe"))
    assert unparsed.skipped == "unparsed"
    missing = run_llm_judge("text", "phrase", settings, lambda _u, _h, _p: {"choices": []})
    assert missing.skipped == "unparsed"
    odd = run_llm_judge(
        "text",
        "phrase",
        settings,
        lambda _u, _h, _p: reply("fail", {"prompt_tokens": True, "completion_tokens": 1}),
    )
    assert odd.skipped == "unparsed"
    over = load_live_judge_settings(_env(MAX_LIVE_SPEND_USD="0.0000001"))
    assert over is not None
    priced = run_llm_judge(
        "text",
        "phrase",
        over,
        lambda _u, _h, _p: reply("fail", {"prompt_tokens": 10, "completion_tokens": 5}),
    )
    assert priced.label is None
    assert priced.skipped == "spend_cap"
    assert priced.spent_usd > over.max_spend_usd
    with pytest.raises(ValueError):
        token_cost(settings, -1, 0)


def test_urllib_transport_reads_a_fake_response(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Body:
        def read(self) -> bytes:
            return json.dumps({"ok": True}).encode("utf-8")

        def __enter__(self) -> _Body:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    def fake_urlopen(request: object, timeout: int = 10) -> _Body:
        del timeout
        assert getattr(request, "full_url", "") == "http://llm.example/chat/completions"
        return _Body()

    monkeypatch.setattr("workshop.evalkit.llm_judge.urllib.request.urlopen", fake_urlopen)
    payload = urllib_transport("http://llm.example/chat/completions", {"content-type": "application/json"}, {})
    assert payload == {"ok": True}

    class _List:
        def read(self) -> bytes:
            return b"[]"

        def __enter__(self) -> _List:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    monkeypatch.setattr(
        "workshop.evalkit.llm_judge.urllib.request.urlopen",
        lambda _request, timeout=10: _List(),
    )
    with pytest.raises(RuntimeError):
        urllib_transport("http://llm.example/chat/completions", {}, {})


def test_llm_judge_cli_exits_2_without_config(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for name in (
        "LIVE_MODE",
        "LLM_BASE_URL",
        "LLM_MODEL",
        "LLM_API_KEY",
        "MAX_LIVE_SPEND_USD",
        "LLM_INPUT_USD_PER_TOKEN",
        "LLM_OUTPUT_USD_PER_TOKEN",
        "LLM_PRICE_DATE",
    ):
        monkeypatch.delenv(name, raising=False)
    assert main(["llm-judge"]) == 2
    text = capsys.readouterr().out
    assert "llm_judge=not_configured" in text
    assert "exit_reason=missing_config" in text
    monkeypatch.setenv("LIVE_MODE", "1")
    assert main(["llm-judge"]) == 2


def test_llm_judge_cli_zero_cap_skips_without_http(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for key, value in _env(MAX_LIVE_SPEND_USD="0").items():
        monkeypatch.setenv(key, value)
    assert main(["llm-judge"]) == 1
    assert "llm_judge_skipped=spend_cap" in capsys.readouterr().out


def test_ci_workflow_does_not_call_the_llm_judge() -> None:
    text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "llm-judge" not in text
    assert "LIVE_MODE" not in text
    assert "LLM_API_KEY" not in text
    assert "LLM_BASE_URL" not in text


def test_human_label_template_is_empty_and_summary_counts_filled_rows(tmp_path: Path) -> None:
    template = ROOT / "templates/human_labels.csv"
    assert summarize_label_csv(template) == {
        "data_rows": 0,
        "human_compared": 0,
        "human_agreements": 0,
    }
    path = tmp_path / "labels.csv"
    rows = [
        "1,alpha,pass,,pass,",
        "2,beta,fail,fail,fail,fail",
        "3,gamma,pass,pass,pass,fail",
        "4,delta,pass,pass,,pass",
    ]
    path.write_text(",".join(HEADER) + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    assert summarize_label_csv(path) == {
        "data_rows": 4,
        "human_compared": 2,
        "human_agreements": 1,
    }
    path.write_text("a,b\n", encoding="utf-8")
    with pytest.raises(ValueError):
        summarize_label_csv(path)
    path.write_text(",".join(HEADER) + "\n1,alpha,pass,,pass,maybe\n", encoding="utf-8")
    with pytest.raises(ValueError):
        summarize_label_csv(path)
