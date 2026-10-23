# Risks

Owners are roles for this teaching repo, not a staffed rota. "Maintainer" is the person who merges changes to this repository.

| Risk | Probability | Impact | Mitigation | Owner |
| --- | --- | --- | --- | --- |
| A learner pastes a real key into an exercise | Medium for a live class, low in this repo's default path | Secret in git history | Live flag off, `.env` gitignored, secret scan in CI, no vendor client in the exercises | Facilitator |
| The class treats the fake provider as a model that read the prompt | Medium | They "fix" the script-independent answer and think the system reasons | Module 1 and the facilitator guide say the script ignores messages. The demo prints `provider: fake` | Facilitator |
| The phrase detector is used as the control | Medium | A new wording bypasses a filter that was never the control | Module 6 grader fails a write even when the phrase is only quoted. Docs say the detector is a label | Maintainer |
| The regression command is "fixed" so it exits 0 | Low | CI no longer proves the gate can go red | CI requires exit code 1. A unit test expects that code | Maintainer |
| The teaching server is deployed as if it were MCP | Low if the docs are read | A client that expects the full spec fails, or a write appears to be in protocol scope | Server exports two read tools. ADR 0003 lists omissions. Legacy `initialize` returns an error that names the supported revision | Maintainer |
| Golden cases lock an exact sentence and rot | Medium | Gate goes red for a wording change that did not change the effect | Cases ask for short facts plus effect checks. Two tool orders are both golden | Maintainer |
| Simulated price is quoted as a vendor price | Medium in a slide | A budget conversation uses a made-up rate | The constant is named simulated. COST.md forbids treating it as an invoice | Facilitator |
| Socket block in tests hides a future test that needed a local pipe | Low | A new test looks flaky | The block patches `connect`, not subprocess pipes. Module 3's stdio test is the pattern | Maintainer |
| Approver string is mistaken for authentication | Medium | A log line "approver=shift-lead" is treated as identity | SECURITY.md and ADR 0004 say it is a label | Facilitator |

Probability and impact here are qualitative labels for teaching, not measured frequencies.
