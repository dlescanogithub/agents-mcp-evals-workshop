# Provenance

This workshop is original material written for this repository. It is not a copy of an employer course, a client workshop, or a vendor tutorial.

## Reference repo that was requested and not readable

The brief for this portfolio asked for a documented copy, where useful, of the eval patterns in:

- Repository: `https://github.com/dlescanogithub/agent-runtime-evals` (private)
- Branch: `cursor/agent-runtime-evals-mvp-7e58`
- Commit: `55cfd4183fb2489d77fc9c8552e008274dc78f77`

On 2026-10-17 the credential available to this working environment received HTTP 404 (`repository not found`) for that repo, that commit, and `git ls-remote`. Nothing from that tree was read, and nothing from it was copied.

The pieces that brief named (an evalkit, a cassette, a fake provider, a JSONL trace, JSON logging, a secret scan) were implemented here from that description. Names overlap on purpose so a reader of both repos can compare them later. The source text does not.

## Spec citation

MCP revision 2026-07-28, accessed 2026-10-17:

- https://modelcontextprotocol.io/specification/2026-07-28
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- https://modelcontextprotocol.io/specification/2026-07-28/server/discover
- https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning

The teaching server follows those pages only for the frames it implements. Differences are listed in [adr/0003-teaching-mcp-subset.md](adr/0003-teaching-mcp-subset.md). The official Python SDK is not a dependency.
