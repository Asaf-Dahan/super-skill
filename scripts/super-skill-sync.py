#!/usr/bin/env python3
# super-skill-sync.py
#
# Before running this script, configure REGISTRY below with your own
# Super Skill repos. See SYNC_SETUP.md for step-by-step instructions.
# Pulls all registered Super Skills, checks monitored URLs for drift,
# regenerates SUMMARY.md for each, and optionally feeds NotebookLM.
#
# Usage (Windows / cross-platform: replace `python3` with `python`):
#   python scripts/super-skill-sync.py              # pull + drift check + update summaries
#   python scripts/super-skill-sync.py --feed       # + push to NotebookLM
#   python scripts/super-skill-sync.py --dry-run    # no files modified
#
# Auto-detect interpreter:
#   python scripts/run.py super-skill-sync --dry-run

import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DRY_RUN  = "--dry-run" in sys.argv
FEED_NLM = "--feed"    in sys.argv

# Add your Super Skills here -- see SYNC_SETUP.md for step-by-step instructions.
# Each entry needs: name (short identifier), path (absolute or ~/relative),
# and monitor_urls (list of URLs to check for drift).
# Example entry (uncomment and edit, then add more as needed):
#
#   {
#       "name": "my-domain-os",
#       "path": "~/super-skill-my-domain-os",
#       "monitor_urls": [
#           "https://example.com/changelog",
#           "https://example.com/docs/release-notes",
#       ],
#   },
#
# Paths that do not exist on disk are skipped with a warning.
REGISTRY = []


def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=cwd
    )
    return result.returncode, result.stdout.strip()


def git_pull(path):
    expanded = Path(path).expanduser()
    if not expanded.exists():
        return False, f"path not found: {expanded}"
    code, out = run(["git", "pull", "--rebase", "origin", "main"], cwd=expanded)
    if code != 0:
        code, out = run(["git", "pull", "--rebase", "origin", "master"], cwd=expanded)
    return code == 0, out


def check_url(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "super-skill-sync/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status == 200, f"HTTP {r.status}"
    except Exception as exc:
        return False, str(exc)[:80]


def write_drift(path, skill_name, url, detail):
    pending = Path(path).expanduser() / "PENDING.md"
    if not pending.exists():
        print(f"    PENDING.md not found, skipping drift write")
        return
    today   = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    content = pending.read_text(encoding="utf-8")
    nums    = [int(x) for x in re.findall(r"DRIFT-(\d+)", content)]
    n       = max(nums) + 1 if nums else 1
    domain  = url.split("/")[2]
    entry = f"""
## DRIFT-{n:03d}: {skill_name} - {domain}
Date detected: {today}
Type: DRIFT DETECTED
Status: AWAITING REVIEW
Severity: LOW

### What Changed
Source URL returned unexpected status: {detail}
Manual review required at: {url}

### Proposed Action
[ ] Review URL manually
[ ] Update CURRENT_STATE.md if changes affect this domain
[ ] No action required - informational only

### Decision
[ ] Reviewed
[ ] Action taken:
"""
    if not DRY_RUN:
        pending.write_text(content.rstrip() + "\n" + entry, encoding="utf-8")
    print(f"    DRIFT-{n:03d} written to PENDING.md")


def update_summary(path):
    script = Path(__file__).parent / "update_summary.py"
    if not script.exists():
        print(f"    update_summary.py not found - skipping SUMMARY.md regeneration")
        return False
    code, out = run(
        [sys.executable, str(script), str(Path(path).expanduser())],
        cwd=Path(path).expanduser()
    )
    if code == 0:
        return True
    print(f"    update_summary.py error: {out[:80]}")
    return False


def feed_notebook(path):
    script = Path(path).expanduser() / "scripts" / "feed_notebook.py"
    if script.exists():
        code, _ = run(
            [sys.executable, str(script)],
            cwd=Path(path).expanduser()
        )
        return code == 0
    return False


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'=' * 54}")
    print(f"  super-skill-sync -- {now}")
    if DRY_RUN:
        print("  [DRY RUN -- no files modified]")
    print(f"{'=' * 54}\n")

    # Empty-state guard: REGISTRY not configured yet.
    has_placeholder = any(
        entry.get("name") == "example-domain-os" for entry in REGISTRY
    )
    if not REGISTRY or has_placeholder:
        print("No Super Skills configured yet.")
        print("")
        print("Open scripts/super-skill-sync.py and add your domains to the")
        print("REGISTRY list. See SYNC_SETUP.md for step-by-step instructions.")
        print("")
        return

    results = []

    for ss in REGISTRY:
        name = ss["name"]
        print(f"[{name}]")

        ok, msg = git_pull(ss["path"])
        if ok:
            print(f"  git: {'up to date' if 'Already up to date' in msg else 'pulled'}")
        else:
            print(f"  git: WARN -- {msg[:60]}")

        for url in ss.get("monitor_urls", []):
            reachable, detail = check_url(url)
            domain = url.split("/")[2]
            if reachable:
                print(f"  url: ok -- {domain}")
            else:
                print(f"  url: FAIL ({detail}) -- {domain}")
                if not DRY_RUN:
                    write_drift(ss["path"], name, url, detail)

        if not DRY_RUN:
            updated = update_summary(ss["path"])
            print(f"  summary: {'regenerated' if updated else 'skipped'}")

        if FEED_NLM:
            fed = feed_notebook(ss["path"])
            print(f"  nlm: {'fed' if fed else 'script not found'}")

        results.append({"name": name, "pulled": ok})
        print()

    pulled = sum(1 for r in results if r["pulled"])
    print("=" * 54)
    print(f"Done. {pulled}/{len(results)} repos updated.")
    if not FEED_NLM:
        print("Tip: run with --feed to also push updates to NotebookLM.")
    print()


if __name__ == "__main__":
    main()
