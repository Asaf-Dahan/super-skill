#!/usr/bin/env python3
# generate_global_graph.py -- Merge knowledge graphs from all local Super Skills.
#
# Scans the parent directory for super-skill-* folders, reads each
# wiki/graph.json, and produces a combined global graph:
#   ~/.claude/global-graph.html   -- interactive visual across all domains
#
# Run with:
#   python scripts/generate_global_graph.py
#   python scripts/run.py generate_global_graph
#
# Stdlib only. No third-party dependencies.

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parent.parent


def find_super_skills(base: Path) -> list:
    """Find all super-skill-* directories that contain wiki/graph.json."""
    results = []
    parent = base.parent
    for d in sorted(parent.iterdir()):
        if not d.is_dir():
            continue
        if not d.name.startswith("super-skill"):
            continue
        graph_file = d / "wiki" / "graph.json"
        if graph_file.exists():
            results.append((d, graph_file))
    return results


def merge_graphs(sources: list) -> dict:
    """Merge multiple graph.json files into a single global graph."""
    all_nodes = []
    all_edges = []
    domain_summaries = []
    total_pending = 0
    total_decisions = 0
    total_drift = 0

    for repo_dir, graph_file in sources:
        try:
            data = json.loads(graph_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  Warning: could not read {graph_file}: {e}")
            continue

        domain = repo_dir.name
        meta = data.get("meta", {})

        total_pending += meta.get("open_pending", 0)
        total_decisions += meta.get("open_decisions", 0)
        total_drift += meta.get("drift_alerts", 0)

        domain_summaries.append({
            "domain": domain,
            "path": str(repo_dir),
            "generated": meta.get("generated", ""),
            "node_count": meta.get("node_count", 0),
            "edge_count": meta.get("edge_count", 0),
            "open_pending": meta.get("open_pending", 0),
            "drift_alerts": meta.get("drift_alerts", 0),
        })

        # Prefix node and edge IDs with domain name to avoid collisions
        for node in data.get("nodes", []):
            node["id"] = f"{domain}/{node['id']}"
            node["domain"] = domain
            all_nodes.append(node)

        for edge in data.get("edges", []):
            edge["source"] = f"{domain}/{edge['source']}"
            edge["target"] = f"{domain}/{edge['target']}"
            all_edges.append(edge)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    global_graph = {
        "meta": {
            "generated": today,
            "type": "global",
            "domain_count": len(domain_summaries),
            "node_count": len(all_nodes),
            "edge_count": len(all_edges),
            "total_pending": total_pending,
            "total_decisions": total_decisions,
            "total_drift": total_drift,
        },
        "domains": domain_summaries,
        "nodes": all_nodes,
        "edges": all_edges,
    }
    return global_graph


def generate_global_html(graph: dict) -> str:
    """Generate a simple global overview HTML."""
    graph_json = json.dumps(graph, indent=2)
    domains = graph.get("domains", [])

    domain_cards = ""
    for d in domains:
        status = ""
        if d["open_pending"] > 0:
            status += f' | <span style="color:#f0883e">{d["open_pending"]} pending</span>'
        if d["drift_alerts"] > 0:
            status += f' | <span style="color:#f85149">{d["drift_alerts"]} drift</span>'
        domain_cards += f'''
        <div class="domain-card">
          <h3>{d["domain"]}</h3>
          <div class="stats">{d["node_count"]} nodes, {d["edge_count"]} edges{status}</div>
          <div class="path">{d["path"]}</div>
          <div class="date">Generated: {d["generated"]}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Super Skill -- Global Knowledge Graph</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: #0d1117; color: #c9d1d9;
  font-family: system-ui, -apple-system, sans-serif;
  padding: 24px;
}}
h1 {{ color: #f0f6fc; margin-bottom: 8px; }}
.subtitle {{ color: #8b949e; margin-bottom: 24px; font-size: 14px; }}
.meta-bar {{
  display: flex; gap: 24px; margin-bottom: 24px;
  padding: 12px 16px; background: #161b22;
  border: 1px solid #30363d; border-radius: 8px; font-size: 13px;
}}
.meta-bar .item {{ color: #8b949e; }}
.meta-bar .value {{ color: #58a6ff; font-weight: 600; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
.domain-card {{
  background: #161b22; border: 1px solid #30363d; border-radius: 8px;
  padding: 16px; transition: border-color 0.2s;
}}
.domain-card:hover {{ border-color: #58a6ff; }}
.domain-card h3 {{ color: #f0f6fc; margin-bottom: 6px; }}
.domain-card .stats {{ color: #c9d1d9; font-size: 13px; margin-bottom: 4px; }}
.domain-card .path {{ color: #484f58; font-size: 11px; word-break: break-all; }}
.domain-card .date {{ color: #484f58; font-size: 11px; margin-top: 4px; }}
</style>
</head>
<body>
<h1>Global Knowledge Graph</h1>
<div class="subtitle">All Super Skills on this machine</div>

<div class="meta-bar">
  <div class="item">Domains: <span class="value">{graph["meta"]["domain_count"]}</span></div>
  <div class="item">Total nodes: <span class="value">{graph["meta"]["node_count"]}</span></div>
  <div class="item">Total edges: <span class="value">{graph["meta"]["edge_count"]}</span></div>
  <div class="item">Open pending: <span class="value">{graph["meta"]["total_pending"]}</span></div>
  <div class="item">Drift alerts: <span class="value">{graph["meta"]["total_drift"]}</span></div>
</div>

<div class="grid">{domain_cards}
</div>

<script>
// Global graph data available for future interactive features
const G = {graph_json};
</script>
</body>
</html>'''


def main():
    base = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else REPO

    sources = find_super_skills(base)
    if not sources:
        print("No super-skill-* directories with wiki/graph.json found.")
        print(f"Searched: {base.parent}")
        print("Run 'python scripts/generate_graph.py' in each Super Skill first.")
        return 1

    print(f"Found {len(sources)} Super Skill(s):")
    for repo_dir, _ in sources:
        print(f"  - {repo_dir.name}")

    graph = merge_graphs(sources)

    # Write to ~/.claude/
    claude_dir = Path.home() / ".claude"
    claude_dir.mkdir(exist_ok=True)

    html_path = claude_dir / "global-graph.html"
    html_path.write_text(generate_global_html(graph), encoding="utf-8")

    print(f"\nGlobal graph generated:")
    print(f"  Domains: {graph['meta']['domain_count']}")
    print(f"  Nodes:   {graph['meta']['node_count']}")
    print(f"  Edges:   {graph['meta']['edge_count']}")
    print(f"  Output:  {html_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
