# © 2026 Gitit Inc · AI Architecture
# feed_notebook.py — Load domain knowledge files into NotebookLM

import os
import sys
from pathlib import Path

def load_env():
    """Read .env file and set environment variables."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        print("ERROR: .env file not found.")
        print("Copy .env.example to .env and set your NOTEBOOK_ID:")
        print("  cp .env.example .env")
        print("  # Edit .env and add your notebook ID")
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

def main():
    load_env()
    notebook_id = os.environ.get("NOTEBOOK_ID")
    if not notebook_id or notebook_id == "your-notebook-id-here":
        print("ERROR: NOTEBOOK_ID is not configured.")
        print("Edit .env and set NOTEBOOK_ID to your actual notebook ID.")
        print("Run: notebooklm create \"My Domain — Super Skill\"")
        sys.exit(1)

    try:
        from notebooklm import NotebookLM
    except ImportError:
        print("ERROR: notebooklm-py is not installed.")
        print("Install it with: pip install \"notebooklm-py[browser]\"")
        sys.exit(1)

    root = Path(__file__).resolve().parent.parent
    knowledge_files = [
        "CONTEXT.md", "DOMAIN_MAP.md", "CURRENT_STATE.md",
        "EVALUATION.md", "DECISIONS.md", "MONITORING.md",
        "LEARNING.md", "PENDING.md", "SKILL.md", "CLAUDE.md"
    ]

    print(f"Feeding notebook: {notebook_id}")
    nb = NotebookLM()
    notebook = nb.get_notebook(notebook_id)

    fed_count = 0
    for filename in knowledge_files:
        filepath = root / filename
        if filepath.exists():
            print(f"  Loading {filename}...")
            content = filepath.read_text(encoding="utf-8")
            notebook.add_source(content, title=filename)
            fed_count += 1
        else:
            print(f"  Skipping {filename} (not found)")

    print(f"Done. {fed_count} files loaded into notebook.")

if __name__ == "__main__":
    main()
