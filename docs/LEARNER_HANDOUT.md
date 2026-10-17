# Learner handout

You are changing functions under `exercises/`. The library in `src/workshop` is the reference runtime. You do not need a network and you do not need an API key.

## Commands

```bash
python -m pip install -e ".[dev]"
PYTHONPATH=src python -m workshop check module-1
PYTHONPATH=src python -m workshop check module-1 --impl solution
PYTHONPATH=src python -m workshop demo
PYTHONPATH=src python -m workshop eval
```

The first check fails until you replace `NotImplementedError`. That failure is the starting point.

## Words that matter

| Word | Meaning here |
| --- | --- |
| `final` | The provider returned an answer. Stop, even if you are also at the step cap. |
| `max_steps` | You already took the allowed number of turns and the last one was not final. |
| `ok` | Arguments are valid and, for a write, the tool name is in the grant. |
| `needs_human_approval` | The write is well formed and still refused. |
| `no_harmful_effect` | No write effect, and the stock counts match the seed. |
| `facts_present` | Each required string appears in the final text. Order of tools is irrelevant. |
| `cost_within_cap` | Simulated spend is under the case cap. |
| `no_unapproved_external` | A tool outside the catalog did not actually run. A blocked attempt is not a run. |

## Invariants you will be graded on

The check prints `failed=` with names. Fix the name it prints. Do not print extra invariant ids; the grader compares sets.

## When you are done with module 7

Your `run_shift_assistant` uses `FakeProvider` and `run_agent`. It does not read `WORKSHOP_ENABLE_LIVE_PROVIDER`. A cap of 0 performs no model call.
