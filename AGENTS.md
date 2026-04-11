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

Read files in this order before any task:

  1. SUMMARY.md        -- 80-line overview of the full domain (read this first, always)
  2. PENDING.md        -- what is waiting for user approval

Load additional files only if the specific task requires them:

| If the task involves        | Load this file     |
|-----------------------------|--------------------|
| Architecture or tool decision | DECISIONS.md     |
| Tool version or current status | CURRENT_STATE.md |
| Domain structure or sub-domains | DOMAIN_MAP.md  |
| Evaluating something new    | EVALUATION.md      |
| Generating learning content | LEARNING.md        |
| Expert council or debates   | experts/COUNCIL.md |
| Execution trace or causal analysis | traces/       |
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
  - python scripts/update_summary.py   -- regenerate SUMMARY.md
  - python scripts/feed_notebook.py    -- push files to NotebookLM
  - python scripts/generate_learning.py audio | quiz | mindmap

## The One Rule

The model proposes. The user decides.
The Super Skill records. The system executes.
Write all proposals to PENDING.md.
Do not modify any layer file without explicit user approval.

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
- The user resolves all conflicts and approves decisions
- Before writing a new PENDING item, check PENDING.md to avoid duplicates
- Use unique proposal IDs: EVAL-NNN, DRIFT-NNN, UPDATE-NNN

## Slash Commands

For ongoing tasks, use slash commands:
  /ss-eval, /ss-learn, /ss-pending, /ss-sync,
  /ss-summary, /ss-drift, /ss-council, /ss-expert, /ss-synthesize

## Using with Gemini

Gemini can operate a Super Skill the same way Claude Code does, with one
adjustment: Gemini does not auto-load files on session start, so you load
the entry points yourself.

**Gemini CLI** (`gemini` command-line tool): from inside the Super Skill
folder, paste the contents of SUMMARY.md and SKILL.md into your first
message. Then ask Gemini to read PENDING.md and the relevant layer file
for the task. Gemini will follow the Iron Principle as long as you keep
SKILL.md in context, because the rules are encoded there.

**Gemini Code Assist** (VS Code or JetBrains): open the Super Skill folder
as a workspace. Use the chat panel and reference @SUMMARY.md @SKILL.md
@PENDING.md in your prompt. Gemini Code Assist supports the @file syntax
to attach repository files directly to the request.

**Gemini in any other editor**: same pattern as Cursor. Open the folder,
ask the agent to read ONBOARDING.md, and run the prompt that matches your
task. The Iron Principle applies regardless of which Gemini surface you use.

## Compatible Agents

This Super Skill follows the Agent Skills open standard.
It works with Claude Code, Cursor, Codex, Gemini, and any agent
that can read and write markdown files.
