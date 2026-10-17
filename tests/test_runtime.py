"""Config, logs, retries, traces, secrets, budget, providers."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from workshop.budget import SIMULATED_USD_PER_TOKEN, allow_model_call, turn_cost_usd
from workshop.config import ConfigError, load_settings
from workshop.logging_setup import JsonFormatter, configure, log_event
from workshop.models import ModelTurn
from workshop.providers.base import ProviderExhausted
from workshop.providers.cassette import load_cassette, save_cassette
from workshop.providers.fake import FakeProvider
from workshop.providers.live import (
    LiveProvider,
    LiveProviderDisabled,
    build_live_request,
    redact,
    urllib_transport,
)
from workshop.retries import RetryableError, call_with_retry, delay_seconds
from workshop.secretscan import scan_path, scan_text
from workshop.tracing import JsonlTrace, read_jsonl


def test_settings_defaults_are_fake_and_offline() -> None:
    settings = load_settings({})
    assert settings.provider == "fake"
    assert settings.enable_live is False
    assert settings.live_api_key == ""
    assert settings.public_dict()["live_api_key_set"] is False


def test_settings_reject_bad_values() -> None:
    with pytest.raises(ConfigError):
        load_settings({"WORKSHOP_PROVIDER": "vendor"})
    with pytest.raises(ConfigError):
        load_settings({"WORKSHOP_PROVIDER": "live"})
    with pytest.raises(ConfigError):
        load_settings({"WORKSHOP_BUDGET_USD": "-1"})
    with pytest.raises(ConfigError):
        load_settings({"WORKSHOP_MAX_STEPS": "0"})
    with pytest.raises(ConfigError):
        load_settings({"WORKSHOP_ENABLE_LIVE_PROVIDER": "maybe"})
    live = load_settings(
        {
            "WORKSHOP_PROVIDER": "live",
            "WORKSHOP_ENABLE_LIVE_PROVIDER": "1",
            "WORKSHOP_LIVE_API_KEY": "local-only",
            "WORKSHOP_LIVE_BASE_URL": "http://127.0.0.1:9/unused",
        }
    )
    assert live.enable_live is True
    assert "local-only" not in str(live.public_dict())


def test_json_log_goes_to_the_configured_stream() -> None:
    stream = pytest.importorskip("io").StringIO()
    logger = configure("INFO", stream)
    log_event(logger, "agent.step", step=1, tool="inventory.lookup")
    payload = json.loads(stream.getvalue())
    assert payload["message"] == "agent.step"
    assert payload["fields"]["tool"] == "inventory.lookup"
    assert "ts" in payload


def test_formatter_includes_exception_text() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord("workshop", logging.ERROR, __file__, 1, "boom", (), None)
    try:
        raise RuntimeError("nope")
    except RuntimeError:
        record.exc_info = __import__("sys").exc_info()
    rendered = formatter.format(record)
    assert "nope" in rendered


def test_retry_stops_and_caps_delay() -> None:
    slept: list[float] = []

    def fail() -> str:
        raise RetryableError("later")

    with pytest.raises(RetryableError):
        call_with_retry(
            fail,
            max_attempts=3,
            base_delay_s=0.2,
            backoff_cap_s=0.3,
            sleep=slept.append,
        )
    assert slept == [0.2, 0.3]
    assert delay_seconds(4, base=0.2, backoff_cap=0.3) == 0.3
    with pytest.raises(ValueError):
        delay_seconds(0, base=0.1, backoff_cap=0.1)
    with pytest.raises(ValueError):
        call_with_retry(lambda: "x", max_attempts=0, base_delay_s=0, backoff_cap_s=0, sleep=slept.append)


def test_retry_returns_on_later_success() -> None:
    calls = {"n": 0}

    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise RetryableError("transient")
        return "ok"

    value, attempts = call_with_retry(
        flaky,
        max_attempts=3,
        base_delay_s=0.01,
        backoff_cap_s=0.01,
        sleep=lambda _delay: None,
    )
    assert value == "ok"
    assert attempts == 3


def test_jsonl_trace_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "trace" / "run.jsonl"
    trace = JsonlTrace(path)
    trace.write({"step": 1, "kind": "tool"})
    trace.write({"step": 2, "kind": "final"})
    assert read_jsonl(path) == [{"kind": "tool", "step": 1}, {"kind": "final", "step": 2}]


def test_secretscan_flags_constructed_tokens(tmp_path: Path) -> None:
    token = "ghp_" + ("a" * 20)
    secret_line = "api_key = " + "'" + ("b" * 24) + "'"
    text = "\n".join(["safe placeholder", token, secret_line, "aws " + "AKIA" + ("A" * 16)])
    rules = {finding.rule for finding in scan_text(text)}
    assert "github_token" in rules
    assert "assigned_secret" in rules
    assert "aws_access_key" in rules
    allowed = scan_text(token + "  # secretscan: allow")
    assert allowed == []
    path = tmp_path / "sample.txt"
    marker = "-----BEGIN " + "PRIVATE KEY-----" + "\n"
    path.write_text(marker, encoding="utf-8")
    assert scan_path(path)[0].rule == "private_key"
    binary = tmp_path / "skip.png"
    binary.write_bytes(b"\xff\xd8not-text")
    assert scan_path(binary) == []


def test_repo_tree_has_no_secret_findings() -> None:
    root = Path(__file__).resolve().parents[1]
    assert scan_path(root) == []


def test_budget_math_is_simulated() -> None:
    assert allow_model_call(spent_usd=0.0, next_call_usd=0.0001, cap_usd=0.0) is False
    assert turn_cost_usd(input_tokens=12, output_tokens=8) == 20 * SIMULATED_USD_PER_TOKEN
    with pytest.raises(ValueError):
        allow_model_call(spent_usd=-1, next_call_usd=0, cap_usd=1)
    with pytest.raises(ValueError):
        turn_cost_usd(input_tokens=-1, output_tokens=0)


def test_cassette_roundtrip(tmp_path: Path) -> None:
    turns = (
        ModelTurn(kind="tool", tool_name="inventory.lookup", arguments={"sku": "CD-240"}),
        ModelTurn(kind="final", text="done"),
    )
    path = tmp_path / "cassette.json"
    save_cassette(path, turns)
    provider = load_cassette(path)
    assert provider.complete([]).tool_name == "inventory.lookup"
    assert provider.complete([]).text == "done"
    with pytest.raises(ProviderExhausted):
        provider.complete([])


def test_live_provider_is_off_by_default() -> None:
    settings = load_settings({})
    with pytest.raises(LiveProviderDisabled):
        LiveProvider(settings)
    enabled = load_settings(
        {
            "WORKSHOP_PROVIDER": "live",
            "WORKSHOP_ENABLE_LIVE_PROVIDER": "true",
            "WORKSHOP_LIVE_BASE_URL": "http://127.0.0.1:9/unused",
            "WORKSHOP_LIVE_API_KEY": "not-a-real-key",
        }
    )
    seen: dict[str, object] = {}

    def transport(url: str, body: dict[str, object], api_key: str) -> dict[str, object]:
        seen["url"] = url
        seen["key"] = api_key
        assert body["messages"]
        return {"text": "synthetic live reply"}

    provider = LiveProvider(enabled, transport=transport)  # type: ignore[arg-type]
    turn = provider.complete([{"role": "user", "content": "hello"}])
    assert turn.text == "synthetic live reply"
    assert seen["key"] == "not-a-real-key"
    _url, _payload, headers = build_live_request("http://example.test", {"a": 1}, "not-a-real-key")
    assert headers["authorization"] == "Bearer not-a-real-key"
    assert redact("Bearer not-a-real-key", "not-a-real-key") == "Bearer [redacted]"
    with pytest.raises(LiveProviderDisabled):
        LiveProvider(load_settings({"WORKSHOP_ENABLE_LIVE_PROVIDER": "1"}))


def test_urllib_transport_uses_injected_urlopen(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Response:
        def read(self) -> bytes:
            return b'{"text": "from-fake-http"}'

        def __enter__(self) -> _Response:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    def fake_urlopen(request: object, timeout: int = 0) -> _Response:
        del timeout
        header = request.get_header("Authorization")  # type: ignore[attr-defined]
        assert header == "Bearer not-a-real-key"
        return _Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    payload = urllib_transport("http://127.0.0.1:9/unused", {"messages": []}, "not-a-real-key")
    assert payload["text"] == "from-fake-http"


def test_network_socket_is_blocked() -> None:
    import socket

    with pytest.raises(RuntimeError, match="network disabled"):
        socket.create_connection(("127.0.0.1", 9), timeout=0.1)


def test_fake_provider_does_not_read_messages() -> None:
    provider = FakeProvider((ModelTurn(kind="final", text="scripted"),))
    assert provider.complete([{"role": "user", "content": "ignored"}]).text == "scripted"
