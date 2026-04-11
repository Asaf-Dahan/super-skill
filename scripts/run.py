#!/usr/bin/env python3
# run.py -- Cross-platform Super Skill script launcher.
#
# Usage:
#   python scripts/run.py update_summary
#   python scripts/run.py super-skill-sync --dry-run
#   python scripts/run.py scheduled_tasks --frequency weekly
#
# Why this exists: Windows installs Python as `python` (or `py`), while macOS
# and Linux usually expose `python3`. This launcher always uses the same
# interpreter that ran it, so the same command works on every platform.

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

# Short aliases that map to full script filenames
ALIASES = {
    "dashboard": "generate_dashboard.py",
}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/run.py <script-name> [args...]")
        print("Available scripts:")
        for f in sorted(SCRIPTS_DIR.glob("*.py")):
            if f.name != "run.py":
                print(f"  {f.stem}")
        return 1

    name = sys.argv[1]
    name = ALIASES.get(name, name)
    if not name.endswith(".py"):
        name += ".py"
    target = SCRIPTS_DIR / name
    if not target.exists():
        print(f"Script not found: {target}")
        return 1

    return subprocess.call([sys.executable, str(target), *sys.argv[2:]])


if __name__ == "__main__":
    sys.exit(main())
