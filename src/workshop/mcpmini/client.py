"""Test client for the teaching server. It speaks over pipes, never over the network."""

from __future__ import annotations

import os
import select
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

from workshop.mcpmini.protocol import (
    ProtocolError,
    build_request,
    decode_tool_text,
    parse_message,
)


def child_env() -> dict[str, str]:
    src = str(Path(__file__).resolve().parents[2])
    current = os.environ.get("PYTHONPATH", "")
    pythonpath = src if current == "" else src + os.pathsep + current
    env = dict(os.environ)
    env["PYTHONPATH"] = pythonpath
    env["PYTHONUNBUFFERED"] = "1"
    env["WORKSHOP_ENABLE_LIVE_PROVIDER"] = "0"
    env.pop("WORKSHOP_LIVE_API_KEY", None)
    return env


class StdioSession:
    def __init__(self, process: subprocess.Popen[str]) -> None:
        self._process = process

    def send(self, payload: Mapping[str, object]) -> dict[str, object]:
        stdin = self._process.stdin
        stdout = self._process.stdout
        if stdin is None or stdout is None:
            raise ProtocolError("stdio pipes are not open")
        import json

        stdin.write(json.dumps(dict(payload)) + "\n")
        stdin.flush()
        ready, _, _ = select.select([stdout], [], [], 2.0)
        if not ready:
            self._process.kill()
            raise ProtocolError("timed out waiting for the teaching server")
        line = stdout.readline()
        if line == "":
            code = self._process.poll()
            raise ProtocolError(f"server closed stdout (returncode={code})")
        return parse_message(line)

    def request(self, method: str, params: Mapping[str, object], request_id: int) -> dict[str, object]:
        return self.send(build_request(method, params, request_id))

    def close(self) -> None:
        if self._process.stdin is not None:
            self._process.stdin.close()
        try:
            self._process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self._process.kill()
            self._process.wait(timeout=2)


def open_session() -> StdioSession:
    process = subprocess.Popen(
        [sys.executable, "-m", "workshop.mcpmini"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        env=child_env(),
        bufsize=1,
    )
    return StdioSession(process)


def lookup_sku(sku: str) -> str:
    session = open_session()
    try:
        session.request("server/discover", {}, 1)
        session.request("tools/list", {}, 2)
        response = session.request(
            "tools/call",
            {"name": "inventory.lookup", "arguments": {"sku": sku}},
            3,
        )
        return decode_tool_text(response)
    finally:
        session.close()
