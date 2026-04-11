# Migration Guide

## Upgrading to v2.7.1 from v2.7.0

Changes in v2.7.1:
- traces/ added to .gitignore
- *.db and *.sqlite added to .gitignore
- desktop.ini added to .gitignore
- exit() replaced with sys.exit() in all NotebookLM scripts
- NOTEBOOK_ID validation moved inside main() in all NotebookLM scripts
- Non-zero exit codes added to super-skill-sync.py and scheduled_tasks.py
- /ss-dashboard added to template/CLAUDE.md command list
- Smart truncation added to update_summary.py
- --all flag added to generate_dashboard.py
- PII and Anthropic logging warnings added to README.md
- Slash command edge case documentation improved
- cat instruction updated for Windows users in README.md
- git pull branch detection improved in super-skill-sync.py
- Explanatory comment added to .gitignore negation pattern
- Partial write safety added to generate_graph.py
- Expert removal process documented in template/experts/COUNCIL.md
- MIGRATION.md created (this file)

## Steps for existing activated Super Skills

1. Pull the latest template: git pull origin main inside your super-skill repo
2. Re-copy slash commands to pick up edge case documentation:
   Windows: xcopy template\.claude\commands .claude\commands /E /I /Y
   Mac/Linux: cp -r template/.claude/commands/ .claude/commands/
3. Run: python scripts/doctor.py -- verify no warnings
4. If doctor.py reports a version mismatch, re-read SUMMARY.md to confirm layer files are intact
5. No layer file content changes are required for this upgrade

## Upgrading from v2.6.x to v2.7.x

If you are on v2.6.x or earlier:
1. Back up your activated layer files (CONTEXT.md through PENDING.md)
2. Pull the latest template: git pull origin main
3. Re-copy slash commands (see step 2 above)
4. Compare your CLAUDE.md with template/CLAUDE.md and merge any new sections
5. Run python scripts/doctor.py to verify setup
6. Run /ss-graph to regenerate the knowledge graph with the latest format
