Generate or regenerate the knowledge graph for this domain.

## Usage
/ss-graph

## What this does
Runs generate_graph.py which reads all layer files, expert profiles,
decisions, pending items, wiki pages, and LOG.md activity. Outputs:
  wiki/graph.json             -- machine-readable routing map for Claude
  wiki/knowledge-graph.html   -- interactive visual (open in browser)
  wiki/GRAPH_SUMMARY.md       -- prose summary for NotebookLM

## When to run
- After any significant change to layer files
- When starting a session with a new domain you do not know yet
- When you want a fresh visual of the domain structure

## Prompt
Run: python scripts/generate_graph.py .

After running, report:
  - Number of nodes and edges found
  - Path to knowledge-graph.html
  - Whether any hotspots were detected (open pending, drift alerts)
  - Whether graph.json was written successfully

Then say exactly:
"Graph updated. Open wiki/knowledge-graph.html in your browser to explore.
Hex nodes = layer files. Circles = experts, decisions, pending items.
Click to focus connections. Double-click for the detail panel."
