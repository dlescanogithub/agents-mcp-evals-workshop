# Scope

## In this repo

- Seven modules with exercises, solutions, and an invariant grader.
- A fake provider, a cassette file, JSON logs, JSONL traces, bounded retries.
- A read-only JSON-RPC stdio server with two synthetic tools, and a test client.
- An eval gate over six golden cases and a forced-regression command that exits 1.
- CI for lint, types, tests, the gate, the secret scan, and the red regression.
- Docs for a facilitator. No slides file, no hosted runner.

## Phases

| Phase | What | Status |
| --- | --- | --- |
| 0. Classroom offline | This repository | Implemented |
| 1. Team shadow | Same gate, their read-only data, still a fake or cassette provider | Not in this repo. See [ADAPT_TO_A_REAL_CLIENT.md](ADAPT_TO_A_REAL_CLIENT.md) |
| 2. Live provider behind the same gate | Optional adapter already refuses to start unless env flags are set | Adapter only. Not run in CI. Vendor-specific modules are design-only |
| 3. Agent guild | A review path for new tools | Design only |

## Assumptions

- Learners can read and write small Python 3.11 functions.
- Two sessions of about three hours each are available. Those durations are [EST].
- Synthetic data is acceptable for the class. Cerulean Depot is not a stand-in for a mapped customer.
- No fee is attached to this material. There is no statement of work here.

## Out of scope

- Training or hosting a model.
- The official MCP SDK, resources, prompts, tasks, pagination, and streamable HTTP.
- Single sign-on, audit storage, multi-tenant data, and a production on-call rota.
- Any claim about a real team's defect rate.

## Exit criteria for the class

- `python -m workshop eval` exits 0.
- `python -m workshop eval-regression` exits 1 and prints `regression_result=gate_red`.
- `python -m workshop check all --impl solution` exits 0.
- Learners can say, without notes, which check is an effect check and which check would be a trajectory check. The second kind is the one this gate refuses to require.

## Exit criteria this repo does not use

- A satisfaction score. The feedback form is a template, not a collected result.
- A before/after on production incidents. There is no production system in the repo.
