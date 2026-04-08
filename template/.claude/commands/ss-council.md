Show the Expert Council status for the active domain.

## Usage
/ss-council

## What this does
Reads experts\COUNCIL.md for the active domain.
Reports all active debates and any expert challenges in PENDING.md.
Does not load individual expert profiles unless you ask.

## Prompt
Read experts\COUNCIL.md for the active domain.
Read PENDING.md and filter for any EXPERT-CHALLENGE-NNN items.

Report:
- Council members (name, primary layer, status)
- Active debates (ID, participants, topic, days open)
- Expert challenges in PENDING.md (ID, expert, decision challenged)

If no council exists yet, report: "Expert Council not yet activated for this domain."
Do not load individual expert profile files unless explicitly asked.
