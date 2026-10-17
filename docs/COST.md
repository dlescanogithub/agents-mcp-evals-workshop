# Cost

Default run cost is zero vendor spend. CI does not call a paid API. Tests refuse socket connects.

The token price in code is simulated. It was chosen on 2026-10-17 so that class numbers stay small and obvious. It is not taken from a vendor price page. Do not quote it as a market rate.

`SIMULATED_USD_PER_TOKEN = 0.000002` in `src/workshop/budget.py`.

A scripted turn in the golden cassette uses 12 input tokens and 8 output tokens, so one accepted turn costs `20 * 0.000002 = 0.00004` simulated USD. The demo takes 3 turns: **0.00012000** simulated USD, printed by `PYTHONPATH=src python -m workshop demo` on 2026-10-17 at package 0.1.1, Python 3.12.3, git commit `f7b0158`.

The gate's six cases printed these simulated costs the same day:

| Case | Simulated USD |
| --- | --- |
| shift_lookup | 0.00012000 |
| shift_lookup_swapped | 0.00012000 |
| missing_sku | 0.00008000 |
| unapproved_adjust | 0.00008000 |
| injection_blocked | 0.00012000 |
| budget_stop | 0.00000000 |

Sum of those printed figures: 0.00052000 simulated USD for one gate run. Arithmetic on the measured lines, not a separate meter.

Latency in the demo is scripted: 5 ms on each of 3 turns, 15 ms total, printed as `simulated_latency_ms`. It does not vary, so this repo does not report a sampled p50 or p95. Wall-clock time of the Python process was not used as a quality number.

Retries on the fake path do not add a second simulated charge. A live call would. That limit is documented in the module 5 lesson. The attempt cap is still enforced.

| Scenario | Model / provider | Tokens or units | Cost / run | p50 / p95 latency | Quality | Price date / source |
| --- | --- | --- | --- | --- | --- | --- |
| Offline demo | Fake script | 60 simulated tokens (3 × 20) | 0.00012000 simulated USD | Scripted 15 ms, deterministic, not a percentile | Final answer contains the bin and the note; stock unchanged | Simulated constant, 2026-10-17, `src/workshop/budget.py`. Not a vendor price. |
| Eval gate, 6 cases | Fake script | See the table above | 0.00052000 simulated USD summed from the printed case lines | Scripted per turn, not sampled | 6/6 invariants pass | Same constant, measured 2026-10-17 via `python -m workshop eval` |
| Optional live call | Off. Generic JSON adapter only | [EST] unknown until a team picks a public price page | [EST] do not copy a price into this repo | [EST] not run | Not run | Not run. Read the provider's own pricing page on the day you need it, and write down the URL and the date. |
| Optional LLM judge | Off. Exit 2 without `LIVE_MODE=1` and the `LLM_*` variables. Not in CI | No tokens recorded | No spend recorded | Not run | Empty results table in [METRICS.md](METRICS.md) | Prices and `LLM_PRICE_DATE` come from the environment on the day someone runs it. None are stored here. |

The admission check uses a reserve of 0.0001 simulated USD per call (`MAX_CALL_RESERVE_USD`), which is larger than one scripted turn, so a cap of 0 refuses the first call without spending.
