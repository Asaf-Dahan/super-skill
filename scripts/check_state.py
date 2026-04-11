#!/usr/bin/env python3
# check_state.py - Ask 3 standard questions to the notebook to verify domain state
#
# Run with:
#   python scripts/check_state.py        (Windows / cross-platform)
#   python3 scripts/check_state.py       (macOS / Linux)
#   python scripts/run.py check_state    (auto-detects interpreter)

import asyncio
import os
import sys

from dotenv import load_dotenv

STANDARD_QUESTIONS = [
    "What is the current state of this domain?",
    "What decisions have been made and what is still pending?",
    "What changes or updates have been detected recently?",
]

async def main():
    load_dotenv()

    notebook_id = os.getenv("NOTEBOOK_ID")
    if not notebook_id:
        print("Error: NOTEBOOK_ID not set.")
        print("Copy .env.example to .env and add your notebook ID.")
        sys.exit(1)

    try:
        from notebooklm import NotebookLMClient
        from notebooklm.auth import AuthTokens
    except ImportError:
        print("ERROR: notebooklm-py is not installed.")
        print("Install it with: pip install \"notebooklm-py[browser]\"")
        sys.exit(1)

    print(f"Checking state for notebook: {notebook_id}")

    try:
        auth_tokens = await AuthTokens.from_storage()
    except Exception as e:
        print(f"ERROR: Could not load auth tokens: {e}")
        print("Run 'notebooklm login' first.")
        sys.exit(1)

    async with NotebookLMClient(auth=auth_tokens) as client:
        for i, question in enumerate(STANDARD_QUESTIONS, 1):
            print(f"\n{'='*60}")
            print(f"Question {i}: {question}")
            print(f"{'='*60}")
            try:
                response = await client.chat.ask(notebook_id, question)
                print(response.answer)
            except Exception as e:
                print(f"ERROR: {e}")

    print(f"\n{'='*60}")
    print("State check complete.")

if __name__ == "__main__":
    asyncio.run(main())
