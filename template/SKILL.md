---
name: super-skill
description: >
  Domain expert layer. Loads full context, methodology, and
  operational knowledge for the defined domain. Gives any AI
  agent complete understanding before any action is taken.
version: "1.0"
author: "[YOUR NAME OR ORGANIZATION]"
---

<!-- TEMPLATE FILE -- Do not edit. This is the scaffold. Root files are your working copy. -->
# Super Skill - Agent Entry Point
<!-- Replace this header with your own project/organization name -->

## Before Any Action

Read these files in this order:
  1. CONTEXT.md        - who owns this, what domain, what goals
  2. CURRENT_STATE.md  - what the domain looks like right now
  3. PENDING.md        - what is waiting for user approval

Never skip this sequence. Context before action, always.

## Operating Principle

The model proposes. The user decides.
The Super Skill records. The system executes.

Write all proposals and evaluations to PENDING.md.
Do not modify any layer file without explicit user approval.

## Domain Files

After reading the three required files above, load the
remaining layer files as needed for the current task:
  DOMAIN_MAP.md          - structure and sub-domain relationships
  EVALUATION.md          - criteria for evaluating new entrants
  DECISIONS.md           - decisions made and reasoning
  MONITORING.md          - sources to watch for drift
  LEARNING.md            - NotebookLM integration structure
  LOG.md                 - change log and audit trail
  experts/COUNCIL.md     - active expert council and debates
  traces/                - execution traces for causal reasoning
  wiki/graph.json        - domain structure map (optional; run /ss-graph to generate)

Individual expert profiles (experts/[name].md) load on demand only,
not by default. Load them when a specific expert's perspective is needed.

## Evidence Routing

Before proposing any change, load the files most likely to contain
relevant evidence for your task type. This prevents blind proposals.

| Task type                    | Evidence files (load in order)                    |
|------------------------------|---------------------------------------------------|
| Evaluate a new tool/method   | EVALUATION.md, CURRENT_STATE.md, DECISIONS.md     |
| Propose architecture change  | DECISIONS.md, DOMAIN_MAP.md, CURRENT_STATE.md     |
| Investigate drift or breakage | MONITORING.md, CURRENT_STATE.md, traces/          |
| Resolve a PENDING item       | PENDING.md, DECISIONS.md, EVALUATION.md           |
| Generate learning content    | LEARNING.md, CONTEXT.md, CURRENT_STATE.md         |
| Root-cause analysis          | traces/, DECISIONS.md, LOG.md                     |
| Cross-domain impact check    | DOMAIN_MAP.md, CURRENT_STATE.md, DECISIONS.md     |
| Expert disagreement          | experts/COUNCIL.md, DECISIONS.md, experts/[name].md |

Load the minimum set. Do not load files not listed for your task type.

## How Prompts Work

All prompts live in ONBOARDING.md.
Claude Code reads and runs them automatically.
Users do not copy prompts after the initial Bootstrap setup.

Slash commands: see CLAUDE.md

## Learning Generation

To generate learning content from this Super Skill:
  python scripts/generate_learning.py audio
  python scripts/generate_learning.py quiz
  python scripts/generate_learning.py mindmap

## Capabilities

### File operations (no shell required)
- Reading and explaining any layer file
- Writing proposals to PENDING.md
- Generating learning content to notebooks/

### Shell required
- python scripts/update_summary.py   (regenerate SUMMARY.md)
- python scripts/feed_notebook.py    (push files to NotebookLM)
- python scripts/generate_learning.py audio | quiz | mindmap
