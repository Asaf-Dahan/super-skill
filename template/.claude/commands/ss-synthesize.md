Synthesize all expert responses for a debate session.

## Usage
/ss-synthesize [session-name]

## What this does
Reads all expert response files for the named session.
Identifies points of agreement and disagreement.
Writes a synthesis summary to experts\debates\[session]-synthesis.md
Writes a proposed decision to PENDING.md as DEC-NNN.
You decide whether to adopt the recommendation.

## Prompt
Read the session definition file:
  experts\debates\$ARGUMENTS.md

Find all expert response files matching the pattern:
  experts\debates\$ARGUMENTS-*.md
Exclude the session file itself and any existing synthesis file.

Read each expert response file.

Write a synthesis to: experts\debates\$ARGUMENTS-synthesis.md

The synthesis must include:
- Points all experts agree on
- Points where experts disagree and why
- The strongest argument from each side
- A recommended path forward based on the weight of expert opinion
- What remains uncertain or unresolved

Then write a proposed decision to PENDING.md as DEC-NNN:
  Title: Expert Synthesis -- $ARGUMENTS
  Recommendation: [one sentence]
  Based on: [expert names who contributed]
  Full analysis: see experts\debates\$ARGUMENTS-synthesis.md

Maximum 6 expert response files per synthesis session. If more than 6 files are present, instruct the user to group them and run synthesis in two rounds.

End with: "Synthesis complete. Review DEC-NNN in PENDING.md and decide."
