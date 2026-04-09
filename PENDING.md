# PENDING.md
# Super Skill - Layer 7: Approval Queue
<!-- Replace this header with your own project/organization name -->

## Operating Rule
Nothing changes in this Super Skill without appearing here first.
The model proposes. The human decides. The Super Skill records. The system executes.

## Pending Item Template

### PENDING-001: [Title]
Type: [drift / evaluation / update / new-decision]
Proposed: [YYYY-MM-DD]
Summary: [What is being proposed and why.]
Affected layers: [Which files would change if approved.]
Recommended action: [What the agent recommends - adopt / reject / defer]
Decision: [APPROVED / REJECTED / DEFERRED - filled in by human]
Outcome: [What happened after the decision.]

## Queue

### PENDING-GRAPH-001: Knowledge graph integration complete
Type: update
Proposed: 2026-04-09
Summary: Knowledge graph system added to the Super Skill framework. New scripts generate_graph.py and generate_global_graph.py produce wiki/graph.json (machine-readable domain map with layer_index, hotspots, staleness, navigation_hints), wiki/knowledge-graph.html (interactive D3.js force-directed visual), and wiki/GRAPH_SUMMARY.md (prose summary for NotebookLM). New /ss-graph slash command added. Graph Navigation Protocol added to CLAUDE.md. doctor.py includes INFO-level graph check. feed_notebook.py updated to include GRAPH_SUMMARY.md. NotebookLM decision: YES to GRAPH_SUMMARY.md (prose), NO to raw graph.json. All changes are additive -- no existing behavior removed or changed. Human review required before merging.
Affected layers: CLAUDE.md, SKILL.md, ONBOARDING.md, README.md, doctor.py, feed_notebook.py
Recommended action: review and adopt
Decision:
Outcome:

## Resolved Items
[Approved and rejected items move here after decision.]
