# Answer key

The runnable answers are the files in `solutions/`. This page is the map, not a second copy of the code.

| Module | File | Idea worth saying out loud |
| --- | --- | --- |
| 1 | `solutions/module_01/solution.py` | If the turn is final, return `final` before you look at the cap. |
| 2 | `solutions/module_02/solution.py` | Reject unknown fields, then types, then the grant. A grant is per tool name. |
| 3 | `solutions/module_03/solution.py` | The version sits on `params._meta`. `isError: true` becomes `ToolFailed`. The server process is local. |
| 4 | `solutions/module_04/solution.py` | A write or a stock change is `no_harmful_effect`. A different tool order with the same facts returns an empty list. |
| 5 | `solutions/module_05/solution.py` | `spent + next <= cap`. The delay doubles and then stops growing at `backoff_cap`. |
| 6 | `solutions/module_06/solution.py` | The phrase marks the note. The invariant function ignores the phrase and looks at effects. Quoting the note is an empty failure list. |
| 7 | `solutions/module_07/solution.py` | `FakeProvider` plus `run_agent`. The default approval is empty, so the adjust script cannot write. |
| 8 | `solutions/module_08/solution.py` | Count checker and LLM-judge booleans against the reference. A missing LLM label is not a comparison. Optional, and not part of the 2×3 h plan. |

Facilitator check:

```bash
PYTHONPATH=src python -m workshop check all --impl solution
```

Measured 2026-10-17, package 0.1.1, Python 3.12.3, git commit `f7b0158`: `python -m workshop check all --impl solution` printed `fail=0` for modules 1–8.

Do not publish this file as a spoiler in the same handout as the exercises if you want people to try first. It is in the repo because the class is open-book and the CI needs the solutions to run.
