#!/usr/bin/env python3
# doctor.py -- Confirms a Super Skill repository is set up correctly.
#
# Checks Python version, layer files, slash commands, scripts,
# and runs update_summary.py once to verify it works end to end.
#
# Run with:
#   python scripts/doctor.py            (Windows / cross-platform)
#   python3 scripts/doctor.py           (macOS / Linux)
#   python scripts/run.py doctor        (auto-detects interpreter)
#
# Stdlib only. No third-party dependencies.

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

LAYER_FILES = [
    "CONTEXT.md", "DOMAIN_MAP.md", "CURRENT_STATE.md", "EVALUATION.md",
    "DECISIONS.md", "MONITORING.md", "LEARNING.md", "PENDING.md",
    "LOG.md", "SKILL.md", "SUMMARY.md",
]

# A placeholder line is one whose stripped content starts with "[" and is
# not a Markdown link of the form [text](url). Template scaffolds use this
# convention for every field that must be filled in during activation.
_PLACEHOLDER_RE = re.compile(r"^\[[^\]]*\]?\s*$")


def _placeholder_ratio(path: Path) -> tuple:
    """Return (placeholder_count, total_content_lines) for a file."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0, 0
    placeholders = 0
    content_lines = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
            continue
        content_lines += 1
        if not stripped.startswith("["):
            continue
        if "](" in stripped:  # Markdown link, not a placeholder
            continue
        if _PLACEHOLDER_RE.match(stripped):
            placeholders += 1
    return placeholders, content_lines


def check_activation():
    """Exit early if any root layer file still contains [placeholder] text."""
    unactivated = []
    for f in LAYER_FILES:
        p = REPO / f
        if not p.exists():
            continue
        ph, total = _placeholder_ratio(p)
        if ph > 0:
            pct = int(ph / total * 100) if total else 100
            unactivated.append(
                f"{f} ({ph} placeholder{'s' if ph != 1 else ''}, "
                f"{pct}% of content)"
            )
    if unactivated:
        print("Layer files are not activated yet. "
              "Run Prompt 1 from ONBOARDING.md first.")
        for item in unactivated:
            print(f"  - {item}")
        sys.exit(1)

EXPECTED_SCRIPTS = [
    "update_summary.py", "feed_notebook.py", "generate_learning.py",
    "scheduled_tasks.py", "super-skill-sync.py",
]


def check(label, ok, detail=""):
    tag = "[PASS]" if ok else "[FAIL]"
    line = f"{tag} {label}"
    if detail:
        line += f" -- {detail}"
    print(line)
    return 1 if ok else 0


def main():
    print("Super Skill Doctor")
    print("=" * 40)

    check_activation()

    score = 0
    total = 6

    # Check 1: Python version
    v = sys.version_info
    score += check(
        "Python >= 3.10",
        v >= (3, 10),
        f"found {v.major}.{v.minor}.{v.micro}",
    )

    # Check 2: All 11 layer files exist at root
    missing = [f for f in LAYER_FILES if not (REPO / f).exists()]
    score += check(
        "All 11 layer files present at root",
        not missing,
        f"missing: {', '.join(missing)}" if missing else "11/11",
    )

    # Check 3: .claude/commands/ has 9 .md files
    cmd_dir = REPO / ".claude" / "commands"
    if not cmd_dir.exists():
        # Pre-activation: commands live under template/.claude/commands/
        cmd_dir = REPO / "template" / ".claude" / "commands"
    cmd_files = sorted(cmd_dir.glob("*.md")) if cmd_dir.exists() else []
    score += check(
        ".claude/commands has 12 slash command files",
        len(cmd_files) == 12,
        f"found {len(cmd_files)} in {cmd_dir.relative_to(REPO) if cmd_dir.exists() else '<missing>'}",
    )

    # Check 4: scripts/ has the 5 expected scripts
    scripts_dir = REPO / "scripts"
    missing_scripts = [
        s for s in EXPECTED_SCRIPTS if not (scripts_dir / s).exists()
    ]
    score += check(
        "scripts/ has 5 core scripts (11 total)",
        not missing_scripts,
        f"missing: {', '.join(missing_scripts)}" if missing_scripts else "5/5",
    )

    # Check 5: .env.example exists
    score += check(
        ".env.example exists",
        (REPO / ".env.example").exists(),
    )

    # Check 6: update_summary.py runs without exception
    update_summary = scripts_dir / "update_summary.py"
    runs_ok = False
    detail = ""
    if update_summary.exists():
        result = subprocess.run(
            [sys.executable, str(update_summary), str(REPO)],
            capture_output=True, text=True,
        )
        runs_ok = result.returncode == 0
        if not runs_ok:
            detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "non-zero exit"
        else:
            detail = result.stdout.strip()
    else:
        detail = "update_summary.py not found"
    score += check("update_summary.py runs cleanly", runs_ok, detail)

    # Check 7 (INFO only): wiki/graph.json exists and is readable
    graph_json = REPO / "wiki" / "graph.json"
    if graph_json.exists():
        import json as _json
        try:
            data = _json.loads(graph_json.read_text(encoding="utf-8"))
            generated = data.get("meta", {}).get("generated", "")
            print(f"[INFO] wiki/graph.json found -- generated: {generated}")
        except Exception as e:
            print(f"[WARN] wiki/graph.json exists but unreadable: {e}")
    else:
        print("[INFO] wiki/graph.json not found -- run /ss-graph to generate the domain knowledge map.")

    print("=" * 40)
    print(f"Score: {score}/{total}")
    if score == total:
        print("Ready to use.")
        return 0
    else:
        print("Fix the items above first.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
