#!/usr/bin/env python3
# =============================================================================
# IMPORTANT: Before running this script, edit the REGISTRY below.
# Replace the example-domain-os placeholder with your actual domain OS entry.
# Running without editing will result in no-op or incorrect sync behavior.
# See SYNC_SETUP.md for full configuration instructions.
# =============================================================================
# super-skill-sync.py
# Pulls all registered Super Skills, checks monitored URLs for drift,
# regenerates SUMMARY.md for each, and optionally feeds NotebookLM.
#
# Usage:
#   python3 scripts/super-skill-sync.py              # pull + drift check + update summaries
#   python3 scripts/super-skill-sync.py --feed       # + push to NotebookLM
#   python3 scripts/super-skill-sync.py --dry-run    # no files modified

import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DRY_RUN  = "--dry-run" in sys.argv
FEED_NLM = "--feed"    in sys.argv

# Configure your Super Skill repos here.
# Each entry needs: name (short identifier), path (absolute or ~/relative),
# and monitor_urls (list of URLs to check for drift).
# Example:
#   {"name": "my-domain-os", "path": "~/super-skill-my-domain-os",
#    "monitor_urls": ["https://example.com/changelog"]}
# Add one entry per Super Skill you maintain. Paths that do not exist
# on disk are skipped with a warning.
REGISTRY = [
    {
        "name": "example-domain-os",
        "path": "~/super-skill-example-domain-os",
        "monitor_urls": [
            "https://example.com/changelog",
            "https://example.com/docs/release-notes",
        ],
    },
    # Add more Super Skills here:
    # {
    #     "name": "another-domain-os",
    #     "path": "~/super-skill-another-domain-os",
    #     "monitor_urls": [
    #         "https://example.com/another-changelog",
    #     ],
    # },
]


def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    return result.returncode, result.stdout.strip()


def git_pull(path):
    expanded = Path(path).expanduser()
    if not expanded.exists():
        return False, f"path not found: {expanded}"
    code, out = run("git pull --rebase origin main", cwd=expanded)
    if code != 0:
        code, out = run("git pull --rebase origin master", cwd=expanded)
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
        f"python3 \"{script}\" \"{Path(path).expanduser()}\"",
        cwd=Path(path).expanduser()
    )
    if code == 0:
        return True
    print(f"    update_summary.py error: {out[:80]}")
    return False


def feed_notebook(path):
    script = Path(path).expanduser() / "scripts" / "feed_notebook.py"
    if script.exists():
        code, _ = run(f"python3 {script}", cwd=Path(path).expanduser())
        return code == 0
    return False


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'=' * 54}")
    print(f"  super-skill-sync -- {now}")
    if DRY_RUN:
        print("  [DRY RUN -- no files modified]")
    print(f"{'=' * 54}\n")

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
