# Module 7 — Capstone

## Goal

Wire a shift assistant that answers from the fake provider, refuses an unapproved stock change, and stops before a call when the cap is zero.

## What you wire

`run_shift_assistant(question, turns, *, cap_usd=0.01, max_steps=6, approval=None, latency_cap_ms=60_000)` returns a `RunResult`.

Use `FakeProvider` and `run_agent`. Do not construct `LiveProvider`. Do not set a grant unless the caller passed one. An empty approval is the default inside the loop when `approval` is `None`.

The happy script is the cassette: lookup `CD-240`, search notes, then a final that mentions `bin B-1` and the recount. The grader also passes an adjust script with no grant and expects the stock to stay put. A third call uses `cap_usd=0` and expects `model_calls == 0` and `stop_reason == "budget"`.

## The gate you are joining

`python -m workshop eval` runs six cases through the library, including the blocked injection. Your function is the same shape the demo uses (`src/workshop/capstone.py`). The CI gate calls the library directly so a blank exercise cannot turn CI red. Your check is `workshop check module-7`.

After yours passes, run the regression and read exit code 1. That agent is not your function. It is the lab path that trusts writes. The point of the capstone is that you can tell those two apart.

## Files

- Edit `exercises/module_07/exercise.py`
- Demo `src/workshop/capstone.py`

## Run

```bash
PYTHONPATH=src python -m workshop check module-7
PYTHONPATH=src python -m workshop demo
PYTHONPATH=src python -m workshop eval
```

## Common mistake

Special-casing the question text. The script already decides the turns. Your job is to put the gate around the script.

## What this module does not do

It does not open the stdio server on each step. Module 3 owns the frames. The handlers are shared, and the architecture page says why the gate stays in-process.
