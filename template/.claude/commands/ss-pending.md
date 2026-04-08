Show all open items awaiting approval across this Super Skill.

## Usage
/ss-pending

## What this does
Reads PENDING.md and reports all open items.
Groups by type: EVAL, DRIFT, UPDATE, DEC.
Shows how many days each item has been waiting.

## Prompt
Read PENDING.md for the active domain.

Report all open items grouped by type:
- EVAL-NNN: evaluations awaiting decision
- DRIFT-NNN: drift alerts awaiting review
- UPDATE-NNN: proposed updates awaiting approval
- DEC-NNN: proposed decisions awaiting approval

For each item show: ID, title, date added, days waiting, recommended action.
If queue is empty, report: "Queue clear. No items awaiting approval."
Do not modify PENDING.md.
