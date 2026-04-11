# NotebookLM -- The Learning Layer

> Warning: NotebookLM integration described here uses the standard NotebookLM
> web interface. There is no official NotebookLM API. No automation is guaranteed
> to work if Google changes the interface. Always verify current NotebookLM behavior
> before relying on these instructions.

NotebookLM is a free tool from Google that turns documents into
an interactive knowledge base. You can ask it questions, generate
audio conversations, take quizzes, and create mind maps -- all
from your own content.

When connected to your Super Skill, NotebookLM holds a living
copy of everything your Super Skill knows. Instead of loading
full files into Claude Code every session, Claude can query the
notebook and get a precise answer in seconds.

NotebookLM is optional. Your Super Skill works fully without it.
Add it when you are ready to deepen the learning layer.

---

## What Gets Loaded Into NotebookLM

When you run the feed script, these files are loaded as sources:

  CONTEXT.md          who you are, what domain, what goals
  DOMAIN_MAP.md       how your domain is structured
  CURRENT_STATE.md    what is true right now
  EVALUATION.md       how you assess new things
  DECISIONS.md        every decision made and why
  MONITORING.md       what you watch for changes
  LEARNING.md         your learning module plan
  PENDING.md          what is waiting for your approval
  notebooks/          any learning modules you have generated

Each file becomes a source in your notebook. NotebookLM reads
them all and can answer questions that draw from any combination.

---

## What You Can Do With the Notebook

### Ask questions

Open your notebook at https://notebooklm.google.com and ask anything:

  "What decisions have I made about my database?"
  "What is waiting for my approval?"
  "What should I monitor this month?"
  "Explain the tradeoffs in my current stack."

NotebookLM answers from your actual files, not from general knowledge.
Every answer cites the source it came from.

### Generate an audio overview

NotebookLM can generate a short audio conversation (5 to 20 minutes)
between two AI hosts who discuss your domain knowledge as if they
are reviewing it together.

This is useful for:
- Understanding your own domain from a fresh angle
- Reviewing decisions while commuting or exercising
- Catching gaps or contradictions in your knowledge base

To generate: click "Audio Overview" in your notebook.
Or run: python scripts/generate_learning.py audio

The audio file is saved to: notebooks/audio-overview.mp3

### Generate a quiz

NotebookLM generates multiple-choice questions based on your content.
Use this to test your own understanding of your domain decisions.

To generate: run: python scripts/generate_learning.py quiz
The quiz is saved to: notebooks/quiz.json

### Generate a mind map

NotebookLM generates a visual map of how concepts in your domain
connect to each other.

To generate: run: python scripts/generate_learning.py mindmap
The mind map is saved to: notebooks/mindmap.json

---

## The Learning Loop

Your Super Skill and NotebookLM reinforce each other over time.

  Your Super Skill teaches Claude Code.
  Claude Code produces better outputs.
  Better outputs are recorded in DECISIONS.md.
  DECISIONS.md is loaded into NotebookLM.
  NotebookLM teaches you through audio and quizzes.
  You make better decisions because you understand your domain better.
  Better decisions improve your Super Skill.
  The loop continues.

---

## How to Set It Up

There are two ways to set this up. Most users should pick the manual
path because it has no dependencies and never breaks.

---

## Manual Setup (Recommended)

This path uses only the official NotebookLM web interface. Nothing to
install. Works on every operating system. Cannot be broken by Google
changing an internal API.

### Step 1: Create a notebook

1. Go to https://notebooklm.google.com
2. Sign in with your Google account
3. Click "New notebook"
4. Name it "[Your Domain] -- Super Skill"

### Step 2: Add your layer files as sources

1. Click "Add source" inside the new notebook
2. Choose "Upload" and select your Super Skill .md files. Upload at least:
     CONTEXT.md, DOMAIN_MAP.md, CURRENT_STATE.md, EVALUATION.md,
     DECISIONS.md, MONITORING.md, LEARNING.md, PENDING.md
3. Wait for each upload to complete (a few seconds each)

### Step 3: Use the notebook

- Ask questions in the chat panel. NotebookLM answers from your files.
- Click "Audio Overview" to generate the AI conversation overview.
- Click "Studio" then "Mind Map" or "Quiz" to generate other artifacts.

### Step 4: Keeping the notebook current

When you approve a change in PENDING.md and update a layer file, re-upload
that file as a new source in NotebookLM. The old source can be deleted from
the source list.

This is the recommended path for most users. Skip the rest of this guide
unless you specifically want script-driven automation.

---

## Automated Setup (Advanced)

> **Warning:** This path uses `notebooklm-py`, an unofficial library that
> wraps undocumented Google APIs. It can break at any time without notice.
> If a script fails after a Google update, fall back to the Manual Setup
> above. Do not file bug reports against Google for this.

### Step 1: Install the library (automatic)

Check if notebooklm-py is already installed:

  python -c "import notebooklm; print('OK')" 2>&1

If not installed, run:

  pip install "notebooklm-py[browser]" --break-system-packages
  playwright install chromium

Windows alternative if pip is not found:
  py -m pip install "notebooklm-py[browser]"

Mac/Linux: use pip3 if pip is not found.

### Step 2: Check session and log in if needed (automatic)

Check if a valid session exists:

  python -c "
import asyncio
from notebooklm.auth import AuthTokens
async def check():
    try:
        await AuthTokens.from_storage()
        print('SESSION_VALID')
    except:
        print('SESSION_MISSING')
asyncio.run(check())
"

If SESSION_VALID: continue to Step 3. Do not ask the user anything.

If SESSION_MISSING:
  Tell the user: "A browser window will open. Log in with your Google account."
  Run: notebooklm login
  After login, continue automatically.

### Step 3: Create a notebook (automatic)

  notebooklm create "[Your Domain] -- Super Skill"

Save the returned notebook ID automatically:

  Write NOTEBOOK_ID=[id] to .env (create from .env.example if needed)
  Record Notebook ID in CONTEXT.md

### Step 4: Feed your Super Skill into the notebook (automatic)

  python scripts/feed_notebook.py

This loads all your layer files as sources. It takes about one minute.
You will see each file name printed as it loads.

### Step 5: Generate your first audio overview (automatic)

  python scripts/generate_learning.py audio

This takes 3 to 10 minutes. The audio file is saved to:
notebooks/audio-overview.mp3

### If any step fails

The flow must always move forward. Present options:
  Option A: retry the failed step
  Option B: switch to Manual Setup (see above)
  Option C: skip NotebookLM for now -- add a PENDING item as a reminder

---

## Keeping the Notebook Current

Every time you approve a change in PENDING.md and update a layer file,
re-run the feed script to keep the notebook in sync:

  python scripts/feed_notebook.py

Or run super-skill-sync with the feed flag:

  python scripts/super-skill-sync.py --feed

This updates all your Super Skills and pushes the latest content
to NotebookLM in one command.

---

## Important Notes

notebooklm-py uses unofficial Google APIs that may change without
notice. It is suitable for personal and internal use.

Session cookies are stored at: ~/.notebooklm/
Protect this folder. Do not commit it to any repository.
It is already excluded by .gitignore.

Your notebook ID is stored in .env
Do not commit .env to any repository.
It is already excluded by .gitignore.

---

## Library API Pattern (for script maintainers)

`notebooklm-py` v0.3.4 (pinned in `requirements.txt`) uses an async client.
All scripts in this template follow this pattern:

```python
import asyncio
from notebooklm import NotebookLMClient
from notebooklm.auth import AuthTokens

async def main():
    auth = await AuthTokens.from_storage()
    async with NotebookLMClient(auth=auth) as client:
        result = await client.sources.add_text(
            notebook_id, title, content
        )

asyncio.run(main())
```

Notes:
- The class is `NotebookLMClient`, not `NotebookLM`.
- `AuthTokens.from_storage()` is async; always `await` it.
- `add_text` signature is `(notebook_id, title, content)`.

## Version Management

This template pins `notebooklm-py` to a specific version. Do not upgrade
automatically. To upgrade intentionally:

1. Check the upstream changelog and review breaking changes.
2. Test `feed_notebook.py` and `generate_learning.py` after upgrading.
3. Update the version in `requirements.txt` and `CURRENT_STATE.md`.

To install the pinned version:

```bash
pip install -r requirements.txt
```

To check your current installed version:

```bash
pip show notebooklm-py
```

---

*Super Skill v2.7.1 -- April 2026*
*github.com/Asaf-Dahan/super-skill*
