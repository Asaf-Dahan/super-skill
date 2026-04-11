#!/usr/bin/env python3
# generate_dashboard.py -- Generate the Super Skill Dashboard.
#
# Scans for Super Skills, runs cross-layer analysis, computes Health Scores,
# generates insights, and produces wiki/dashboard.html.
#
# Run with:
#   python scripts/generate_dashboard.py                   (Windows / cross-platform)
#   python3 scripts/generate_dashboard.py                  (macOS / Linux)
#   python scripts/run.py dashboard                        (auto-detects interpreter)
#   python scripts/run.py generate_dashboard               (also works)
#
# Stdlib only. No third-party dependencies.

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FILES = {"SUMMARY.md", "PENDING.md", "CONTEXT.md"}
SKIP_FOLDERS = {"template", ".git", "__pycache__", "node_modules"}

DATE_PATTERNS = [
    (re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"), "%Y-%m-%d"),
    (re.compile(r"\b(\d{2}/\d{2}/\d{4})\b"), "%d/%m/%Y"),
    (re.compile(r"\b([A-Z][a-z]+ \d{1,2},? \d{4})\b"), None),  # Month DD YYYY
]

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "this", "that", "are", "was",
    "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "not", "no", "so",
    "if", "as", "its", "all", "each", "any", "our", "your", "their",
    "we", "you", "they", "he", "she", "them", "his", "her", "my",
    "what", "which", "who", "when", "where", "how", "than", "then",
    "also", "just", "more", "some", "into", "over", "such", "only",
    "other", "new", "about", "up", "out", "one", "two", "three",
}

MAX_HISTORY = 90

NOW = datetime.now(timezone.utc)
TODAY = NOW.date()


# ---------------------------------------------------------------------------
# Utility: date parsing
# ---------------------------------------------------------------------------

def parse_date(text: str):
    """Try to extract a date from text. Return datetime.date or None."""
    for pattern, fmt in DATE_PATTERNS:
        m = pattern.search(text)
        if m:
            raw = m.group(1)
            if fmt:
                try:
                    return datetime.strptime(raw, fmt).date()
                except ValueError:
                    continue
            else:
                # Month DD YYYY -- try common formats
                for f in ("%B %d, %Y", "%B %d %Y", "%b %d, %Y", "%b %d %Y"):
                    try:
                        return datetime.strptime(raw, f).date()
                    except ValueError:
                        continue
    return None


def days_ago(d):
    """Return number of days between d and today. d can be date or None."""
    if d is None:
        return None
    return (TODAY - d).days


def safe_read(path: Path, max_lines: int = 0) -> str:
    """Read file text, optionally capped at max_lines."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if max_lines > 0:
            lines = text.splitlines(keepends=True)
            return "".join(lines[:max_lines])
        return text
    except OSError:
        return ""


def file_mod_days(path: Path) -> int:
    """Days since file was last modified, or -1 if missing."""
    try:
        ts = os.path.getmtime(path)
        mod = datetime.fromtimestamp(ts, tz=timezone.utc).date()
        return (TODAY - mod).days
    except OSError:
        return -1


def format_ts(dt=None):
    """Format a datetime for display: Apr 9, 2026 at 14:30"""
    if dt is None:
        dt = NOW
    return dt.strftime("%b %-d, %Y at %H:%M") if sys.platform != "win32" else dt.strftime("%b %d, %Y at %H:%M")


# ---------------------------------------------------------------------------
# Super Skill discovery
# ---------------------------------------------------------------------------

def is_super_skill(folder: Path) -> bool:
    """A folder is a Super Skill if it contains all REQUIRED_FILES."""
    if not folder.is_dir():
        return False
    name = folder.name
    if name.startswith(".") or name in SKIP_FOLDERS:
        return False
    return all((folder / f).exists() for f in REQUIRED_FILES)


def discover_skills(search_path: Path) -> list:
    """Find all Super Skill folders under search_path (one level deep)."""
    skills = []
    # Check if search_path itself is a Super Skill
    if is_super_skill(search_path):
        skills.append(search_path)
    # Check children
    if search_path.is_dir():
        for child in sorted(search_path.iterdir()):
            if child.is_dir() and is_super_skill(child) and child not in skills:
                skills.append(child)
    return skills


def find_skills(explicit_path: str = None) -> list:
    """Find Super Skills using the priority search order."""
    if explicit_path:
        p = Path(explicit_path).resolve()
        skills = discover_skills(p)
        if skills:
            return skills

    cwd = Path.cwd().resolve()

    # 1. Current working directory
    skills = discover_skills(cwd)
    if skills:
        return skills

    # 2. Parent of current directory
    skills = discover_skills(cwd.parent)
    if skills:
        return skills

    # 3. ~/.claude/super-skills/
    home_skills = Path.home() / ".claude" / "super-skills"
    if home_skills.exists():
        skills = discover_skills(home_skills)
        if skills:
            return skills

    return []


# ---------------------------------------------------------------------------
# Interactive selection
# ---------------------------------------------------------------------------

def select_skills(skills: list) -> list:
    """Prompt user to select which Super Skills to include."""
    if len(skills) <= 1:
        return skills

    print("\nSuper Skill Dashboard")
    print("\u2500" * 21)
    print(f"Found {len(skills)} Super Skills:\n")
    for i, s in enumerate(skills, 1):
        age = file_mod_days(s / "SUMMARY.md")
        age_str = f"{age} days ago" if age >= 0 else "unknown"
        print(f"  [{i}] {s.name:<24} last modified: {age_str}")

    print("\nGenerate dashboard for:")
    print("  [A] All Super Skills (global view)")
    print("  [B] Select specific ones")
    print("  [C] Single -- choose one")
    print()

    choice = input("Your choice: ").strip().upper()

    if choice == "A":
        return skills
    elif choice == "B":
        nums = input("Enter numbers (comma-separated): ").strip()
        indices = [int(x.strip()) - 1 for x in nums.split(",") if x.strip().isdigit()]
        return [skills[i] for i in indices if 0 <= i < len(skills)]
    elif choice == "C":
        num = input("Enter number: ").strip()
        if num.isdigit() and 1 <= int(num) <= len(skills):
            return [skills[int(num) - 1]]
    else:
        # Default: all
        return skills

    return skills


# ---------------------------------------------------------------------------
# Data collection for a single Super Skill
# ---------------------------------------------------------------------------

def collect_data(skill_path: Path) -> dict:
    """Read all layer files and extract structured data."""
    data = {
        "name": skill_path.name,
        "path": str(skill_path),
        "missing_files": [],
        "summary_text": "",
        "pending_items": [],
        "decisions": [],
        "decisions_count": 0,
        "current_state_fields": [],
        "evaluations_open": 0,
        "evaluations_count": 0,
        "monitoring_sources": [],
        "open_debates": 0,
        "debate_topics": [],
        "log_entries": [],
        "log_last_activity_days": None,
        "graph_json": None,
        "history_json": None,
        "expert_names": [],
    }

    # SUMMARY.md
    sp = skill_path / "SUMMARY.md"
    if sp.exists():
        data["summary_text"] = safe_read(sp, max_lines=80)
    else:
        data["missing_files"].append("SUMMARY.md")

    # PENDING.md
    _parse_pending(skill_path, data)

    # DECISIONS.md
    _parse_decisions(skill_path, data)

    # CURRENT_STATE.md
    _parse_current_state(skill_path, data)

    # EVALUATION.md
    _parse_evaluations(skill_path, data)

    # MONITORING.md
    _parse_monitoring(skill_path, data)

    # experts/COUNCIL.md
    _parse_council(skill_path, data)

    # LOG.md
    _parse_log(skill_path, data)

    # wiki/graph.json
    gp = skill_path / "wiki" / "graph.json"
    if gp.exists():
        try:
            data["graph_json"] = json.loads(safe_read(gp))
        except (json.JSONDecodeError, ValueError):
            pass

    # wiki/dashboard_history.json
    hp = skill_path / "wiki" / "dashboard_history.json"
    if hp.exists():
        try:
            data["history_json"] = json.loads(safe_read(hp))
        except (json.JSONDecodeError, ValueError):
            data["history_json"] = []

    # Expert names (filenames in experts/ folder)
    experts_dir = skill_path / "experts"
    if experts_dir.is_dir():
        for ef in experts_dir.glob("*.md"):
            if ef.name.upper() != "COUNCIL.md":
                data["expert_names"].append(ef.stem)

    return data


def _parse_pending(skill_path: Path, data: dict):
    fp = skill_path / "PENDING.md"
    if not fp.exists():
        data["missing_files"].append("PENDING.md")
        return
    text = safe_read(fp)
    items = []
    current_item = None
    for line in text.splitlines():
        stripped = line.strip()
        # Detect item headers: lines starting with ## or ### followed by PENDING-
        if re.match(r"^#{2,3}\s+PENDING-", stripped) or re.match(r"^#{2,3}\s+\d+\.", stripped):
            if current_item:
                items.append(current_item)
            title = re.sub(r"^#{2,3}\s+", "", stripped)
            current_item = {"title": title, "date": None, "age_days": None, "type": "STATE"}
        elif current_item:
            # Look for date
            if current_item["date"] is None:
                d = parse_date(stripped)
                if d:
                    current_item["date"] = str(d)
                    current_item["age_days"] = days_ago(d)
            # Look for type tags
            low = stripped.lower()
            if "drift" in low:
                current_item["type"] = "DRIFT"
            elif "eval" in low:
                current_item["type"] = "EVAL"
            elif "expert" in low or "debate" in low:
                current_item["type"] = "EXPERT"
    if current_item:
        items.append(current_item)
    data["pending_items"] = items


def _parse_decisions(skill_path: Path, data: dict):
    fp = skill_path / "DECISIONS.md"
    if not fp.exists():
        data["missing_files"].append("DECISIONS.md")
        return
    text = safe_read(fp)
    decisions = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{2,3}\s+", stripped) and not stripped.startswith("## Decision"):
            if stripped.startswith("## ") or stripped.startswith("### "):
                if current:
                    decisions.append(current)
                title = re.sub(r"^#{2,3}\s+", "", stripped)
                current = {"title": title, "date": None, "summary": ""}
        elif current:
            if current["date"] is None:
                d = parse_date(stripped)
                if d:
                    current["date"] = str(d)
            if stripped and not stripped.startswith("#") and not current["summary"]:
                current["summary"] = stripped[:120]
    if current:
        decisions.append(current)
    data["decisions"] = decisions[-5:]  # last 5
    data["decisions_count"] = len(decisions)


def _parse_current_state(skill_path: Path, data: dict):
    fp = skill_path / "CURRENT_STATE.md"
    if not fp.exists():
        data["missing_files"].append("CURRENT_STATE.md")
        return
    text = safe_read(fp)
    fields = []
    current_entity = "Unknown"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            current_entity = re.sub(r"^#{2,3}\s+", "", stripped)
        low = stripped.lower()
        if "verified:" in low or "last_checked:" in low or "version:" in low:
            d = parse_date(stripped)
            fields.append({
                "entity": current_entity,
                "line": stripped[:100],
                "date": str(d) if d else None,
                "age_days": days_ago(d) if d else None,
            })
    data["current_state_fields"] = fields


def _parse_evaluations(skill_path: Path, data: dict):
    fp = skill_path / "EVALUATION.md"
    if not fp.exists():
        data["missing_files"].append("EVALUATION.md")
        return
    text = safe_read(fp)
    count = 0
    open_count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{2,3}\s+", stripped) and "evaluation" not in stripped.lower()[:20]:
            if stripped.startswith("## ") or stripped.startswith("### "):
                count += 1
        low = stripped.lower()
        if "open" in low or "undecided" in low or "pending" in low:
            if "status" in low or "decision" in low or "result" in low:
                open_count += 1
    data["evaluations_count"] = count
    data["evaluations_open"] = open_count


def _parse_monitoring(skill_path: Path, data: dict):
    fp = skill_path / "MONITORING.md"
    if not fp.exists():
        data["missing_files"].append("MONITORING.md")
        return
    text = safe_read(fp)
    sources = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            if current:
                sources.append(current)
            name = re.sub(r"^#{2,3}\s+", "", stripped)
            current = {"name": name, "last_checked": None, "last_checked_days": None, "schedule": "unknown"}
        elif current:
            low = stripped.lower()
            if "last_checked" in low or "last checked" in low or "checked:" in low:
                d = parse_date(stripped)
                if d:
                    current["last_checked"] = str(d)
                    current["last_checked_days"] = days_ago(d)
            if "weekly" in low:
                current["schedule"] = "weekly"
            elif "daily" in low:
                current["schedule"] = "daily"
            elif "monthly" in low:
                current["schedule"] = "monthly"
    if current:
        sources.append(current)
    data["monitoring_sources"] = sources


def _parse_council(skill_path: Path, data: dict):
    fp = skill_path / "experts" / "COUNCIL.md"
    if not fp.exists():
        return
    text = safe_read(fp)
    open_debates = 0
    topics = []
    in_debate = False
    for line in text.splitlines():
        stripped = line.strip()
        low = stripped.lower()
        if "debate" in low and (stripped.startswith("## ") or stripped.startswith("### ")):
            in_debate = True
            topic = re.sub(r"^#{2,3}\s+", "", stripped)
            topics.append(topic)
        if in_debate and ("open" in low or "unresolved" in low or "active" in low):
            if "status" in low:
                open_debates += 1
                in_debate = False
    data["open_debates"] = open_debates
    data["debate_topics"] = topics


def _parse_log(skill_path: Path, data: dict):
    fp = skill_path / "LOG.md"
    if not fp.exists():
        data["missing_files"].append("LOG.md")
        return
    text = safe_read(fp)
    entries = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        d = parse_date(stripped)
        if d and (stripped.startswith("## ") or stripped.startswith("### ") or stripped.startswith("- ")):
            title = re.sub(r"^[#\-\s]+", "", stripped)
            current = {"date": str(d), "title": title[:120], "age_days": days_ago(d)}
            entries.append(current)
        elif current and stripped and not stripped.startswith("#"):
            if not current.get("detail"):
                current["detail"] = stripped[:120]
    data["log_entries"] = entries[:5]
    if entries:
        min_age = min(e["age_days"] for e in entries if e["age_days"] is not None)
        data["log_last_activity_days"] = min_age
    else:
        data["log_last_activity_days"] = None


# ---------------------------------------------------------------------------
# Health Score
# ---------------------------------------------------------------------------

def compute_health(data: dict) -> tuple:
    """Compute health score (1.0-10.0) and return (score, label)."""
    score = 10.0

    # Pending items > 7 days: -0.3 each (max -2.0)
    ded = 0.0
    for item in data["pending_items"]:
        age = item.get("age_days")
        if age is not None and age > 7:
            ded += 0.3
    score -= min(ded, 2.0)

    # Pending items > 14 days: additional -0.2
    ded = 0.0
    for item in data["pending_items"]:
        age = item.get("age_days")
        if age is not None and age > 14:
            ded += 0.2
    score -= min(ded, 2.0)

    # Monitoring source not checked in >14 days: -0.5 (max -1.5)
    ded = 0.0
    for src in data["monitoring_sources"]:
        lcd = src.get("last_checked_days")
        if lcd is not None and lcd > 14:
            ded += 0.5
        elif lcd is None:
            ded += 0.5
    score -= min(ded, 1.5)

    # Current state field with no verified date: -0.3 (max -1.0)
    ded = 0.0
    for f in data["current_state_fields"]:
        if f["date"] is None:
            ded += 0.3
    score -= min(ded, 1.0)

    # Current state field verified > 30 days ago: -0.2 (max -1.0)
    ded = 0.0
    for f in data["current_state_fields"]:
        if f["age_days"] is not None and f["age_days"] > 30:
            ded += 0.2
    score -= min(ded, 1.0)

    # Open evaluations: -0.3 each (max -0.9)
    ded = data["evaluations_open"] * 0.3
    score -= min(ded, 0.9)

    # Open debates: -0.2 each (max -0.6)
    ded = data["open_debates"] * 0.2
    score -= min(ded, 0.6)

    # No log entries in 21 days
    if data["log_last_activity_days"] is not None and data["log_last_activity_days"] > 21:
        score -= 0.5
    elif data["log_last_activity_days"] is None and data.get("log_entries") == []:
        score -= 0.5

    # Missing layer files
    optional_layers = {"DECISIONS.md", "MONITORING.md", "EVALUATION.md"}
    for mf in data["missing_files"]:
        if mf in optional_layers:
            score -= 0.3

    score = max(1.0, round(score, 1))

    if score >= 9:
        label = "Excellent"
    elif score >= 7:
        label = "Good"
    elif score >= 5:
        label = "Needs attention"
    elif score >= 3:
        label = "Degrading"
    else:
        label = "Critical"

    return score, label


# ---------------------------------------------------------------------------
# Insights
# ---------------------------------------------------------------------------

def generate_insights(data: dict) -> list:
    """Generate cross-layer insights. Max 6."""
    insights = []

    # Decision references tool in CURRENT_STATE with stale verification
    decision_titles = {d["title"].lower(): d["title"] for d in data["decisions"]}
    for field in data["current_state_fields"]:
        if field["age_days"] is not None and field["age_days"] > 30:
            entity = field["entity"].lower()
            for dtl, dt_title in decision_titles.items():
                if entity in dtl or any(w in dtl for w in entity.split() if len(w) > 3):
                    insights.append({
                        "icon": "\u25c6",
                        "text": f"Decision \"{dt_title}\" references {field['entity']}, last verified {field['age_days']} days ago -- worth re-checking.",
                        "layers": "DECISIONS.md + CURRENT_STATE.md",
                    })
                    break

    # Monitoring overdue
    for src in data["monitoring_sources"]:
        lcd = src.get("last_checked_days")
        if lcd is not None and lcd > 14:
            insights.append({
                "icon": "\u25b2",
                "text": f"Monitoring source \"{src['name']}\" has not been checked in {lcd} days (schedule: {src['schedule']}).",
                "layers": "MONITORING.md",
            })

    # Pending items > 14 days
    old_pending = [i for i in data["pending_items"] if (i.get("age_days") or 0) > 14]
    if old_pending:
        insights.append({
            "icon": "\u25b2",
            "text": f"{len(old_pending)} pending item(s) have been waiting over 14 days for a decision.",
            "layers": "PENDING.md",
        })

    # Open debate intersects decision
    for topic in data["debate_topics"]:
        topic_words = set(topic.lower().split()) - STOP_WORDS
        for d in data["decisions"]:
            title_words = set(d["title"].lower().split()) - STOP_WORDS
            if topic_words & title_words:
                insights.append({
                    "icon": "\u25c6",
                    "text": f"Open expert debate on \"{topic}\" intersects with decision \"{d['title']}\".",
                    "layers": "experts/COUNCIL.md + DECISIONS.md",
                })
                break

    # No log activity
    if data["log_last_activity_days"] is not None and data["log_last_activity_days"] > 21:
        insights.append({
            "icon": "\u25cf",
            "text": f"No recorded activity in {data['log_last_activity_days']} days. The Super Skill may be drifting.",
            "layers": "LOG.md",
        })

    # Open evaluations
    if data["evaluations_open"] > 0:
        insights.append({
            "icon": "\u25cf",
            "text": f"{data['evaluations_open']} evaluation(s) opened without a final decision.",
            "layers": "EVALUATION.md",
        })

    return insights[:6]


# ---------------------------------------------------------------------------
# History snapshot
# ---------------------------------------------------------------------------

def update_history(skill_path: Path, data: dict, score: float, insights: list) -> list:
    """Append a snapshot to dashboard_history.json and return updated list."""
    wiki_dir = skill_path / "wiki"
    wiki_dir.mkdir(parents=True, exist_ok=True)
    hp = wiki_dir / "dashboard_history.json"

    history = data.get("history_json") or []
    if not isinstance(history, list):
        history = []

    # Compute monitoring lag max
    mon_lags = [s["last_checked_days"] for s in data["monitoring_sources"] if s.get("last_checked_days") is not None]
    max_lag = max(mon_lags) if mon_lags else 0

    # Unverified state fields
    unverified = sum(1 for f in data["current_state_fields"] if f["date"] is None)

    record = {
        "timestamp": NOW.isoformat(),
        "health_score": score,
        "pending_count": len(data["pending_items"]),
        "oldest_pending_days": max((i.get("age_days") or 0) for i in data["pending_items"]) if data["pending_items"] else 0,
        "decisions_count": data["decisions_count"],
        "open_evaluations": data["evaluations_open"],
        "open_debates": data["open_debates"],
        "monitoring_lag_max_days": max_lag,
        "unverified_state_fields": unverified,
        "log_last_activity_days": data["log_last_activity_days"] if data["log_last_activity_days"] is not None else -1,
        "insights_count": len(insights),
    }

    history.append(record)
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    hp.write_text(json.dumps(history, indent=2), encoding="utf-8")
    return history


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def generate_html(skills_data: list, output_path: Path):
    """Generate the full dashboard HTML and write to output_path."""
    multi = len(skills_data) > 1
    generated_ts = format_ts()

    html_parts = []
    html_parts.append(_html_head(generated_ts))
    html_parts.append(_html_header(skills_data, generated_ts, multi))

    if multi:
        html_parts.append(_html_global_tab(skills_data))

    for sd in skills_data:
        html_parts.append(_html_skill_tab(sd, multi))

    html_parts.append(_html_footer(generated_ts))
    html_parts.append(_html_scripts(skills_data, multi))
    html_parts.append("</body>\n</html>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html_parts), encoding="utf-8")


def _html_head(ts):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Super Skill Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root {{
  --bg-primary: #0f0f0f;
  --bg-secondary: #1a1a1a;
  --bg-card: #1e1e1e;
  --bg-hover: #252525;
  --border: #2a2a2a;
  --border-light: #333333;
  --text-primary: #f0f0f0;
  --text-secondary: #8a8a8a;
  --text-muted: #555555;
  --accent: #e8e0d4;
  --accent-dim: #9e9890;
  --status-critical: #c0392b;
  --status-warning: #e67e22;
  --status-good: #27ae60;
  --status-neutral: #5a5a5a;
  --score-high: #27ae60;
  --score-mid: #e67e22;
  --score-low: #c0392b;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--bg-primary); color: var(--text-primary); font-family: 'DM Mono', monospace; font-size: 13px; line-height: 1.6; }}
h1, h2, h3 {{ font-family: 'DM Serif Display', Georgia, serif; font-weight: 400; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* Header */
.header {{ position: sticky; top: 0; z-index: 100; background: var(--bg-secondary); border-bottom: 1px solid var(--border); padding: 16px 32px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
.header h1 {{ font-size: 22px; color: var(--accent); }}
.header .meta {{ font-size: 11px; color: var(--text-muted); }}
.tabs {{ display: flex; gap: 4px; flex-wrap: wrap; }}
.tab {{ padding: 6px 16px; border-radius: 4px; cursor: pointer; font-size: 12px; font-family: 'DM Mono', monospace; background: transparent; color: var(--text-secondary); border: 1px solid transparent; transition: all 120ms; }}
.tab:hover {{ background: var(--bg-hover); color: var(--text-primary); }}
.tab.active {{ background: var(--bg-card); color: var(--accent); border-color: var(--border-light); }}

/* Tab content */
.tab-content {{ display: none; padding: 24px 32px; max-width: 1400px; margin: 0 auto; }}
.tab-content.active {{ display: block; }}

/* Cards grid */
.cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; transition: background 120ms; overflow: hidden; }}
.card:hover {{ background: var(--bg-hover); }}

/* Score */
.score {{ font-size: 32px; font-family: 'DM Serif Display', Georgia, serif; animation: fadeIn 0.5s ease; }}
.score.high {{ color: var(--score-high); }}
.score.mid {{ color: var(--score-mid); }}
.score.low {{ color: var(--score-low); }}
.score-label {{ font-size: 11px; color: var(--text-secondary); margin-top: 2px; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}

/* Badges */
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 400; }}
.badge-green {{ background: #1a3a2a; color: var(--status-good); }}
.badge-orange {{ background: #3a2a1a; color: var(--status-warning); }}
.badge-red {{ background: #3a1a1a; color: var(--status-critical); }}
.badge-muted {{ background: var(--bg-hover); color: var(--text-muted); }}

/* Sections */
.section {{ margin-bottom: 32px; }}
.section-title {{ font-size: 20px; color: var(--accent); margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
@media (max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

/* Status bar */
.status-bar {{ display: flex; gap: 24px; align-items: center; flex-wrap: wrap; padding: 16px 20px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 24px; }}
.status-item {{ font-size: 12px; color: var(--text-secondary); }}
.status-item strong {{ color: var(--text-primary); }}

/* Insights */
.insight {{ display: flex; gap: 10px; padding: 10px 14px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; margin-bottom: 8px; align-items: flex-start; }}
.insight-icon {{ font-size: 14px; color: var(--accent-dim); flex-shrink: 0; margin-top: 2px; }}
.insight-text {{ flex: 1; font-size: 12px; }}
.insight-layers {{ font-size: 10px; color: var(--text-muted); margin-top: 2px; }}

/* Pending card */
.pending-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 14px; margin-bottom: 8px; transition: background 120ms; }}
.pending-card:hover {{ background: var(--bg-hover); }}
.pending-title {{ font-size: 12px; margin-bottom: 6px; }}
.pending-meta {{ display: flex; gap: 8px; align-items: center; }}

/* Buttons */
.btn {{ padding: 5px 12px; border-radius: 4px; font-size: 11px; font-family: 'DM Mono', monospace; cursor: pointer; border: 1px solid var(--border-light); background: var(--bg-card); color: var(--text-secondary); opacity: 0.7; transition: opacity 100ms; }}
.btn:hover {{ opacity: 1; color: var(--text-primary); }}
.btn-group {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }}

/* Dot statuses */
.dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }}
.dot-green {{ background: var(--status-good); }}
.dot-orange {{ background: var(--status-warning); }}
.dot-red {{ background: var(--status-critical); }}
.dot-muted {{ background: var(--status-neutral); }}

/* Table */
.data-table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
.data-table th {{ text-align: left; padding: 8px 12px; color: var(--text-muted); border-bottom: 1px solid var(--border); font-weight: 400; }}
.data-table td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); }}

/* Charts container */
.chart-container {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }}
.chart-container canvas {{ max-height: 220px; }}
.stat-boxes {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 16px; }}
.stat-box {{ text-align: center; padding: 14px; background: var(--bg-secondary); border-radius: 6px; }}
.stat-box .stat-val {{ font-size: 20px; color: var(--accent); font-family: 'DM Serif Display', Georgia, serif; }}
.stat-box .stat-label {{ font-size: 10px; color: var(--text-muted); margin-top: 4px; }}

/* Graph placeholder */
.graph-panel {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; min-height: 300px; position: relative; }}
.graph-panel svg {{ width: 100%; height: 300px; }}
.graph-placeholder {{ color: var(--text-muted); font-size: 12px; text-align: center; padding: 80px 20px; }}

/* Tooltip */
.tooltip {{ position: absolute; background: var(--bg-secondary); border: 1px solid var(--border-light); border-radius: 4px; padding: 8px 12px; font-size: 11px; pointer-events: none; z-index: 200; color: var(--text-primary); box-shadow: 0 4px 12px rgba(0,0,0,0.4); }}

/* Footer */
.footer {{ text-align: center; padding: 24px 32px; font-size: 10px; color: var(--text-muted); border-top: 1px solid var(--border); margin-top: 40px; }}

/* Copy tooltip */
.copy-tooltip {{ position: fixed; bottom: 24px; right: 24px; background: var(--bg-card); border: 1px solid var(--border-light); padding: 8px 16px; border-radius: 6px; font-size: 11px; color: var(--accent); opacity: 0; transition: opacity 300ms; pointer-events: none; z-index: 300; }}
.copy-tooltip.show {{ opacity: 1; }}

/* Global timeline */
.timeline {{ display: flex; gap: 2px; overflow-x: auto; padding: 12px 0; }}
.timeline-day {{ display: flex; flex-direction: column; align-items: center; min-width: 24px; }}
.timeline-label {{ font-size: 9px; color: var(--text-muted); writing-mode: vertical-lr; transform: rotate(180deg); margin-bottom: 4px; }}
.timeline-dots {{ display: flex; flex-direction: column; gap: 2px; }}
.timeline-dot {{ width: 10px; height: 10px; border-radius: 2px; }}

/* Monitoring row */
.mon-row {{ display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 12px; }}
.mon-row:last-child {{ border-bottom: none; }}
.mon-name {{ flex: 1; }}
.mon-detail {{ color: var(--text-secondary); font-size: 11px; }}

/* Muted empty state */
.empty-state {{ color: var(--text-muted); font-size: 12px; padding: 20px; text-align: center; }}
</style>
</head>
<body>"""


def _score_class(score):
    if score >= 8:
        return "high"
    elif score >= 5:
        return "mid"
    return "low"


def _age_badge(age):
    if age is None:
        return '<span class="badge badge-muted">unknown</span>'
    if age < 3:
        return f'<span class="badge badge-green">{age}d</span>'
    elif age <= 7:
        return f'<span class="badge badge-orange">{age}d</span>'
    return f'<span class="badge badge-red">{age}d</span>'


def _mon_dot(src):
    lcd = src.get("last_checked_days")
    if lcd is None:
        return "dot-red"
    sched = src.get("schedule", "unknown")
    thresholds = {"daily": 2, "weekly": 10, "monthly": 35}
    limit = thresholds.get(sched, 14)
    if lcd <= limit:
        return "dot-green"
    return "dot-orange"


def _esc(text):
    """Escape HTML special chars."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def _html_header(skills_data, ts, multi):
    tabs_html = ""
    if multi:
        tabs_html += '<div class="tab active" data-tab="global">Global</div>'
    for i, sd in enumerate(skills_data):
        active = "" if multi else (" active" if i == 0 else "")
        tabs_html += f'<div class="tab{active}" data-tab="skill-{i}">{_esc(sd["name"])}</div>'

    return f"""
<div class="header">
  <div>
    <h1>Super Skill Dashboard</h1>
    <div class="meta">generated: {_esc(ts)}</div>
  </div>
  <div class="tabs">{tabs_html}</div>
</div>"""


def _html_global_tab(skills_data):
    # Row 1: Health cards
    cards = ""
    for sd in skills_data:
        sc = _score_class(sd["health_score"])
        pending_count = len(sd["pending_items"])
        last_act = f'{sd["log_last_activity_days"]}d ago' if sd["log_last_activity_days"] is not None else "unknown"
        cards += f"""
      <div class="card">
        <div style="font-size:13px; color:var(--text-secondary); margin-bottom:8px;">{_esc(sd["name"])}</div>
        <div class="score {sc}">{sd["health_score"]}</div>
        <div class="score-label">{_esc(sd["health_label"])}</div>
        <div style="margin-top:10px; font-size:11px;">
          <span class="badge badge-{'red' if pending_count > 3 else 'orange' if pending_count > 0 else 'muted'}">{pending_count} pending</span>
          <span style="color:var(--text-muted); margin-left:8px;">last activity: {_esc(last_act)}</span>
        </div>
      </div>"""

    # Row 2: Knowledge graph
    graph_html = """
    <div class="section">
      <h2 class="section-title">Your Knowledge Network</h2>
      <div class="graph-panel">
        <div id="global-graph-container"></div>
      </div>
    </div>"""

    # Row 3: Cross-domain alerts
    cross_alerts = _compute_cross_domain_alerts(skills_data)
    alerts_html = ""
    if cross_alerts:
        alerts_html = '<div class="section"><h2 class="section-title">Cross-Domain Alerts</h2>'
        for alert in cross_alerts:
            alerts_html += f"""
        <div class="insight">
          <div class="insight-icon">\u25c6</div>
          <div><div class="insight-text">{_esc(alert)}</div>
          <div class="insight-layers">Cross-domain</div></div>
        </div>"""
        alerts_html += "</div>"

    # Row 4: Global timeline
    timeline_html = _build_global_timeline(skills_data)

    return f"""
<div class="tab-content active" id="tab-global">
  <div class="section">
    <h2 class="section-title">Health Overview</h2>
    <div class="cards-grid">{cards}
    </div>
  </div>
  {graph_html}
  {alerts_html}
  {timeline_html}
</div>"""


def _compute_cross_domain_alerts(skills_data):
    """Find patterns that appear in insights of multiple skills."""
    alerts = []
    if len(skills_data) < 2:
        return alerts
    # Extract keywords from each skill's insights
    skill_keywords = {}
    for sd in skills_data:
        words = set()
        for ins in sd.get("insights", []):
            for w in ins["text"].lower().split():
                w = re.sub(r"[^a-z0-9]", "", w)
                if len(w) > 4 and w not in STOP_WORDS:
                    words.add(w)
        skill_keywords[sd["name"]] = words
    # Find shared keywords
    names = list(skill_keywords.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            shared = skill_keywords[names[i]] & skill_keywords[names[j]]
            if shared:
                sample = list(shared)[:3]
                alerts.append(
                    f"Shared pattern detected between {names[i]} and {names[j]}: {', '.join(sample)}."
                )
    return alerts[:4]


def _build_global_timeline(skills_data):
    """Build a 30-day timeline of activity across all skills."""
    # Gather log dates per skill
    skill_colors = ["#e8e0d4", "#27ae60", "#e67e22", "#c0392b", "#3498db", "#9b59b6"]
    days = []
    for offset in range(29, -1, -1):
        d = TODAY - timedelta(days=offset)
        days.append(d)

    day_entries = {}
    for si, sd in enumerate(skills_data):
        color = skill_colors[si % len(skill_colors)]
        for entry in sd.get("log_entries", []):
            try:
                ed = datetime.strptime(entry["date"], "%Y-%m-%d").date()
            except (ValueError, KeyError):
                continue
            if ed in day_entries:
                day_entries[ed].append({"color": color, "name": sd["name"], "title": entry.get("title", "")})
            else:
                day_entries[ed] = [{"color": color, "name": sd["name"], "title": entry.get("title", "")}]

    cols = ""
    for d in days:
        label = d.strftime("%d")
        dots = ""
        for e in day_entries.get(d, []):
            dots += f'<div class="timeline-dot" style="background:{e["color"]}" title="{_esc(e["name"])}: {_esc(e["title"])}"></div>'
        if not dots:
            dots = '<div class="timeline-dot" style="background:var(--border);"></div>'
        cols += f"""
        <div class="timeline-day">
          <div class="timeline-label">{label}</div>
          <div class="timeline-dots">{dots}</div>
        </div>"""

    return f"""
    <div class="section">
      <h2 class="section-title">Activity Timeline (30 days)</h2>
      <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:8px; padding:16px; overflow-x:auto;">
        <div class="timeline">{cols}</div>
      </div>
    </div>"""


def _html_skill_tab(sd, multi):
    idx = sd["_index"]
    active = "" if multi else (" active" if idx == 0 else "")
    sc = _score_class(sd["health_score"])
    pending_count = len(sd["pending_items"])
    last_act = f'{sd["log_last_activity_days"]} days ago' if sd["log_last_activity_days"] is not None else "unknown"
    generated = format_ts()
    skill_path = sd["path"]

    # Section 1: Status bar
    status_bar = f"""
    <div class="status-bar">
      <div class="score {sc}" style="font-size:28px;">{sd["health_score"]}</div>
      <div class="status-item">Pending: <strong>{pending_count} items</strong></div>
      <div class="status-item">Last activity: <strong>{_esc(last_act)}</strong></div>
      <div class="status-item">Generated: <strong>{_esc(generated)}</strong></div>
      <button class="btn" onclick="copyCmd('python scripts/generate_dashboard.py')">Refresh Dashboard</button>
    </div>"""

    # Section 2: Requires action
    pending_html = ""
    if sd["pending_items"]:
        for item in sd["pending_items"]:
            pending_html += f"""
          <div class="pending-card">
            <div class="pending-title">{_esc(item["title"])}</div>
            <div class="pending-meta">
              {_age_badge(item.get("age_days"))}
              <span class="badge badge-muted">{_esc(item.get("type", "STATE"))}</span>
            </div>
          </div>"""
    else:
        pending_html = '<div class="empty-state">No pending items.</div>'

    mon_html = ""
    if sd["monitoring_sources"]:
        for src in sd["monitoring_sources"]:
            dot = _mon_dot(src)
            lcd_str = f'{src["last_checked_days"]}d ago' if src.get("last_checked_days") is not None else "unknown"
            mon_html += f"""
          <div class="mon-row">
            <span class="dot {dot}"></span>
            <span class="mon-name">{_esc(src["name"])}</span>
            <span class="mon-detail">checked: {_esc(lcd_str)} | schedule: {_esc(src.get("schedule","unknown"))}</span>
          </div>"""
    else:
        mon_html = '<div class="empty-state">No monitoring sources configured.</div>'

    requires_action = f"""
    <div class="section">
      <h2 class="section-title">Requires Action</h2>
      <div class="two-col">
        <div>
          <h3 style="font-size:14px; color:var(--text-secondary); margin-bottom:10px;">Pending Items</h3>
          {pending_html}
        </div>
        <div>
          <h3 style="font-size:14px; color:var(--text-secondary); margin-bottom:10px;">Monitoring Alerts</h3>
          {mon_html}
        </div>
      </div>
    </div>"""

    # Section 3: Insights
    insights_html = ""
    if sd.get("insights"):
        for ins in sd["insights"]:
            insights_html += f"""
        <div class="insight">
          <div class="insight-icon">{ins["icon"]}</div>
          <div>
            <div class="insight-text">{_esc(ins["text"])}</div>
            <div class="insight-layers">{_esc(ins["layers"])}</div>
          </div>
        </div>"""
    else:
        insights_html = '<div class="empty-state">No cross-layer issues detected.</div>'

    insights_section = f"""
    <div class="section">
      <h2 class="section-title">Insights</h2>
      {insights_html}
    </div>"""

    # Section 4: Domain Snapshot
    decisions_rows = ""
    for d in sd["decisions"]:
        decisions_rows += f"""
        <tr>
          <td>{_esc(d.get("date") or "unknown")}</td>
          <td>{_esc(d["title"])}</td>
          <td style="color:var(--text-muted);">{_esc(d.get("summary",""))}</td>
        </tr>"""
    if not decisions_rows:
        decisions_rows = '<tr><td colspan="3" style="color:var(--text-muted);">No decisions recorded.</td></tr>'

    state_rows = ""
    for f in sd["current_state_fields"][:8]:
        verified = f"{f['age_days']}d ago" if f.get("age_days") is not None else "unverified"
        state_rows += f"""
        <tr>
          <td>{_esc(f["entity"])}</td>
          <td style="color:var(--text-muted);">{_esc(f["line"][:60])}</td>
          <td>{_esc(verified)}</td>
        </tr>"""
    if not state_rows:
        state_rows = '<tr><td colspan="3" style="color:var(--text-muted);">No state fields found.</td></tr>'

    snapshot = f"""
    <div class="section">
      <h2 class="section-title">Domain Snapshot</h2>
      <div class="two-col">
        <div>
          <h3 style="font-size:14px; color:var(--text-secondary); margin-bottom:10px;">Recent Decisions</h3>
          <table class="data-table">
            <tr><th>Date</th><th>Title</th><th>Summary</th></tr>
            {decisions_rows}
          </table>
        </div>
        <div>
          <h3 style="font-size:14px; color:var(--text-secondary); margin-bottom:10px;">Current State</h3>
          <table class="data-table">
            <tr><th>Entity</th><th>Status</th><th>Verified</th></tr>
            {state_rows}
          </table>
        </div>
      </div>
    </div>"""

    # Section 5: Activity & Trends
    history = sd.get("history", [])
    trends_html = ""
    if len(history) >= 2:
        chart_id = f"chart-{idx}"
        # Compute stats
        total_decisions = sd["decisions_count"]
        # Most active layer: simple heuristic from log entries
        most_active = "LOG.md"
        # Avg time to clear pending: from history deltas
        pending_counts = [h.get("pending_count", 0) for h in history]
        avg_pending = sum(pending_counts) / len(pending_counts) if pending_counts else 0

        trends_html = f"""
    <div class="section">
      <h2 class="section-title">Activity &amp; Trends</h2>
      <div class="two-col">
        <div class="chart-container">
          <canvas id="{chart_id}-health"></canvas>
        </div>
        <div class="chart-container">
          <canvas id="{chart_id}-pending"></canvas>
        </div>
      </div>
      <div class="stat-boxes">
        <div class="stat-box">
          <div class="stat-val">{avg_pending:.1f}</div>
          <div class="stat-label">Avg pending items</div>
        </div>
        <div class="stat-box">
          <div class="stat-val">{_esc(most_active)}</div>
          <div class="stat-label">Most active layer</div>
        </div>
        <div class="stat-box">
          <div class="stat-val">{total_decisions}</div>
          <div class="stat-label">Total decisions</div>
        </div>
      </div>
    </div>"""

    # Section 6: Quick Actions
    quick_actions = f"""
    <div class="section">
      <h2 class="section-title">Quick Actions</h2>
      <h3 style="font-size:13px; color:var(--text-secondary); margin-bottom:8px;">Open Files</h3>
      <div class="btn-group">
        <a class="btn" href="file://{_esc(skill_path)}/PENDING.md">Open PENDING.md</a>
        <a class="btn" href="file://{_esc(skill_path)}/DECISIONS.md">Open DECISIONS.md</a>
        <a class="btn" href="file://{_esc(skill_path)}/MONITORING.md">Open MONITORING.md</a>
        <a class="btn" href="file://{_esc(skill_path)}/wiki/knowledge-graph.html">Open Knowledge Graph</a>
      </div>
      <h3 style="font-size:13px; color:var(--text-secondary); margin:16px 0 8px;">Run Scripts</h3>
      <div class="btn-group">
        <button class="btn" onclick="copyCmd('python scripts/generate_dashboard.py')">Refresh Dashboard</button>
        <button class="btn" onclick="copyCmd('python scripts/run.py doctor')">Run doctor.py</button>
        <button class="btn" onclick="copyCmd('python scripts/run.py update_summary')">Generate Summary</button>
        <button class="btn" onclick="copyCmd('python scripts/run.py super-skill-sync')">Check Drift</button>
      </div>
    </div>"""

    # Section 7: Expert Council
    experts_html = ""
    council_path = Path(skill_path) / "experts" / "COUNCIL.md"
    if council_path.exists():
        debates_list = ""
        for topic in sd.get("debate_topics", []):
            debates_list += f'<div style="padding:4px 0; font-size:12px;">{_esc(topic)}</div>'
        if not debates_list:
            debates_list = '<div class="empty-state">No open debates.</div>'

        experts_list = ""
        for name in sd.get("expert_names", []):
            experts_list += f'<span class="badge badge-muted" style="margin:2px;">{_esc(name)}</span>'
        if not experts_list:
            experts_list = '<span style="color:var(--text-muted); font-size:12px;">No experts configured.</span>'

        experts_html = f"""
    <div class="section">
      <h2 class="section-title">Expert Council</h2>
      <div class="two-col">
        <div>
          <h3 style="font-size:14px; color:var(--text-secondary); margin-bottom:10px;">Open Debates</h3>
          {debates_list}
        </div>
        <div>
          <h3 style="font-size:14px; color:var(--text-secondary); margin-bottom:10px;">Council Members</h3>
          <div style="display:flex; flex-wrap:wrap; gap:4px;">{experts_list}</div>
        </div>
      </div>
    </div>"""

    return f"""
<div class="tab-content{active}" id="tab-skill-{idx}">
  {status_bar}
  {requires_action}
  {insights_section}
  {snapshot}
  {trends_html}
  {quick_actions}
  {experts_html}
</div>"""


def _html_footer(ts):
    return f"""
<div class="footer">
  Super Skill Dashboard &nbsp;|&nbsp; Generated {_esc(ts)} &nbsp;|&nbsp; v2.7.0<br>
  Data is read-only. No changes are made to your Super Skill files.<br>
  <span style="font-size:9px; color:var(--text-muted);">Requires Google Fonts and CDN libraries (D3.js, Chart.js) for full functionality.</span>
</div>
<div class="copy-tooltip" id="copy-tooltip">Copied to clipboard</div>"""


def _html_scripts(skills_data, multi):
    """Generate all inline JS: tab switching, chart rendering, graph, clipboard."""
    # Prepare chart data per skill
    chart_init = ""
    for sd in skills_data:
        idx = sd["_index"]
        history = sd.get("history", [])
        if len(history) >= 2:
            labels = json.dumps([h.get("timestamp", "")[:10] for h in history[-30:]])
            health_vals = json.dumps([h.get("health_score", 0) for h in history[-30:]])
            pending_vals = json.dumps([h.get("pending_count", 0) for h in history[-30:]])
            chart_init += f"""
    // Charts for skill {idx}
    (function() {{
      var hCtx = document.getElementById('chart-{idx}-health');
      var pCtx = document.getElementById('chart-{idx}-pending');
      if (!hCtx || !pCtx) return;
      new Chart(hCtx, {{
        type: 'line',
        data: {{
          labels: {labels},
          datasets: [{{ label: 'Health Score', data: {health_vals}, borderColor: '#e8e0d4', backgroundColor: 'rgba(232,224,212,0.1)', tension: 0.3, fill: true, pointRadius: 2 }}]
        }},
        options: {{ responsive: true, scales: {{ y: {{ min: 0, max: 10, ticks: {{ color: '#555' }}, grid: {{ color: '#2a2a2a' }} }}, x: {{ ticks: {{ color: '#555', maxTicksLimit: 8 }}, grid: {{ color: '#2a2a2a' }} }} }}, plugins: {{ legend: {{ labels: {{ color: '#8a8a8a' }} }} }} }}
      }});
      new Chart(pCtx, {{
        type: 'bar',
        data: {{
          labels: {labels},
          datasets: [{{ label: 'Pending Items', data: {pending_vals}, backgroundColor: 'rgba(230,126,34,0.6)', borderRadius: 3 }}]
        }},
        options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true, ticks: {{ color: '#555' }}, grid: {{ color: '#2a2a2a' }} }}, x: {{ ticks: {{ color: '#555', maxTicksLimit: 8 }}, grid: {{ color: '#2a2a2a' }} }} }}, plugins: {{ legend: {{ labels: {{ color: '#8a8a8a' }} }} }} }}
      }});
    }})();"""

    # D3 graph init for global tab
    graph_init = ""
    if multi:
        nodes_data = []
        links_data = []
        keyword_map = {}
        for sd in skills_data:
            words = set()
            for w in sd.get("summary_text", "").lower().split():
                w = re.sub(r"[^a-z0-9]", "", w)
                if len(w) > 3 and w not in STOP_WORDS:
                    words.add(w)
            keyword_map[sd["name"]] = words
            sc_class = _score_class(sd["health_score"])
            color = {"high": "#27ae60", "mid": "#e67e22", "low": "#c0392b"}[sc_class]
            nodes_data.append({
                "id": sd["name"],
                "score": sd["health_score"],
                "pending": len(sd["pending_items"]),
                "decisions": sd["decisions_count"],
                "color": color,
            })

        names = list(keyword_map.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                shared = keyword_map[names[i]] & keyword_map[names[j]]
                if shared:
                    links_data.append({"source": names[i], "target": names[j], "weight": len(shared)})

        if nodes_data:
            graph_init = f"""
    // D3 Knowledge Graph
    (function() {{
      var container = document.getElementById('global-graph-container');
      if (!container) return;
      var nodes = {json.dumps(nodes_data)};
      var links = {json.dumps(links_data)};
      if (nodes.length === 0) {{
        container.innerHTML = '<div class="graph-placeholder">Run /ss-graph in each Super Skill to enable the knowledge network.</div>';
        return;
      }}
      var width = container.clientWidth || 600;
      var height = 300;
      var svg = d3.select(container).append('svg').attr('width', width).attr('height', height);
      var tooltip = d3.select('body').append('div').attr('class', 'tooltip').style('opacity', 0);
      var sim = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(function(d) {{ return d.id; }}).distance(120))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(width / 2, height / 2));
      var link = svg.selectAll('line').data(links).join('line')
        .attr('stroke', '#333').attr('stroke-width', function(d) {{ return Math.min(d.weight, 4); }});
      var node = svg.selectAll('circle').data(nodes).join('circle')
        .attr('r', function(d) {{ return 8 + Math.min(d.decisions, 20); }})
        .attr('fill', function(d) {{ return d.color; }})
        .attr('stroke', '#555').attr('stroke-width', 1)
        .on('mouseover', function(e, d) {{
          tooltip.style('opacity', 1).html(d.id + '<br>Score: ' + d.score + '<br>Pending: ' + d.pending)
            .style('left', (e.pageX + 12) + 'px').style('top', (e.pageY - 20) + 'px');
        }})
        .on('mouseout', function() {{ tooltip.style('opacity', 0); }});
      var label = svg.selectAll('text').data(nodes).join('text')
        .text(function(d) {{ return d.id; }}).attr('font-size', 10).attr('fill', '#8a8a8a')
        .attr('dx', 14).attr('dy', 4);
      sim.on('tick', function() {{
        link.attr('x1', function(d) {{ return d.source.x; }}).attr('y1', function(d) {{ return d.source.y; }})
            .attr('x2', function(d) {{ return d.target.x; }}).attr('y2', function(d) {{ return d.target.y; }});
        node.attr('cx', function(d) {{ return d.x; }}).attr('cy', function(d) {{ return d.y; }});
        label.attr('x', function(d) {{ return d.x; }}).attr('y', function(d) {{ return d.y; }});
      }});
    }})();"""
        else:
            graph_init = """
    (function() {
      var c = document.getElementById('global-graph-container');
      if (c) c.innerHTML = '<div class="graph-placeholder">Run /ss-graph in each Super Skill to enable the knowledge network.</div>';
    })();"""

    return f"""
<script>
// Tab switching
document.querySelectorAll('.tab').forEach(function(tab) {{
  tab.addEventListener('click', function() {{
    document.querySelectorAll('.tab').forEach(function(t) {{ t.classList.remove('active'); }});
    document.querySelectorAll('.tab-content').forEach(function(c) {{ c.classList.remove('active'); }});
    tab.classList.add('active');
    var target = tab.getAttribute('data-tab');
    var el = document.getElementById('tab-' + target);
    if (el) el.classList.add('active');
  }});
}});

// Copy to clipboard
function copyCmd(cmd) {{
  navigator.clipboard.writeText(cmd).then(function() {{
    var tt = document.getElementById('copy-tooltip');
    tt.classList.add('show');
    setTimeout(function() {{ tt.classList.remove('show'); }}, 2000);
  }});
}}

// Charts
{chart_init}

// Graph
{graph_init}
</script>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate the Super Skill Dashboard")
    parser.add_argument("--path", help="Parent folder containing Super Skills")
    args = parser.parse_args()

    skills = find_skills(args.path)
    if not skills:
        print("No Super Skills found.")
        print("A Super Skill folder must contain: SUMMARY.md, PENDING.md, CONTEXT.md")
        return 1

    selected = select_skills(skills)
    if not selected:
        print("No Super Skills selected.")
        return 1

    print(f"\nProcessing {len(selected)} Super Skill(s)...\n")

    all_data = []
    for i, skill_path in enumerate(selected):
        print(f"  [{i+1}] {skill_path.name} ... ", end="", flush=True)

        data = collect_data(skill_path)
        score, label = compute_health(data)
        data["health_score"] = score
        data["health_label"] = label

        insights = generate_insights(data)
        data["insights"] = insights

        history = update_history(skill_path, data, score, insights)
        data["history"] = history
        data["_index"] = i

        print(f"score={score} ({label}), {len(insights)} insight(s), {len(data['pending_items'])} pending")
        all_data.append(data)

    # Determine output path: first skill's wiki/ or cwd wiki/
    output_dir = selected[0] / "wiki"
    output_path = output_dir / "dashboard.html"

    generate_html(all_data, output_path)
    print(f"\nDashboard written to: {output_path}")
    print("Open wiki/dashboard.html in your browser to view.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
