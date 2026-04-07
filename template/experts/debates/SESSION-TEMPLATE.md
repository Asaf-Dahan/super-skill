# Expert Debate Session -- [SESSION-NAME]
# Created: [YYYY-MM-DD]
# Domain: [domain name]
# Status: OPEN

## The Question

[One clear question or problem that requires expert analysis.
Be specific. The more precise the question, the more useful the expert responses.]

## Context

[2-3 sentences of relevant background from CURRENT_STATE.md or DECISIONS.md.
What has already been decided that experts should know about?]

## What We Need

[What kind of output do you want from the experts?
Example: "A recommendation on which approach to take."
Example: "An analysis of risks we have not considered."]

## Experts Assigned

| Expert | Profile file | Status |
|--------|-------------|--------|
| [Name] | experts\[firstname-lastname].md | Pending |
| [Name] | experts\[firstname-lastname].md | Pending |

## How to Run This Session

Open a separate Claude Code terminal for each expert.
In each terminal, run:
  /ss-expert [expert-name] [session-name]

Each expert writes their analysis to:
  experts\debates\[session-name]-[expert-name].md

When all experts have written, run in the main terminal:
  /ss-synthesize [session-name]

## Synthesis

[Written by the orchestrator session after all experts have responded.
Summarizes agreements, disagreements, and a recommended path forward.
Goes to PENDING.md as DEC-NNN for owner approval.]
