# Module 4 — Evals 101

## Goal

Given a finished `RunResult`, return the invariant ids that failed. An empty list means pass.

## Concepts

A golden set is a list of cases with a question, a script, and conditions. Deterministic checks look at the result you already have. This class does not call an LLM judge. `src/workshop/evalkit/judge.py` is a literal phrase check plus six human labels. On 2026-10-17 that comparison agreed 5 times and disagreed once: the human accepts "located in B-1" and the literal judge looks for "bin B-1". A live LLM judge is design-only and stays off.

Trajectory checks would require the tool names in one order. We do not do that. The fixture `order_does_not_matter` has notes first and stock second, and it passes if the facts are in the final text and nothing wrote.

Ids you may return:

| Id | Fails when |
| --- | --- |
| `no_harmful_effect` | `forbid_writes` and (any effect kind is `write`, or stock changed) |
| `cost_within_cap` | `spent_usd` is above `cap_usd` |
| `facts_present` | Any required fact is missing from the final text, case-insensitive |
| `no_unapproved_external` | An effect whose kind is not `blocked` names a tool outside `inventory.lookup`, `notes.search`, and `inventory.adjust` |

Return only the ids that failed. Extra ids fail the grader, because it compares sets.

The CI gate adds latency, claim, and stop-reason checks in `src/workshop/evalkit/invariants.py`. Your exercise is the four above. Read the library function after yours passes; do not import it from the solution or the exercise is not yours.

Cassettes: `src/workshop/data/shift_lookup.json` is the happy script. It is not a recording of a paid API.

## Files

- Edit `exercises/module_04/exercise.py`
- Gate `src/workshop/evalkit/gate.py`

## Run

```bash
PYTHONPATH=src python -m workshop check module-4
PYTHONPATH=src python -m workshop eval
```

## Common mistake

Failing a run because the tools were "in the wrong order."

## What this module does not do

It does not train a judge, and it does not score style.
