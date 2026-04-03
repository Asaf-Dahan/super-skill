# © 2026 Gitit Inc · AI Architecture
# generate_learning.py - Generate audio overview, quiz, or mind map from NotebookLM

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

VALID_MODES = ["audio", "quiz", "mindmap"]

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VALID_MODES:
        print(f"Usage: python generate_learning.py [{' | '.join(VALID_MODES)}]")
        sys.exit(1)

    mode = sys.argv[1]
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

    root = Path(__file__).resolve().parent.parent
    output_dir = root / "notebooks"
    output_dir.mkdir(exist_ok=True)

    print(f"Generating {mode} for notebook: {notebook_id}")
    nb = NotebookLM()
    notebook = nb.get_notebook(notebook_id)

    if mode == "audio":
        print("Generating audio overview (this may take a few minutes)...")
        audio = notebook.generate_audio(timeout=600)
        output_path = output_dir / "audio-overview.wav"
        audio.save(str(output_path))
        print(f"Audio saved to: {output_path}")

    elif mode == "quiz":
        print("Generating quiz...")
        quiz = notebook.generate_quiz(timeout=600)
        output_path = output_dir / "quiz.md"
        output_path.write_text(str(quiz), encoding="utf-8")
        print(f"Quiz saved to: {output_path}")

    elif mode == "mindmap":
        print("Generating mind map...")
        mindmap = notebook.generate_mindmap(timeout=600)
        output_path = output_dir / "mindmap.md"
        output_path.write_text(str(mindmap), encoding="utf-8")
        print(f"Mind map saved to: {output_path}")

    print("Done.")

if __name__ == "__main__":
    main()
