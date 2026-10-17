# Provenance

This workshop is original teaching material. Nothing in it is copied from employer work or from a client engagement.

## Shared utilities

A few small utilities are maintained in parallel across the portfolio repositories and kept aligned:

- cassette provider
- invariant checks
- JSON trace
- structured logging
- secretscan

They are vendored copies, not a published package. A change to the scanner pattern list is meant to land in each repository that vendors the file, together with a new checksum.

## What was adapted here

The cassette, the invariant gate, the JSONL trace, and the JSON logger are those shared ideas, fitted to the Cerulean Depot exercises and to the stdio teaching server. The secret scanner is the aligned copy. The deterministic checker, the optional LLM-judge client, and the module exercises are specific to this workshop.

## secretscan checksum

`src/workshop/secretscan.py` is the vendored copy. Keep it identical to the copy in the other portfolio repositories.

sha256: f796c96f9120734e120dc04660ad8f1a95d1af024f7e93b60ab789208db55296

Recompute and check with `make secretscan-hash`. `tests/test_secretscan.py` checks the same digest.

## Spec citation

MCP revision 2026-07-28, accessed 2026-10-17:

- https://modelcontextprotocol.io/specification/2026-07-28
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- https://modelcontextprotocol.io/specification/2026-07-28/server/discover
- https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning

The teaching server follows those pages only for the frames it implements. Differences are listed in [adr/0003-teaching-mcp-subset.md](adr/0003-teaching-mcp-subset.md). The official Python SDK is not a dependency and is not used.
