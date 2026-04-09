# CLAUDE.md
# Super Skill - Claude Code Operating Instructions
<!-- Replace this header with your own project/organization name -->

## Session Start Protocol

Every session starts with two files only:

1. SUMMARY.md        -- domain snapshot, 80 lines max, start here
2. PENDING.md        -- open items awaiting owner approval

Read both before anything else. Do not load additional files unless
the specific task requires it. See the Load Protocol table in SUMMARY.md.

## How to Find Available Prompts

All prompts and slash commands: see ONBOARDING.md

## When to Load Full Files

| Task type                        | File to load           |
|----------------------------------|------------------------|
| Architecture or tech decision    | DECISIONS.md           |
| Tool version, plan, or status    | CURRENT_STATE.md       |
| Approve or respond to a proposal | PENDING.md             |
| Domain structure or sub-domains  | DOMAIN_MAP.md          |
| Evaluate a new tool or method    | EVALUATION.md          |
| Generate learning content        | LEARNING.md            |
| Expert council or debates        | experts/COUNCIL.md     |
| Individual expert profile        | experts/[name].md      |
| Change history or audit trail    | LOG.md                 |
| Understand domain structure quickly | wiki/graph.json      |
| Execution trace or causal analysis | traces/              |

Never load a file the current task does not require.
Individual expert profiles load on demand only, not by default.

## Graph Navigation Protocol

Before loading layer files, check wiki/graph.json if it exists.
It routes you to the right file without loading everything.

## Operating Rules

- Never modify a layer file without explicit approval from the owner
- All proposals go to PENDING.md -- never directly to layer files
- If a task affects multiple sub-domains, note all impacts in PENDING.md
- If asked about something not in the current state, say so honestly
- Generate learning content on request -- write output to notebooks/ folder

## What Requires Owner Approval

- Any change to CURRENT_STATE.md
- Any new entry in DECISIONS.md
- Any adoption or rejection in EVALUATION.md
- Any update to DOMAIN_MAP.md

## What Does Not Require Approval

- Reading and explaining existing content
- Generating learning modules to notebooks/
- Writing proposals to PENDING.md
- Running scripts (feed, generate, check, update_summary)

## Keeping SUMMARY.md Current

After any approved change to any layer file, run:

  python scripts/update_summary.py

Or let super-skill-sync handle it automatically on the next pull.

## Expert Perspectives Protocol

When returning answers on architecture, evaluation, or decisions:

1. Check if experts in experts/COUNCIL.md hold conflicting positions on this topic.
2. If yes: append an Expert Perspectives block after your answer.
3. If consensus or the topic is routine: no block needed.
4. Active debates in COUNCIL.md always surface when their topic is touched.

Expert Perspectives block format:

  Expert Perspectives:
  [Expert Name, Layer N]: [one sentence -- agrees / disagrees / challenges]
  [Expert Name, Layer N]: [one sentence]

Maximum 3 experts per block. Maximum 1 line per expert.
Do not mention experts on routine tasks or settled decisions with no friction.

## Iron Principle

The model proposes.
The human decides.
The Super Skill records.
The system executes.
