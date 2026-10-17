"""JSON-RPC frames for the teaching server.

Spec cited by the lesson (accessed 2026-10-17):
https://modelcontextprotocol.io/specification/2026-07-28
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

PROTOCOL_VERSION = "2026-07-28"
VERSION_META_KEY = "io.modelcontextprotocol/protocolVersion"
SERVER_INFO_KEY = "io.modelcontextprotocol/serverInfo"
SERVER_NAME = "cerulean-depot-teaching"
SERVER_VERSION = "0.1.0"
UNSUPPORTED_VERSION = -32022


class ProtocolError(ValueError):
    """The frame is not usable."""


class ToolFailed(RuntimeError):
    """tools/call completed with isError true."""


def parse_message(line: str) -> dict[str, object]:
    try:
        raw = cast(object, json.loads(line))
    except json.JSONDecodeError as exc:
        raise ProtocolError("parse error") from exc
    if not isinstance(raw, dict):
        raise ProtocolError("message must be a JSON object")
    return {str(key): value for key, value in raw.items()}


def encode_line(payload: Mapping[str, object]) -> str:
    return json.dumps(dict(payload), sort_keys=True) + "\n"


def build_request(method: str, params: Mapping[str, object], request_id: int) -> dict[str, object]:
    body = dict(params)
    body["_meta"] = {VERSION_META_KEY: PROTOCOL_VERSION}
    return {"jsonrpc": "2.0", "id": request_id, "method": method, "params": body}


def error_response(
    request_id: object,
    code: int,
    message: str,
    data: Mapping[str, object] | None = None,
) -> dict[str, object]:
    error: dict[str, object] = {"code": code, "message": message}
    if data is not None:
        error["data"] = dict(data)
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def protocol_version(params: Mapping[str, object]) -> str | None:
    meta = params.get("_meta")
    if not isinstance(meta, dict):
        return None
    raw = meta.get(VERSION_META_KEY)
    if not isinstance(raw, str):
        return None
    return raw


def first_text(result: Mapping[str, object]) -> str:
    content = result.get("content")
    if not isinstance(content, list) or not content:
        raise ProtocolError("result has no content")
    first = content[0]
    if not isinstance(first, dict):
        raise ProtocolError("content item must be an object")
    text = first.get("text")
    if not isinstance(text, str):
        raise ProtocolError("content text must be a string")
    return text


def decode_tool_text(message: Mapping[str, object]) -> str:
    if "error" in message:
        raise ProtocolError(str(message["error"]))
    result = message.get("result")
    if not isinstance(result, dict):
        raise ProtocolError("missing result")
    text = first_text(result)
    if result.get("isError") is True:
        raise ToolFailed(text)
    return text
