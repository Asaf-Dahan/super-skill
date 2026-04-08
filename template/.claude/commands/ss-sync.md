Pull all Super Skill repos and check for drift.

> Before first use: configure REGISTRY in scripts/super-skill-sync.py
> (see SYNC_SETUP.md). Without configuration, the script prints a friendly
> reminder and exits.

## Usage
/ss-sync

## What this does
Runs super-skill-sync.py which:
- Pulls latest from GitHub for all registered Super Skills
- Checks all monitoring URLs for drift
- Regenerates SUMMARY.md for each domain
- Writes any detected drift to PENDING.md

## Prompt
Run the sync script:
  python scripts\super-skill-sync.py

Report the output exactly as returned.
If drift was detected, summarize what changed and in which domain.
If PENDING.md was updated, report the new item IDs.
Do not modify any layer file directly.
