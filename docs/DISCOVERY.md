# Discovery

Ten questions to ask before copying this workshop onto a real team. Each answer changes the design. None of these were collected from a real client; they are the questions the material expects.

1. Who is in the room: engineers who will edit the loop, or people who will only watch a demo?
   If they will not edit Python, keep modules 1, 4, and 6 as discussion and do not assign the grader. The capstone assumes they can change a function.

2. Do they already ship something that calls tools?
   If yes, start from module 2 and module 4. The loop explanation can be short. If no, module 1 is the whole first hour.

3. Which effects are allowed to be real?
   If the answer is "reads only," do not register a write tool at all. This repo keeps `inventory.adjust` off the MCP export and behind a grant, so the class can see a blocked write. A read-only team can delete the write tool.

4. Who is allowed to grant a write, and how do you know it is them?
   This repo only checks that the tool name is in a set. If the answer is "a named role in our directory," the grant has to come from that system. The string `approver` here is not that system.

5. What is the money cap per task, and who raises it?
   The number in `.env.example` (`WORKSHOP_BUDGET_USD=0.01`) is a simulated cap for class. A real cap is their number. The admission check in `budget.py` stays; the constant price does not.

6. Can the room reach the internet?
   If no, you are already on the supported path. If yes, still leave the live flag off until the gate is green. CI in this repo never sets the flag.

7. Do they need a vendor-specific module (a particular host's tool format)?
   That module is design-only. If they need it, cite the vendor's public page with the date you read it, and do not put a live call in the shared exercises.

8. What does "good" mean: a fact in the answer, a human preference, or both?
   Facts and effects are implemented. Preference is the calibration section: the literal judge and the human label disagree once on purpose. If they need a real judge model, it stays out of the default gate until they have labels.

9. Who owns the golden set six weeks later?
   If nobody owns it, the gate will rot. The adopting engineering lead should own cases. The facilitator owns them only during the class.

10. What is the rollback if a gate is wrong (too strict, or blind)?
    Too strict: a case demands an exact sentence the product no longer uses. Fix the fact, do not delete the effect check. Blind: the regression command exits 0. Treat that as a broken alarm, which is what CI does. See [RUNBOOK.md](RUNBOOK.md).
