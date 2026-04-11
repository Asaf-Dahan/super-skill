<!-- TEMPLATE FILE -- Do not edit. This is the scaffold. Root files are your working copy. -->
# SCHEDULE.md
# Super Skill - Scheduled Maintenance Tasks
<!-- Replace this header with your own project/organization name -->

## Purpose

This file defines all recurring maintenance tasks for this Super Skill.
Tasks are run by Claude Code on a schedule you define.
Every task writes findings to PENDING.md only.
Nothing changes automatically. You decide on every item.

## How to Run

Manual trigger (any time):
  python scripts\scheduled_tasks.py --task [task-name]

Run all tasks for current frequency:
  python scripts\scheduled_tasks.py --frequency weekly
  python scripts\scheduled_tasks.py --frequency monthly
  python scripts\scheduled_tasks.py --frequency quarterly

Dry run (no files written):
  python scripts\scheduled_tasks.py --dry-run

## Weekly Tasks

### TASK-W1: Drift Check
Script trigger: --task drift-check
What it does: Checks all URLs in MONITORING.md for availability.
Writes DRIFT-NNN to PENDING.md for any source that fails or changes.
Time to run: under 2 minutes.

### TASK-W2: SUMMARY.md Refresh
Script trigger: --task summary-refresh
What it does: Regenerates SUMMARY.md from all layer files.
Ensures the session entry point is current.
Time to run: under 30 seconds.

### TASK-W3: PENDING.md Health Check
Script trigger: --task pending-check
What it does: Reports all items open for more than 7 days.
Flags items with no decision as stale.
Does not modify PENDING.md -- reports only.
Time to run: under 10 seconds.

## Monthly Tasks

### TASK-M1: NotebookLM Sync
Script trigger: --task notebooklm-sync
What it does: Runs feed_notebook.py to push all layer files to NotebookLM.
Keeps the learning layer current.
Time to run: 2-5 minutes depending on file count.

### TASK-M2: Expert Council Review
Script trigger: --task council-review
What it does: Reports all debates open for more than 30 days.
Flags expert challenges that have not been reviewed.
Does not modify any file -- reports only.
Time to run: under 30 seconds.

### TASK-M3: Monitoring Sources Audit
Script trigger: --task monitoring-audit
What it does: Verifies all URLs in MONITORING.md are still valid.
Flags sources that have moved, changed, or disappeared.
Writes UPDATE-NNN to PENDING.md for any source needing replacement.
Time to run: 2-3 minutes.

## Quarterly Tasks

### TASK-Q1: CURRENT_STATE.md Verification
Script trigger: --task state-verify
What it does: Prompts you to manually verify each item in CURRENT_STATE.md.
Generates a verification checklist in notebooks\verification-[date].md
Does not modify CURRENT_STATE.md -- you update it after review.
Time to run: depends on domain size.

### TASK-Q2: DECISIONS.md Audit
Script trigger: --task decisions-audit
What it does: Reviews all decisions older than 90 days.
Flags any decision that references a tool or version that may have changed.
Writes UPDATE-NNN to PENDING.md for any decision needing re-evaluation.
Time to run: under 2 minutes.

### TASK-Q3: EVALUATION.md Review
Script trigger: --task evaluation-review
What it does: Reviews all rejected evaluations older than 90 days.
Flags any rejected tool that has since released major updates.
Writes EVAL-NNN to PENDING.md for any tool worth re-evaluating.
Time to run: under 1 minute.

### TASK-Q4: Expert Council Refresh
Script trigger: --task council-refresh
What it does: Reviews all expert profiles for continued relevance.
Flags any expert whose known position may have changed based on recent publications.
Writes UPDATE-NNN to PENDING.md for any profile needing review.
Time to run: under 1 minute.

## Recommended Schedule

| Frequency | When to run |
|-----------|-------------|
| Weekly | Every Sunday morning before starting work |
| Monthly | First Sunday of each month |
| Quarterly | First Sunday of January, April, July, October |

Run weekly tasks first. Monthly tasks include weekly tasks.
Quarterly tasks include monthly and weekly tasks.

## Output

All task output goes to PENDING.md as the appropriate item type.
Nothing is written to layer files directly.
The model proposes. The user decides. The Super Skill records. The system executes.
