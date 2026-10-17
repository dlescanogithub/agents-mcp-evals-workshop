# Business case

Audience: someone deciding whether a delivery team should spend two sessions on this material. The team in the story is fictional. The name used here is Taller Bruma. There is no engagement behind it.

## What would change in team behaviour

The bet, stated as a hypothesis, is narrow:

- A practice change includes an invariant check, not only a transcript of a happy chat.
- A write tool does not ship on "the prompt says be careful."
- A budget figure exists before the first live call, even if the figure is a cap the team picks.

This repository does not measure those behaviours on a real team. [METRICS.md](METRICS.md) says which of the numbers exist here and which are [EST].

## ROI sketch [EST]

Planning assumptions, not a measurement and not a fee:

| Input | Figure | Kind |
| --- | --- | --- |
| People in the room | 12 | [EST] |
| Sessions | 2 × 3 hours | [EST]. The workshop has not been delivered |
| Facilitator time, including prep | 8 hours | [EST] |
| Learner time | 12 × 6 hours = 72 hours | [EST] |
| Vendor API spend for the labs | 0 | Measured path: fake provider, no network. The demo's simulated token cost on 2026-10-17 was 0.00012000 USD at the made-up rate in `budget.py`. That number is not an invoice. |

There is no dollar return in this repo. A team that wanted a money model would need its own loaded cost per hour and its own incident history. Those are not here, and inventing them would be a fake case.

## What the material is worth practicing

The expensive failure mode the modules point at is a write or an external send that nobody approved, discovered after the fact. The workshop makes that failure mode show up on purpose (`eval-regression`) so the group can see a red gate. That is a teaching result, not a claim that a red gate in class prevents a production incident.

## What this case is not

It is not a proposal with a price. It is not evidence that a named employer runs this class. It is not a comparison against a vendor's course.
