#!/usr/bin/env python3
# scheduled_tasks.py
# Runs scheduled maintenance tasks for a Super Skill.
# All findings go to PENDING.md. Nothing changes automatically.
#
# Usage (Windows / cross-platform: replace `python3` with `python`):
#   python scripts/scheduled_tasks.py --task drift-check
#   python scripts/scheduled_tasks.py --frequency weekly
#   python scripts/scheduled_tasks.py --frequency monthly
#   python scripts/scheduled_tasks.py --frequency quarterly
#   python scripts/scheduled_tasks.py --dry-run
#
# Auto-detect interpreter:
#   python scripts/run.py scheduled_tasks --frequency weekly

import argparse
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

DRY_RUN = False

WEEKLY_TASKS    = ["drift-check", "summary-refresh", "pending-check"]
MONTHLY_TASKS   = WEEKLY_TASKS + ["notebooklm-sync", "council-review", "monitoring-audit"]
QUARTERLY_TASKS = MONTHLY_TASKS + ["state-verify", "decisions-audit", "evaluation-review", "council-refresh"]

TASK_DESCRIPTIONS = {
    "drift-check":        "Check all monitoring URLs for availability",
    "summary-refresh":    "Regenerate SUMMARY.md from all layer files",
    "pending-check":      "Report items in PENDING.md open over 7 days",
    "notebooklm-sync":    "Push all layer files to NotebookLM",
    "council-review":     "Report Expert Council debates open over 30 days",
    "monitoring-audit":   "Verify all monitoring source URLs are still valid",
    "state-verify":       "Generate CURRENT_STATE.md verification checklist",
    "decisions-audit":    "Flag decisions older than 90 days for re-evaluation",
    "evaluation-review":  "Flag rejected tools that may warrant re-evaluation",
    "council-refresh":    "Flag expert profiles that may need updating",
}


def now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def read_file(path):
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def append_pending(repo_path, entry):
    pending = Path(repo_path) / "PENDING.md"
    if not pending.exists():
        print(f"  PENDING.md not found at {pending}")
        return
    content = pending.read_text(encoding="utf-8")
    if not DRY_RUN:
        pending.write_text(content.rstrip() + "\n\n" + entry, encoding="utf-8")
        print(f"  Written to PENDING.md")
    else:
        print(f"  [DRY RUN] Would write to PENDING.md:")
        print(f"  {entry[:120]}...")


def next_pending_id(repo_path, prefix):
    content = read_file(Path(repo_path) / "PENDING.md")
    import re
    nums = [int(x) for x in re.findall(rf"{prefix}-(\d+)", content)]
    return max(nums) + 1 if nums else 1


def check_url(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "super-skill-scheduled/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status == 200, f"HTTP {r.status}"
    except Exception as e:
        return False, str(e)[:80]


def task_drift_check(repo_path):
    print("  Running: drift-check")
    monitoring = read_file(Path(repo_path) / "MONITORING.md")
    if not monitoring:
        print("  MONITORING.md not found. Skipping.")
        return

    import re
    urls = re.findall(r"URL.*?:\s*(https?://\S+)", monitoring)
    if not urls:
        print("  No URLs found in MONITORING.md.")
        return

    print(f"  Checking {len(urls)} URLs...")
    failed = []
    for url in urls:
        ok, detail = check_url(url)
        status = "ok" if ok else f"FAIL ({detail})"
        print(f"    {url[:60]} -- {status}")
        if not ok:
            failed.append((url, detail))

    if failed:
        n = next_pending_id(repo_path, "DRIFT")
        entry = f"\n## DRIFT-{n:03d}: Scheduled drift check -- {today_str()}\n"
        entry += f"Date detected: {today_str()}\nType: DRIFT DETECTED\nStatus: AWAITING REVIEW\n\n"
        entry += "### Failed Sources\n"
        for url, detail in failed:
            entry += f"- {url}: {detail}\n"
        entry += "\n### Proposed Action\n[ ] Review each URL manually\n"
        entry += "[ ] Update MONITORING.md if source has moved\n[ ] No action required\n"
        entry += "\n### Decision\n[ ] Reviewed\n[ ] Action taken:\n"
        append_pending(repo_path, entry)
    else:
        print(f"  All {len(urls)} URLs reachable. No drift detected.")


def task_summary_refresh(repo_path):
    print("  Running: summary-refresh")
    script = Path(repo_path) / "scripts" / "update_summary.py"
    if not script.exists():
        print("  update_summary.py not found. Skipping.")
        return
    result = subprocess.run(
        [sys.executable, str(script), str(repo_path)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  {result.stdout.strip()}")
    else:
        print(f"  ERROR: {result.stderr.strip()[:100]}")


def task_pending_check(repo_path):
    print("  Running: pending-check")
    import re
    content = read_file(Path(repo_path) / "PENDING.md")
    if not content:
        print("  PENDING.md not found.")
        return

    dates = re.findall(r"Date.*?(\d{4}-\d{2}-\d{2})", content)
    stale = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    for d in dates:
        try:
            dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if dt < cutoff:
                days_open = (datetime.now(timezone.utc) - dt).days
                stale.append((d, days_open))
        except ValueError:
            pass

    if stale:
        print(f"  {len(stale)} item(s) open for more than 7 days:")
        for d, days in stale:
            print(f"    Added: {d} -- {days} days open")
    else:
        print("  No stale items. All pending items are under 7 days old.")


def task_notebooklm_sync(repo_path):
    print("  Running: notebooklm-sync")
    script = Path(repo_path) / "scripts" / "feed_notebook.py"
    if not script.exists():
        print("  feed_notebook.py not found. Skipping.")
        return
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True,
        cwd=str(repo_path)
    )
    print(result.stdout.strip()[:200] if result.stdout else "No output.")
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()[:100]}")


def task_council_review(repo_path):
    print("  Running: council-review")
    import re
    council = read_file(Path(repo_path) / "experts" / "COUNCIL.md")
    if not council:
        print("  experts/COUNCIL.md not found. Skipping.")
        return

    dates = re.findall(r"Date opened:\s*(\d{4}-\d{2}-\d{2})", council)
    old = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    for d in dates:
        try:
            dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if dt < cutoff:
                days_open = (datetime.now(timezone.utc) - dt).days
                old.append((d, days_open))
        except ValueError:
            pass

    if old:
        print(f"  {len(old)} debate(s) open for more than 30 days:")
        for d, days in old:
            print(f"    Opened: {d} -- {days} days open")
    else:
        print("  No debates open for more than 30 days.")


def task_monitoring_audit(repo_path):
    print("  Running: monitoring-audit")
    task_drift_check(repo_path)


def task_state_verify(repo_path):
    print("  Running: state-verify")
    current = read_file(Path(repo_path) / "CURRENT_STATE.md")
    if not current:
        print("  CURRENT_STATE.md not found. Skipping.")
        return

    out_dir = Path(repo_path) / "notebooks"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"verification-{today_str()}.md"

    checklist = f"# CURRENT_STATE.md Verification Checklist\n"
    checklist += f"Generated: {today_str()}\n\n"
    checklist += "Review each item below and confirm it is still accurate.\n"
    checklist += "Mark each line: [ ] Not verified  [x] Confirmed  [!] Needs update\n\n"

    for line in current.split("\n"):
        if line.startswith("|") and "---" not in line:
            checklist += f"[ ] {line.strip()}\n"

    if not DRY_RUN:
        out_path.write_text(checklist, encoding="utf-8")
        print(f"  Checklist written to: {out_path.name}")
    else:
        print(f"  [DRY RUN] Would write checklist to: {out_path.name}")


def task_decisions_audit(repo_path):
    print("  Running: decisions-audit")
    import re
    decisions = read_file(Path(repo_path) / "DECISIONS.md")
    if not decisions:
        print("  DECISIONS.md not found. Skipping.")
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    old_decisions = []
    blocks = decisions.split("### DEC-")
    for block in blocks[1:]:
        match = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", block)
        title_line = block.split("\n")[0].strip()
        if match:
            try:
                dt = datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if dt < cutoff:
                    days_old = (datetime.now(timezone.utc) - dt).days
                    old_decisions.append((title_line, match.group(1), days_old))
            except ValueError:
                pass

    if old_decisions:
        print(f"  {len(old_decisions)} decision(s) older than 90 days:")
        for title, date, days in old_decisions:
            print(f"    DEC-{title} ({date}) -- {days} days old")
        n = next_pending_id(repo_path, "UPDATE")
        entry = f"\n## UPDATE-{n:03d}: Decisions audit -- {today_str()}\n"
        entry += f"Date: {today_str()}\nType: DECISIONS AUDIT\nStatus: AWAITING REVIEW\n\n"
        entry += "### Decisions older than 90 days\n"
        for title, date, days in old_decisions:
            entry += f"- DEC-{title}: {date} ({days} days)\n"
        entry += "\n### Proposed Action\n[ ] Review each decision for continued validity\n"
        entry += "[ ] Update DECISIONS.md if context has changed\n[ ] No action required\n"
        entry += "\n### Decision\n[ ] Reviewed\n[ ] Action taken:\n"
        append_pending(repo_path, entry)
    else:
        print("  All decisions are under 90 days old.")


def task_evaluation_review(repo_path):
    print("  Running: evaluation-review")
    evaluation = read_file(Path(repo_path) / "EVALUATION.md")
    if not evaluation:
        print("  EVALUATION.md not found. Skipping.")
        return
    print("  EVALUATION.md exists. Manual review recommended for rejected items.")


def task_council_refresh(repo_path):
    print("  Running: council-refresh")
    council = read_file(Path(repo_path) / "experts" / "COUNCIL.md")
    if not council:
        print("  experts/COUNCIL.md not found. Skipping.")
        return
    print("  Expert Council found. Manual review recommended for profile accuracy.")


TASK_MAP = {
    "drift-check":       task_drift_check,
    "summary-refresh":   task_summary_refresh,
    "pending-check":     task_pending_check,
    "notebooklm-sync":   task_notebooklm_sync,
    "council-review":    task_council_review,
    "monitoring-audit":  task_monitoring_audit,
    "state-verify":      task_state_verify,
    "decisions-audit":   task_decisions_audit,
    "evaluation-review": task_evaluation_review,
    "council-refresh":   task_council_refresh,
}

FREQUENCY_MAP = {
    "weekly":    WEEKLY_TASKS,
    "monthly":   MONTHLY_TASKS,
    "quarterly": QUARTERLY_TASKS,
}


def main():
    global DRY_RUN
    parser = argparse.ArgumentParser(description="Super Skill scheduled maintenance tasks.")
    parser.add_argument("--task",      help="Run a specific task by name")
    parser.add_argument("--frequency", choices=["weekly", "monthly", "quarterly"],
                        help="Run all tasks for this frequency")
    parser.add_argument("--dry-run",   action="store_true", help="Report only, no files written")
    parser.add_argument("--repo",      default=".", help="Path to the Super Skill repo (default: current directory)")
    args = parser.parse_args()

    DRY_RUN = args.dry_run
    repo_path = Path(args.repo).resolve()

    print(f"\n{'='*54}")
    print(f"  Super Skill Scheduled Tasks -- {now_str()}")
    if DRY_RUN:
        print("  [DRY RUN -- no files written]")
    print(f"  Repo: {repo_path}")
    print(f"{'='*54}\n")

    tasks_to_run = []

    if args.task:
        if args.task not in TASK_MAP:
            print(f"Unknown task: {args.task}")
            print(f"Available: {', '.join(TASK_MAP.keys())}")
            sys.exit(1)
        tasks_to_run = [args.task]
    elif args.frequency:
        tasks_to_run = FREQUENCY_MAP[args.frequency]
    else:
        parser.print_help()
        sys.exit(0)

    for task_name in tasks_to_run:
        desc = TASK_DESCRIPTIONS.get(task_name, task_name)
        print(f"[{task_name}] {desc}")
        TASK_MAP[task_name](repo_path)
        print()

    print("="*54)
    print(f"Done. {len(tasks_to_run)} task(s) completed.")
    if not DRY_RUN:
        print("Review PENDING.md for any new items.")
    print()


if __name__ == "__main__":
    main()
