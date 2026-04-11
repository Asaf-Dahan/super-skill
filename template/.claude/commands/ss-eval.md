Evaluate a new tool, service, or method against this Super Skill.

## Usage
/ss-eval [name of tool or service]

## What this does
Reads SUMMARY.md and EVALUATION.md for the active domain.
Runs a full evaluation against the criteria defined in EVALUATION.md.
Writes the result to PENDING.md as EVAL-NNN.
Does not recommend adoption -- writes findings only.
You decide.

## Prompt
Read SUMMARY.md and EVALUATION.md for the active domain.
Do not load any other files unless EVALUATION.md references them.

Evaluate: $ARGUMENTS

Score against every criterion in EVALUATION.md.
Write the full evaluation to PENDING.md as EVAL-NNN.
Include: what it is, scores per criterion, total score, what it would replace or complement.
Do not recommend adoption or rejection.
If a new tool scores identically to an existing tool, apply secondary comparison on lock-in risk and implementation complexity as defined in EVALUATION.md. If still tied, write both to PENDING.md and flag as a tie for user decision.
End with: "Evaluation written to PENDING.md. Review and decide."
