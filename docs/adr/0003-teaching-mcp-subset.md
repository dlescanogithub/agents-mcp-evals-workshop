# 0003 Teaching MCP subset, not the official SDK

## Status

Accepted. 2026-10-17.

## Context

The class needs to see frames on stdio without a network install and without an API key. The official Python SDK is not used. Tests have to pass offline after the dev tools are installed.

The spec revision cited is 2026-07-28, accessed 2026-10-17. That revision is stateless: protocol version travels on `_meta`, `server/discover` is required of servers, and `initialize` is the legacy handshake (revisions through 2025-11-25).

## Decision

`workshop.mcpmini` is a small JSON-RPC stdio process. It implements `server/discover`, `tools/list`, and `tools/call` for two read-only synthetic tools. It returns a JSON-RPC error for `initialize` and names `2026-07-28` as the supported revision. It returns code `-32022` when the version is missing or different.

## Consequences

Learners can point a subprocess at the server and read one line back. The official SDK is not used. This process is not compatible with that SDK, with streamable HTTP, or with resources, prompts, tasks, or pagination. A production integration should use the official SDK and the current spec, not this process.

## What we copied from the spec

The method names, the newline framing described for stdio, `resultType`, `content`, `isError`, `inputSchema` as a small object, and `ttlMs` / `cacheScope` on discover and tools/list. We did not copy the spec text into the repo.
