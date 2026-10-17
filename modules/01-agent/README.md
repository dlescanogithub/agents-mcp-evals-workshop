# Module 1 — What is an agent

## Goal

Implement the stop rule for a loop that already has a provider and a step counter.

## Concepts

The loop in `src/workshop/agent/loop.py` asks the provider for a turn, records the cost, and either stops or runs a tool. Your function is the classification a person should be able to say out loud:

- `final` when the turn is an answer, including when `steps` is already at `max_steps`
- `max_steps` when the turn is a tool and `steps >= max_steps`
- `None` when the loop should take another turn

The production loop also refuses to start a call when the step count is already spent, and it has a safety ceiling so a broken provider cannot spin. Your function does not replace that ceiling. The grader calls your function on a table of turns and on a short harness.

## Files

- Edit `exercises/module_01/exercise.py`
- Answer key `solutions/module_01/solution.py`
- Library `src/workshop/agent/loop.py` and `src/workshop/agent/stopping.py`

## Run

```bash
PYTHONPATH=src python -m workshop check module-1
PYTHONPATH=src python -m workshop check module-1 --impl solution
```

## Invariants

`classifies_final`, `classifies_continue`, `classifies_max_steps`, `final_wins_at_cap`, `harness_stops_on_final`, `harness_obeys_cap`.

## Common mistake

Returning `max_steps` for a final turn that happens to land on the cap. The answer is `final`. The run finished.

## What this module does not do

It does not call a model. The provider in the harness is a list of turns.
