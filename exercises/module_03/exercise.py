"""Module 3 exercise. Speak a small JSON-RPC subset to the teaching server."""

from __future__ import annotations

from workshop.mcpmini.protocol import ToolFailed


def encode_request(method: str, params: dict[str, object], request_id: int) -> dict[str, object]:
    """Build one JSON-RPC request for protocol revision 2026-07-28.

    Put the protocol version on params["_meta"]["io.modelcontextprotocol/protocolVersion"].
    """

    raise NotImplementedError("module 3: build a JSON-RPC request")


def decode_tool_text(message: dict[str, object]) -> str:
    """Return the text content. Raise ToolFailed when result.isError is true."""

    raise NotImplementedError("module 3: read a tools/call result")


def run_tool(name: str, arguments: dict[str, object]) -> str:
    """Call the stdio teaching server and return the tool text. No network."""

    raise NotImplementedError("module 3: call the teaching server")


def list_tool_names() -> list[str]:
    """Return the exported tool names in sorted order."""

    raise NotImplementedError("module 3: list tools")


__all__ = ["ToolFailed", "decode_tool_text", "encode_request", "list_tool_names", "run_tool"]
