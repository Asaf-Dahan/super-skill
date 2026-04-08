# ONBOARDING.md
# This file contains all activation and operational prompts.
# The Bootstrap prompt in README.md triggers the initial setup.
# After activation, Claude Code reads and runs prompts from here.

---

## Prompt 0 -- New Super Skill Setup

For users who already have one Super Skill and want to create another.
Claude Code runs this automatically when a user asks for a new domain.

```
I want to create a new Super Skill for a new domain.

STEP 1: Ask me exactly this and wait for the answer:
  "What is your new domain?
   This becomes the name of your Super Skill folder.
   Examples: garden, investments, fitness, marketing, stack
   One word or short phrase, no spaces."

Use the answer as [domain] in all following steps.

STEP 2: Clone the template into a new folder next to this one.

  git clone https://github.com/Asaf-Dahan/super-skill.git ../super-skill-[domain]

Confirm all template files are present before continuing.

Change into the new folder:
  cd ../super-skill-[domain]

STEP 3: Set up git identity in the new folder.

Check:
  git -C ../super-skill-[domain] config user.name
  git -C ../super-skill-[domain] config user.email

If either is empty, ask:
  "What name should appear on your saved changes?"
  "What email address should be linked to them?"

Then set them:
  git -C ../super-skill-[domain] config user.name "[name]"
  git -C ../super-skill-[domain] config user.email "[email]"

STEP 4: Back up to GitHub (optional)

Ask the user exactly this and wait for the answer:
  "Do you want to save this Super Skill to GitHub?
   This keeps a backup online and lets you access it
   from any computer. Answer yes or no."

If yes:
  Tell the user:
    "Go to https://github.com/new
     Create a new PRIVATE repository.
     Name it: super-skill-[domain]
     Do not add a README, .gitignore, or license.
     Click Create repository.
     Copy the URL shown and paste it here."

  Wait for the URL. Then run:
    git -C ../super-skill-[domain] remote set-url origin [URL]
    git -C ../super-skill-[domain] push -u origin main

  Tell the user: "Backed up to GitHub."

If no:
  Continue. Saved locally only.

STEP 5: Ensure you are in the new folder:
  cd ../super-skill-[domain]

Read ONBOARDING.md
Run Prompt 1 from that file in full.
All file operations happen inside this folder.
Do not ask the user to copy Prompt 1. Run it yourself.

STEP 6: After activation is complete:
  git -C ../super-skill-[domain] add .
  git -C ../super-skill-[domain] commit -m "feat: activate Super Skill -- [domain]"

Tell the user:
  "Your new Super Skill is live.
   To open it: open Claude Code on the super-skill-[domain] folder.
   Then update your global router with Prompt 2-update below."

STEP 7: Update the global Claude Code router.
Note: this step will update your global Claude Code router at
~/.claude/CLAUDE.md to include this Super Skill.

Read ~/.claude/CLAUDE.md (the global router).
Add a new row to the Super Skills Registry table for this domain.
Use specific trigger keywords that do not overlap with existing entries.
```

---

### Prompt 1 -- Domain Activation

```
Before anything else:
Check if git user.name and user.email are configured:
  git config user.name
  git config user.email
If either returns empty, ask me for my name and email, then run:
  git config user.name "My Name"
  git config user.email "my@email.com"

I am activating a Super Skill for my domain.
Read SUPER_SKILL_MANIFESTO.md in this repository.
Understand what a Super Skill is and what the layer files must contain.

This activation has three stages. Complete each stage fully before
moving to the next. Pause after Stage 2 and wait for my response.

--- STAGE 1: Domain Layer Generation ---

Scan the local environment to infer as much context as possible before asking.
Ask me at most 3 questions. Infer everything you can first.

After my answers, generate all 10 files directly into this repository,
replacing the empty placeholder files at the ROOT of the repo. Do not
edit anything inside the template/ directory -- those are pristine
scaffolds and must stay untouched. Working copy lives at the root.

  CONTEXT.md        (Layer 0: Who owns this, what domain, what goals)
  DOMAIN_MAP.md     (Layer 1: How your domain is organized -- what areas exist and how they connect to each other, not just a list)
  CURRENT_STATE.md  (Layer 2: What is true right now -- tools, versions, plans, statuses)
  EVALUATION.md     (Layer 3: How to assess anything new before adding it to your domain)
  DECISIONS.md      (Layer 4: Decisions log -- start empty)
  MONITORING.md     (Layer 5: What to watch and how often to check it)
  LEARNING.md       (Layer 6: NotebookLM learning module plan)
  PENDING.md        (Layer 7: Approval queue -- start empty)
  CLAUDE.md         (How Claude Code should operate in this domain)
  SKILL.md          (Agent Skills entry point with domain metadata)

Then generate SUMMARY.md by running:
  python scripts/update_summary.py .

If Python is not installed or not on PATH, generate SUMMARY.md directly
from the layer files instead of running the script.
SUMMARY.md must be 80 lines or fewer.

Rules for generation:
  - No placeholder text -- every file must contain real content
  - No em-dashes anywhere
  - SKILL.md must include YAML frontmatter with name and description
  - DOMAIN_MAP.md must show how different areas of your domain connect to each other, not just a flat list
  - EVALUATION.md must include specific criteria for this domain
  - CLAUDE.md must match the template/CLAUDE.md load protocol exactly
  - CLAUDE.md must include the Expert Perspectives Protocol section from template/CLAUDE.md
  - Super Skill repos commit directly to main.
    The feature branch rule applies to product codebases only, not to Super Skill repos.

Copy the slash commands and agent template into the working directory.

```
# Windows
xcopy template\.claude\commands .claude\commands /E /I /Y
xcopy template\.claude\agents .claude\agents /E /I /Y
```

```
# macOS / Linux
cp -r template/.claude/commands/ .claude/commands/
cp -r template/.claude/agents/ .claude/agents/
```

Confirm the .claude/commands/ directory contains 9 command files.

Create the experts/debates/ directory for future debate sessions.

```
# Windows
if not exist experts\debates mkdir experts\debates
```

```
# macOS / Linux
mkdir -p experts/debates
```

Add this item to PENDING.md under the Queue section:

  ### PENDING-002: NotebookLM not yet connected
  Type: update
  Proposed: [today's date]
  Summary: The NotebookLM learning layer is not yet connected. When ready, follow NOTEBOOKLM_GUIDE.md or run /ss-learn to generate audio, quizzes, and mind maps from your domain knowledge.
  Affected layers: LEARNING.md
  Recommended action: adopt when ready
  Decision:
  Outcome:

After all 10 files, SUMMARY.md, .claude/ setup, and experts/debates/ are complete, confirm:
"Stage 1 complete. Proceeding to Expert Council."

--- STAGE 2: Expert Council Research ---

Research the domain described above and propose 10 real, leading experts.
These must be real people with verifiable published work relevant to this domain.

For each expert, present:
  Name: [full name]
  Current role: [title and organization]
  Core methodology: [2 sentences describing their approach]
  Primary layer: Layer [N] - [layer name they contribute most to]
  Key works: [3 titles -- must be exact published titles with year.
  Books, papers, or named talks only. Not blog descriptions or company names.
  If unsure of exact title, mark it [VERIFY: exact title uncertain].]
  Domain relevance: [1 sentence on how they challenge or enrich this specific domain]

After presenting all 10, ask exactly:
"These are your proposed Expert Council members for [domain].
Choose who joins -- select by number, name experts not listed, or type ALL."

Wait for my response. Do not generate any files during Stage 2.

--- STAGE 3: Expert Profile Generation ---

For each expert I chose in Stage 2:
  Generate experts/[firstname-lastname].md using the structure
  defined in template/experts/EXPERT_TEMPLATE.md.

  Expert profiles are created directly in the repo root under experts/
  not inside template/experts/.
  template/experts/ contains only COUNCIL.md and EXPERT_TEMPLATE.md as structural templates.

Then generate experts/COUNCIL.md using the structure defined
in template/experts/COUNCIL.md.

Rules for Stage 3:
  - Real verifiable information only. Never invent positions or works.
  - Third person throughout every expert profile.
  - Debates only for genuine methodological conflicts, not style differences.
  - If an expert's known position conflicts with a decision in DECISIONS.md:
    write EXPERT-CHALLENGE-NNN to PENDING.md with the expert name,
    the decision ID, and a one-sentence description of the conflict.
  - No em-dashes anywhere.
  - Flag any Key Work entry that is not a book, paper, or named talk with a
    verifiable title. Mark it: [VERIFY: description of issue]
    Do not block file creation -- flag and continue.

After all profiles and COUNCIL.md are generated, confirm:
"Expert Council active. [N] members. [N] debates. Run update_summary.py.

Optional next step: set up NotebookLM to activate the learning layer.
Open NOTEBOOKLM_GUIDE.md or run /ss-learn when ready."

Then ask exactly:
"Would you like to set up NotebookLM now?
 Yes: I will walk you through NOTEBOOKLM_GUIDE.md step by step.
 No: A reminder is already in PENDING.md. Run /ss-learn when ready."

If yes: read NOTEBOOKLM_GUIDE.md and follow the setup steps.
If no: confirm the PENDING item about NotebookLM is present and continue.

My domain: [DESCRIBE IN ONE TO THREE SENTENCES]
What I want to achieve: [YOUR GOAL]
```

---

### Prompt 2 -- Create Global Router (first time)

```
Create the file ~/.claude/CLAUDE.md as a global router for Claude Code.

It must contain:
  - A Super Skills Registry table with this Super Skill as the first entry
  - The correct local path to this repository
  - Trigger keywords for this domain
  - The session start protocol: read SUMMARY.md first, then PENDING.md
  - The Iron Principle
  - A note that if a Super Skill path does not exist, skip and proceed

Use this exact session start protocol in the file:

  Session Start:
  1. Identify domain from task description
  2. Load [domain]/SUMMARY.md
  3. Load [domain]/PENDING.md
  4. If task requires more: follow Load Protocol table in SUMMARY.md
  5. Never start from zero. Never re-litigate settled decisions.
```

### Prompt 2-update -- Add a Second Super Skill to an Existing Router

```
Read ~/.claude/CLAUDE.md (on Windows: C:\Users\YourName\.claude\CLAUDE.md).
Find the Super Skills Registry table.
Add a new row matching the exact format of the existing rows.

Do not change any other part of the file.

After adding the new entry:
  - Verify that all existing Super Skill paths in the registry actually exist on disk
  - Flag any path that does not exist with a comment: # PATH NOT FOUND
  - Use specific trigger keywords that do not overlap with existing entries
  - If overlap is unavoidable, note it explicitly

New Super Skill to add:
  Name: [super-skill-name]
  Path: [full absolute path to the repo folder]
  Triggers: [2-3 specific keywords that will activate this domain]
```

---

## NotebookLM -- Connect the Learning Layer (Optional)

Full setup guide: NOTEBOOKLM_GUIDE.md -- we recommend the Manual Setup
path (no installs, never breaks).

Recommended path:
  1. Go to https://notebooklm.google.com and create a new notebook
  2. Upload your layer .md files as sources
  3. Use the chat, audio overview, mind map, and quiz features in the UI

Advanced path (uses the unofficial notebooklm-py library, may break):

  pip install "notebooklm-py[browser]"
  notebooklm login
  notebooklm create "[Your Domain] -- Super Skill"
  cp .env.example .env
  python scripts/feed_notebook.py
  python scripts/generate_learning.py audio

---

## Prompt 3 -- Evaluate Something New

```
Using the Super Skill in this repository, evaluate the following.

Read SUMMARY.md and EVALUATION.md first.
Apply the evaluation criteria defined there.

Do not recommend adoption.
Write your full evaluation to PENDING.md.
I will approve or reject it.

What to evaluate: [NAME OR DESCRIPTION]
Why I am considering it: [ONE SENTENCE]
What it might replace or add to: [EXISTING ELEMENT OR "new addition"]
```

---

## Prompt 4 -- Generate Learning Content

```
Using the Super Skill in this repository, generate a complete
learning module on the following topic.

Read SUMMARY.md and CONTEXT.md first so the content is specific
to my domain and situation.

The module must include:
  - What this topic means in the context of my domain
  - How it applies to my specific situation and goals
  - Key decisions or facts already established that are relevant
  - Common mistakes to avoid in my specific context
  - A NotebookLM-ready summary (clear sections, no bullet walls)

Save the NotebookLM summary to: notebooks/[topic]-learning.md
Then run: python scripts/feed_notebook.py

Topic: [ANY TOPIC WITHIN YOUR DOMAIN]
```

---

Note on numbering: Prompt 5 is reserved for future use. There is no
Prompt 5 in this version. Prompt 6 follows directly.

---

## Prompt 6 -- Approve a PENDING Item

```
Read PENDING.md.
Show me each open item with a one-line summary.

For each item, ask: "Approve, reject, or defer?"

On approval:
  Move the item to the correct layer file.
  Mark it as Approved in PENDING.md with the date.
  Run: python scripts/update_summary.py .

On rejection:
  Move the item to the Resolved section in PENDING.md.
  Include the reason for rejection and the date.

On defer:
  Leave the item in place.
  Add a note: "Deferred: [date] -- [reason if given]"

After all items are reviewed, report:
  "[N] approved, [N] rejected, [N] deferred."
```

---

## Prompt 7 -- Run Expert Debate Session

```
Read experts/COUNCIL.md.
Select one active debate (Status: Open).

Load both expert profiles from experts/[name].md for the
two participants in the debate.

Present both positions in the context of this specific domain:
  - What each expert argues and why
  - What specific decision or tradeoff the debate affects
  - What the owner gains or risks from each position
  - Where the positions overlap, if at all

Write a structured debate summary to:
  experts/debates/[DEBATE-ID]-[date].md

Use this format:
  # [DEBATE-ID]: [debate title]
  Date: [today]
  Participants: [Expert A] vs [Expert B]

  ## Position A: [Expert A name]
  [2-3 paragraphs presenting their argument in this domain's context]

  ## Position B: [Expert B name]
  [2-3 paragraphs presenting their argument in this domain's context]

  ## What This Means for This Domain
  [2-3 paragraphs on the specific impact and tradeoffs]

  ## Decision Required
  [One sentence framing the choice the owner needs to make]

  Status: Unresolved -- awaiting owner decision.

Do not resolve the debate. Surface the tension. Let the owner decide.
```

---

## Domain Agent Template

The file template/.claude/agents/domain-agent.md provides a ready-made
Claude Code agent definition for your domain. It loads CURRENT_STATE.md,
DECISIONS.md, and PENDING.md before every task, and enforces the Iron
Principle automatically. Rename it to match your domain after activation.

## Using with Other Agents

The Super Skill framework works with any AI agent that can read
and write files. You do not need Claude Code.

Cursor: Open the Super Skill folder in Cursor.
Ask Cursor to read ONBOARDING.md and run the relevant prompt.

Codex: Open the Super Skill folder. Ask Codex to read
ONBOARDING.md and run the relevant prompt.

Other agents: Any agent that supports file read/write and follows
the Agent Skills standard can operate a Super Skill. See AGENTS.md.

The Iron Principle applies regardless of agent:
The model proposes. The human decides. The Super Skill records. The system executes.
