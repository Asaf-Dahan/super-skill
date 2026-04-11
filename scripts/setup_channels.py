#!/usr/bin/env python3
# setup_channels.py -- Check prerequisites for Claude Code Channels.
#
# Read-only diagnostic. No file writes, no API calls, no interactive input.
# Prints a checklist of prerequisites and the exact commands to run.
#
# Run with:
#   python scripts/setup_channels.py       (Windows / cross-platform)
#   python3 scripts/setup_channels.py      (macOS / Linux)
#   python scripts/run.py setup_channels   (auto-detects interpreter)
#
# Stdlib only. No third-party dependencies.

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def check_tool(name, commands):
    """Try each command in order. Return (found, version_string)."""
    for cmd in commands:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                version = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "found"
                return True, version
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return False, ""


def main():
    print("Super Skill -- Channels Setup Check")
    print("=" * 42)
    print()

    checks = []

    # 1. Claude Code
    found, version = check_tool("claude", [["claude", "--version"]])
    if found:
        print(f"[OK]      Claude Code: {version}")
    else:
        print("[MISSING] Claude Code: not found on PATH")
        print("          Install: npm install -g @anthropic-ai/claude-code")
    checks.append(("Claude Code", found))

    # 2. tmux
    found, version = check_tool("tmux", [["tmux", "-V"]])
    if found:
        print(f"[OK]      tmux: {version}")
    else:
        print("[MISSING] tmux: not found on PATH")
        if sys.platform == "darwin":
            print("          Install: brew install tmux")
        elif sys.platform == "win32":
            print("          tmux requires WSL on Windows.")
            print("          Install WSL: wsl --install  (PowerShell as Admin)")
            print("          Then inside WSL: sudo apt install tmux")
        else:
            print("          Install: sudo apt install tmux  (Debian/Ubuntu)")
            print("                   sudo dnf install tmux  (Fedora/RHEL)")
    checks.append(("tmux", found))

    # 3. Super Skill activated (CONTEXT.md has real content)
    context_file = REPO / "CONTEXT.md"
    activated = False
    if context_file.exists():
        text = context_file.read_text(encoding="utf-8", errors="ignore")
        # Check if it still has placeholder brackets
        placeholder_lines = sum(
            1 for line in text.splitlines()
            if line.strip().startswith("[") and "](" not in line.strip()
        )
        content_lines = sum(
            1 for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("<!--")
        )
        activated = content_lines > 0 and (placeholder_lines / max(content_lines, 1)) < 0.5
    if activated:
        print("[OK]      Super Skill: activated")
    else:
        print("[MISSING] Super Skill: not activated yet")
        print("          Run Prompt 1 from ONBOARDING.md to activate first.")
    checks.append(("Super Skill activated", activated))

    # 4. CHANNELS_GUIDE.md exists
    guide = REPO / "CHANNELS_GUIDE.md"
    if guide.exists():
        print(f"[OK]      CHANNELS_GUIDE.md: present")
    else:
        print("[MISSING] CHANNELS_GUIDE.md: not found at repo root")
    checks.append(("CHANNELS_GUIDE.md", guide.exists()))

    print()
    print("-" * 42)

    all_ok = all(ok for _, ok in checks)

    if all_ok:
        print()
        print("All prerequisites met. Run these commands in order:")
        print()
        print("  1. Start a tmux session:")
        print("     tmux new -s superskill")
        print()
        print("  2. Navigate to your Super Skill and start Claude Code:")
        print(f"     cd {REPO}")
        print("     claude --channels .")
        print()
        print("  3. In Claude Code, configure Telegram:")
        print("     /telegram:configure")
        print()
        print("  4. Follow the pairing instructions in CHANNELS_GUIDE.md.")
    else:
        print()
        print("Some prerequisites are missing. Fix the items above first.")
        print("Full setup guide: CHANNELS_GUIDE.md")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
