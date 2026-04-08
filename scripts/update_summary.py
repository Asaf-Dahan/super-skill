#!/usr/bin/env python3
# update_summary.py
# Regenerates SUMMARY.md from all Super Skill layers.
# Run after any change to any layer file.
# Also runs automatically as part of super-skill-sync.

import re
import sys
from pathlib import Path
from datetime import datetime, timezone


def extract_domain_line(context_md: str) -> str:
    lines = context_md.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "## Domain":
            for j in range(i + 1, min(i + 4, len(lines))):
                candidate = lines[j].strip()
                if candidate:
                    return candidate
    return "[see CONTEXT.md]"


def extract_owner(context_md: str) -> str:
    lines = context_md.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "## Owner":
            for j in range(i + 1, min(i + 4, len(lines))):
                candidate = lines[j].strip()
                if candidate:
                    return candidate
    return "[see CONTEXT.md]"


def extract_current_state_facts(current_state_md: str) -> list:
    facts = []
    last_verified = ""
    for line in current_state_md.split("\n"):
        if "last verified" in line.lower() or "last full verification" in line.lower():
            parts = line.split(":", 1)
            if len(parts) > 1:
                last_verified = parts[1].strip()
        if "|" in line and ("active" in line.lower() or "pre-launch" in line.lower()
                            or "running" in line.lower() or "live" in line.lower()):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                facts.append(f"- {parts[0]}: {parts[-1]}")
        if len(facts) >= 5:
            break
    if not facts:
        for line in current_state_md.split("\n"):
            if line.startswith("- ") and len(line) > 10:
                facts.append(line)
            if len(facts) >= 5:
                break
    return facts, last_verified


def extract_decisions(decisions_md: str) -> list:
    lines = []
    for block in decisions_md.split("### DEC-"):
        if not block.strip():
            continue
        num_line = block.split("\n")[0].strip()
        num = num_line.split(":")[0].strip() if ":" in num_line else num_line[:6]
        decision_line = ""
        for line in block.split("\n"):
            if line.startswith("Decision:") or line.startswith("**Decision:**"):
                decision_line = line.split(":", 1)[-1].strip().replace("**", "")
                break
        if not decision_line:
            for line in block.split("\n")[1:]:
                candidate = line.strip()
                if candidate and not candidate.startswith("#"):
                    decision_line = candidate
                    break
        if decision_line:
            lines.append(f"- DEC-{num}: {decision_line[:80]}")
    return lines[:10]


def extract_pending(pending_md: str) -> tuple:
    open_items = re.findall(
        r"## (EVAL|DRIFT|UPDATE|DEC)-\d+", pending_md
    )
    resolved_section = pending_md.find("## Resolved")
    if resolved_section > 0:
        open_text = pending_md[:resolved_section]
        open_items = re.findall(r"## (EVAL|DRIFT|UPDATE|DEC)-\d+", open_text)
    last_date = ""
    dates = re.findall(r"Date.*?(\d{4}-\d{2}-\d{2})", pending_md)
    if dates:
        last_date = sorted(dates)[-1]
    return len(open_items), last_date


def extract_drift_alerts(monitoring_md: str) -> list:
    alerts = []
    for line in monitoring_md.split("\n"):
        if "CRITICAL" in line or "HIGH" in line or "ALERT" in line:
            alerts.append(f"- {line.strip()}")
    return alerts


def generate_summary(repo_path: Path) -> str:
    repo_path = repo_path.resolve()

    def read(filename):
        f = repo_path / filename
        return f.read_text(encoding="utf-8") if f.exists() else ""

    context      = read("CONTEXT.md")
    current      = read("CURRENT_STATE.md")
    decisions    = read("DECISIONS.md")
    pending      = read("PENDING.md")
    monitoring   = read("MONITORING.md")

    domain_line          = extract_domain_line(context)
    owner_line           = extract_owner(context)
    state_facts, verified = extract_current_state_facts(current)
    decision_lines       = extract_decisions(decisions)
    pending_count, last  = extract_pending(pending)
    drift_alerts         = extract_drift_alerts(monitoring)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output = []
    output.append(f"# {repo_path.name} -- Summary")
    output.append(f"Generated: {today} | Verified: {verified or 'see CURRENT_STATE.md'}")
    output.append("")
    output.append("## Domain")
    output.append(domain_line)
    output.append("")
    output.append("## Owner")
    output.append(owner_line)
    output.append("")
    output.append("## Current State")
    output += state_facts if state_facts else ["- [see CURRENT_STATE.md]"]
    output.append("")
    output.append("## Active Decisions")
    output += decision_lines if decision_lines else ["- [see DECISIONS.md]"]
    output.append("")
    output.append("## Open Pending")
    if pending_count:
        output.append(
            f"- {pending_count} item{'s' if pending_count != 1 else ''} awaiting approval"
            + (f" | Last: {last}" if last else "")
        )
    else:
        output.append("- Queue clear")
    output.append("")
    output.append("## Load Protocol")
    output.append("")
    output.append("Read this file first. Load full files only when the task requires it.")
    output.append("")
    output.append("| If task involves       | Load this file        |")
    output.append("|------------------------|-----------------------|")
    output.append("| Architecture decision  | DECISIONS.md          |")
    output.append("| Tool version or state  | CURRENT_STATE.md      |")
    output.append("| Approval action        | PENDING.md            |")
    output.append("| Domain structure       | DOMAIN_MAP.md         |")
    output.append("| Evaluation of new tool | EVALUATION.md         |")
    output.append("| Learning content       | LEARNING.md           |")
    output.append("| Expert council or debates | experts/COUNCIL.md |")
    output.append("")
    output.append("Default: work from this summary only.")
    output.append("")
    output.append("## Drift Alerts")
    output += drift_alerts if drift_alerts else ["- No active alerts"]

    result = "\n".join(output)
    lines = result.split("\n")
    if len(lines) > 80:
        result = "\n".join(lines[:80])
        result += "\n[Truncated -- see full layer files for details]"

    return result


if __name__ == "__main__":
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path(".")
    summary = generate_summary(path)
    out = path / "SUMMARY.md"
    out.write_text(summary, encoding="utf-8")
    line_count = len(summary.splitlines())
    print(f"SUMMARY.md written: {line_count} lines -> {out}")
