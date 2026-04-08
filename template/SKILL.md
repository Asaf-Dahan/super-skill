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
  DOMAIN_MAP.md          - structure and sub-domain relationships
  EVALUATION.md          - criteria for evaluating new entrants
  DECISIONS.md           - decisions made and reasoning
  MONITORING.md          - sources to watch for drift
  LEARNING.md            - NotebookLM integration structure
  experts/COUNCIL.md     - active expert council and debates

Individual expert profiles (experts/[name].md) load on demand only,
not by default. Load them when a specific expert's perspective is needed.

## Domain Scope

Products: [LIST YOUR PRODUCTS OR PROJECTS]
Shared services: [SERVICES USED ACROSS PRODUCTS]
[Product A]-specific: [SERVICES UNIQUE TO THIS PRODUCT]
[Product B]-specific: [SERVICES UNIQUE TO THIS PRODUCT]

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
