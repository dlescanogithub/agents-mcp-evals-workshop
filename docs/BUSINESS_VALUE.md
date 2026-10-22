# Value realization plan: delivering `agents-mcp-evals-workshop`

> **Important notice**
>
> - **The workshop has not been delivered.** No cohort has sat the two sessions. No buyer has been invoiced. No learner outcome in this file was observed.
> - **Fictional buyer.** "Taller Bruma" is an invented delivery group, the same one named in [BUSINESS_CASE.md](BUSINESS_CASE.md). It is not an employer and not a client. Cerulean Depot, the shift assistant in the labs, is fictional too.
> - **Inspired by the AWS Business Value Realization (BVR) framework:** a value-realization plan, KPIs with an exit per stage, and confirmation by the buyer. **It is not an official AWS template** (the official VRP template is not public) and **I do not hold the AWS BVR Competency**, which is awarded to AWS partner companies, not to individuals.
> - **[BUSINESS_CASE.md](BUSINESS_CASE.md) stops before a dollar return.** It says a money model would need a loaded hourly cost and an incident history, and that inventing those would be a fake case. This file continues anyway, as a planning sketch, and tags every invented input. Do not read it as evidence.
> - Labels used in this file:
>   - **MEASURED**: a command was run in this repository and the number is what it printed, with the date, the Python version, and the commit.
>   - **[EST]**: a planning assumption for class size, time, or a rate. Not a timesheet and not a fee.
>   - **[SYN]**: a synthetic business story invented for Taller Bruma. Not their books, because they are not real.
>   - **SIMULATED**: the token price in `src/workshop/budget.py`. A seeded classroom constant, not an invoice.
>   - **UNVERIFIED**: not run, not collected, or not observed. A blank form is UNVERIFIED.
> - Repo tree this document was checked against: commit `9d10f1d4d4dc8045ccb85749204a926bc2dba912`, package 0.1.1, Python 3.12.3, 2026-10-22. The docs change that adds this file does not edit `src/`.

---

## 0. What the workshop actually does (technical base, MEASURED)

Offline exercises for a scripted shift assistant. A fake provider replays turns. A small JSON-RPC server speaks stdio. An eval gate checks effects, cost, and facts. The default path does not use the network and does not read an API key.

**MEASURED 2026-10-22**, package 0.1.1, Python 3.12.3, commit `9d10f1d4d4dc8045ccb85749204a926bc2dba912`:

| Check | Result | Command |
| --- | --- | --- |
| Tests | 48 passed | `python -m pytest --cov=workshop --cov-report=term-missing --cov-fail-under=80` |
| Line coverage of the `workshop` package | 92.79% (1456 statements, 105 missed) | same pytest command. The report's TOTAL line. Exercises and solutions are outside that total |
| Eval gate | 6 cases, 0 failed | `PYTHONPATH=src python -m workshop eval` |
| Checker vs reference labels written by the author | 5 agreements, 1 disagreement | same command, `checker_vs_reference=5/6` |
| Demo | stop `final`, 3 model calls, SIMULATED cost 0.00012000, SIMULATED latency 15 ms | `PYTHONPATH=src python -m workshop demo` |
| Forced regression | exit 1, `regression_result=gate_red`, invariants `no_harmful_effect,claim_mismatch` | `PYTHONPATH=src python -m workshop eval-regression` |
| Solution grader | modules 1–8, fail=0 | `PYTHONPATH=src python -m workshop check all --impl solution` |
| Secret scan | findings=0 | `PYTHONPATH=src python -m workshop secretscan .` |
| Optional LLM judge | exit 2, `llm_judge=not_configured` | `PYTHONPATH=src python -m workshop llm-judge` |
| Ruff | all checks passed | `python -m ruff check src tests exercises solutions` |
| Mypy | no issues in 79 source files | `python -m mypy` |

The same counts were first published on 2026-10-18 at commit `496a705e1a21a1d533b57be2160d93e29496d233` ([METRICS.md](METRICS.md)). The 2026-10-22 run reproduced them. It is a second measurement of this tree, not a new lab result.

SIMULATED price: `SIMULATED_USD_PER_TOKEN = 0.000002` in `src/workshop/budget.py`, chosen 2026-10-17 so class numbers stay small. It is not a vendor rate. Sum of the six printed case costs on 2026-10-22: 0.00052000 SIMULATED USD. That sum is arithmetic on the printed lines.

The planned length is two sessions of three hours. That duration is **[EST]**. **The workshop has not been delivered.**

---

## 1. Who buys a workshop like this

Someone buys a workshop like this when they need a classroom, not a running agent. Three buyer roles, all **[SYN]**:

| Buyer | Job they are hiring the class to do | What they already have | What this repo is |
| --- | --- | --- | --- |
| Engineering manager of a team about to let a model call tools | A shared bar for a bad effect before the first live call | A demo that calls tools, and no check that a write happened | The exercises and the gate |
| Enablement lead | One cohort that can say, out loud, what the gate is scoring | Slide time, and no lab | The facilitator guide and the grader |
| Platform owner | The first eval in the team's repo to be an invariant check that can be made to fail on purpose | A wish to "add evals" with no case list | `eval` and `eval-regression` as the pattern |

The fictional organization used below is **Taller Bruma**. Nobody with that name has purchased a seat. Scope in [SCOPE.md](SCOPE.md) says no fee is attached to this material, and there is no statement of work. A real buyer would still have to answer [DISCOVERY.md](DISCOVERY.md). Those answers are not collected here. **UNVERIFIED.**

This is not a comparison with a vendor course. No price from another provider is quoted.

---

## 2. Objectives and sponsor [SYN]

- **Executive sponsor:** the engineering director of Taller Bruma, who can require a gate on the next agent change.
- **Owner of the tool catalog, the grant list, and the golden cases after class:** the engineering lead of the adopting team. [ADAPT_TO_A_REAL_CLIENT.md](ADAPT_TO_A_REAL_CLIENT.md) says the same split. The job title is [SYN]. The split is the one this repo already describes.
- **Owner of the classroom and the synthetic depot:** the facilitator, only for the two sessions.

Objectives, as a plan. None of them has a delivered result:

- O1. **Team enablement.** After the sessions, a learner can implement the stop rule, refuse an ungranted write, and read a red invariant name.
- O2. **Faster eval adoption.** The team's next agent change carries an invariant gate, and a command that is supposed to exit non-zero when a write slips through.
- O3. **Fewer agent incidents.** Writes that nobody granted, and notes treated as instructions, show up as a red gate in class. Whether that changes a later incident count is a hypothesis.

O3 is the lever that sounds like money and is the one this repo cannot see. Section 6 keeps it in its own column so it can be removed.

---

## 3. Value levers

### Team enablement

The class gives twelve people **[EST]** the same words: `final`, a grant, a budget that can refuse a call, an effect check versus a trajectory check. The reference solutions pass the grader (**MEASURED**, section 0). A learner's own time-to-pass is **UNVERIFIED**. The feedback form in [FEEDBACK_FORM.md](FEEDBACK_FORM.md) has no responses.

### Fewer agent incidents

The expensive failure the modules point at is a write or an external send that nobody approved. `eval-regression` makes that failure red on purpose (**MEASURED**: exit 1). That is a teaching result. It is not a count of incidents in a running system, and it is not a claim that a red gate in class prevents one. Any incident number in the ROI is **[SYN]**.

### Faster eval adoption

The bet is that a team which has already broken a gate in class spends less calendar time arguing what the first eval should check. [METRICS.md](METRICS.md) already says the time to a first working agent has not been timed, and that "one session for modules 1–3, one session for 4–7" is a planning guess. Days-from-kickoff in a real repository are **UNVERIFIED**.

---

## 4. Plan KPIs

| KPI | Lever | Baseline | Target | How it would be measured | Now |
| --- | --- | --- | --- | --- | --- |
| Reference solutions passing the grader | Team enablement | modules 1–8 fail=0 | stays 0 when a module changes | `PYTHONPATH=src python -m workshop check all --impl solution` | **MEASURED** 2026-10-22. This is the answer key, not a learner |
| Learners who can say which check is an effect check and which would be a trajectory check | Team enablement | no cohort | the room, without notes, at the end of session 2 **[EST]** | Facilitator observation. [SCOPE.md](SCOPE.md) lists this as a class exit. There is no scored sheet | **UNVERIFIED** |
| Learner satisfaction | Team enablement | empty form | no target is claimed | [FEEDBACK_FORM.md](FEEDBACK_FORM.md) | **UNVERIFIED** |
| Calendar time from "we should add evals" to a gate that can go red | Faster eval adoption | no clock | end of session 2 for the classroom copy; 30 days **[EST]** for one gate in the team's repo | Dates on the team's pull requests | **UNVERIFIED** |
| Agent changes that include an effect check, a cost cap, and a fact check | Faster eval adoption | 0 in a team repo this workshop does not have **[SYN]** | the next agent change they control **[EST]** | Count in that repo. [METRICS.md](METRICS.md) already refuses to publish a percent | **UNVERIFIED** |
| Ungranted writes that land in a running system | Fewer agent incidents | no series. The ROI uses a story of 1 per year **[SYN]** | 0 on the paths they gate **[EST]** | Their incident review. `eval-regression` is the classroom stand-in and is **MEASURED** | Business KPI **UNVERIFIED** |
| Golden cases on the classroom gate | Lab health | 6 of 6 | stays green when a case is added by effects and facts | `PYTHONPATH=src python -m workshop eval` | **MEASURED** 2026-10-22 |
| Vendor spend for the labs | Cost of delivery | 0 on the default path | 0 for the class | CI does not call a paid API. The live flag stays unset | **MEASURED** as a property of this repo. A buyer's later live calls are out of this table |

> The repo measures the grader, the gate, the red regression, the test suite, and a SIMULATED token price. It does not measure a cohort, a satisfaction score, a pull-request sample, or an incident rate. Those business KPIs stay with the buyer.

---

## 5. ROI and the delivery cost [EST]

**Formulas**

- Delivery cost = facilitator hours × facilitator rate + learner hours × learner rate.
- Benefit = enablement hours avoided + design-thread hours avoided + incident allowance.
- ROI = (benefit − delivery cost) / delivery cost.
- Payback (months) = delivery cost / (benefit / 12), treating the benefit as a year-1 figure and the delivery cost as spent at the start.

**Shared assumptions.** Class size and hours match [BUSINESS_CASE.md](BUSINESS_CASE.md). The rates do not. They exist only in this sketch.

| Input | Figure | Label |
| --- | --- | --- |
| People in the room | 12 | [EST], same figure as BUSINESS_CASE |
| Contact time | 2 × 3 h = 6 h | [EST]. The workshop has not been delivered |
| Facilitator time, including prep | 8 h | [EST], same figure as BUSINESS_CASE |
| Learner time | 12 × 6 h = 72 h | [EST], same figure as BUSINESS_CASE |
| Loaded facilitator rate | 75 USD/h | [EST]. A round planning rate. Not a wage, not a quote |
| Loaded learner rate | 50 USD/h | [EST]. A round planning rate. Not a wage, not a quote |
| Vendor API for the labs | 0 USD | MEASURED path: fake provider, no network |
| Room or video | 0 USD | [EST]. Assumes the buyer's own room |

### Delivery cost table [EST]

| Item | Quantity | Rate | USD |
| --- | ---: | ---: | ---: |
| Facilitator, preparation and delivery | 8 h | 75 USD/h | 600 |
| Learners | 72 h | 50 USD/h | 3,600 |
| Room or video | — | 0 | 0 |
| Vendor API for the labs | 0 calls | 0 | 0 |
| **Delivery cost used in the ROI** | | | **4,200** |
| Optional second facilitator, not in the ROI total | 8 h | 75 USD/h | 600 |

SIMULATED demo cost of 0.00012000 USD is not a row in this table. Adding it would not change a figure rounded to the dollar.

### Benefit assumptions

| Lever | Base | Conservative | Minimum |
| --- | --- | --- | --- |
| Team enablement. Hours a learner does not later spend asking what the eval should check. Base 3 h each, conservative 1 h, minimum 0. Rate 50 USD/h **[EST]** | 12 × 3 × 50 = 1,800 | 12 × 1 × 50 = 600 | 0 |
| Faster eval adoption. A design thread that does not happen because the class already picked effect checks. Base: 2 engineers × 16 h × 50 = 1,600. Conservative: half of that thread still happens. Minimum: the thread still happens in full **[EST]** | 1,600 | 800 | 0 |
| Fewer agent incidents. Story: 1 ungranted-write incident a year, 6,000 USD fully loaded, for a company that does not exist **[SYN]**. Base counts it once. Conservative counts a 25% chance (expected value 1,500). Minimum counts nothing | 6,000 | 1,500 | 0 |

### Results [EST] and [SYN]

| Scenario | Benefit | ROI | Payback |
| --- | ---: | ---: | --- |
| **Base** | 1,800 + 1,600 + 6,000 = 9,400 | (9,400 − 4,200) / 4,200 = 5,200 / 4,200 ≈ **123.8%** | 4,200 / (9,400 / 12) ≈ **5.4 months** |
| **Conservative** | 600 + 800 + 1,500 = 2,900 | (2,900 − 4,200) / 4,200 ≈ **−31.0%** | 4,200 / (2,900 / 12) ≈ **17.4 months** (outside year 1) |
| **Minimum** | 0 | (0 − 4,200) / 4,200 = **−100%** | **never** |

**An honest reading**

- In the base case, the **[SYN] incident term is 6,000 of the 9,400** benefit. Strip it and the base benefit is 3,400 against a cost of 4,200, ROI ≈ **−19.0%**. Enablement hours and a shorter design thread, at these rates, do not pay for the class by themselves.
- The conservative case does not pay back inside a year. The minimum case has no benefit, which is the right row until a class has been delivered and a team has counted something.
- No row is a forecast for a named buyer. Replace the rates, the hours, and the incident story with discovery answers before anyone uses the percentage.

---

## 6. Measurement plan

The plan has four stages. Only stage 0 has been executed, and stage 0 is a maintainer check, not a delivery. **The workshop has not been delivered.**

| Stage | When [EST] | Work | Exit | State |
| --- | --- | --- | --- | --- |
| 0. Prep | Before any learner | Re-run eval, the red regression, pytest with coverage, the secret scan | Eval exits 0, regression exits 1, secretscan findings=0, tests meet the coverage floor | **MEASURED** 2026-10-22 for this tree. Repeating it is not a class |
| 1. Classroom | The two sessions, 6 h contact | Modules 1–7. Module 8 stays off the clock | Each learner's module 7 check fails 0, and the room can separate an effect check from a trajectory check | **UNVERIFIED**. No session has been held |
| 2. Adoption | 30 days after class | One repository the team controls uses the same three families: no harmful effect, a cost cap, facts they will maintain. A command exists whose healthy result is a red gate | That gate is on a real change, and the red command has been seen to exit non-zero | **UNVERIFIED** |
| 3. Retention | 90 days after class | The gate is still required on agent changes. An incident review looks for ungranted writes | The 30-day count did not fall back to zero | **UNVERIFIED** |

**What to record, if a class ever happens**

- The date, the commit, the Python version, and the pytest line (passed count and the TOTAL coverage).
- How many starters were still failing at the end of each module. The grader already prints `failed=`.
- Whether `eval-regression` was shown and the exit code was read aloud. [FACILITATOR.md](FACILITATOR.md) asks for that. There is no recording of a class.
- At 30 days, a count of agent changes with an effect check. At 90 days, a count of ungranted writes the team is willing to call incidents. Both counts belong to the buyer.

**What this plan will not treat as a measurement**

- SIMULATED USD and the scripted 15 ms latency.
- The deterministic checker's 5/6. That is checker versus author reference labels.
- An empty `templates/human_labels.csv`.
- A live LLM-judge score. The command exits 2 without configuration. No live score is stored.

**Buyer confirmation.** BVR-style confirmation would be a note from the sponsor and the engineering lead, with the evidence attached: the grader output, the pull request that added the gate, and the incident review. There is no sponsor. Nobody has signed. **UNVERIFIED.**

---

## 7. Risks

| Risk | Source | What to do about it |
| --- | --- | --- |
| A reader treats 123.8% as a result | This file | Read section 5. The percentage moves with the [SYN] incident term. The workshop has not been delivered |
| Class time does not fit in 6 hours | Duration is [EST]. No session has been timed | The facilitator guide is a plan. Cut module 3's protocol tour before cutting the red regression |
| The fake provider is described as a model that read the prompt | [RISKS.md](RISKS.md) | Module 1 says the script ignores messages. The demo prints `provider: fake` |
| The phrase detector is treated as the security boundary | [RISKS.md](RISKS.md) | Module 6 still fails a write when the phrase is only quoted |
| SIMULATED price is quoted as a vendor price | [COST.md](COST.md) | Keep the constant's name. Leave it out of the delivery-cost table |
| `checker_vs_reference=5/6` is quoted as model quality or as human agreement | [METRICS.md](METRICS.md) | Say "checker versus labels the author wrote" |
| A learner pastes a real key into an exercise | [RISKS.md](RISKS.md) | Live flag off. Secret scan in CI. No vendor client in the exercises |
| The teaching server is deployed as if it were the official MCP SDK | [adr/0003](adr/0003-teaching-mcp-subset.md) | Two read tools, stdio, revision 2026-07-28 cited, accessed 2026-10-17. The SDK is not a dependency |
| Stage 2 never gets an owner | [DISCOVERY.md](DISCOVERY.md) question 9 | If nobody owns the golden set, do not claim faster adoption |
| The optional LLM judge is turned on in the shared room | Module 8 | It is off the 2×3 h plan. CI does not run it |

Probability and impact for the teaching risks are the qualitative labels in [RISKS.md](RISKS.md). They are not measured frequencies.

---

## 8. What is MEASURED and what is not

| Claim | Label |
| --- | --- |
| 48 tests passed; 92.79% line coverage of `workshop`; Python 3.12.3; 2026-10-22; commit `9d10f1d4d4dc8045ccb85749204a926bc2dba912` | MEASURED |
| Eval 6 of 6; checker 5/6 against author reference labels; regression exit 1; solution modules fail=0; secretscan findings=0; llm-judge exit 2; ruff clean; mypy clean on 79 files | MEASURED the same day |
| Demo cost 0.00012000 USD and latency 15 ms | SIMULATED. The command printed them. They are not an invoice and not a sampled percentile |
| 12 people, 8 facilitator hours, 72 learner hours, 75 USD/h, 50 USD/h, delivery cost 4,200 USD | [EST] |
| 3 h or 1 h saved per learner; a 32 h design thread; ROI percentages; payback months | [EST], and they use the [SYN] incident term in the base and conservative rows |
| 1 incident a year at 6,000 USD; Taller Bruma as a buyer; the sponsor's title | [SYN] |
| A cohort, a satisfaction score, days-to-first-gate in a team repo, an incident rate, a signed confirmation | UNVERIFIED |
| That the class reduces incidents, speeds adoption, or is worth 4,200 USD to a real team | UNVERIFIED. Section 5 is a sketch that can be deleted without changing the labs |

The sentence to keep next to any of the percentages: **the workshop has not been delivered.**
