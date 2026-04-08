# LEARNING.md
# Layer 6: NotebookLM learning module plan

## Purpose

This file lists learning modules to generate from this Super Skill.
Each module becomes a NotebookLM source. Together they teach the
owner more about their own portfolio over time.

## Planned Modules

### LM-001: Drift-Based Rebalancing in Practice
What it covers: How DEC-003 actually plays out across realistic
market conditions. Worked examples for moderate, severe, and
asymmetric drift scenarios.
Source files: DEC-003, CURRENT_STATE.md, MONITORING.md
Output: notebooks/rebalancing-learning.md
Status: Planned

### LM-002: Single-Name Concentration Risk
What it covers: Why the 15% cap exists, what historical drawdowns
look like at different concentration levels, and how to measure
implicit single-name exposure inside index funds.
Source files: DEC-002, CURRENT_STATE.md (Risk Posture)
Output: notebooks/concentration-learning.md
Status: Planned

### LM-003: Tax-Aware Selling
What it covers: When a sale is the right move despite the tax bill,
holding period implications, and tax-loss harvesting basics.
Source files: EVALUATION.md (Tax efficiency criterion), DECISIONS.md
Output: notebooks/tax-aware-learning.md
Status: Planned

## How to Generate

  python scripts/feed_notebook.py
  python scripts/generate_learning.py audio
  python scripts/generate_learning.py quiz
  python scripts/generate_learning.py mindmap

## NotebookLM Sources

When this Super Skill is fed to NotebookLM, the following files
become sources: CONTEXT.md, DOMAIN_MAP.md, CURRENT_STATE.md,
EVALUATION.md, DECISIONS.md, MONITORING.md, PENDING.md, plus any
notebooks/ files generated from this plan.
