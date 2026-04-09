# Super Skill

Super Skill is an open framework for creating private domain experts
for you and your AI agents.

A domain is any area of knowledge you work in: your tech stack,
your investment portfolio, your garden, your marketing strategy,
your fitness plan. Anything you know about and want your AI to know too.

Each Super Skill is an intelligence layer: a self-growing knowledge base
that your AI agents read before every task. It remembers what you have
decided, what tools you use, what is waiting for your approval, and what
must never be re-argued. Your AI stops starting from zero.

With NotebookLM (optional), your Super Skill also teaches you back:
audio overviews, quizzes, and mind maps generated from your own
domain knowledge.

Multiple agents. One source of truth. Always current.

---

> Early-stage open-source project. No SLA, no commercial support.
> AI outputs are not guaranteed to be accurate or suitable for any purpose.
> Verify all AI-generated content before use. MIT License -- no warranty of any kind.

---

## What You Need Before Starting

You need four things installed on your computer.
If any of these are missing, the Bootstrap prompt below will detect it
and tell you exactly what to install before continuing.

- **Claude Code** -- the AI that builds your Super Skill.
  Install via terminal: npm install -g @anthropic-ai/claude-code
  Full guide: https://docs.anthropic.com/en/docs/claude-code

- **Git** -- downloads the Super Skill template to your computer.
  Install from: https://git-scm.com/download
  Windows: run the installer, keep all default settings.
  Mac: Git is pre-installed on most Macs.

- **Python** (minimum version: Python 3.10) -- runs the Super Skill automation scripts.
  Install from: https://python.org/downloads
  Windows: check the box "Add Python to PATH" before clicking Install.
  Mac: Python 3 is pre-installed on most Macs.

  Note on `python` vs `python3`: macOS and Linux usually expose `python3`,
  while Windows installs Python as `python`. Throughout this README we use
  `python`. If you are on macOS or Linux and `python` is not found, use
  `python3` instead. You can also run any script via the cross-platform
  launcher, which auto-detects your interpreter:
    python scripts/run.py <script-name>

  For NotebookLM integration (optional): after cloning, run:
    pip install -r requirements.txt
  This is only needed if you plan to use the NotebookLM learning layer.
  Core activation works without it.

- **A free GitHub account** -- stores your Super Skill safely online.
  Create one at: https://github.com
  You will need this if you want to save your work to the cloud.

---

## How to Start

Three steps. One prompt. Under 15 minutes (if Git, Python, and Claude Code are already installed).

### Step 1: Create a folder

Create a folder on your computer called `super-skills`.
This is where all your Super Skills will live.

Windows: right-click on your Desktop, select New > Folder, name it `super-skills`.
Mac: right-click on your Desktop, select New Folder, name it `super-skills`.

### Step 2: Open Claude Code

Open a terminal in your `super-skills` folder and run:

  claude .

### Step 3: Copy and paste the Bootstrap prompt

Copy the entire block below. Paste it into Claude Code. That is all.

Or download and paste: `cat scripts/bootstrap.md`

After cloning, run `python scripts/doctor.py` to confirm your setup is complete.

Claude Code will check your setup, ask you one question about your domain,
download the template, and build your complete Super Skill automatically.

```
You are setting up a Super Skill.
Work through the following steps in order.
Stop and explain clearly if anything is missing before continuing.

STEP 1: Environment Check

Check git:
  run: git --version

If git is NOT installed, stop and tell the user:
  "Git is not installed.
   Git downloads the Super Skill template to your computer.
   Download it here: https://git-scm.com/download
   Windows: run the installer, keep all default settings.
   Mac: run the installer or type 'xcode-select --install' in Terminal.
   After installing, come back and paste this prompt again."

Check Python:
  run: python3 --version
  if that fails try: python --version

If Python is NOT installed, stop and tell the user:
  "Python is not installed.
   Python runs the Super Skill scripts.
   Download it here: https://python.org/downloads
   Windows: run the installer. Check the box that says
   'Add Python to PATH' before clicking Install.
   Mac: run the installer.
   After installing, come back and paste this prompt again."

Report: git version, python version, working directory. Then continue.

STEP 2: Domain Name and Description

Ask the user exactly this and wait for the answer:
  "What is your domain?
   This becomes the name of your Super Skill folder.
   Examples: garden, investments, fitness, marketing, stack
   One word or short phrase, no spaces."

Use the answer as [domain] in all following steps.

Then ask:
  "Describe your domain in one to three sentences.
   What does it cover? What are you building or managing?"

Use the answer as [domain-description] in Step 5.

Then ask:
  "What do you want to achieve with this Super Skill? One sentence."

Use the answer as [domain-goal] in Step 5.

STEP 3: Clone

run: git clone https://github.com/Asaf-Dahan/super-skill.git super-skill-[domain]

Forking this template? Replace the URL above with your own fork's URL.

Confirm all template files are present before continuing.

If you plan to use NotebookLM: copy .env.example to .env
and add your notebook ID after completing the NotebookLM setup
in NOTEBOOKLM_GUIDE.md.

STEP 4: Git Identity

Check:
  git -C super-skill-[domain] config user.name
  git -C super-skill-[domain] config user.email

If either is empty, ask:
  "What name should appear on your saved changes?"
  "What email address should be linked to them?"

Then set them:
  git -C super-skill-[domain] config user.name "[name]"
  git -C super-skill-[domain] config user.email "[email]"

STEP 5: Activate

Change into the cloned repository first:
  cd super-skill-[domain]

Read: SUPER_SKILL_MANIFESTO.md
Read: ONBOARDING.md

Run Prompt 1 from ONBOARDING.md in full.
All file operations happen inside this folder.
All generated files go here. Do not ask the user to copy Prompt 1.
Run it yourself.

When Prompt 1 reaches the placeholders at the end, fill them in
using the answers collected in Step 2:
  My domain: [domain-description]
  What I want to achieve: [domain-goal]
Do not ask the user again. Use the answers already collected.

STEP 6: First Commit

After all files are generated and SUMMARY.md exists:

git -C super-skill-[domain] add .
git -C super-skill-[domain] commit -m "feat: activate Super Skill -- [domain]"

STEP 7: Back up to GitHub (optional)

Ask the user exactly this and wait for the answer:
  "Do you want to save your Super Skill to GitHub?
   This keeps a backup online and lets you access it
   from any computer. You will need a free GitHub account
   at https://github.com
   Answer yes or no."

If yes:
  Tell the user:
    "Go to https://github.com/new
     - Repository name: super-skill-[domain]
     - Visibility: Private
     - Leave all checkboxes unchecked (no README, no .gitignore, no license)
     - Click 'Create repository'

     After the page reloads, look for the section titled:
       '...or push an existing repository from the command line'
     Copy the URL from that section. It looks like:
       https://github.com/your-username/super-skill-[domain].git

     Important: complete all steps on github.com/new before pasting.
     Do not paste the URL until after clicking 'Create repository.'

     Paste it here."

  Wait for the URL. Then run:
    git -C super-skill-[domain] remote set-url origin [URL]
    git -C super-skill-[domain] push -u origin main

  Add a line to CONTEXT.md under the identity or header section:
    Repository: [URL]

  Tell the user:
    "Your Super Skill is backed up to GitHub.
     The remote URL has been recorded in CONTEXT.md."

If no:
  Add this item to PENDING.md under the Queue section:

    ### PENDING-001: GitHub backup not configured
    Type: update
    Proposed: [today's date]
    Summary: GitHub backup was skipped during activation. To add later: create a repository at https://github.com/new, then run git remote set-url origin [URL] followed by git push -u origin main.
    Affected layers: CONTEXT.md
    Recommended action: adopt when ready
    Decision:
    Outcome:

  Tell the user:
    "Skipped. Your Super Skill is saved locally only.
     A reminder has been added to PENDING.md.
     Run /ss-pending when you are ready to set up GitHub backup."

Then tell the user:
  "Your Super Skill is live.
   To open it next time: open Claude Code on the
   super-skill-[domain] folder.
   Use /ss-eval, /ss-learn, /ss-pending and other
   slash commands for everything from here.

   Optional next step: connect the NotebookLM learning layer.
   See NOTEBOOKLM_GUIDE.md to generate audio, quizzes, and mind maps
   from your domain knowledge."
```

---

## What Happens After Activation

Once your Super Skill is active, you never need to copy prompts again.
Everything runs through slash commands. Type any of these into Claude Code:

| Command | What it does | Example |
|---------|-------------|---------|
| /ss-eval | Evaluate a new tool, method, or approach against your domain | `/ss-eval Stripe Connect` |
| /ss-graph | Generate the interactive knowledge graph | `/ss-graph` |
| /ss-learn | Generate a learning module on any topic in your domain | `/ss-learn drip irrigation` |
| /ss-pending | Show all items waiting for your approval | `/ss-pending` |
| /ss-query | Search wiki notes by keyword | `/ss-query caching` |
| /ss-sync | Pull updates from all your Super Skills and check for drift | `/ss-sync` |
| /ss-summary | Regenerate your SUMMARY.md from all layer files | `/ss-summary` |
| /ss-drift | Check your monitored sources for changes | `/ss-drift weekly` |
| /ss-council | Show your Expert Council debates and open challenges | `/ss-council` |
| /ss-expert | Run a structured expert debate session | `/ss-expert DEBATE-001` |
| /ss-synthesize | Synthesize insights across multiple layers | `/ss-synthesize tax efficiency` |

### Scripts reference

| Script | Purpose |
|---|---|
| `doctor.py` | Confirms your setup is complete |
| `update_summary.py` | Regenerates SUMMARY.md from the layer files |
| `super-skill-sync.py` | Pulls all configured Super Skills and checks drift URLs |
| `scheduled_tasks.py` | Runs maintenance tasks weekly/monthly/quarterly |
| `generate_graph.py` | Generates wiki/graph.json and wiki/knowledge-graph.html |
| `generate_global_graph.py` | Merges graphs from all local Super Skills into a global view |
| `feed_notebook.py` | (NotebookLM, optional) uploads layer files as sources |
| `generate_learning.py` | (NotebookLM, optional) generates audio / quiz / mind map |
| `check_state.py` | (NotebookLM, optional) asks the notebook 3 standard questions |
| `run.py` | Cross-platform launcher: `python scripts/run.py <name>` |

### Knowledge Graph

/ss-graph generates two files: an interactive visual (wiki/knowledge-graph.html)
and a machine-readable map (wiki/graph.json). Open the HTML file in any browser
to explore how your domain's knowledge is connected. Claude Code reads graph.json
to navigate your domain without loading all layer files every session.

To regenerate after any major change: /ss-graph

To generate a global graph across all your Super Skills: python scripts/generate_global_graph.py

---

## Adding a Second Super Skill

Each Super Skill lives in its own folder and tracks one domain.
To add a second domain, run Prompt 0 from ONBOARDING.md in a new terminal window.
Prompt 0 creates a fresh Super Skill folder alongside your existing one --
your first Super Skill is not affected.

Once you have two or more Super Skills, you can merge them into a single
knowledge map by running:

    python scripts/generate_global_graph.py

The output opens at ~/.claude/global-graph.html.

To keep multiple Super Skills in sync, see SYNC_SETUP.md.

---

## Skill vs Super Skill

| | Skill | Super Skill |
|---|---|---|
| What it is | A file | A living knowledge architecture |
| Knows how to | Do a task | Understand a full domain |
| Self-growing | No | Yes |
| Detects drift | No | Yes |
| Teaches the agent | Yes | Yes |
| Teaches you | No | Yes -- audio, quiz, mind map |
| Works with | Claude Code | Claude Code, Cursor, Codex, Gemini, any agent |
| Time to activate | 1 minute | Under 15 minutes |

---

## The Layer Architecture

> **Root vs `template/`** -- The layer files at the repository root are your
> working copy: Prompt 1 fills them in during activation. The `template/`
> directory contains the same files as a clean scaffold -- use it to
> regenerate or compare against the originals. Do not edit anything in
> `template/` directly.

Every Super Skill contains the same core files regardless of domain.
The structure is identical. The content is yours.

```
SUMMARY.md          session entry point -- 80 lines, always current
SKILL.md            agent skills format entry point
CLAUDE.md           Claude Code operating instructions
AGENTS.md           instructions for any other agent
CONTEXT.md          layer 0: identity, principles, scope
DOMAIN_MAP.md       layer 1: domain structure and sub-domain relationships
CURRENT_STATE.md    layer 2: verified current state
EVALUATION.md       layer 3: framework for evaluating anything new
DECISIONS.md        layer 4: decisions log and reasoning
MONITORING.md       layer 5: drift detection sources
LEARNING.md         layer 6: NotebookLM notebook plan
PENDING.md          layer 7: approval queue
LOG.md              change log and audit trail
experts/COUNCIL.md  layer X: expert council and debates
experts/[name].md   individual expert profiles
notebooks/          NotebookLM-ready learning files
                    (gitignored by design -- user-generated, not part of template)
wiki/               quick-reference notes, searchable via /ss-query
wiki/graph.json     machine-readable domain map (generated by /ss-graph)
wiki/knowledge-graph.html  interactive visual (open in browser)
template/SCHEDULE.md  scheduled maintenance tasks
scripts/            automation: feed, generate, check, sync, update_summary, scheduled_tasks
template/.claude/commands/   slash commands for Claude Code
template/experts/debates/    parallel expert debate sessions
```

---

## The Operating Principle

The model proposes.
The human decides.
The Super Skill records.
The system executes.

No layer file changes without your approval.
Every proposed change goes to PENDING.md first.
You review, you decide, then and only then it is recorded.

---

## NotebookLM -- The Learning Layer

NotebookLM is optional but transforms what a Super Skill can do.

Without NotebookLM: your agents read Markdown files from the repository.
Full context, zero re-explanation, every session.

With NotebookLM: the knowledge base grows beyond static files.
You and your agents can add research, documents, and new sources.
Claude proposes additions with your approval. You add directly in the notebook.
The notebook generates audio overviews, quizzes, and mind maps from your
own domain knowledge. Token usage drops significantly because Claude queries
the notebook instead of loading full files.

Connect it via the NotebookLM section in ONBOARDING.md. Skip it and add it later if you prefer.

---

## Expert Council

During activation, Claude Code researches your domain and proposes
10 real, leading experts with verifiable published work. You choose
who joins your council. Each expert is assigned to the layer they
contribute most to and given a full profile with methodology,
frameworks, red lines, and five questions they would ask you.

When experts disagree, the disagreement is recorded as a debate in
experts/COUNCIL.md. Claude Code surfaces expert perspectives only
when genuine friction exists -- not on routine tasks.

If an expert's position conflicts with a decision in DECISIONS.md,
it goes to PENDING.md as an expert challenge for your review.

---

## Domain Types

Super Skill works for any domain where knowledge matters and decisions accumulate.

Technical: software infrastructure, database architecture, security frameworks,
DevOps pipelines, product methodology, AI agent systems.

Professional: investment portfolio, legal review, medical documentation,
marketing strategy, real estate, financial modeling, operations.

Personal: home garden, fitness, nutrition, home renovation, language learning,
travel planning, personal finance.

Craft: photography, woodworking, wine, cooking techniques, academic research.

If you can describe it, a Super Skill can master it.

---

## Version

Super Skill v2.6.0

## License

MIT License -- Fork it. Build your own.

Super Skill is an open-source public template. No affiliation or ownership
is implied beyond authorship of the original template.

Fork it. Build your own. Publish your Super Skills.

---

## Important Notes

notebooklm-py is an unofficial library that uses undocumented Google APIs.
It may change without notice. Suitable for personal and internal use.
Not recommended for production systems serving external users.

Keep domain-specific Super Skills in private repositories.
Never commit API keys or tokens to any layer file.
Use .env for all sensitive values.

All agent actions follow one rule:
The model proposes. The human decides. The Super Skill records. The system executes.
Nothing changes without your approval.

---

## Created By

Super Skill was built by Asaf Dahan,
AI Solutions Architect at Gitit Inc.

Company: Gitit Inc
GitHub: https://github.com/Asaf-Dahan
