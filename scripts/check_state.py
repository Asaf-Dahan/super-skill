# © 2026 Gitit Inc · AI Architecture
# check_state.py — Ask 3 standard questions to the notebook to verify domain state

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
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

STANDARD_QUESTIONS = [
    "What is the current state of this domain and what are the key elements?",
    "What decisions have been made recently and what is still pending approval?",
    "Are there any areas where the domain knowledge may be outdated or drifting?",
]

def main():
    load_env()

    notebook_id = os.environ.get("NOTEBOOK_ID")
    if not notebook_id or notebook_id == "your-notebook-id-here":
        print("ERROR: NOTEBOOK_ID is not configured.")
        print("Edit .env and set NOTEBOOK_ID to your actual notebook ID.")
        sys.exit(1)

    try:
        from notebooklm import NotebookLM
    except ImportError:
        print("ERROR: notebooklm-py is not installed.")
        print("Install it with: pip install \"notebooklm-py[browser]\"")
        sys.exit(1)

    print(f"Checking state for notebook: {notebook_id}")
    nb = NotebookLM()
    notebook = nb.get_notebook(notebook_id)

    for i, question in enumerate(STANDARD_QUESTIONS, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}: {question}")
        print(f"{'='*60}")
        response = notebook.ask(question)
        print(response)

    print(f"\n{'='*60}")
    print("State check complete.")

if __name__ == "__main__":
    main()
