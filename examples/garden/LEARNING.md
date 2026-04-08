# LEARNING.md
# Layer 6: NotebookLM learning module plan

## Purpose

This file lists learning modules to generate from this Super Skill.
Each module becomes a NotebookLM source. Together they teach the
owner more about their own garden over time.

## Planned Modules

### LM-001: Crop Rotation Strategies for Small Beds
What it covers: How three-year rotation by family applies to a
five-bed garden. Worked examples for nightshade, brassica, allium,
legume, and cover crop rotations.
Source files: DECISIONS.md (DEC-002), DOMAIN_MAP.md
Output: notebooks/crop-rotation-learning.md
Status: Planned

### LM-002: Drip Irrigation Schedules for Dry-Summer Climates
What it covers: How to calculate run time and frequency by crop
type and bed size. References this garden's actual bed dimensions.
Source files: CURRENT_STATE.md, DEC-001
Output: notebooks/drip-irrigation-learning.md
Status: Planned

### LM-003: Composting Without Synthetic Inputs
What it covers: Browns vs greens, temperature management, avoiding
weed seed contamination. References the compost bin's current state.
Source files: DEC-003, CURRENT_STATE.md (compost section)
Output: notebooks/composting-learning.md
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
