---
name: super-skill
description: >
  Domain expert layer. Loads full context, methodology, and
  operational knowledge for the defined domain. Gives any AI
  agent complete understanding before any action is taken.
version: "1.0"
author: "Gitit Inc"
---

# Super Skill - Agent Entry Point
# © 2026 Gitit Inc - AI Architecture
# MIT License - Fork it. Build your own.

## Before Any Action

Read these files in this order:
  1. CONTEXT.md        - who owns this, what domain, what goals
  2. CURRENT_STATE.md  - what the domain looks like right now
  3. PENDING.md        - what is waiting for human approval

Never skip this sequence. Context before action, always.

## Operating Principle

The model proposes. The human decides.
The Super Skill records. The system executes.

Write all proposals and evaluations to PENDING.md.
Do not modify any layer file without explicit human approval.

## Domain Files

After reading the three required files above, load the
remaining layer files as needed for the current task:
  DOMAIN_MAP.md     - structure and sub-domain relationships
  EVALUATION.md     - criteria for evaluating new entrants
  DECISIONS.md      - decisions made and reasoning
  MONITORING.md     - sources to watch for drift
  LEARNING.md       - NotebookLM integration structure

## Learning Generation

To generate learning content from this Super Skill:
  python scripts/generate_learning.py audio
  python scripts/generate_learning.py quiz
  python scripts/generate_learning.py mindmap
