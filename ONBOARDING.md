# Super Skill - Onboarding Prompts

These prompts are also in SUPER_SKILL_MANIFESTO.md.
This file is the quick-reference copy for daily use.

Three prompts. Copy, paste, done.

---

## Prompt 1 - Activate Your Super Skill

Paste this into any AI agent after cloning this repo.

```
I am activating a Super Skill for my domain.
Read SUPER_SKILL_MANIFESTO.md in this repository to understand
what a Super Skill is and what structure it requires.

I will describe my domain and context.
Ask me the minimum number of questions needed to generate my
complete Super Skill. Do not ask more than 3 questions.
Infer everything you can before asking.

After your questions and my answers, generate these files:
  CONTEXT.md, DOMAIN_MAP.md, CURRENT_STATE.md, EVALUATION.md,
  DECISIONS.md, MONITORING.md, LEARNING.md, PENDING.md,
  CLAUDE.md, SKILL.md

My domain: [DESCRIBE IN ONE TO THREE SENTENCES]
What I am building or managing: [YOUR PROJECTS OR GOALS]
```

---

## Prompt 2 - Evaluate Something New

```
Using the Super Skill in this repository, evaluate the following
against my existing domain in CURRENT_STATE.md and EVALUATION.md.

Do not recommend adoption. Write your evaluation to PENDING.md.
I will approve or reject it.

What to evaluate: [NAME OR DESCRIPTION]
Why I am considering it: [ONE SENTENCE]
What it might replace: [EXISTING ELEMENT OR "unsure"]
```

---

## Prompt 3 - Generate Learning Content

```
Using the Super Skill in this repository, generate a complete
learning module on the following topic as it applies to my
specific domain and current state.

Include: concept explanation, how it applies to my situation,
relevant decisions already made, and a NotebookLM-ready summary.

Output the summary to: notebooks/[topic]-learning.md

Topic: [TOPIC WITHIN YOUR DOMAIN]
```
