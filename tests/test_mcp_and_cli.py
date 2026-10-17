"""Teaching server, grader, and the command line."""

from __future__ import annotations

import io
import json

import pytest

from workshop.cli import main
from workshop.domain import fresh_state
from workshop.grading import grade
from workshop.mcpmini.client import lookup_sku
from workshop.mcpmini.protocol import PROTOCOL_VERSION, build_request
from workshop.mcpmini.server import handle, serve
from workshop.mcpmini.server import main as server_main


def _request(method: str, params: dict[str, object] | None = None, request_id: int = 1) -> dict[str, object]:
    return build_request(method, {} if params is None else params, request_id)


def test_server_discover_list_and_call() -> None:
    state = fresh_state()
    discovered = handle(_request("server/discover"), state)
    assert discovered is not None
    result = discovered["result"]
    assert isinstance(result, dict)
    assert result["supportedVersions"] == [PROTOCOL_VERSION]
    listed = handle(_request("tools/list", {}, 2), state)
    assert listed is not None
    tools = listed["result"]
    assert isinstance(tools, dict)
    tool_list = tools["tools"]
    assert isinstance(tool_list, list)
    names = [tool["name"] for tool in tool_list if isinstance(tool, dict)]
    assert names == ["inventory.lookup", "notes.search"]
    called = handle(
        _request("tools/call", {"name": "inventory.lookup", "arguments": {"sku": "CD-240"}}, 3),
        state,
    )
    assert called is not None
    body = called["result"]
    assert isinstance(body, dict)
    assert body["isError"] is False
    content = body["content"]
    assert isinstance(content, list)
    first = content[0]
    assert isinstance(first, dict)
    assert "bin=B-1" in first["text"]
    missing = handle(
        _request("tools/call", {"name": "inventory.lookup", "arguments": {"sku": "CD-999"}}, 4),
        state,
    )
    assert missing is not None
    missing_body = missing["result"]
    assert isinstance(missing_body, dict)
    assert missing_body["isError"] is True


def test_server_rejects_legacy_initialize_and_bad_version() -> None:
    state = fresh_state()
    legacy = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, state)
    assert legacy is not None
    error = legacy["error"]
    assert isinstance(error, dict)
    assert error["code"] == -32601
    data = error["data"]
    assert isinstance(data, dict)
    supported = data["supported"]
    assert isinstance(supported, list)
    assert PROTOCOL_VERSION in supported
    bare = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, state)
    assert bare is not None
    bare_error = bare["error"]
    assert isinstance(bare_error, dict)
    assert bare_error["code"] == -32022
    unknown = handle(_request("prompts/list"), state)
    assert unknown is not None
    unknown_error = unknown["error"]
    assert isinstance(unknown_error, dict)
    assert unknown_error["code"] == -32601
    hidden = handle(
        _request("tools/call", {"name": "inventory.adjust", "arguments": {"sku": "CD-100", "delta": -1}}),
        state,
    )
    assert hidden is not None
    hidden_error = hidden["error"]
    assert isinstance(hidden_error, dict)
    assert hidden_error["code"] == -32602
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}, state) is None
    invalid = handle({"jsonrpc": "1.0", "id": 1, "method": "tools/list"}, state)
    assert invalid is not None
    invalid_error = invalid["error"]
    assert isinstance(invalid_error, dict)
    assert invalid_error["code"] == -32600


def test_serve_parse_error_and_main(monkeypatch: pytest.MonkeyPatch) -> None:
    stdin = io.StringIO('not-json\n{"jsonrpc":"2.0","method":"notifications/ping"}\n')
    stdout = io.StringIO()
    serve(stdin, stdout)
    first = json.loads(stdout.getvalue().splitlines()[0])
    assert first["error"]["code"] == -32700
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    monkeypatch.setattr("sys.stdout", io.StringIO())
    assert server_main() == 0


def test_subprocess_lookup() -> None:
    text = lookup_sku("CD-240")
    assert "bin=B-1" in text


def test_solutions_pass_and_exercises_fail() -> None:
    for module_id in ("1", "2", "3", "4", "5", "6", "7"):
        solution = grade(module_id, "solution")
        assert solution.failed == 0, solution.failed_names
        exercise = grade(module_id, "exercise")
        assert exercise.failed > 0


def test_cli_demo_eval_and_regression(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["demo"]) == 0
    demo = capsys.readouterr().out
    assert "bin B-1" in demo
    assert "provider: fake" in demo
    assert main(["eval"]) == 0
    evaluation = capsys.readouterr().out
    assert "gate=pass cases=6 failed=0" in evaluation
    assert "calibration_agreement=5/6" in evaluation
    assert main(["eval-regression"]) == 1
    regression = capsys.readouterr().out
    assert "regression_result=gate_red" in regression
    assert main(["check", "module-1", "--impl", "solution"]) == 0
    assert "fail=0" in capsys.readouterr().out
    assert main(["check", "module-1"]) == 1
    assert main(["check", "nope"]) == 2
    assert main(["secretscan", "."]) == 0


def test_cli_version() -> None:
    with pytest.raises(SystemExit) as caught:
        main(["--version"])
    assert caught.value.code == 0
