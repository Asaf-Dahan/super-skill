# AGENTS.md
# Super Skill - Instructions for Any AI Agent
<!-- Replace this header with your own project/organization name -->

## What This Repository Is

This is a Super Skill repository. It contains structured domain
knowledge organized in 8 layers. Your role is to read, apply,
and maintain this knowledge on behalf of the owner.

This file is self-contained. You do not need to read another file
to understand the operating rules. Everything you need is here.

## Load Protocol

Note: This file is the entry point for non-Claude agents.
It uses the lightweight SUMMARY.md-first protocol.
Claude Code uses SKILL.md or CLAUDE.md which follow a different
load sequence designed for its specific capabilities.

Read files in this order before any task:

  1. SUMMARY.md        -- 80-line overview of the full domain (read this first, always)
  2. PENDING.md        -- what is waiting for human approval

Load additional files only if the specific task requires them:

| If the task involves        | Load this file     |
|-----------------------------|--------------------|
| Architecture or tool decision | DECISIONS.md     |
| Tool version or current status | CURRENT_STATE.md |
| Domain structure or sub-domains | DOMAIN_MAP.md  |
| Evaluating something new    | EVALUATION.md      |
| Generating learning content | LEARNING.md        |
| Expert council or debates   | experts/COUNCIL.md |
| Approval action             | PENDING.md         |

Individual expert profiles (experts/[name].md) load on demand only,
not by default. Load them when a specific expert's perspective is needed.

Never load a file the task does not require.

## Capability Map

File-only (no shell required):
  - Reading and explaining any layer file
  - Writing proposals to PENDING.md
  - Generating learning content to notebooks/

Shell required:
  - python3 scripts/update_summary.py   -- regenerate SUMMARY.md
  - python3 scripts/feed_notebook.py    -- push files to NotebookLM
  - python3 scripts/generate_learning.py audio | quiz | mindmap

## The One Rule

The model proposes. The human decides.
The Super Skill records. The system executes.
Write all proposals to PENDING.md.
Do not modify any layer file without explicit human approval.

## What Requires Approval

- Any change to CURRENT_STATE.md
- Any new entry in DECISIONS.md
- Any adoption or rejection in EVALUATION.md
- Any change to DOMAIN_MAP.md

## What Does Not Require Approval

- Reading and explaining existing content
- Writing proposals to PENDING.md
- Generating learning modules to notebooks/
- Running scripts

## Multi-Agent Use

If multiple agents are writing to this repository:

- Each agent writes proposals to PENDING.md independently
- The human resolves all conflicts and approves decisions
- Before writing a new PENDING item, check PENDING.md to avoid duplicates
- Use unique proposal IDs: EVAL-NNN, DRIFT-NNN, UPDATE-NNN

## Slash Commands

For ongoing tasks, use slash commands:
  /ss-eval, /ss-learn, /ss-pending, /ss-sync,
  /ss-summary, /ss-drift, /ss-council, /ss-expert, /ss-synthesize

## Compatible Agents

This Super Skill follows the Agent Skills open standard.
It works with Claude Code, Cursor, Codex, and any agent
that can read and write markdown files.
