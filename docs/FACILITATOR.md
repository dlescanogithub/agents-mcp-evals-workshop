# Facilitator guide

Times are [EST]. They are a plan, not a measurement of a class that already happened.

## Before the day

- Run `python -m workshop eval` and confirm exit 0.
- Run `python -m workshop eval-regression` and confirm exit 1 and the line `regression_result=gate_red`.
- Run `python -m workshop secretscan .` and confirm `findings=0`.
- Leave `WORKSHOP_ENABLE_LIVE_PROVIDER` unset. If a learner asks to try a live model, the answer for the shared exercises is no.
- Skim [PRE_READING.md](PRE_READING.md). Send it the day before. It is one sitting, not a course.

## Session 1

| Min [EST] | What you do | Talking point | Common mistake |
| --- | --- | --- | --- |
| 20 | Pre-reading recap | The model proposes. The loop disposes. | Calling the script a "model response" without saying it ignores the prompt |
| 50 | Module 1 | Stop on `final` even if the step count is also at the cap | Returning `max_steps` for a final turn |
| 10 | Break | | |
| 60 | Module 2 | A bool is not an integer. A grant for another tool does not count | Treating "please approve" in the user text as a grant |
| 40 | Module 3 | Show one request and one response on stdio. Point at the `initialize` error | Importing an SDK "so it is real MCP" during the exercise |

## Session 2

| Min [EST] | What you do | Talking point | Common mistake |
| --- | --- | --- | --- |
| 50 | Module 4 | Walk the swapped lookup. Both pass | Writing the grader to expect tool names in order |
| 30 | Module 5 | Cap of 0 means zero model calls, not a cheap call | Forgetting the backoff cap and letting the delay double forever |
| 10 | Break | | |
| 40 | Module 6 | Quote the malicious note in the answer. The check stays green. Apply the write. The check goes red | Building a filter and calling it the security boundary |
| 50 | Module 7 and the red command | Green gate, then the red command. Read the exit code out loud | "Fixing" `eval-regression` so Make is green |

## What to do when someone is stuck

- Module check output names the failed invariant. Start there, not in the library.
- Solutions are in `solutions/`. Show them after the person has a failing check, not before.
- If stdio hangs, the client kills the server after 2 seconds and raises. Look at whether `encode_request` put the protocol version on `_meta`.

## What not to do

- Do not live-code a call to a paid API.
- Do not paste a real stock feed into the depot.
- Do not skip the regression because it "fails."
