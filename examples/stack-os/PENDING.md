# PENDING.md
# Layer 7: Approval queue for all proposed changes

## Operating Rule
Nothing changes in this Super Skill without appearing here first.
The model proposes. The human decides. The Super Skill records. The system executes.

## Pending Item Template

### PENDING-001: DBHost connection pooling limit change
Type: drift
Proposed: 2026-03-20
Summary: DBHost updated their free tier to reduce max connections from 60 to 20. Both products share a single instance. Current usage peaks at 35 connections during evening traffic.
Affected layers: CURRENT_STATE.md, MONITORING.md
Recommended action: adopt -- upgrade to the starter tier or add connection pooling via PgBouncer
Decision:
Outcome:

## Queue
### PENDING-002: NotebookLM not yet connected
Type: update
Proposed: 2026-04-09
Summary: The NotebookLM learning layer is not yet connected. When ready, follow NOTEBOOKLM_GUIDE.md or run /ss-learn to generate audio, quizzes, and mind maps from your domain knowledge.
Affected layers: LEARNING.md
Recommended action: adopt when ready
Decision:
Outcome:

## Resolved Items
[Approved and rejected items move here after decision.]
