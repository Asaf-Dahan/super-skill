# © 2026 Gitit Inc · AI Architecture
# feed_notebook.py - Load domain knowledge files into NotebookLM

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

NOTEBOOK_ID = os.getenv("NOTEBOOK_ID")
if not NOTEBOOK_ID:
    print("Error: NOTEBOOK_ID not set.")
    print("Copy .env.example to .env and add your notebook ID.")
    exit(1)

async def main():
    try:
        from notebooklm import NotebookLMClient
        from notebooklm.auth import AuthTokens
    except ImportError:
        print("ERROR: notebooklm-py is not installed.")
        print("Install it with: pip install \"notebooklm-py[browser]\"")
        sys.exit(1)

    root = Path(__file__).resolve().parent.parent

    # Collect all .md files from repo root (exclude README.md and LICENSE)
    root_md_files = sorted([
        f for f in root.glob("*.md")
        if f.name not in ("README.md", "LICENSE")
    ])

    # Collect all .md files from notebooks/ folder
    notebooks_dir = root / "notebooks"
    notebooks_md_files = sorted(notebooks_dir.glob("*.md")) if notebooks_dir.exists() else []

    knowledge_files = root_md_files + notebooks_md_files

    if not knowledge_files:
        print("No .md files found to feed.")
        sys.exit(1)

    print(f"Feeding notebook: {NOTEBOOK_ID}")
    print(f"Found {len(knowledge_files)} files to load.\n")

    try:
        auth_tokens = await AuthTokens.from_storage()
    except Exception as e:
        print(f"ERROR: Could not load auth tokens: {e}")
        print("Run 'notebooklm login' first.")
        sys.exit(1)

    fed_count = 0
    skipped = []
    added = []

    async with NotebookLMClient(auth=auth_tokens) as client:
        for filepath in knowledge_files:
            filename = filepath.name
            print(f"  Loading {filename}...")
            content = filepath.read_text(encoding="utf-8")
            try:
                await client.sources.add_text(NOTEBOOK_ID, filename, content)
                added.append(filename)
                fed_count += 1
            except Exception as e:
                print(f"  ERROR adding {filename}: {e}")
                skipped.append(filename)

    print(f"\nDone. {fed_count} files loaded into notebook.")
    if added:
        print(f"Added: {', '.join(added)}")
    if skipped:
        print(f"Skipped: {', '.join(skipped)}")

if __name__ == "__main__":
    asyncio.run(main())
