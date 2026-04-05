#!/usr/bin/env python3
"""
super-skill-sync - checks and updates all registered Super Skills.

Usage:
  python scripts/super-skill-sync.py              # pull + drift check
  python scripts/super-skill-sync.py --feed       # + NotebookLM update
  python scripts/super-skill-sync.py --dry-run    # no files modified

Registration:
  Edit REGISTRY below to add your Super Skills.
  Each entry needs: name, path, and monitor_urls from MONITORING.md.
"""

import subprocess
import sys
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

DRY_RUN = "--dry-run" in sys.argv
FEED_NLM = "--feed" in sys.argv

REGISTRY = [
    {
        "name": "stack-os",
        "path": "~/super-skill-stack-os",
        "monitor_urls": [
            "https://lovable.dev/changelog",
            "https://docs.anthropic.com/en/release-notes",
            "https://supabase.com/changelog",
            "https://railway.app/changelog",
            "https://blog.cloudflare.com",
        ],
    },
    {
        "name": "make-os",
        "path": "~/super-skill-make-os",
        "monitor_urls": [
            "https://www.make.com/en/release-notes",
        ],
    },
    {
        "name": "supabase-os",
        "path": "~/super-skill-supabase-os",
        "monitor_urls": [
            "https://supabase.com/changelog",
        ],
    },
    {
        "name": "agent-os",
        "path": "~/super-skill-agent-os",
        "monitor_urls": [
            "https://github.com/VoltAgent/awesome-agent-skills/commits/main",
            "https://docs.anthropic.com/en/release-notes",
        ],
    },
    {
        "name": "monday-os",
        "path": "~/super-skill-monday-os",
        "monitor_urls": [
            "https://developer.monday.com/changelog",
        ],
    },
    {
        "name": "az-skills",
        "path": "~/az-skills",
        "monitor_urls": [
            "https://github.com/VoltAgent/awesome-agent-skills/commits/main",
        ],
    },
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
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    content = pending.read_text(encoding="utf-8")
    nums = [int(x) for x in re.findall(r"DRIFT-(\d+)", content)]
    n = max(nums) + 1 if nums else 1
    entry = f"""
## DRIFT-{n:03d}: {skill_name} -- {url.split('/')[2]}
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
[ ] No action required -- informational only

### Decision
[ ] Reviewed by Asaf Dahan
[ ] Action taken:
"""
    if not DRY_RUN:
        pending.write_text(content.rstrip() + "\n" + entry, encoding="utf-8")
    print(f"    DRIFT-{n:03d} written to PENDING.md")


def feed_notebook(path):
    script = Path(path).expanduser() / "scripts" / "feed_notebook.py"
    if script.exists():
        code, _ = run(f"python {script}", cwd=Path(path).expanduser())
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
            if "Already up to date" in msg:
                print("  git: up to date")
            else:
                print(f"  git: pulled -- {msg[:60]}")
        else:
            print(f"  git: WARN -- {msg[:60]}")

        for url in ss.get("monitor_urls", []):
            reachable, detail = check_url(url)
            domain = url.split("/")[2]
            if reachable:
                print(f"  url: ok -- {domain}")
            else:
                print(f"  url: FAIL ({detail}) -- {domain}")
                write_drift(ss["path"], name, url, detail)

        if FEED_NLM:
            fed = feed_notebook(ss["path"])
            print(f"  nlm: {'fed' if fed else 'script not found'}")

        results.append({"name": name, "pulled": ok})
        print()

    pulled = sum(1 for r in results if r["pulled"])
    print("=" * 54)
    print(f"Done. {pulled}/{len(results)} repos updated.")
    if not FEED_NLM:
        print("Tip: run with --feed to push updates to NotebookLM.")
    print()


if __name__ == "__main__":
    main()
