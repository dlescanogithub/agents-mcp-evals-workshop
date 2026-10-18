# Metrics

## Measured in this repo (2026-10-18, package 0.1.1, Python 3.12.3, main commit `496a705e1a21a1d533b57be2160d93e29496d233`)

The original workshop is PR #1, squash `c590b91` on main. The commands below were run again on the main commit named above.

| Metric | Value | Command |
| --- | --- | --- |
| Golden cases passed | 6 of 6 | `PYTHONPATH=src python -m workshop eval` |
| Checker vs reference labels written by the author | 5 agreements, 1 disagreement, 6 items | same command, `checker_vs_reference=5/6` |
| Optional LLM judge | not configured; exit 2; no live result | `PYTHONPATH=src python -m workshop llm-judge` |
| Forced regression | exit 1, harmful effect detected | `PYTHONPATH=src python -m workshop eval-regression` |
| Tests | 48 passed | `PYTHONPATH=src python -m pytest` |
| Line coverage of `src/workshop` | 92.79% | same pytest run, `--cov-fail-under=80` |
| Solution checks | 8 modules, fail=0 | `PYTHONPATH=src python -m workshop check all --impl solution` |
| Demo simulated cost | 0.00012000 USD at the simulated rate | `PYTHONPATH=src python -m workshop demo` |
| Secret findings in the tree | 0 | `PYTHONPATH=src python -m workshop secretscan .` |

The disagreement is the item whose text says "located in B-1" while the deterministic checker looks for the phrase "bin B-1". The reference label, written by the author, says pass. That gap is checker vs those reference labels. It is not an agreement with a person and it is not a model score.

## Optional LLM judge

On 2026-10-18, `PYTHONPATH=src python -m workshop llm-judge` exited 2 with `llm_judge=not_configured`. A live comparison was not re-measured. It needs an endpoint and a key. This table stays empty.

| item_id | checker | llm_judge | reference_label | human_label |
| --- | --- | --- | --- | --- |

## Not measured

| Metric | Why it is not here |
| --- | --- |
| Percent of real pull requests with an eval gate | No product repository is wired up. A team could count this later. [EST] target if they adopt the pattern: the practice repos they control, not a number this workshop can claim. |
| Time to first working agent | The self-study path exists. Nobody has been timed. [EST] for a reader who already writes Python: one session to finish modules 1–3, one session for 4–7. That is a planning guess. |
| Production incident rate | There is no production system. |
| Learner satisfaction | [docs/FEEDBACK_FORM.md](FEEDBACK_FORM.md) is a blank form. |
| Live model quality or latency | The live adapter and the optional LLM judge are off. No percentile was sampled. No live label was recorded. |

## How a team would read the gate after class

Keep the same three families: no harmful effect, cost within the cap they chose, facts they are willing to maintain. Add a case when a new effect appears. Do not add a case whose only assertion is the sequence of tool names.
