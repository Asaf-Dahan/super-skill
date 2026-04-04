# Super Skill - Onboarding Prompts

These prompts are also in SUPER_SKILL_MANIFESTO.md.
This file is the quick-reference copy for daily use.

Three prompts. Copy, paste, done.

---

## Prompt 1 - Activate Your Super Skill

Paste this into any AI agent after cloning this repo.
Replace the two lines at the bottom with your own context.

```
I am activating a Super Skill for my domain.
Read SUPER_SKILL_MANIFESTO.md in this repository.
Understand what a Super Skill is and what the 10 layer
files must contain.

Then ask me the minimum number of questions needed to
generate my complete Super Skill. Do not ask more than
3 questions. Infer everything you can before asking.

After my answers, generate all 10 files directly into
this repository, replacing the empty template files:

  CONTEXT.md        (Layer 0: Identity and principles)
  DOMAIN_MAP.md     (Layer 1: Domain structure and sub-domains)
  CURRENT_STATE.md  (Layer 2: Current verified state)
  EVALUATION.md     (Layer 3: Framework for evaluating anything new)
  DECISIONS.md      (Layer 4: Decisions log - start empty)
  MONITORING.md     (Layer 5: What to watch and how often)
  LEARNING.md       (Layer 6: NotebookLM learning module plan)
  PENDING.md        (Layer 7: Approval queue - start empty)
  CLAUDE.md         (How Claude Code should operate in this domain)
  SKILL.md          (Agent Skills entry point with domain metadata)

Rules for generation:

  No placeholder text - every file must contain real content
  No em-dashes anywhere
  SKILL.md must include YAML frontmatter with name and description
  DOMAIN_MAP.md must include sub-domain relationships, not just a list
  EVALUATION.md must include specific criteria for this domain
  CLAUDE.md must include the file reading order and operating rules

My domain: [DESCRIBE IN ONE TO THREE SENTENCES - any topic, any field]
What I want to achieve: [YOUR GOAL - learn, manage, improve, master]
```

---

## Prompt 2 - Evaluate Something New

```
Using the Super Skill in this repository, evaluate the following.

Read CURRENT_STATE.md and EVALUATION.md first.
Apply the evaluation criteria defined there.

Do not recommend adoption.
Write your full evaluation to PENDING.md.
I will approve or reject it.

What to evaluate: [NAME OR DESCRIPTION]
Why I am considering it: [ONE SENTENCE]
What it might replace or add to: [EXISTING ELEMENT OR "new addition"]
```

---

## Prompt 3 - Generate Learning Content

```
Using the Super Skill in this repository, generate a
complete learning module on the following topic.

Read CONTEXT.md and CURRENT_STATE.md first so the
content is specific to my domain and situation.

The module must include:

  What this topic means in the context of my domain
  How it applies to my specific situation and goals
  Key decisions or facts already established that are relevant
  Common mistakes to avoid in my specific context
  A NotebookLM-ready summary (clear sections, no bullet walls)

Save the NotebookLM summary to: notebooks/[topic]-learning.md
Then tell me to run: python scripts/feed_notebook.py

Topic: [ANY TOPIC WITHIN YOUR DOMAIN]
```
