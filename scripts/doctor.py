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

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

LAYER_FILES = [
    "CONTEXT.md", "DOMAIN_MAP.md", "CURRENT_STATE.md", "EVALUATION.md",
    "DECISIONS.md", "MONITORING.md", "LEARNING.md", "PENDING.md",
    "SKILL.md", "SUMMARY.md",
]

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

    score = 0
    total = 6

    # Check 1: Python version
    v = sys.version_info
    score += check(
        "Python >= 3.8",
        v >= (3, 8),
        f"found {v.major}.{v.minor}.{v.micro}",
    )

    # Check 2: All 10 layer files exist at root
    missing = [f for f in LAYER_FILES if not (REPO / f).exists()]
    score += check(
        "All 10 layer files present at root",
        not missing,
        f"missing: {', '.join(missing)}" if missing else "10/10",
    )

    # Check 3: .claude/commands/ has 9 .md files
    cmd_dir = REPO / ".claude" / "commands"
    if not cmd_dir.exists():
        # Pre-activation: commands live under template/.claude/commands/
        cmd_dir = REPO / "template" / ".claude" / "commands"
    cmd_files = sorted(cmd_dir.glob("*.md")) if cmd_dir.exists() else []
    score += check(
        ".claude/commands has 9 .md files",
        len(cmd_files) == 9,
        f"found {len(cmd_files)} in {cmd_dir.relative_to(REPO) if cmd_dir.exists() else '<missing>'}",
    )

    # Check 4: scripts/ has the 5 expected scripts
    scripts_dir = REPO / "scripts"
    missing_scripts = [
        s for s in EXPECTED_SCRIPTS if not (scripts_dir / s).exists()
    ]
    score += check(
        "scripts/ has 5 expected scripts",
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
