"""Module 3 answer. Stdio JSON-RPC against the read-only teaching server."""

from __future__ import annotations

from workshop.mcpmini.client import open_session
from workshop.mcpmini.protocol import (
    PROTOCOL_VERSION,
    VERSION_META_KEY,
    ProtocolError,
    ToolFailed,
    first_text,
)


def encode_request(method: str, params: dict[str, object], request_id: int) -> dict[str, object]:
    body = dict(params)
    body["_meta"] = {VERSION_META_KEY: PROTOCOL_VERSION}
    return {"jsonrpc": "2.0", "id": request_id, "method": method, "params": body}


def decode_tool_text(message: dict[str, object]) -> str:
    if "error" in message:
        raise ProtocolError(str(message["error"]))
    result = message.get("result")
    if not isinstance(result, dict):
        raise ProtocolError("missing result")
    text = first_text(result)
    if result.get("isError") is True:
        raise ToolFailed(text)
    return text


def run_tool(name: str, arguments: dict[str, object]) -> str:
    session = open_session()
    try:
        session.send(encode_request("server/discover", {}, 1))
        session.send(encode_request("tools/list", {}, 2))
        response = session.send(encode_request("tools/call", {"name": name, "arguments": arguments}, 3))
    finally:
        session.close()
    return decode_tool_text(response)


def list_tool_names() -> list[str]:
    session = open_session()
    try:
        discover = session.send(encode_request("server/discover", {}, 1))
        if "error" in discover:
            raise ProtocolError(str(discover["error"]))
        listed = session.send(encode_request("tools/list", {}, 2))
    finally:
        session.close()
    result = listed.get("result")
    if not isinstance(result, dict):
        raise ProtocolError("missing result")
    tools = result.get("tools")
    if not isinstance(tools, list):
        raise ProtocolError("missing tools")
    names: list[str] = []
    for tool in tools:
        if isinstance(tool, dict) and isinstance(tool.get("name"), str):
            names.append(str(tool["name"]))
    return sorted(names)
