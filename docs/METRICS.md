# Metrics

## Measured in this repo (2026-10-17, package 0.1.0, Python 3.12.3, git commit `631012d`)

| Metric | Value | Command |
| --- | --- | --- |
| Golden cases passed | 6 of 6 | `PYTHONPATH=src python -m workshop eval` |
| Literal judge vs human labels | 5 agreements, 1 disagreement, 6 items | same command, `calibration_agreement=5/6` |
| Forced regression | exit 1, harmful effect detected | `PYTHONPATH=src python -m workshop eval-regression` |
| Tests | 34 passed | `PYTHONPATH=src python -m pytest` |
| Line coverage of `src/workshop` | 92.25% | same pytest run, `--cov-fail-under=80` |
| Solution checks | 7 modules, fail=0 | `PYTHONPATH=src python -m workshop check all --impl solution` |
| Demo simulated cost | 0.00012000 USD at the simulated rate | `PYTHONPATH=src python -m workshop demo` |
| Secret findings in the tree | 0 | `PYTHONPATH=src python -m workshop secretscan .` |

The disagreement is the item whose text says "located in B-1" while the literal judge looks for the phrase "bin B-1". The human label says pass. That gap is the calibration lesson, not a quality score for a product.

## Not measured

| Metric | Why it is not here |
| --- | --- |
| Percent of real pull requests with an eval gate | No product repository is wired up. A team could count this later. [EST] target if they adopt the pattern: the practice repos they control, not a number this workshop can claim. |
| Time to first working agent | The self-study path exists. Nobody has been timed. [EST] for a reader who already writes Python: one session to finish modules 1–3, one session for 4–7. That is a planning guess. |
| Production incident rate | There is no production system. |
| Learner satisfaction | [docs/FEEDBACK_FORM.md](FEEDBACK_FORM.md) is a blank form. |
| Live model quality or latency | The live adapter is off. No percentile was sampled. |

## How a team would read the gate after class

Keep the same three families: no harmful effect, cost within the cap they chose, facts they are willing to maintain. Add a case when a new effect appears. Do not add a case whose only assertion is the sequence of tool names.
