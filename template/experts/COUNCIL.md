# Expert Council - [domain name]

Activated: [activation date]
Members: [member count]

## Council Members

| Name | Primary Layer | One-Line Methodology | Status |
|------|---------------|----------------------|--------|
| [Expert 1 full name] | Layer [N]: [layer name] | [One sentence describing their core approach] | Active |
| [Expert 2 full name] | Layer [N]: [layer name] | [One sentence describing their core approach] | Active |
| [Expert 3 full name] | Layer [N]: [layer name] | [One sentence describing their core approach] | Active |

## Active Debates

Active debates surface automatically when Claude Code touches the relevant topic.
Each debate represents a genuine methodological disagreement between council members.

### DEBATE-001: [debate title]

Participants: [Expert A] vs [Expert B]
Layer affected: Layer [N] - [layer name]
Topic: [One sentence describing the point of disagreement]
Position A: [Expert A name] holds that [one sentence position].
Position B: [Expert B name] holds that [one sentence position].
Status: Open
Date opened: [date]

Implications for this domain:
[Two to three sentences on how this disagreement affects the owner's specific context.]

<!-- Add as many DEBATE-NNN sections as needed. There is no cap on debate count. -->

### DEBATE-NNN: [next debate title]

Participants: [Expert C] vs [Expert D]
Layer affected: Layer [N] - [layer name]
Topic: [One sentence describing the point of disagreement]
Position A: [Expert C name] holds that [one sentence position].
Position B: [Expert D name] holds that [one sentence position].
Status: Open
Date opened: [date]

Implications for this domain:
[Two to three sentences on how this disagreement affects the owner's specific context.]

## Expert-Challenged Decisions

When an expert's known position conflicts with a decision recorded in DECISIONS.md,
the challenge is written to PENDING.md as EXPERT-CHALLENGE-NNN.

The owner reviews the challenge and decides whether to:
- Reaffirm the original decision with the expert's objection noted
- Reopen the decision for re-evaluation
- Record the expert's position as a dissenting view

Challenges do not override decisions. The user decides.

| Challenge ID | Expert | Decision Challenged | Status |
|--------------|--------|---------------------|--------|
| [EXPERT-CHALLENGE-001] | [Expert name] | [DEC-NNN: short description] | [Pending / Resolved] |

## How Expert Perspectives Surface

Claude Code does not mention experts on every response.
Expert perspectives appear only when:

1. The topic touches an active debate listed above.
2. An expert's known position directly conflicts with a proposed action.
3. The owner asks for expert input explicitly.

Format when surfacing:

  Expert Perspectives:
  [Expert Name, Layer N]: [one sentence position]

Maximum 3 experts per block. Maximum 1 line per expert.
Routine tasks and settled decisions do not trigger expert perspectives.

## Removing or Replacing an Expert

To remove an expert from the council:
1. Write a PENDING item: "Remove [Expert Name] from council -- reason: [reason]"
2. User approves the PENDING item
3. Move the expert's .md file from experts/ to experts/archive/ (create the folder if needed)
4. Remove the expert's entry from COUNCIL.md active members list
5. Update SUMMARY.md via /ss-summary

To replace an expert: complete the removal steps above, then run /ss-council to propose a replacement.
