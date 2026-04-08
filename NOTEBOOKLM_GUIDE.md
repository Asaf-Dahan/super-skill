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
Or run: python3 scripts/generate_learning.py audio

The audio file is saved to: notebooks/audio-overview.mp3

### Generate a quiz

NotebookLM generates multiple-choice questions based on your content.
Use this to test your own understanding of your domain decisions.

To generate: run: python3 scripts/generate_learning.py quiz
The quiz is saved to: notebooks/quiz.json

### Generate a mind map

NotebookLM generates a visual map of how concepts in your domain
connect to each other.

To generate: run: python3 scripts/generate_learning.py mindmap
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

### Step 1: Install the library

  pip install "notebooklm-py[browser]"
  playwright install chromium

Windows alternative if pip is not found:
  py -m pip install "notebooklm-py[browser]"

Mac/Linux: use pip3 if pip is not found.

### Step 2: Log in

  notebooklm login

This opens a browser window. Log in with your Google account.
The session is saved so you do not need to log in again.

### Step 3: Create a notebook

  notebooklm create "[Your Domain] -- Super Skill"

Copy the notebook ID that is returned.

### Step 4: Configure

  cp .env.example .env

Open the .env file and paste your notebook ID:

  NOTEBOOK_ID=your-notebook-id-here

### Step 5: Feed your Super Skill into the notebook

  python3 scripts/feed_notebook.py

This loads all your layer files as sources. It takes about one minute.
You will see each file name printed as it loads.

### Step 6: Generate your first audio overview

  python3 scripts/generate_learning.py audio

This takes 3 to 10 minutes. The audio file is saved to:
notebooks/audio-overview.mp3

---

## No-Code Alternative

You do not need to use any scripts.

1. Go to https://notebooklm.google.com
2. Click "New notebook"
3. Click "Add source"
4. Upload your .md files one at a time
5. Start asking questions or generate an audio overview from the UI

This gives you the full NotebookLM experience without any
terminal commands.

---

## Keeping the Notebook Current

Every time you approve a change in PENDING.md and update a layer file,
re-run the feed script to keep the notebook in sync:

  python3 scripts/feed_notebook.py

Or run super-skill-sync with the feed flag:

  python3 scripts/super-skill-sync.py --feed

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

*Super Skill v2.3.1 -- April 2026*
*github.com/Asaf-Dahan/super-skill*
