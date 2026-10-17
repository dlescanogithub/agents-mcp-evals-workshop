# Module 3 — MCP basics, as a small stdio server

## Goal

Build a JSON-RPC request, read a tool result, and call the local teaching server. No socket and no API key.

## Concepts

MCP revision 2026-07-28 (accessed 2026-10-17) uses JSON-RPC 2.0. On stdio, each message is one JSON object and a newline. The current revision puts the protocol version on every request:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28"}}}
```

The teaching server implements `server/discover`, `tools/list`, and `tools/call`. Tools are `inventory.lookup` and `notes.search`. `inventory.adjust` is not exported. A legacy `initialize` call gets an error that names `2026-07-28`, because `initialize` belongs to revisions through 2025-11-25.

This is not the official SDK. The SDK would be the thing you pin for a production integration. It is not installed here, so the class stays on the standard library. Omissions are in [docs/adr/0003-teaching-mcp-subset.md](../../docs/adr/0003-teaching-mcp-subset.md).

Spec pages used, accessed 2026-10-17:

- https://modelcontextprotocol.io/specification/2026-07-28
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- https://modelcontextprotocol.io/specification/2026-07-28/server/discover

## Files

- Edit `exercises/module_03/exercise.py`
- Server `src/workshop/mcpmini/server.py`
- Start it yourself with `PYTHONPATH=src python -m workshop.mcpmini`

## Run

```bash
PYTHONPATH=src python -m workshop check module-3
```

The solution check starts the server as a subprocess. A request has to carry the protocol version or the server answers `-32022`.

## Invariants

The request frame has `jsonrpc` `2.0`, the method, the id, and the version meta. A normal result returns the text. `isError: true` raises `ToolFailed`. Lookup of `CD-240` contains `bin=B-1`. Notes for `CD-240` mention the recount. An unknown SKU raises `ToolFailed`. The exported names are exactly the two read tools, sorted.

## Common mistake

Writing logs to stdout inside the server. Stdout is the protocol. Logs go to stderr. The library already does that.

## What this module does not do

Pagination, resources, prompts, tasks, HTTP, or authentication. Stdio in the spec is not where you put a bearer token.
