Regenerate SUMMARY.md for the active domain.

## Usage
/ss-summary

## What this does
Runs update_summary.py which reads all layer files
and produces a fresh 80-line SUMMARY.md.
Run this after any approved change to any layer file.

## Prompt
Run the summary update script:
  python scripts\update_summary.py .

Report:
- How many lines the new SUMMARY.md contains
- Whether it was truncated (over 80 lines)
- Any layer files that were missing or unreadable
If the script fails, report the error and stop.
