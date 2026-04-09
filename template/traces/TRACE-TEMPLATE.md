<!-- TEMPLATE FILE -- Do not edit. This is the scaffold. Root files are your working copy. -->
# Execution Traces
# Super Skill - Execution Trace Log

## Purpose
This file records raw execution traces: what was attempted, what
happened, and what was inferred. Traces enable causal reasoning
across decisions, evaluations, and drift events.

Each trace links to related decisions (DEC-NNN), evaluations (EVAL-NNN),
or prior traces (TRC-NNN) to form causal chains.

## Trace Template

### TRC-001: [Trace Title]
Date: [YYYY-MM-DD]
Trigger: [What initiated this action -- user request, drift alert, evaluation, scheduled task, etc.]
Attempted: [What was tried, in one sentence.]
Result: [What actually happened -- success, failure, partial, unexpected.]
Inference: [What was learned or concluded from the result.]
Causal links: [DEC-NNN, TRC-NNN, EVAL-NNN -- related items, or "none"]
Status: [recorded | superseded-by TRC-NNN]

## Trace Log
[Empty -- traces are added here as actions are executed and recorded.]
