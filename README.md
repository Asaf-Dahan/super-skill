# Super Skill

> A Super Skill is a portable, AI-native intelligence layer that gives
> any language model full context, methodology, and operational
> capability over a defined domain.
>
> A Super Skill is the new Domain Expert for you and your AI.

## Skill vs. Super Skill

|                    | Skill          | Super Skill         |
|--------------------|----------------|---------------------|
| What it is         | A file         | A living knowledge architecture |
| Knows how to       | Do a task      | Understand a domain |
| Self-updating      | No             | Yes                 |
| Teaches you        | No             | Yes — audio, quiz, mind map |
| Works with         | Claude Code    | Any model, any agent |
| Time to activate   | 1 minute       | 15 minutes          |

## Get Started in 4 Steps

### 1. Clone this repo

```bash
git clone https://github.com/Asaf-Dahan/super-skill
mv super-skill super-skill-[your-domain]
```

### 2. Install notebooklm-py and connect your Google account

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
```

See SETUP.md for details on Google authentication.

### 3. Paste Prompt 1 from ONBOARDING.md into any AI agent

The agent reads the template structure and asks you 3 questions maximum.
You answer. It generates all 10 layer files for your domain.

### 4. Run the feed script

```bash
cp .env.example .env
# Edit .env and add your notebook ID
python scripts/feed_notebook.py
```

Your Super Skill is live. Audio overview available.

## What You Get

A domain expert that:
- Knows everything in your domain and how it connects
- Detects when knowledge drifts and surfaces it for your review
- Generates audio overviews, quizzes, and mind maps from your knowledge
- Never changes anything without your explicit approval
- Works with Claude Code, Claude Projects, Cursor, or any AI agent

## Domain Types

Super Skill works for any domain.

**Technical:** software infrastructure, database architecture, DevOps,
security, product development

**Non-technical:** investment portfolio, legal review, medical documentation,
marketing strategy, real estate, financial modeling

## License

MIT License — © 2026 Gitit Inc · AI Architecture

Fork it. Build your own. Publish your Super Skills.
