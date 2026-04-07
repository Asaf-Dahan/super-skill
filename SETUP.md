# Setup Guide

This file covers the notebooklm-py API pattern and version pinning.
For full setup instructions, see NOTEBOOKLM_GUIDE.md.

## Correct API Pattern

notebooklm-py v0.3.4 uses an async client.
All scripts in this template use the following pattern:

```python
import asyncio
from notebooklm import NotebookLMClient, AuthTokens

async def main():
    auth = await AuthTokens.from_storage()
    async with NotebookLMClient(auth=auth) as client:
        result = await client.sources.add_text(
            notebook_id, title, content
        )

asyncio.run(main())
```

Note: The class is `NotebookLMClient`, not `NotebookLM`.
Note: `AuthTokens.from_storage()` is async, always `await` it.
Note: `add_text` signature is `(notebook_id, title, content)`.

## Version Management

This template pins notebooklm-py to a specific version.
Do not upgrade automatically.

To upgrade intentionally:

1. Check the changelog: github.com/teng-lin/notebooklm-py/blob/main/CHANGELOG.md
2. Review any breaking changes
3. Test feed_notebook.py and generate_learning.py after upgrading
4. Update the version in requirements.txt and CURRENT_STATE.md

To install the pinned version:

```bash
pip install -r requirements.txt
```

To check your current installed version:

```bash
pip show notebooklm-py
```

## Using with Non-Claude-Code Agents

If you use Cursor, Codex, or another AI agent that can read and write
files, see AGENTS.md for self-contained operating instructions. It
includes the load protocol, approval rules, and capability map so any
compatible agent can work with this Super Skill without needing
Claude Code or its .claude/ configuration.
