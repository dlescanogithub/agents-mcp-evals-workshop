"""Read-only JSON-RPC stdio server for two synthetic tools.

This is a teaching subset of MCP revision 2026-07-28. It is not the official SDK.
Omitted on purpose: resources, prompts, tasks, pagination, streamable HTTP, icons,
full JSON Schema validation, and the legacy initialize handshake.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Mapping
from typing import TextIO

from workshop.domain import DepotState, fresh_state
from workshop.logging_setup import configure, log_event
from workshop.mcpmini.protocol import (
    PROTOCOL_VERSION,
    SERVER_INFO_KEY,
    SERVER_NAME,
    SERVER_VERSION,
    UNSUPPORTED_VERSION,
    ProtocolError,
    error_response,
    parse_message,
    protocol_version,
)
from workshop.models import no_approval
from workshop.tools.execute import execute
from workshop.tools.specs import MCP_EXPORTED

LOGGER = logging.getLogger("workshop.mcpmini")


def _tool_payloads() -> list[dict[str, object]]:
    payloads: list[dict[str, object]] = []
    for spec in MCP_EXPORTED:
        properties: dict[str, object] = {}
        required: list[str] = []
        for field in spec.fields:
            json_type = "integer" if field.type_name == "integer" else "string"
            properties[field.name] = {"type": json_type}
            if field.required:
                required.append(field.name)
        payloads.append(
            {
                "name": spec.name,
                "title": spec.name,
                "description": spec.description,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                    "additionalProperties": False,
                },
            }
        )
    return payloads


def _version_error(params: Mapping[str, object]) -> dict[str, object] | None:
    version = protocol_version(params)
    if version == PROTOCOL_VERSION:
        return None
    return {
        "supported": [PROTOCOL_VERSION],
        "requested": version if version is not None else "",
    }


def handle(message: Mapping[str, object], state: DepotState) -> dict[str, object] | None:
    if message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
        return error_response(message.get("id"), -32600, "invalid request")
    method = message["method"]
    if not isinstance(method, str):
        return error_response(message.get("id"), -32600, "invalid request")
    if "id" not in message:
        return None
    request_id = message.get("id")
    raw_params = message.get("params", {})
    if raw_params is None:
        raw_params = {}
    if not isinstance(raw_params, dict):
        return error_response(request_id, -32602, "invalid params")
    params = {str(key): value for key, value in raw_params.items()}
    if method == "initialize":
        return error_response(
            request_id,
            -32601,
            (
                "initialize is the legacy handshake used through MCP revision 2025-11-25. "
                "This teaching server supports revision 2026-07-28 only."
            ),
            {"supported": [PROTOCOL_VERSION], "requested": "legacy-initialize"},
        )
    mismatch = _version_error(params)
    if mismatch is not None:
        return error_response(
            request_id,
            UNSUPPORTED_VERSION,
            "Unsupported protocol version",
            mismatch,
        )
    if method == "server/discover":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resultType": "complete",
                "supportedVersions": [PROTOCOL_VERSION],
                "capabilities": {"tools": {}},
                "instructions": "Synthetic Cerulean Depot lookups. Read-only tools only.",
                "ttlMs": 3_600_000,
                "cacheScope": "public",
                "_meta": {SERVER_INFO_KEY: {"name": SERVER_NAME, "version": SERVER_VERSION}},
            },
        }
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resultType": "complete",
                "tools": _tool_payloads(),
                "ttlMs": 300_000,
                "cacheScope": "public",
            },
        }
    if method == "tools/call":
        return _call_tool(request_id, params, state)
    return error_response(request_id, -32601, f"method not found: {method}")


def _call_tool(request_id: object, params: Mapping[str, object], state: DepotState) -> dict[str, object]:
    name = params.get("name")
    arguments = params.get("arguments", {})
    if not isinstance(name, str) or not isinstance(arguments, dict):
        return error_response(request_id, -32602, "invalid params")
    exported = {spec.name for spec in MCP_EXPORTED}
    if name not in exported:
        return error_response(request_id, -32602, f"tool is not exported: {name}")
    _state, effect, text = execute(
        state,
        name,
        {str(key): value for key, value in arguments.items()},
        no_approval(),
    )
    is_error = effect.detail == "missing"
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "resultType": "complete",
            "content": [{"type": "text", "text": text}],
            "isError": is_error,
        },
    }


def serve(stdin: TextIO, stdout: TextIO) -> None:
    state = fresh_state()
    for line in stdin:
        if not line.strip():
            continue
        try:
            message = parse_message(line)
        except ProtocolError:
            stdout.write(json_line(error_response(None, -32700, "parse error")))
            stdout.flush()
            continue
        method = message.get("method")
        log_event(LOGGER, "mcp.request", method=method if isinstance(method, str) else "")
        response = handle(message, state)
        if response is None:
            continue
        stdout.write(json_line(response))
        stdout.flush()


def json_line(payload: Mapping[str, object]) -> str:
    import json

    return json.dumps(dict(payload), sort_keys=True) + "\n"


def main() -> int:
    configure()
    serve(sys.stdin, sys.stdout)
    return 0
