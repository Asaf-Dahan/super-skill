<!--
Note: All names, companies, and projects in this example are fictional
and used for instructional purposes only.
-->
---
name: super-skill-stack-os
description: >
  Technical stack domain expert for a solopreneur SaaS operation.
  Loads full context on infrastructure, hosting, services, tiers,
  and cross-product dependencies for GreenLedger and PulseLog.
  Gives any AI agent verified current state before any action.
version: "1.0"
author: "Tomer Naveh / Raincode Labs"
tags:
  - infrastructure
  - hosting
  - technical-stack
  - devops
  - cloud-services
---

# Super Skill -- Stack OS

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

## Domain Scope

Products: GreenLedger (sustainability reporting SaaS),
  PulseLog (uptime and incident logging dashboard)
Shared services: DBHost, CDNLayer, GitHub, Anthropic API
GreenLedger-specific: UIBuilder, Stripe, Resend
PulseLog-specific: AppHost, Streamlit (admin), Python backend

## Domain Files

After reading the three required files above, load the
remaining layer files as needed for the current task:
  DOMAIN_MAP.md     - structure and sub-domain relationships
  EVALUATION.md     - criteria for evaluating new entrants
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
