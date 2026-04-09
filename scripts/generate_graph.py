#!/usr/bin/env python3
# generate_graph.py -- Build a knowledge graph from Super Skill layer files.
#
# Outputs:
#   wiki/graph.json             -- machine-readable domain map for Claude Code
#   wiki/knowledge-graph.html   -- interactive D3.js visual for humans
#
# Run with:
#   python scripts/generate_graph.py            (Windows / cross-platform)
#   python3 scripts/generate_graph.py           (macOS / Linux)
#   python scripts/run.py generate_graph        (auto-detects interpreter)
#
# Stdlib only. No third-party dependencies.

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Layer metadata: cluster assignments, descriptions, question routing
# ---------------------------------------------------------------------------

LAYER_META = {
    "CONTEXT.md":       {"layer": 0, "cluster": "identity",  "label": "Identity",
                         "answers": ["what domain", "who owns this", "operating principles"]},
    "DOMAIN_MAP.md":    {"layer": 1, "cluster": "identity",  "label": "Domain Map",
                         "answers": ["domain structure", "sub-domains", "how areas connect"]},
    "CURRENT_STATE.md": {"layer": 2, "cluster": "state",     "label": "Current State",
                         "answers": ["current tools", "versions", "what is true right now"]},
    "EVALUATION.md":    {"layer": 3, "cluster": "knowledge", "label": "Evaluation",
                         "answers": ["evaluation criteria", "how to assess new entrants"]},
    "DECISIONS.md":     {"layer": 4, "cluster": "knowledge", "label": "Decisions",
                         "answers": ["decisions made", "reasoning", "rejected alternatives"]},
    "MONITORING.md":    {"layer": 5, "cluster": "state",     "label": "Monitoring",
                         "answers": ["drift detection", "what sources to watch"]},
    "LEARNING.md":      {"layer": 6, "cluster": "knowledge", "label": "Learning",
                         "answers": ["NotebookLM plan", "learning content"]},
    "PENDING.md":       {"layer": 7, "cluster": "control",   "label": "Pending",
                         "answers": ["open approvals", "proposed changes"]},
    "LOG.md":           {"layer": -1, "cluster": "control",  "label": "Change Log",
                         "answers": ["change history", "audit trail", "activity log"]},
    "SKILL.md":         {"layer": -1, "cluster": "control",  "label": "Skill Entry",
                         "answers": ["agent entry point", "slash commands"]},
    "SUMMARY.md":       {"layer": -1, "cluster": "control",  "label": "Summary",
                         "answers": ["domain snapshot", "quick overview"]},
}

CLUSTER_LABELS = {
    "identity":  "Identity Layer",
    "state":     "State Layer",
    "knowledge": "Knowledge Layer",
    "control":   "Control Layer",
    "experts":   "Expert Council",
}

# Navigation hints -- pre-computed question routing
NAVIGATION_HINTS = [
    {"if_user_asks_about": "architecture decisions",       "read_first": "DECISIONS.md"},
    {"if_user_asks_about": "what is waiting for approval", "read_first": "PENDING.md"},
    {"if_user_asks_about": "current tools or versions",    "read_first": "CURRENT_STATE.md"},
    {"if_user_asks_about": "who are the domain experts",   "read_first": "experts/COUNCIL.md"},
    {"if_user_asks_about": "domain structure or areas",    "read_first": "DOMAIN_MAP.md"},
    {"if_user_asks_about": "how to evaluate something new","read_first": "EVALUATION.md"},
    {"if_user_asks_about": "what has changed recently",    "read_first": "LOG.md"},
    {"if_user_asks_about": "drift or monitoring alerts",   "read_first": "MONITORING.md"},
    {"if_user_asks_about": "learning or NotebookLM",       "read_first": "LEARNING.md"},
]

# Placeholder detection (reused from doctor.py logic)
_PLACEHOLDER_RE = re.compile(r"^\[[^\]]*\]?\s*$")


def _file_last_modified(path: Path) -> str:
    """Return last-modified date as YYYY-MM-DD, or empty string if missing."""
    try:
        ts = os.path.getmtime(path)
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except OSError:
        return ""


def _is_activated(path: Path) -> bool:
    """Return True if the file has real content (not mostly placeholders)."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    placeholders = 0
    content_lines = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
            continue
        content_lines += 1
        if not stripped.startswith("["):
            continue
        if "](" in stripped:
            continue
        if _PLACEHOLDER_RE.match(stripped):
            placeholders += 1
    if content_lines == 0:
        return False
    return (placeholders / content_lines) < 0.5


def _count_pending_open(path: Path) -> int:
    """Count open PENDING items (lines matching ### PENDING- or ### EVAL- etc.)."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    # Only count items above the Resolved section
    resolved_idx = text.find("## Resolved")
    if resolved_idx > 0:
        text = text[:resolved_idx]
    return len(re.findall(r"###\s+(PENDING|EVAL|DRIFT|UPDATE|DEC)-\d+", text))


def _count_decisions(path: Path) -> int:
    """Count DEC- entries."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    return len(re.findall(r"###\s+DEC-\d+", text))


def _count_drift_alerts(path: Path) -> int:
    """Count CRITICAL/HIGH lines in MONITORING.md."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    count = 0
    for line in text.splitlines():
        if "CRITICAL" in line or "HIGH" in line or "ALERT" in line:
            count += 1
    return count


def _extract_log_entries(path: Path, max_entries: int = 20) -> list:
    """Extract recent LOG-NNN entries with date and title."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    entries = []
    blocks = text.split("### LOG-")
    for block in blocks[1:]:
        lines = block.strip().split("\n")
        title_line = lines[0].strip() if lines else ""
        num = title_line.split(":")[0].strip() if ":" in title_line else title_line[:4]
        title = title_line.split(":", 1)[1].strip() if ":" in title_line else title_line
        date = ""
        for line in lines[1:5]:
            if line.strip().startswith("Date:"):
                date = line.split(":", 1)[1].strip()
                break
        if _PLACEHOLDER_RE.match(title.strip()):
            continue
        entries.append({"id": f"LOG-{num}", "title": title, "date": date})
    entries.reverse()
    return entries[:max_entries]


def _extract_detail(path: Path) -> str:
    """Extract a short description from the file (first non-heading, non-placeholder line)."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("<!--") or stripped.startswith("---"):
            continue
        if _PLACEHOLDER_RE.match(stripped):
            continue
        if stripped.startswith("[") and "](" not in stripped:
            continue
        return stripped[:120]
    return ""


def _find_experts(repo: Path) -> list:
    """Find expert profile .md files under experts/."""
    experts_dir = repo / "experts"
    if not experts_dir.is_dir():
        return []
    out = []
    for f in sorted(experts_dir.glob("*.md")):
        if f.name in ("COUNCIL.md", "EXPERT_TEMPLATE.md"):
            continue
        out.append(f)
    return out


def _find_wiki_pages(repo: Path) -> list:
    """Find .md files in wiki/ excluding README.md."""
    wiki_dir = repo / "wiki"
    if not wiki_dir.is_dir():
        return []
    return [f for f in sorted(wiki_dir.glob("*.md")) if f.name != "README.md"]


# ---------------------------------------------------------------------------
# Edge inference: which files reference which others
# ---------------------------------------------------------------------------

def _infer_edges(repo: Path, node_ids: set) -> list:
    """Scan file contents for cross-references between known node IDs."""
    edges = []
    seen = set()
    for nid in node_ids:
        path = repo / nid
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for target in node_ids:
            if target == nid:
                continue
            # Check for filename reference (e.g. "DECISIONS.md" mentioned in PENDING.md)
            if target in text:
                key = (nid, target)
                if key not in seen:
                    edges.append({"source": nid, "target": target, "type": "reference"})
                    seen.add(key)
    # Structural edges: PENDING -> every numbered layer file (approval flows into them)
    structural = [
        ("PENDING.md", "DECISIONS.md", "approval_flow"),
        ("PENDING.md", "CURRENT_STATE.md", "approval_flow"),
        ("PENDING.md", "EVALUATION.md", "approval_flow"),
        ("PENDING.md", "DOMAIN_MAP.md", "approval_flow"),
        ("SUMMARY.md", "CONTEXT.md", "generated_from"),
        ("SUMMARY.md", "CURRENT_STATE.md", "generated_from"),
        ("SUMMARY.md", "DECISIONS.md", "generated_from"),
        ("SUMMARY.md", "PENDING.md", "generated_from"),
        ("SUMMARY.md", "MONITORING.md", "generated_from"),
        ("LOG.md", "PENDING.md", "records_from"),
    ]
    for src, tgt, etype in structural:
        key = (src, tgt)
        if key not in seen and src in node_ids and tgt in node_ids:
            edges.append({"source": src, "target": tgt, "type": etype})
            seen.add(key)
    return edges


# ---------------------------------------------------------------------------
# Hotspot and staleness detection
# ---------------------------------------------------------------------------

def _compute_hotspots(nodes: list, open_pending: int, drift_alerts: int) -> list:
    """Identify nodes with high activity or concern."""
    hotspots = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for n in nodes:
        lm = n.get("last_modified", "")
        if not lm:
            continue
        try:
            days_ago = (datetime.strptime(today, "%Y-%m-%d") -
                        datetime.strptime(lm, "%Y-%m-%d")).days
        except ValueError:
            continue
        if n["id"] == "PENDING.md" and open_pending > 0:
            hotspots.append({
                "file": "PENDING.md",
                "reason": f"{open_pending} open item{'s' if open_pending != 1 else ''}",
                "priority": "high" if open_pending >= 3 else "medium",
            })
        elif n["id"] == "MONITORING.md" and drift_alerts > 0:
            hotspots.append({
                "file": "MONITORING.md",
                "reason": f"{drift_alerts} drift alert{'s' if drift_alerts != 1 else ''}",
                "priority": "high",
            })
        elif days_ago <= 2 and n["id"] not in ("SUMMARY.md", "SKILL.md"):
            hotspots.append({
                "file": n["id"],
                "reason": f"modified {days_ago} day{'s' if days_ago != 1 else ''} ago",
                "priority": "medium",
            })
    return hotspots


def _compute_staleness(nodes: list) -> list:
    """Identify layer files not updated recently."""
    stale = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    watchlist = {
        "CURRENT_STATE.md": "verified state may be outdated",
        "MONITORING.md":    "drift undetected",
        "EVALUATION.md":    "evaluation criteria may be outdated",
        "DOMAIN_MAP.md":    "domain structure may have changed",
    }
    for n in nodes:
        if n["id"] not in watchlist:
            continue
        lm = n.get("last_modified", "")
        if not lm:
            stale.append({
                "file": n["id"],
                "last_modified": "unknown",
                "risk": watchlist[n["id"]],
            })
            continue
        try:
            days_ago = (datetime.strptime(today, "%Y-%m-%d") -
                        datetime.strptime(lm, "%Y-%m-%d")).days
        except ValueError:
            continue
        if days_ago > 30:
            stale.append({
                "file": n["id"],
                "last_modified": lm,
                "risk": watchlist[n["id"]],
            })
    return stale


# ---------------------------------------------------------------------------
# Main graph builder
# ---------------------------------------------------------------------------

def build_graph(repo: Path) -> dict:
    """Build the full graph data structure."""
    repo = repo.resolve()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    nodes = []
    node_ids = set()

    # --- Layer file nodes ---
    for filename, meta in LAYER_META.items():
        path = repo / filename
        exists = path.exists()
        node = {
            "id": filename,
            "type": "layer",
            "label": meta["label"],
            "layer": meta["layer"],
            "cluster": meta["cluster"],
            "file": path.name,
            "exists": exists,
            "activated": _is_activated(path) if exists else False,
            "last_modified": _file_last_modified(path) if exists else "",
            "detail": _extract_detail(path) if exists else "",
            "answers": meta["answers"],
        }
        nodes.append(node)
        node_ids.add(filename)

    # --- Expert nodes ---
    council_path = repo / "experts" / "COUNCIL.md"
    if council_path.exists():
        node = {
            "id": "experts/COUNCIL.md",
            "type": "council",
            "label": "Expert Council",
            "layer": -1,
            "cluster": "experts",
            "file": council_path.name,
            "exists": True,
            "activated": _is_activated(council_path),
            "last_modified": _file_last_modified(council_path),
            "detail": _extract_detail(council_path),
            "answers": ["domain expert opinions", "methodology", "debates"],
        }
        nodes.append(node)
        node_ids.add("experts/COUNCIL.md")

    for expert_file in _find_experts(repo):
        rel = f"experts/{expert_file.name}"
        node = {
            "id": rel,
            "type": "expert",
            "label": expert_file.stem.replace("-", " ").title(),
            "layer": -1,
            "cluster": "experts",
            "file": expert_file.name,
            "exists": True,
            "activated": True,
            "last_modified": _file_last_modified(expert_file),
            "detail": _extract_detail(expert_file),
            "answers": [],
        }
        nodes.append(node)
        node_ids.add(rel)

    # --- Wiki page nodes ---
    for wiki_file in _find_wiki_pages(repo):
        rel = f"wiki/{wiki_file.name}"
        node = {
            "id": rel,
            "type": "wiki",
            "label": wiki_file.stem.replace("-", " ").title(),
            "layer": -1,
            "cluster": "knowledge",
            "file": wiki_file.name,
            "exists": True,
            "activated": True,
            "last_modified": _file_last_modified(wiki_file),
            "detail": _extract_detail(wiki_file),
            "answers": [],
        }
        nodes.append(node)
        node_ids.add(rel)

    # --- Edges ---
    edges = _infer_edges(repo, node_ids)

    # --- Degree computation ---
    degree = {nid: 0 for nid in node_ids}
    for e in edges:
        degree[e["source"]] = degree.get(e["source"], 0) + 1
        degree[e["target"]] = degree.get(e["target"], 0) + 1
    for n in nodes:
        n["degree"] = degree.get(n["id"], 0)

    # --- Aggregate counts ---
    open_pending = _count_pending_open(repo / "PENDING.md")
    open_decisions = _count_decisions(repo / "DECISIONS.md")
    drift_alerts = _count_drift_alerts(repo / "MONITORING.md")
    log_entries = _extract_log_entries(repo / "LOG.md")

    # --- Hotspots and staleness ---
    hotspots = _compute_hotspots(nodes, open_pending, drift_alerts)
    staleness = _compute_staleness(nodes)

    # --- Layer index ---
    layer_index = {
        "identity":  LAYER_META["CONTEXT.md"]["answers"] + LAYER_META["DOMAIN_MAP.md"]["answers"],
        "state":     LAYER_META["CURRENT_STATE.md"]["answers"] + LAYER_META["MONITORING.md"]["answers"],
        "knowledge": LAYER_META["EVALUATION.md"]["answers"] + LAYER_META["DECISIONS.md"]["answers"]
                     + LAYER_META["LEARNING.md"]["answers"],
        "control":   LAYER_META["PENDING.md"]["answers"] + LAYER_META["LOG.md"]["answers"]
                     + LAYER_META["SUMMARY.md"]["answers"],
        "experts":   ["domain expert opinions", "methodology", "debates"],
    }

    # --- Clusters for rendering ---
    clusters = {}
    for n in nodes:
        c = n["cluster"]
        if c not in clusters:
            clusters[c] = {"label": CLUSTER_LABELS.get(c, c), "nodes": []}
        clusters[c]["nodes"].append(n["id"])

    graph = {
        "meta": {
            "generated": today,
            "repo": repo.name,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "open_pending": open_pending,
            "open_decisions": open_decisions,
            "drift_alerts": drift_alerts,
        },
        "layer_index": layer_index,
        "navigation_hints": NAVIGATION_HINTS,
        "hotspots": hotspots,
        "staleness": staleness,
        "log_entries": log_entries,
        "nodes": nodes,
        "edges": edges,
        "clusters": clusters,
    }
    return graph


# ---------------------------------------------------------------------------
# HTML generator
# ---------------------------------------------------------------------------

def generate_html(graph: dict) -> str:
    """Generate a self-contained interactive knowledge graph HTML file."""
    graph_json = json.dumps(graph, indent=2)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Super Skill -- Knowledge Graph</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0d1117; color: #c9d1d9; font-family: system-ui, -apple-system, sans-serif; overflow: hidden; }}

/* Log bar */
#log-bar {{
  position: fixed; top: 0; left: 0; right: 0; height: 32px; z-index: 100;
  background: #161b22; border-bottom: 1px solid #30363d;
  display: flex; align-items: center; padding: 0 12px;
  font-size: 11px; color: #8b949e; overflow: hidden; white-space: nowrap;
}}
#log-bar .log-entry {{ margin-right: 24px; }}
#log-bar .log-muted {{ color: #484f58; font-style: italic; }}

/* Controls */
#controls {{
  position: fixed; top: 40px; right: 12px; z-index: 90;
  display: flex; flex-direction: column; gap: 6px;
}}
#controls button {{
  background: #21262d; border: 1px solid #30363d; color: #c9d1d9;
  padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 12px;
}}
#controls button:hover {{ background: #30363d; }}

/* Search */
#search-box {{
  position: fixed; top: 40px; left: 12px; z-index: 90;
}}
#search-box input {{
  background: #0d1117; border: 1px solid #30363d; color: #c9d1d9;
  padding: 5px 10px; border-radius: 6px; font-size: 12px; width: 200px;
}}

/* Filter buttons */
#filters {{
  position: fixed; top: 72px; left: 12px; z-index: 90;
  display: flex; gap: 4px; flex-wrap: wrap;
}}
#filters button {{
  background: #21262d; border: 1px solid #30363d; color: #8b949e;
  padding: 3px 8px; border-radius: 12px; cursor: pointer; font-size: 10px;
}}
#filters button.active {{ border-color: #58a6ff; color: #58a6ff; }}

/* Detail panel */
#panel {{
  position: fixed; top: 40px; right: 180px; z-index: 80;
  background: #161b22; border: 1px solid #30363d; border-radius: 8px;
  padding: 16px; width: 320px; max-height: calc(100vh - 60px);
  overflow-y: auto; display: none; font-size: 13px;
}}
#panel h3 {{ color: #f0f6fc; margin-bottom: 8px; font-size: 15px; }}
#panel .meta {{ color: #8b949e; font-size: 11px; margin-bottom: 6px; }}
#panel .detail {{ color: #c9d1d9; margin-bottom: 10px; line-height: 1.5; }}
#panel .connections {{ margin-top: 8px; }}
#panel .conn-item {{ color: #58a6ff; font-size: 12px; cursor: pointer; padding: 2px 0; }}
#panel .conn-item:hover {{ text-decoration: underline; }}
#panel .btn-row {{ display: flex; gap: 6px; margin-top: 10px; }}
#panel .btn-row button {{
  background: #21262d; border: 1px solid #30363d; color: #c9d1d9;
  padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 11px;
}}
#panel .btn-row button:hover {{ background: #30363d; }}
#panel-close {{
  position: absolute; top: 8px; right: 8px; background: none;
  border: none; color: #8b949e; cursor: pointer; font-size: 16px;
}}

/* Minimap */
#minimap {{
  position: fixed; bottom: 12px; right: 12px; z-index: 80;
  width: 160px; height: 120px; background: #161b22;
  border: 1px solid #30363d; border-radius: 6px; overflow: hidden;
}}

/* Legend */
#legend {{
  position: fixed; bottom: 12px; left: 12px; z-index: 80;
  background: #161b22; border: 1px solid #30363d; border-radius: 6px;
  padding: 8px 12px; font-size: 10px;
}}
#legend .item {{ display: flex; align-items: center; gap: 6px; margin: 3px 0; }}
#legend .swatch {{ width: 10px; height: 10px; border-radius: 2px; }}

/* Canvas */
#graph-canvas {{ display: block; }}
</style>
</head>
<body>

<!-- Log bar -->
<div id="log-bar"></div>

<!-- Search -->
<div id="search-box"><input id="search" type="text" placeholder="Search nodes... (/)"></div>

<!-- Filters -->
<div id="filters"></div>

<!-- Controls -->
<div id="controls">
  <button id="btn-reset" title="Reset view (F)">&#x2b1b; Reset</button>
  <button id="btn-zoom-in" title="Zoom in">+</button>
  <button id="btn-zoom-out" title="Zoom out">&minus;</button>
</div>

<!-- Detail panel -->
<div id="panel">
  <button id="panel-close">&times;</button>
  <h3 id="panel-title"></h3>
  <div id="panel-meta" class="meta"></div>
  <div id="panel-detail" class="detail"></div>
  <div id="panel-connections" class="connections"></div>
  <div class="btn-row">
    <button id="btn-copy-path">Copy path</button>
    <button id="btn-open-vscode">Open in VS Code</button>
  </div>
</div>

<!-- Minimap -->
<canvas id="minimap"></canvas>

<!-- Legend -->
<div id="legend"></div>

<!-- Main canvas -->
<canvas id="graph-canvas"></canvas>

<script>
// =========================================================================
// DATA
// =========================================================================
const G = {graph_json};

// =========================================================================
// CONSTANTS
// =========================================================================
const COLORS = {{
  identity: "#3fb950", state: "#58a6ff", knowledge: "#d2a8ff",
  control: "#f0883e", experts: "#f778ba",
}};
const CLUSTER_LABELS = {{
  identity: "Identity Layer", state: "State Layer",
  knowledge: "Knowledge Layer", control: "Control Layer",
  experts: "Expert Council",
}};
const NODE_SHAPES = {{ layer: "hexagon", council: "diamond", expert: "circle", wiki: "square" }};

// =========================================================================
// STATE
// =========================================================================
let tx = 0, ty = 0, sc = 1;
let selectedNode = null;
let hoveredNode = null;
let dragNode = null;
let filterType = null;
let searchTerm = "";
const canvas = document.getElementById("graph-canvas");
const ctx = canvas.getContext("2d");

// =========================================================================
// LAYOUT: force-directed simulation (simple Fruchterman-Reingold)
// =========================================================================
const W = window.innerWidth, H = window.innerHeight;
canvas.width = W; canvas.height = H;

// Initialize node positions
const nodes = G.nodes.map((n, i) => ({{
  ...n, x: W/2 + (Math.random()-0.5)*400, y: H/2 + (Math.random()-0.5)*400,
  vx: 0, vy: 0, radius: 12 + Math.min(n.degree * 3, 18),
}}));
const nodeMap = {{}};
nodes.forEach(n => nodeMap[n.id] = n);

const edges = G.edges.map(e => ({{ source: nodeMap[e.source], target: nodeMap[e.target], type: e.type }}))
  .filter(e => e.source && e.target);

// Hotspot set for quick lookup
const hotspotSet = new Set(G.hotspots.map(h => h.file));

// Recent log dates for recency ring
const recentFiles = new Set();
if (G.log_entries && G.log_entries.length > 0) {{
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  // We cannot reliably parse all date formats, so just mark files from recent log entries
  G.log_entries.forEach(le => {{
    if (le.date) {{
      try {{
        const d = new Date(le.date);
        if (d >= cutoff) {{
          // Extract file names from title heuristically
          nodes.forEach(n => {{
            if (le.title && le.title.toLowerCase().includes(n.id.toLowerCase().replace(".md",""))) {{
              recentFiles.add(n.id);
            }}
          }});
        }}
      }} catch(e) {{}}
    }}
  }});
}}
// Also mark nodes modified in last 7 days
const now = new Date();
nodes.forEach(n => {{
  if (n.last_modified) {{
    try {{
      const d = new Date(n.last_modified);
      if ((now - d) / 86400000 <= 7) recentFiles.add(n.id);
    }} catch(e) {{}}
  }}
}});

function simulate(iterations) {{
  const k = Math.sqrt((W * H) / nodes.length) * 0.4;
  for (let iter = 0; iter < iterations; iter++) {{
    // Repulsion
    for (let i = 0; i < nodes.length; i++) {{
      nodes[i].vx = 0; nodes[i].vy = 0;
      for (let j = 0; j < nodes.length; j++) {{
        if (i === j) continue;
        let dx = nodes[i].x - nodes[j].x;
        let dy = nodes[i].y - nodes[j].y;
        let dist = Math.sqrt(dx*dx + dy*dy) || 1;
        let force = (k * k) / dist;
        nodes[i].vx += (dx / dist) * force;
        nodes[i].vy += (dy / dist) * force;
      }}
    }}
    // Attraction along edges
    edges.forEach(e => {{
      let dx = e.target.x - e.source.x;
      let dy = e.target.y - e.source.y;
      let dist = Math.sqrt(dx*dx + dy*dy) || 1;
      let force = (dist * dist) / k;
      let fx = (dx / dist) * force * 0.05;
      let fy = (dy / dist) * force * 0.05;
      e.source.vx += fx; e.source.vy += fy;
      e.target.vx -= fx; e.target.vy -= fy;
    }});
    // Cluster gravity
    const clusterCenters = {{}};
    nodes.forEach(n => {{
      if (!clusterCenters[n.cluster]) clusterCenters[n.cluster] = {{ sx: 0, sy: 0, c: 0 }};
      clusterCenters[n.cluster].sx += n.x;
      clusterCenters[n.cluster].sy += n.y;
      clusterCenters[n.cluster].c++;
    }});
    Object.keys(clusterCenters).forEach(k => {{
      const cc = clusterCenters[k];
      cc.x = cc.sx / cc.c; cc.y = cc.sy / cc.c;
    }});
    nodes.forEach(n => {{
      const cc = clusterCenters[n.cluster];
      if (cc) {{
        n.vx += (cc.x - n.x) * 0.01;
        n.vy += (cc.y - n.y) * 0.01;
      }}
    }});
    // Center gravity
    nodes.forEach(n => {{
      n.vx += (W/2 - n.x) * 0.001;
      n.vy += (H/2 - n.y) * 0.001;
    }});
    // Apply with damping
    const temp = 1 - (iter / iterations);
    nodes.forEach(n => {{
      let mag = Math.sqrt(n.vx*n.vx + n.vy*n.vy) || 1;
      n.x += (n.vx / mag) * Math.min(mag, k * temp);
      n.y += (n.vy / mag) * Math.min(mag, k * temp);
      n.x = Math.max(50, Math.min(W-50, n.x));
      n.y = Math.max(50, Math.min(H-50, n.y));
    }});
  }}
}}
simulate(200);

// =========================================================================
// DRAWING
// =========================================================================
function toScreen(x, y) {{ return [x * sc + tx, y * sc + ty]; }}
function toWorld(sx, sy) {{ return [(sx - tx) / sc, (sy - ty) / sc]; }}

function drawHexagon(cx, cy, r) {{
  ctx.beginPath();
  for (let i = 0; i < 6; i++) {{
    const angle = Math.PI / 3 * i - Math.PI / 6;
    const x = cx + r * Math.cos(angle);
    const y = cy + r * Math.sin(angle);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }}
  ctx.closePath();
}}

function drawDiamond(cx, cy, r) {{
  ctx.beginPath();
  ctx.moveTo(cx, cy - r); ctx.lineTo(cx + r, cy);
  ctx.lineTo(cx, cy + r); ctx.lineTo(cx - r, cy);
  ctx.closePath();
}}

function drawNode(n) {{
  const [sx, sy] = toScreen(n.x, n.y);
  const r = n.radius * sc;
  if (r < 1) return;

  const isFiltered = filterType && n.type !== filterType && n.cluster !== filterType;
  const isSearchHidden = searchTerm && !n.id.toLowerCase().includes(searchTerm)
    && !n.label.toLowerCase().includes(searchTerm);
  const alpha = (isFiltered || isSearchHidden) ? 0.12 : 1.0;
  const baseColor = COLORS[n.cluster] || "#8b949e";

  // Recency ring (pulsing outer ring for recently modified nodes)
  if (recentFiles.has(n.id) && alpha > 0.5) {{
    const t = (Date.now() % 2000) / 2000;
    const pulseR = r + 4 + Math.sin(t * Math.PI * 2) * 3;
    const pulseAlpha = 0.3 + Math.sin(t * Math.PI * 2) * 0.15;
    ctx.beginPath();
    ctx.arc(sx, sy, pulseR, 0, Math.PI * 2);
    ctx.strokeStyle = baseColor.replace(")", `,$ {{pulseAlpha}})`).replace("rgb", "rgba");
    ctx.lineWidth = 2 * sc;
    ctx.stroke();
  }}

  // Node shape
  ctx.globalAlpha = n.activated ? alpha : alpha * 0.4;
  const shape = NODE_SHAPES[n.type] || "circle";
  if (shape === "hexagon") drawHexagon(sx, sy, r);
  else if (shape === "diamond") drawDiamond(sx, sy, r);
  else if (shape === "square") {{
    ctx.beginPath();
    ctx.rect(sx - r*0.75, sy - r*0.75, r*1.5, r*1.5);
  }} else {{
    ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2);
  }}

  ctx.fillStyle = baseColor;
  ctx.fill();

  // Border
  ctx.lineWidth = (selectedNode === n ? 3 : n === hoveredNode ? 2 : 1) * sc;
  ctx.strokeStyle = selectedNode === n ? "#f0f6fc" : n.activated ? baseColor : "#484f58";
  if (!n.activated) ctx.setLineDash([4 * sc, 3 * sc]);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;

  // Unactivated badge
  if (!n.activated && alpha > 0.5) {{
    const bx = sx + r * 0.6, by = sy - r * 0.6;
    ctx.fillStyle = "#f85149";
    ctx.font = `bold ${{Math.max(9, 10 * sc)}}px system-ui`;
    ctx.textAlign = "center";
    ctx.fillText("!", bx, by + 3 * sc);
  }}

  // Label
  if (r > 6) {{
    ctx.fillStyle = alpha > 0.5 ? "#f0f6fc" : "#484f58";
    ctx.font = `${{Math.max(8, 11 * sc)}}px system-ui`;
    ctx.textAlign = "center";
    ctx.fillText(n.label, sx, sy + r + 14 * sc);
  }}
}}

function draw() {{
  ctx.clearRect(0, 0, W, H);

  // Cluster halos
  const clusterNodes = {{}};
  nodes.forEach(n => {{
    if (!clusterNodes[n.cluster]) clusterNodes[n.cluster] = [];
    clusterNodes[n.cluster].push(n);
  }});
  Object.entries(clusterNodes).forEach(([cluster, cnodes]) => {{
    if (cnodes.length < 2) return;
    let cx = 0, cy = 0;
    cnodes.forEach(n => {{ cx += n.x; cy += n.y; }});
    cx /= cnodes.length; cy /= cnodes.length;
    let maxDist = 0;
    cnodes.forEach(n => {{
      const d = Math.sqrt((n.x - cx)**2 + (n.y - cy)**2);
      if (d > maxDist) maxDist = d;
    }});
    const hr = maxDist + 60;
    const [scx, scy] = toScreen(cx, cy);
    const sr = hr * sc;
    const color = COLORS[cluster] || "#8b949e";
    ctx.beginPath();
    ctx.arc(scx, scy, sr, 0, Math.PI * 2);
    ctx.fillStyle = color.replace(")", ", 0.04)").replace("rgb", "rgba");
    ctx.fill();
    ctx.strokeStyle = color.replace(")", ", 0.15)").replace("rgb", "rgba");
    ctx.lineWidth = 1;
    ctx.stroke();

    // Cluster label
    ctx.fillStyle = color.replace(")", ", 0.6)").replace("rgb", "rgba");
    ctx.font = `${{Math.max(9, 10 * sc)}}px system-ui`;
    ctx.textAlign = "center";
    ctx.fillText(CLUSTER_LABELS[cluster] || cluster, scx, scy - sr + 14 * sc);
  }});

  // Edges
  edges.forEach(e => {{
    const [sx, sy] = toScreen(e.source.x, e.source.y);
    const [ex, ey] = toScreen(e.target.x, e.target.y);
    const isHighlighted = selectedNode && (e.source === selectedNode || e.target === selectedNode);
    ctx.beginPath();
    ctx.moveTo(sx, sy); ctx.lineTo(ex, ey);
    ctx.strokeStyle = isHighlighted ? "#58a6ff" : "#21262d";
    ctx.lineWidth = isHighlighted ? 1.5 * sc : 0.5 * sc;
    ctx.globalAlpha = isHighlighted ? 0.8 : 0.3;
    ctx.stroke();
    ctx.globalAlpha = 1;
  }});

  // Nodes
  nodes.forEach(drawNode);

  drawMinimap();
}}

// =========================================================================
// MINIMAP
// =========================================================================
const miniCanvas = document.getElementById("minimap");
const mctx = miniCanvas.getContext("2d");
miniCanvas.width = 160; miniCanvas.height = 120;

function drawMinimap() {{
  mctx.clearRect(0, 0, 160, 120);
  mctx.fillStyle = "#0d1117";
  mctx.fillRect(0, 0, 160, 120);

  // Bounding box of all nodes
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  nodes.forEach(n => {{
    if (n.x < minX) minX = n.x; if (n.y < minY) minY = n.y;
    if (n.x > maxX) maxX = n.x; if (n.y > maxY) maxY = n.y;
  }});
  const pad = 40;
  minX -= pad; minY -= pad; maxX += pad; maxY += pad;
  const rangeX = maxX - minX || 1, rangeY = maxY - minY || 1;
  const msc = Math.min(150 / rangeX, 110 / rangeY);
  const mox = (160 - rangeX * msc) / 2;
  const moy = (120 - rangeY * msc) / 2;

  // Draw nodes as dots
  nodes.forEach(n => {{
    const mx = (n.x - minX) * msc + mox;
    const my = (n.y - minY) * msc + moy;
    mctx.fillStyle = COLORS[n.cluster] || "#8b949e";
    mctx.fillRect(mx - 1.5, my - 1.5, 3, 3);
  }});

  // Viewport rectangle
  const tl = toWorld(0, 32);  // top of canvas below log bar
  const br = toWorld(W, H);
  const vlx = (tl[0] - minX) * msc + mox;
  const vly = (tl[1] - minY) * msc + moy;
  const vrx = (br[0] - minX) * msc + mox;
  const vry = (br[1] - minY) * msc + moy;
  mctx.strokeStyle = "#ff79c6";
  mctx.lineWidth = 1.5;
  mctx.strokeRect(vlx, vly, vrx - vlx, vry - vly);
}}

// =========================================================================
// LOG BAR
// =========================================================================
function initLogBar() {{
  const bar = document.getElementById("log-bar");
  if (G.log_entries && G.log_entries.length > 0) {{
    bar.innerHTML = G.log_entries.slice(0, 8).map(e =>
      `<span class="log-entry">${{e.id}}: ${{e.title}} (${{e.date || "no date"}})</span>`
    ).join("");
  }} else {{
    bar.innerHTML = '<span class="log-muted">No LOG.md yet &mdash; run /ss-log to start tracking activity</span>';
  }}
}}

// =========================================================================
// FILTERS
// =========================================================================
function initFilters() {{
  const types = ["layer", "expert", "council", "wiki"];
  const clusters = Object.keys(CLUSTER_LABELS);
  const container = document.getElementById("filters");

  function addBtn(label, value, group) {{
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.onclick = () => {{
      if (filterType === value) {{ filterType = null; btn.classList.remove("active"); }}
      else {{
        container.querySelectorAll("button").forEach(b => b.classList.remove("active"));
        filterType = value; btn.classList.add("active");
      }}
      draw();
    }};
    container.appendChild(btn);
  }}
  addBtn("All", null);
  types.forEach(t => addBtn(t.charAt(0).toUpperCase() + t.slice(1), t));
  clusters.forEach(c => addBtn(CLUSTER_LABELS[c], c));
}}

// =========================================================================
// LEGEND
// =========================================================================
function initLegend() {{
  const legend = document.getElementById("legend");
  const items = [
    ["#3fb950", "Identity"], ["#58a6ff", "State"],
    ["#d2a8ff", "Knowledge"], ["#f0883e", "Control"], ["#f778ba", "Experts"],
  ];
  legend.innerHTML = items.map(([c, l]) =>
    `<div class="item"><div class="swatch" style="background:${{c}}"></div>${{l}}</div>`
  ).join("");
}}

// =========================================================================
// DETAIL PANEL
// =========================================================================
function showPanel(n) {{
  const panel = document.getElementById("panel");
  document.getElementById("panel-title").textContent = n.label;

  let meta = `${{n.id}} | ${{n.type}}`;
  if (n.layer >= 0) meta += ` | Layer ${{n.layer}}`;
  if (n.last_modified) meta += ` | Modified: ${{n.last_modified}}`;
  if (!n.activated) meta += ` | NOT ACTIVATED`;
  document.getElementById("panel-meta").textContent = meta;

  document.getElementById("panel-detail").textContent = n.detail || "(no description)";

  // Connections
  const conns = edges.filter(e => e.source === n || e.target === n);
  const connDiv = document.getElementById("panel-connections");
  if (conns.length > 0) {{
    connDiv.innerHTML = "<strong>Connections:</strong><br>" + conns.map(e => {{
      const other = e.source === n ? e.target : e.source;
      return `<div class="conn-item" data-id="${{other.id}}">${{other.label}} (${{e.type}})</div>`;
    }}).join("");
    connDiv.querySelectorAll(".conn-item").forEach(el => {{
      el.onclick = () => {{
        const target = nodeMap[el.dataset.id];
        if (target) {{ selectedNode = target; showPanel(target); draw(); }}
      }};
    }});
  }} else {{
    connDiv.innerHTML = "<em>No connections</em>";
  }}

  // Buttons
  document.getElementById("btn-copy-path").onclick = () => {{
    try {{ navigator.clipboard.writeText(n.file); }} catch(e) {{}}
  }};
  document.getElementById("btn-open-vscode").onclick = () => {{
    try {{ window.open("vscode://file/" + n.file); }} catch(e) {{}}
  }};

  panel.style.display = "block";
}}

function hidePanel() {{
  document.getElementById("panel").style.display = "none";
  selectedNode = null;
  draw();
}}

document.getElementById("panel-close").onclick = hidePanel;

// =========================================================================
// INTERACTION
// =========================================================================
function hitTest(sx, sy) {{
  const [wx, wy] = toWorld(sx, sy);
  for (let i = nodes.length - 1; i >= 0; i--) {{
    const n = nodes[i];
    const dx = wx - n.x, dy = wy - n.y;
    if (dx*dx + dy*dy <= (n.radius + 4) ** 2) return n;
  }}
  return null;
}}

let isPanning = false, panStart = [0, 0];
let lastClick = 0;

canvas.addEventListener("mousedown", e => {{
  const n = hitTest(e.clientX, e.clientY);
  if (n) {{
    dragNode = n;
    const now = Date.now();
    if (now - lastClick < 350 && selectedNode === n) {{
      // Double click -> show detail panel
      showPanel(n);
    }} else {{
      selectedNode = n;
      draw();
    }}
    lastClick = now;
  }} else {{
    isPanning = true;
    panStart = [e.clientX - tx, e.clientY - ty];
  }}
}});

canvas.addEventListener("mousemove", e => {{
  if (dragNode) {{
    const [wx, wy] = toWorld(e.clientX, e.clientY);
    dragNode.x = wx; dragNode.y = wy;
    draw();
  }} else if (isPanning) {{
    tx = e.clientX - panStart[0];
    ty = e.clientY - panStart[1];
    draw();
  }} else {{
    const n = hitTest(e.clientX, e.clientY);
    if (n !== hoveredNode) {{ hoveredNode = n; canvas.style.cursor = n ? "pointer" : "default"; draw(); }}
  }}
}});

canvas.addEventListener("mouseup", () => {{ dragNode = null; isPanning = false; }});

canvas.addEventListener("wheel", e => {{
  e.preventDefault();
  const factor = e.deltaY > 0 ? 0.9 : 1.1;
  const mx = e.clientX, my = e.clientY;
  tx = mx - (mx - tx) * factor;
  ty = my - (my - ty) * factor;
  sc *= factor;
  draw();
}}, {{ passive: false }});

// =========================================================================
// CONTROLS
// =========================================================================
function fitAll() {{
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  nodes.forEach(n => {{
    if (n.x < minX) minX = n.x; if (n.y < minY) minY = n.y;
    if (n.x > maxX) maxX = n.x; if (n.y > maxY) maxY = n.y;
  }});
  const pad = 80;
  const rw = maxX - minX + pad * 2, rh = maxY - minY + pad * 2;
  sc = Math.min(W / rw, (H - 40) / rh, 2);
  tx = (W - (minX + maxX) * sc) / 2;
  ty = ((H + 40) - (minY + maxY) * sc) / 2;
  draw();
}}

document.getElementById("btn-reset").onclick = fitAll;
document.getElementById("btn-zoom-in").onclick = () => {{
  const cx = W/2, cy = H/2;
  tx = cx - (cx - tx) * 1.2; ty = cy - (cy - ty) * 1.2; sc *= 1.2; draw();
}};
document.getElementById("btn-zoom-out").onclick = () => {{
  const cx = W/2, cy = H/2;
  tx = cx - (cx - tx) * 0.8; ty = cy - (cy - ty) * 0.8; sc *= 0.8; draw();
}};

// =========================================================================
// SEARCH
// =========================================================================
const searchInput = document.getElementById("search");
searchInput.addEventListener("input", e => {{
  searchTerm = e.target.value.toLowerCase();
  draw();
}});

// =========================================================================
// KEYBOARD SHORTCUTS
// =========================================================================
document.addEventListener("keydown", e => {{
  if (e.target === searchInput) {{
    if (e.key === "Escape") {{ searchInput.blur(); searchTerm = ""; searchInput.value = ""; draw(); }}
    return;
  }}
  if (e.key === "Escape") {{ hidePanel(); }}
  else if (e.key === "f" || e.key === "F") {{ fitAll(); }}
  else if (e.key === "/") {{ e.preventDefault(); searchInput.focus(); }}
}});

// =========================================================================
// INIT
// =========================================================================
initLogBar();
initFilters();
initLegend();
fitAll();
</script>
</body>
</html>'''


# ---------------------------------------------------------------------------
# GRAPH_SUMMARY.md generator (for NotebookLM)
# ---------------------------------------------------------------------------

def generate_graph_summary(graph: dict) -> str:
    """Generate a prose summary of the knowledge graph for NotebookLM."""
    meta = graph["meta"]
    nodes = graph["nodes"]
    edges = graph["edges"]

    lines = [
        "# Knowledge Graph Summary",
        f"Generated: {meta['generated']} | Repo: {meta['repo']}",
        "",
        "## Overview",
        f"This domain has {meta['node_count']} knowledge nodes connected by "
        f"{meta['edge_count']} relationships.",
        f"Open pending items: {meta['open_pending']}. "
        f"Active decisions: {meta['open_decisions']}. "
        f"Drift alerts: {meta['drift_alerts']}.",
        "",
    ]

    # Most connected nodes
    by_degree = sorted(nodes, key=lambda n: n.get("degree", 0), reverse=True)
    lines.append("## Most Connected Nodes")
    for n in by_degree[:5]:
        status = "activated" if n.get("activated") else "NOT activated"
        lines.append(
            f"- {n['id']} ({n.get('degree', 0)} connections, {status}): "
            f"{n.get('detail', '')[:80]}"
        )
    lines.append("")

    # Cluster summary
    lines.append("## Clusters")
    cluster_groups = {}
    for n in nodes:
        c = n.get("cluster", "unknown")
        if c not in cluster_groups:
            cluster_groups[c] = []
        cluster_groups[c].append(n["id"])
    for c, members in cluster_groups.items():
        label = CLUSTER_LABELS.get(c, c)
        lines.append(f"- {label}: {', '.join(members)}")
    lines.append("")

    # Hotspots
    if graph.get("hotspots"):
        lines.append("## Active Hotspots")
        for h in graph["hotspots"]:
            lines.append(f"- {h['file']}: {h['reason']} (priority: {h['priority']})")
        lines.append("")

    # Staleness
    if graph.get("staleness"):
        lines.append("## Stale Layers")
        for s in graph["staleness"]:
            lines.append(
                f"- {s['file']}: last modified {s['last_modified']}, "
                f"risk: {s['risk']}"
            )
        lines.append("")

    # Key relationships
    lines.append("## Key Relationships")
    approval_flows = [e for e in edges if e.get("type") == "approval_flow"]
    if approval_flows:
        targets = [e["target"] for e in approval_flows]
        lines.append(
            f"- PENDING.md feeds approved changes into: {', '.join(targets)}"
        )
    gen_flows = [e for e in edges if e.get("type") == "generated_from"]
    if gen_flows:
        sources = [e["target"] for e in gen_flows]
        lines.append(
            f"- SUMMARY.md is generated from: {', '.join(sources)}"
        )
    ref_edges = [e for e in edges if e.get("type") == "reference"]
    if ref_edges:
        lines.append(f"- {len(ref_edges)} cross-reference links between files")
    lines.append("")

    # Navigation hints
    lines.append("## Navigation Guide")
    for hint in graph.get("navigation_hints", []):
        lines.append(
            f'- If asked about "{hint["if_user_asks_about"]}", '
            f'read {hint["read_first"]} first.'
        )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    repo = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else REPO

    graph = build_graph(repo)

    wiki_dir = repo / "wiki"
    wiki_dir.mkdir(exist_ok=True)

    # Write graph.json
    graph_path = wiki_dir / "graph.json"
    graph_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")

    # Write knowledge-graph.html
    html_path = wiki_dir / "knowledge-graph.html"
    html_path.write_text(generate_html(graph), encoding="utf-8")

    # Write GRAPH_SUMMARY.md (for NotebookLM)
    summary_path = wiki_dir / "GRAPH_SUMMARY.md"
    summary_path.write_text(generate_graph_summary(graph), encoding="utf-8")

    print(f"Graph generated: {graph['meta']['node_count']} nodes, "
          f"{graph['meta']['edge_count']} edges")
    print(f"  wiki/graph.json           -> {graph_path}")
    print(f"  wiki/knowledge-graph.html -> {html_path}")
    print(f"  wiki/GRAPH_SUMMARY.md     -> {summary_path}")

    if graph["hotspots"]:
        print(f"  Hotspots: {len(graph['hotspots'])} detected")
        for h in graph["hotspots"]:
            print(f"    - {h['file']}: {h['reason']} ({h['priority']})")
    if graph["staleness"]:
        print(f"  Stale layers: {len(graph['staleness'])}")
        for s in graph["staleness"]:
            print(f"    - {s['file']}: {s['risk']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
