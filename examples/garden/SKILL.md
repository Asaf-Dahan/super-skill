<!--
Note: This example is illustrative. Garden details are fictional and
used for instructional purposes only.
-->
---
name: super-skill-garden
description: >
  Home vegetable garden domain expert. Loads full context on beds,
  soil, water, crop rotation, and seasonal planning. Enforces water
  efficiency and organic-only operating principles before any action.
version: "1.0"
author: "Home gardener"
tags:
  - garden
  - vegetables
  - soil
  - irrigation
  - crop-rotation
---

# Super Skill -- Garden

## Before Any Action

Read these files in this order:
  1. CONTEXT.md        - who owns this, what domain, what goals
  2. CURRENT_STATE.md  - what the garden looks like right now
  3. PENDING.md        - what is waiting for user approval

Never skip this sequence. Context before action, always.

## Operating Principle

The model proposes. The user decides.
The Super Skill records. The system executes.

Write all proposals and evaluations to PENDING.md.
Do not modify any layer file without explicit user approval.

## Domain Scope

Beds: Five active raised beds (1-5), one perennial strawberry bed
Sub-domains: Seasonal calendar, soil management, water systems,
  pest and disease control, crop rotation
Excluded: Fruit trees, ornamentals, lawn, indoor plants

## Domain Files

After reading the three required files above, load the
remaining layer files as needed for the current task:
  DOMAIN_MAP.md     - sub-domain structure and relationships
  EVALUATION.md     - criteria for evaluating new plants or methods
  DECISIONS.md      - decisions made and reasoning
  MONITORING.md     - sources to watch for drift
  LEARNING.md       - NotebookLM integration structure
  traces/           - execution traces for causal reasoning

## Evidence Routing

Before proposing any change, load the files most likely to contain
relevant evidence for your task type.

| Task type                    | Evidence files (load in order)                    |
|------------------------------|---------------------------------------------------|
| Evaluate a new tool/method   | EVALUATION.md, CURRENT_STATE.md, DECISIONS.md     |
| Propose architecture change  | DECISIONS.md, DOMAIN_MAP.md, CURRENT_STATE.md     |
| Investigate drift or breakage | MONITORING.md, CURRENT_STATE.md, traces/          |
| Resolve a PENDING item       | PENDING.md, DECISIONS.md, EVALUATION.md           |
| Generate learning content    | LEARNING.md, CONTEXT.md, CURRENT_STATE.md         |
| Root-cause analysis          | traces/, DECISIONS.md, LOG.md                     |
| Cross-domain impact check    | DOMAIN_MAP.md, CURRENT_STATE.md, DECISIONS.md     |

Load the minimum set. Do not load files not listed for your task type.

## Learning Generation

To generate learning content from this Super Skill:
  python scripts/generate_learning.py audio
  python scripts/generate_learning.py quiz
  python scripts/generate_learning.py mindmap
