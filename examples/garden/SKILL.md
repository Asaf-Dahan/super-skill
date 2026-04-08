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
  3. PENDING.md        - what is waiting for human approval

Never skip this sequence. Context before action, always.

## Operating Principle

The model proposes. The human decides.
The Super Skill records. The system executes.

Write all proposals and evaluations to PENDING.md.
Do not modify any layer file without explicit human approval.

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

## Learning Generation

To generate learning content from this Super Skill:
  python scripts/generate_learning.py audio
  python scripts/generate_learning.py quiz
  python scripts/generate_learning.py mindmap
