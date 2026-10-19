# Number trace: agents_mcp_evals_workshop_demo_en.mp4

Every number on screen or in the narration, with its source. Asserted by script (`code/build_trace.py`) at build time against the take recording (`take.json`) and the repo README (clone of main, HEAD 2b1209375b8f, package 0.1.1, run on Python 3.12.15). Spoken numbers are written in words. No live model call and no network call was made; the badge says OFFLINE (fake model, no API key). Everything in the terminal is a real run of the repo's own commands.

## Scene commands (real, offline, `lab $` prompt)
| Scene | Command shown | Output |
|---|---|---|
| A, B | `python -m workshop demo 2>/dev/null` | answer, stop final, 3 model calls, effects, simulated cost, provider fake, network none |
| C | `jq` over `rq/list.json` and `rq/adjust.json` (JSON-RPC requests, in `sources/rq/`), then `python -m workshop.mcpmini < rq/...` | tool list, error for the write tool |
| D | `python -m workshop eval 2>/dev/null` | 6 cases, gate pass |
| E | `python -m workshop eval-regression 2>/dev/null; echo exit=$?` | lab agent obeys injection, gate red, exit 1 |
| F | `python -m workshop check module-1` (starter, first line) and `check all --impl solution` | module results |
| G | `sed -n` on README.md | README text (not a run) |

## Numbers
| On screen / narration | Value | Source |
|---|---|---|
| "three model calls, two reads" | `model_calls: 3`, `effects: read:inventory.lookup,read:notes.search` | `workshop demo` output; README Results (Demo row) |
| "simulated cost zero point zero zero zero one two dollars, network none" | `simulated_cost_usd: 0.00012000`, `network: none` (also `simulated_latency_ms: 15`, on screen) | demo output; README Results (cost is simulated, `SIMULATED_USD_PER_TOKEN`) |
| "two read tools" | `["inventory.lookup","notes.search"]` | `workshop.mcpmini` `tools/list` reply |
| "Ask it to adjust stock: refused" | JSON-RPC error `-32602`, "tool is not exported: inventory.adjust" | `workshop.mcpmini` `tools/call` reply |
| "Six golden cases, zero failed" | `gate=pass cases=6 failed=0` | `workshop eval`; README Results |
| "the two lookups use different tool orders" | `shift_lookup` and `shift_lookup_swapped` both pass | eval output; README line after Results table |
| "agrees with the author on five of six; one disagreement" | `checker_vs_reference=5/6 disagreements=1` | eval output; README Results |
| Forced regression "exit one" | `regression_result=gate_red`, `failed=no_harmful_effect,claim_mismatch`, `exit=1` | `workshop eval-regression` |
| "module one, six failures" | `module=1 impl=exercise pass=0 fail=6` | `workshop check module-1` (starter) |
| "Solutions pass, modules one to eight" | pass=6,8,7,6,7,5,3,2 and fail=0 for modules 1 to 8 | `workshop check all --impl solution`; README "modules 1–8 fail=0" |
| "two sessions of three hours is [EST]", "Not delivered" | 2×3 h, [EST], not delivered | README lines 9 and 154 (on screen) |

## Closing slide
Deployment-strategist angle, not covered list and cost/[EST] notes are quoted from README "Business strategy", "Not covered yet" and "How to reproduce" (zero vendor spend by default); the business sketch is [EST] (`docs/BUSINESS_CASE.md`).

## Caveats not in the video
- Passing the gate means synthetic cases passed; it does not show production readiness. The model is a script (fake provider). The workshop has not been delivered. The MCP server is a small teaching subset, not the official SDK (said in the video).
- README records numbers measured on main commit `496a705` and Python 3.12.3; this take ran on main `2b12093` (docs-only commits since), Python 3.12.15. The numbers shown match the README.
- Not shown: pytest (48 passed, 92.79 percent coverage), ruff, mypy, secretscan results quoted in README.
