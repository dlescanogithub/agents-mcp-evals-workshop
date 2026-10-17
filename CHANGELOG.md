# Changelog

## 0.1.1 - 2026-10-17

- Renamed the phrase check to deterministic checker. The 5/6 figure is checker vs reference labels written by the author.
- Added an optional LLM-judge client. It is off unless `LIVE_MODE=1` and the `LLM_*` variables are set, it exits 2 without that configuration, and CI does not run it.
- Added optional module 8 and an empty human-label CSV. The results table is empty. No live comparison is recorded.
- Aligned the secret scanner with the vendored pattern list and recorded its sha256.
- Stated that the planned 2×3 h duration is [EST] and that the workshop has not been delivered. The official MCP SDK is not used. The cited spec revision remains 2026-07-28, accessed 2026-10-17.

## 0.1.0 - 2026-10-17

- Initial teaching repo: seven modules, fake provider, cassette, stdio MCP subset, invariant gate, forced regression, CI.
- No live provider calls in the default path.

This version is the workshop material. It is not a release of a hosted product, and this changelog is not a GitHub Release.
