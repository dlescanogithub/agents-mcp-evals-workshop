# Module 5 — Cost, latency, and the retry cap

## Goal

Two pure functions: may the loop spend another call, and how long may it wait before a retry.

## Concepts

The simulated price is `0.000002` USD per token in `src/workshop/budget.py`, dated 2026-10-17, and it is not a vendor price. The loop charges a scripted turn after the provider returns it. Before the call it holds back `MAX_CALL_RESERVE_USD` (`0.0001`). If `spent + reserve` does not fit, the stop reason is `budget` and the provider is not called. A cap of `0` therefore means zero calls.

Your `allow_model_call` is that comparison: `spent_usd + next_call_usd <= cap_usd`, with a tiny tolerance so binary floats do not flap.

Retries: `call_with_retry` tries at most `max_attempts` and only catches `RetryableError`. After attempt 1 it sleeps `base`, then doubles, and never sleeps more than `backoff_cap`. Your `delay_seconds` is that curve. `attempt` is 1-based.

Scripted latency is a field on the turn (`simulated_latency_ms`). The gate can fail `latency_within_cap` when the sum is above the case cap. The fake provider does not sleep that many milliseconds. Do not report it as a measured model percentile.

A retry on the fake path does not add a second simulated charge. A live HTTP call would cost each attempt. The attempt ceiling is the part this module enforces.

## Files

- Edit `exercises/module_05/exercise.py`
- Library `src/workshop/retries.py` and `src/workshop/budget.py`

## Run

```bash
PYTHONPATH=src python -m workshop check module-5
```

The delay checks use base `0.2` and cap `0.5`: `0.2`, `0.4`, `0.5`, `0.5`.

## Common mistake

A cap of zero that still allows a call because the call is "cheap."

## What this module does not do

It does not read a price page and it does not time a network round trip.
