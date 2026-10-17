# 0002 Invariants, not trajectories

## Status

Accepted. 2026-10-17.

## Context

Recording the exact sequence of tool calls makes a golden test fail when the agent looks up notes before stock, even if the answer and the effects are fine.

## Decision

The gate fails a case only for named conditions: a write or a stock change when writes are forbidden, simulated spend above the cap, scripted latency above the case cap, a missing fact in the final text, a tool outside the catalog that actually ran, a claim that does not match the stock, or a stop reason outside `final`, `budget`, and `max_steps`.

`shift_lookup` and `shift_lookup_swapped` are both golden. They differ in tool order.

## Consequences

A regression that still says the right sentence but changes stock goes red (`claim_mismatch` and `no_harmful_effect`). A harmless reordering stays green. The grader's module 4 fixtures repeat the same idea for learners.
