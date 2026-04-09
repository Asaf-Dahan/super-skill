---
name: super-skill
description: >
  Domain expert layer. Loads full context, methodology, and
  operational knowledge for the defined domain. Gives any AI
  agent complete understanding before any action is taken.
version: "1.0"
author: "[YOUR NAME OR ORGANIZATION]"
---

# Super Skill - Agent Entry Point
<!-- Replace this header with your own project/organization name -->

## Before Any Action

Read these files in this order:
  1. CONTEXT.md        - who owns this, what domain, what goals
  2. CURRENT_STATE.md  - what the domain looks like right now
  3. PENDING.md        - what is waiting for human approval

Never skip this sequence. Context before action, always.

## Operating Principle

Iron Principle: propose → PENDING.md → human decides → system executes.

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
  wiki/graph.json        - domain structure map (optional; run /ss-graph to generate)

Individual expert profiles (experts/[name].md) load on demand only,
not by default. Load them when a specific expert's perspective is needed.

## How Prompts Work

All prompts live in ONBOARDING.md.
Claude Code reads and runs them automatically.
Users do not copy prompts after the initial Bootstrap setup.

Slash commands: see CLAUDE.md

## Capabilities

Operating rules and capabilities: see CLAUDE.md
