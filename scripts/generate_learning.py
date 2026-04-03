# © 2026 Gitit Inc · AI Architecture
# generate_learning.py - Generate audio overview, quiz, or mind map from NotebookLM

import asyncio
import json
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

VALID_MODES = ["audio", "quiz", "mindmap"]

async def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VALID_MODES:
        print(f"Usage: python generate_learning.py [{' | '.join(VALID_MODES)}]")
        sys.exit(1)

    mode = sys.argv[1]

    try:
        from notebooklm import NotebookLMClient
        from notebooklm.auth import AuthTokens
    except ImportError:
        print("ERROR: notebooklm-py is not installed.")
        print("Install it with: pip install \"notebooklm-py[browser]\"")
        sys.exit(1)

    root = Path(__file__).resolve().parent.parent
    output_dir = root / "notebooks"
    output_dir.mkdir(exist_ok=True)

    print(f"Generating {mode} for notebook: {NOTEBOOK_ID}")

    try:
        auth_tokens = await AuthTokens.from_storage()
    except Exception as e:
        print(f"ERROR: Could not load auth tokens: {e}")
        print("Run 'notebooklm login' first.")
        sys.exit(1)

    async with NotebookLMClient(auth=auth_tokens) as client:
        if mode == "audio":
            print("Generating audio overview (this may take a few minutes)...")
            status = await client.artifacts.generate_audio(NOTEBOOK_ID)
            if status.is_failed:
                print(f"ERROR: Audio generation failed: {status.error}")
                sys.exit(1)
            print(f"Audio generation started (task: {status.task_id}), polling...")
            result = await client.artifacts.wait_for_completion(
                NOTEBOOK_ID, status.task_id, timeout=600.0
            )
            if result.is_failed:
                print(f"ERROR: Audio generation failed: {result.error}")
                sys.exit(1)
            output_path = output_dir / "audio-overview.mp3"
            await client.artifacts.download_audio(
                NOTEBOOK_ID, str(output_path)
            )
            size = output_path.stat().st_size
            print(f"Audio saved to: {output_path} ({size:,} bytes)")

        elif mode == "quiz":
            print("Generating quiz...")
            status = await client.artifacts.generate_quiz(NOTEBOOK_ID)
            if status.is_failed:
                print(f"ERROR: Quiz generation failed: {status.error}")
                sys.exit(1)
            print(f"Quiz generation started (task: {status.task_id}), polling...")
            result = await client.artifacts.wait_for_completion(
                NOTEBOOK_ID, status.task_id, timeout=600.0
            )
            if result.is_failed:
                print(f"ERROR: Quiz generation failed: {result.error}")
                sys.exit(1)
            output_path = output_dir / "quiz.json"
            await client.artifacts.download_quiz(
                NOTEBOOK_ID, str(output_path)
            )
            size = output_path.stat().st_size
            print(f"Quiz saved to: {output_path} ({size:,} bytes)")

        elif mode == "mindmap":
            print("Generating mind map (no polling needed)...")
            result = await client.artifacts.generate_mind_map(NOTEBOOK_ID)
            mind_map = result.get("mind_map")
            note_id = result.get("note_id")
            if mind_map is None:
                print("ERROR: Mind map generation returned no data.")
                sys.exit(1)
            output_path = output_dir / "mindmap.json"
            output_path.write_text(
                json.dumps(mind_map, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            size = output_path.stat().st_size
            print(f"Mind map saved to: {output_path} ({size:,} bytes)")
            if note_id:
                print(f"Also saved as note in notebook (note_id: {note_id})")

    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
