# Runbook

This operates the workshop repo, not a production agent.

## Roles

| Role | Owns |
| --- | --- |
| Facilitator | The room, the timing [EST], the decision to show solutions |
| Learner | Their copy of `exercises/` |
| Maintainer | CI, the golden cases, the regression fixture, dependency updates |

There is no on-call schedule. Nobody is paged by this repository.

## Operate

From a clean checkout:

```bash
python -m pip install -e ".[dev]"
PYTHONPATH=src python -m workshop demo
PYTHONPATH=src python -m workshop eval
```

Expect the demo to print `provider: fake` and `network: none`. Expect the eval to print `gate=pass`.

Logs are JSON on stderr. Protocol frames for the teaching server, if you run module 3, are JSON lines on that process's stdout. Do not point a log collector at the server's stdout.

## Monitor

For a class, "monitor" means:

- The eval command exits 0 at the start of the day.
- The regression command exits 1.
- `python -m workshop secretscan .` prints `findings=0`.

There is no dashboard.

## Incidents

| Symptom | What it means | What to do |
| --- | --- | --- |
| `workshop eval` exits 1 | A golden invariant failed | Read the `failed=` list. Do not weaken the invariant to go green unless the case is wrong. If the fact string drifted, update the fact and say why in the commit. |
| `workshop eval-regression` exits 0 | The alarm is broken. The lab agent changed stock and the gate stayed green | Treat the branch as unsafe to teach. Restore the `trust_writes` lab path or the `no_harmful_effect` check. CI fails this case when the exit code is not 1. |
| Regression exits with something other than 1 | Crash, or the failure was a different bug | Read stderr. A traceback is not a successful red gate. |
| Module 3 times out | The teaching server did not answer within 2 seconds | Run `PYTHONPATH=src python -m workshop.mcpmini` by hand and send one JSON line. A hang with empty stdout usually means an exception before the first flush, which would be on stderr. |
| A learner's check fails on the starter | Expected | They still have `NotImplementedError` in the exercise. |
| Secret scan finds a line | A token-shaped string is in the tree | Remove it, rotate the credential if it was real, and do not "allow" it unless the line is a test fixture that is not a real secret. |

## Rollback

The class has no deployed service. Rollback is git.

- If a merged change makes `workshop eval` fail, revert that commit.
- If a merged change makes `workshop eval-regression` exit 0, revert that commit even if the rest of the tests are green.
- Do not roll forward by deleting the regression test.

## Handoff

Give the next facilitator this README, [FACILITATOR.md](FACILITATOR.md), and the command list. Tell them the red regression is supposed to be red. Tell them not to enable the live provider for the shared exercises.

If a team adopts the pattern, hand them [ADAPT_TO_A_REAL_CLIENT.md](ADAPT_TO_A_REAL_CLIENT.md) and leave this repo's synthetic depot in place as the reference implementation.
