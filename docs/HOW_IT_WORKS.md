# How the workshop works

This is a walkthrough for engineers and buyers. The code is in English. The idea is below.

## An analogy

Treat the workshop as a fire drill in a warehouse. The warehouse is fictional (Cerulean Depot, three SKUs, three notes). The "model" does not think: it reads a script, the way an actor repeats a script. What the class trains is the building around that script: which door can open, who signs a goods issue, and which checklist must go red when someone removes stock without permission.

The checklist does not say "you walked aisle A and then aisle B". It asks "did anyone get hurt?", "did you spend too much?", "does the answer name the right bin?". Two different paths can pass.

## The flow, step by step

1. A person writes a question, for example where kit CD-240 is.
2. The loop builds two messages: a fixed system rule, and the question.
3. Before calling the provider, it checks the simulated budget. If the next call does not fit, it stops with `budget` and does not call.
4. The fake provider returns the next turn of the script: either a tool request, or a closing text.
5. If it requests a tool, the code validates the arguments. If the tool writes, it requires a human grant in a set (`Approval.granted`). Text from the model is not enough to grant itself permission.
6. The tool result goes back into the history marked as data. A note can say "ignore the instructions". On the normal path that does not become a call.
7. The loop repeats until a final answer, the step cap, or the budget.
8. The eval looks at the result: did stock change? does the text contain the requested facts? did the simulated cost stay under the cap? It does not look at the exact tool order.

The class server (module 3) is another door into the same warehouse, over stdio, in JSON-RPC. The closing agent does not open a process for each step: it calls the same functions. Module 3 is where the frames are visible.

## How it is taught

The planned length is two blocks of three hours (2×3 h). That number is [EST]. The workshop has not been delivered: there is no cohort and no class date.

The first block builds the loop, the grant, and the small server. The second block writes the eval, the money cap, the injection lab, and the close. The close has to stay green. Then run `python -m workshop eval-regression`. It has to exit with code 1. If it exits 0, the alarm is broken: the vulnerable agent changed stock and nothing flagged it.

The grader (`python -m workshop check module-N`) looks at the exercise functions. The starter raises `NotImplementedError` on purpose. The solution lives in `solutions/`. You do not need it to understand the exercise, and it is there for the facilitator.

## Glossary

| Word | What it means here |
| --- | --- |
| Agent | A loop that alternates "ask for a turn" and "run a tool", with a stop. |
| Turn | A provider response: a tool, or final text. |
| Effect | What actually happened: a read, a write, or a block. |
| Invariant | A condition on the effect, not on the path. |
| Cassette | A file that holds the script. It is not a recording from a paid provider. |
| Grant | The set of tool names a person authorized for that run. |
| Gate | The command that fails if any invariant fails. In CI it has to pass. |
| Forced regression | A lab agent that does write. The gate has to go red. |

## Limits

- The fake provider does not read the prompt. If you change the question and not the script, the answer does not change. That is intentional: the class does not depend on a model.
- The detector for the phrase "Ignore previous instructions" does not protect anything. The protection is that a write without a grant does not run.
- The deterministic checker looks for a phrase. Compare it with reference labels written by the author, not with a model and not with a jury. On the measured run of 2026-10-17 it agreed on 5 of 6 (`checker_vs_reference=5/6`): the text "located in B-1" does not contain "bin B-1", and the reference label says that case passes.
- There is an optional model-judge client. It is off. Without `LIVE_MODE=1` and the rest of the `LLM_*` variables, the command exits with code 2. There is no live run and no results table. CI does not call it.
- The server does not use the official MCP SDK. It follows a subset of revision 2026-07-28, accessed 2026-10-17: `server/discover`, `tools/list`, and `tools/call`.
- None of this shows production experience. It shows that these synthetic cases pass or fail the way the gate says.
