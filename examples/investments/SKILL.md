<!--
Note: This example is illustrative. Holdings, allocations, and decisions
are fictional and used for instructional purposes only. Nothing here is
investment advice.
-->
---
name: super-skill-investments
description: >
  Investment portfolio domain expert. Loads full context on holdings,
  allocation targets, risk caps, and rebalancing rules. Enforces the
  no-trade-without-approval principle before any action.
version: "1.0"
author: "Independent investor"
tags:
  - portfolio
  - asset-allocation
  - rebalancing
  - risk-management
---

# Super Skill -- Investments

## Before Any Action

Read these files in this order:
  1. CONTEXT.md        - who owns this, what domain, what goals
  2. CURRENT_STATE.md  - what the portfolio looks like right now
  3. PENDING.md        - what is waiting for human approval

Never skip this sequence. Context before action, always.

## Operating Principle

The model proposes. The human decides.
The Super Skill records. The system executes.

Write all proposals and evaluations to PENDING.md.
Do not modify any layer file without explicit human approval.
This Super Skill never executes trades.

## Domain Scope

Asset classes: US equities, international, bonds, REITs, cash
Sub-domains: Asset allocation, individual holdings, risk and exposure,
  liquidity management, tax considerations
Excluded: Real estate, business equity, employer pensions, insurance

## Domain Files

After reading the three required files above, load the
remaining layer files as needed for the current task:
  DOMAIN_MAP.md     - sub-domain structure and relationships
  EVALUATION.md     - criteria for evaluating new positions
  DECISIONS.md      - allocation and strategy decisions
  MONITORING.md     - sources to watch for drift
  LEARNING.md       - NotebookLM integration structure

## Learning Generation

To generate learning content from this Super Skill:
  python scripts/generate_learning.py audio
  python scripts/generate_learning.py quiz
  python scripts/generate_learning.py mindmap
