# agents-mcp-evals-workshop

Offline workshop on agents, a tiny MCP teaching server, and eval gates. What is tested is a scripted shift assistant for the fictional Cerulean Depot: invariants on effects, cost, and facts, not a fixed tool-call script.

## Problem and result

Delivery teams can demo an agent that calls tools and still have no check that a write happened, that a note was treated as data, or that a run stayed inside a budget. The planned length is two sessions of three hours (2×3 h). That duration is [EST]. This workshop has not been delivered. The labs practice those checks with a fake model. Nothing here is a production deployment, and no real client is connected.

Measured result: on 2026-10-17 the offline gate passed **6 of 6** golden cases (package 0.1.1, Python 3.12.3, git commit `COMMIT_SHA`, command `PYTHONPATH=src python -m workshop eval`). The same day, `PYTHONPATH=src python -m pytest` reported **48 passed** and **92.79%** coverage of `src/workshop`. A later commit that only records this hash does not change the runtime.

## Demo

One command, no network, no API key:

```bash
PYTHONPATH=src python -m workshop demo
```

`make demo` is the same command. Structured JSON logs go to stderr. The answer is on stdout. The fake provider replays `src/workshop/data/shift_lookup.json`.

## Business case

For a fictional delivery group ("Taller Bruma"), the session is a way to get a shared bar before anyone turns on a live model: an eval gate on the practice PR, a human grant for writes, and a budget that can refuse a call. The cost of running the labs is zero vendor spend. A worked [EST] sketch of facilitator time and learner time is in [docs/BUSINESS_CASE.md](docs/BUSINESS_CASE.md). This repo does not show money saved in a real organization.

## Architecture

```mermaid
flowchart TD
  learner[Learner exercise] --> grader["workshop check"]
  grader --> invariants[Invariant checks]
  demo["workshop demo"] --> loop[Agent loop]
  loop --> fake[Fake provider or cassette]
  loop --> tools[Tool gate]
  tools --> depot[Cerulean Depot synthetic data]
  eval["workshop eval"] --> loop
  eval --> invariants
  client[Teaching MCP client] --> server[JSON-RPC stdio server]
  server --> depot
  lab[Vulnerable lab agent] --> invariants
```

The capstone calls the same depot handlers the teaching server calls. It does not open a socket. Module 3 is the piece that speaks JSON-RPC over stdio. Detail is in [docs/architecture.md](docs/architecture.md).

## Results

Measured 2026-10-17, package 0.1.1, Python 3.12.3, git commit `COMMIT_SHA`. Costs below are simulated (see `SIMULATED_USD_PER_TOKEN` in `src/workshop/budget.py`). They are not invoices.

| Check | Result | Command |
| --- | --- | --- |
| Unit and integration tests | 48 passed, coverage 92.79% | `PYTHONPATH=src python -m pytest` |
| Eval gate | 6 cases, 0 failed | `PYTHONPATH=src python -m workshop eval` |
| Checker vs reference labels written by the author | 5 agreements, 1 disagreement, 6 items | printed by the eval command as `checker_vs_reference=5/6` |
| Optional LLM judge | not run; command exits 2 without configuration | `PYTHONPATH=src python -m workshop llm-judge` |
| Demo | stop `final`, 3 model calls, simulated cost 0.00012000, simulated latency 15 ms | `PYTHONPATH=src python -m workshop demo` |
| Forced regression | exit 1, `regression_result=gate_red`, invariants `no_harmful_effect,claim_mismatch` | `PYTHONPATH=src python -m workshop eval-regression` |
| Solution grader | modules 1–8 fail=0 | `PYTHONPATH=src python -m workshop check all --impl solution` |
| Secret scan | findings=0 | `PYTHONPATH=src python -m workshop secretscan .` |
| Ruff | all checks passed | `python -m ruff check src tests exercises solutions` |
| Mypy | no issues in 79 source files | `python -m mypy` |

The two lookup cases use different tool orders and both pass. That is the trajectory point: the gate asks for the bin and the note, and it asks that stock did not change.

## Use cases, governance and business strategy

### 1. Use cases

Client-style means "shaped like a delivery-team problem." The company names are fictional. Nothing here was taken from a real client.

| Use case | Status | Problem | Who approves | Gated effects | How this repo handles it |
| --- | --- | --- | --- | --- | --- |
| Enablement program for Taller Bruma, a fictional delivery org | Implemented | People can wire a tool loop and still have no shared bar for effects, cost, or untrusted text | Facilitator, with the team's engineering lead if they adopt the pattern | Stock writes and any tool outside the catalog | Seven modules, `workshop check`, and the CI eval gate. No external system is connected. |
| Internal agent guild that reviews new tools | Design only | There is no standing forum in this repo for a second team to propose a tool | A guild chair role, not built | A new tool would need an entry in the catalog and a human grant if it writes | Listed as a later phase in [docs/SCOPE.md](docs/SCOPE.md). No guild workflow is implemented. |

| Use case | Status | Problem | Who approves | Gated effects | How this repo handles it |
| --- | --- | --- | --- | --- | --- |
| Self-study path | Implemented | One person needs to practice the loop without a vendor key | The learner | Same gates as the class | `exercises/`, `solutions/`, and `workshop check module-N` |
| Team lunch-and-learn | Design only | A short slot cannot host the labs | The host | No writes in the outline | [docs/SLIDES_OUTLINE.md](docs/SLIDES_OUTLINE.md) is an outline only |

Design-only vs implemented:

| Item | Status |
| --- | --- |
| Modules 1–7, fake provider, cassettes, grader, CI gate, forced red regression, stdio teaching server | Implemented |
| Deterministic checker vs reference labels written by the author | Implemented. Not a model score |
| Optional module 8 and LLM judge client | Implemented and off by default. Not part of the 2×3 h plan. Not run live. Not in CI |
| Human-label CSV | Template only (`templates/human_labels.csv`). No filled rows |
| Slide deck | Design only (outline) |
| Hosted classroom environment | Design only |
| Vendor modules for a specific model host | Design only. If added later, use only public docs, cited and dated |
| Live provider | Optional adapter, off by default, not used by the gate |

### 2. Governance checklist

| Control | Where it lives |
| --- | --- |
| Tool args are typed; unknown fields are rejected | `src/workshop/tools/auth.py`, module 2 |
| Human approval is a grant set in code, not a sentence in the prompt | `src/workshop/models.py` (`Approval`), `src/workshop/tools/auth.py` |
| Write tools are absent from the MCP export | `src/workshop/tools/specs.py` (`MCP_EXPORTED`) |
| Untrusted note text is not parsed into tool calls on the hardened path | `src/workshop/agent/loop.py` |
| Trace of steps | `src/workshop/tracing.py` (JSONL) and JSON logs in `src/workshop/logging_setup.py` |
| Budget admission check and simulated price | `src/workshop/budget.py` |
| Bounded retries (max attempts and a backoff cap) | `src/workshop/retries.py` |
| Eval gate in CI, no paid API | `.github/workflows/ci.yml`, `src/workshop/evalkit/gate.py` |
| Proof the gate can go red | `python -m workshop eval-regression` |
| Secret scan | `src/workshop/secretscan.py` |
| Deterministic checker vs author reference labels | `src/workshop/evalkit/checker.py` |
| Optional LLM judge, off unless configured, never in CI | `src/workshop/evalkit/llm_judge.py` |
| Risks | [docs/RISKS.md](docs/RISKS.md) |
| Costs | [docs/COST.md](docs/COST.md) |
| Incident and rollback | [docs/RUNBOOK.md](docs/RUNBOOK.md) |

Not covered yet: real identity for the approver, a review queue, vendor authentication, persistent memory, multi-user tenancy, a hosted runner, and a recorded live LLM-judge result. The client exists and stays off.

### 3. Business strategy

The business problem this material is aimed at: a delivery team starts calling tools from a model before it has a definition of a bad effect. The [EST] ROI sketch and the behaviour metrics are in [docs/BUSINESS_CASE.md](docs/BUSINESS_CASE.md) and [docs/METRICS.md](docs/METRICS.md). Scope and phases are in [docs/SCOPE.md](docs/SCOPE.md).

Deployment Strategist conversation: start with discovery ([docs/DISCOVERY.md](docs/DISCOVERY.md)), not with a model name. Run the agent in shadow against a cassette and the invariant gate. Only then talk about a live provider, still behind the same gate. The facilitator owns the classroom and the synthetic data. The engineering lead of the adopting team would own the tool catalog, the grant list, and the golden cases. This repo does not assign those roles to a real team.

## Decisions

- [0001 Fake provider by default](docs/adr/0001-fake-provider-by-default.md)
- [0002 Invariants, not trajectories](docs/adr/0002-invariants-not-trajectories.md)
- [0003 Teaching MCP subset, not the official SDK](docs/adr/0003-teaching-mcp-subset.md)
- [0004 The human gate is code](docs/adr/0004-human-gate-is-code.md)
- [0005 Environment-only configuration](docs/adr/0005-env-only-config.md)

## Security and known limits

What this does NOT do:

- It does not call a paid model API in tests or in CI.
- It does not authenticate a person. `Approval.approver` is a label.
- It does not stop prompt injection by scanning text. The lab phrase detector is a label. The control is that tool calls come from the provider turn, and writes need a grant.
- It does not implement MCP. It implements a small JSON-RPC subset so a class can see frames on stdio. The official SDK is not used. The cited revision is 2026-07-28, accessed 2026-10-17. See [docs/adr/0003-teaching-mcp-subset.md](docs/adr/0003-teaching-mcp-subset.md).
- It does not record real vendor traffic. Cassettes are scripts.
- It does not prove a team is ready for production. Passing the gate means the synthetic cases passed.
- It does not store secrets. `.env` is gitignored. The live key is never written to the JSON log on purpose (`Settings.public_dict`).

More in [SECURITY.md](SECURITY.md) and [docs/RISKS.md](docs/RISKS.md).

## How to reproduce

Cost of a run: zero by default. The fake provider does not use the network. Do not set `WORKSHOP_ENABLE_LIVE_PROVIDER`.

Prerequisites: Python 3.11 or newer (measured here on 3.12.3), git. `make` is optional.

Audience: delivery engineers who will sit next to an agent feature. Comfort with Python functions and JSON is enough. No vendor account.

Learning outcomes: explain the loop and a stop rule; reject a badly typed tool call; require a human grant for a write; call the teaching server over stdio; score a run by invariants; refuse a call that does not fit a budget; show a synthetic injection that fails closed; leave the capstone gate green and the regression red.

Agenda, planning only. The 2×3 h length is [EST]. The workshop has not been delivered:

| Block | Minutes [EST] | Module |
| --- | --- | --- |
| Welcome and pre-reading | 20 | [docs/PRE_READING.md](docs/PRE_READING.md) |
| What is an agent | 50 | [modules/01-agent/README.md](modules/01-agent/README.md) |
| Break | 10 | |
| Tools and the human gate | 60 | [modules/02-tools/README.md](modules/02-tools/README.md) |
| MCP teaching server | 40 | [modules/03-mcp/README.md](modules/03-mcp/README.md) |
| Evals | 50 | [modules/04-evals/README.md](modules/04-evals/README.md) |
| Cost and retries | 30 | [modules/05-cost/README.md](modules/05-cost/README.md) |
| Break | 10 | |
| Injection lab | 40 | [modules/06-injection/README.md](modules/06-injection/README.md) |
| Capstone and the red gate | 50 | [modules/07-capstone/README.md](modules/07-capstone/README.md) |

Setup and commands. If `make` is missing, use the `python -m` line.

```bash
python -m pip install -e ".[dev]"    # make setup
python -m ruff check src tests exercises solutions
python -m ruff format --check src tests exercises solutions
python -m mypy                        # make lint runs ruff and mypy
python -m pytest                      # make test
python -m workshop eval               # make eval
python -m workshop demo               # make demo
python -m workshop check module-1     # starter, expected to fail until you implement it
python -m workshop check module-1 --impl solution
```

`make eval-regression` is supposed to exit non-zero. A red result means the gate noticed the lab agent changed stock. CI treats exit code 1 as the success condition for that step.

Module 8 is optional and is not on that agenda. `python -m workshop llm-judge` exits 2 until `LIVE_MODE=1` and the `LLM_*` variables are set. CI does not run it. The results table in [modules/08-llm-judge/README.md](modules/08-llm-judge/README.md) is empty.

Copy `.env.example` to `.env` only on your machine if you want the variables set. The program reads the process environment. It does not open `.env` itself.

## Next steps

- Keep the gate green when a case is added. Add a case by effects and facts, not by locking a tool order.
- A slide file and a hosted runner are intentionally not in this repo.
- A vendor-specific module, if someone writes one later, has to cite public docs with the access date and stay out of CI.
- An adopting team would replace Cerulean Depot with their own read-only lookup behind the same grant rule. See [docs/ADAPT_TO_A_REAL_CLIENT.md](docs/ADAPT_TO_A_REAL_CLIENT.md).

## Docs index

- [How it works (rioplatense)](docs/HOW_IT_WORKS.md)
- [Business case](docs/BUSINESS_CASE.md)
- [Discovery questions](docs/DISCOVERY.md)
- [Scope](docs/SCOPE.md)
- [Risks](docs/RISKS.md)
- [Metrics](docs/METRICS.md)
- [Cost](docs/COST.md)
- [Runbook](docs/RUNBOOK.md)
- [Architecture](docs/architecture.md)
- [Adapt to a real client](docs/ADAPT_TO_A_REAL_CLIENT.md)
- [Provenance](docs/PROVENANCE.md)
- [Facilitator guide](docs/FACILITATOR.md)
- [Learner handout](docs/LEARNER_HANDOUT.md)
- [Pre-reading](docs/PRE_READING.md)
- [Answer key](docs/ANSWER_KEY.md)
- [Feedback form](docs/FEEDBACK_FORM.md)
- [Slides outline (design only)](docs/SLIDES_OUTLINE.md)
- [Decisions](docs/adr/)
