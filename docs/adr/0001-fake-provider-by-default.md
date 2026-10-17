# 0001 Fake provider by default

## Status

Accepted. 2026-10-17.

## Context

The workshop has to run in CI and in a room without a vendor account. A live model would make the gate non-deterministic and would spend money.

## Decision

`WORKSHOP_PROVIDER` defaults to `fake`. The fake provider replays a script and does not read messages. A cassette is a JSON copy of that script. The live adapter exists, raises unless `WORKSHOP_ENABLE_LIVE_PROVIDER=1` and `WORKSHOP_PROVIDER=live` are both set, and is not used by the eval command or by tests.

## Consequences

Every published number from the gate is reproducible. The class cannot claim the model "understood" the question. A team that wants a live model has to turn it on locally and keep it out of CI.
