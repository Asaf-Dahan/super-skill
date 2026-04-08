# Expert Debates

This folder contains parallel expert analysis sessions.

## How It Works

Each debate is a structured question put to two or more experts
from the Expert Council simultaneously. Experts work in separate
Claude Code terminals using git worktrees so they cannot see
each other's responses until synthesis.

## File Naming

| File | Purpose |
|------|---------|
| [session-name].md | Session definition and question |
| [session-name]-[expert-name].md | One expert's analysis |
| [session-name]-synthesis.md | Final synthesis across all experts |

## Running a Session

Step 1: Copy SESSION-TEMPLATE.md and fill in the question.
Step 2: Set up git worktrees for parallel terminals:
  git worktree add ..\[repo]-expert-1 main
  git worktree add ..\[repo]-expert-2 main
Step 3: Open Claude Code in each worktree terminal.
Step 4: Run /ss-expert [name] [session] in each terminal.
Step 5: When all experts have written, run /ss-synthesize [session]
        in the main terminal.
Step 6: Review the DEC-NNN item in PENDING.md and decide.

## Git Worktrees -- Quick Reference

Create worktrees:
  git worktree add ..\[repo]-expert-1 main
  git worktree add ..\[repo]-expert-2 main

List active worktrees:
  git worktree list

Remove a worktree after the session:
  git worktree remove ..\[repo]-expert-1
