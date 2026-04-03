# Setup Guide

## Prerequisites

- Python 3.10 or higher
- A Google account with NotebookLM access
- Any AI agent: Claude Code, Cursor, Codex, or Claude Projects

## Install notebooklm-py

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
```

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

## Authenticate with Google

```bash
notebooklm login
```

This opens a browser. Log in with the Google account you use
for NotebookLM. The session is saved locally at ~/.notebooklm/

### Check authentication

```bash
notebooklm auth check --test
```

You should see: `connected`

## Configure your notebook ID

After activating your Super Skill, create your notebook:

```bash
notebooklm create "My Domain - Super Skill"
```

Copy the notebook ID returned. Then:

```bash
cp .env.example .env
```

Edit .env and set:

```
NOTEBOOK_ID=your-actual-notebook-id-here
```

## Important Notes

notebooklm-py is an unofficial library. It uses undocumented
Google APIs that may change without notice. It is suitable for
personal use, research, and internal projects.

Session cookies are stored at ~/.notebooklm/ - protect this file.

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

## Run the feed script

```bash
python scripts/feed_notebook.py
```

This loads your domain knowledge files into your NotebookLM notebook.

## Generate learning content

```bash
python scripts/generate_learning.py audio
python scripts/generate_learning.py quiz
python scripts/generate_learning.py mindmap
```

## Language Settings

NotebookLM generates audio and content in the language of your
Google account locale by default.

To generate in a specific language, add instructions when running:

```bash
python scripts/generate_learning.py audio
```

Or customize directly in the NotebookLM web UI:
Audio Overview - Customize - Language

Supported languages: 50+ including English, Hebrew, Spanish,
French, German, and more. See the full list:

```bash
notebooklm language list
```
