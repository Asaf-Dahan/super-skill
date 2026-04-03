# Super Skill

> A Super Skill is a portable, AI-native intelligence layer that gives
> any language model full context, methodology, and operational
> capability over a defined domain.
>
> A Super Skill is the new Domain Expert for you and your AI.
>
> It is not just a file the agent reads.
> It is an interactive knowledge system that grows with you,
> teaches both the model and the human, and keeps your domain
> knowledge current, auditable, and alive.

## Skill vs. Super Skill

| | Skill | Super Skill |
|---|---|---|
| What it is | A file | A living knowledge architecture |
| Knows how to | Do a task | Understand a full domain |
| Self-updating | No | Yes |
| Detects drift | No | Yes |
| Teaches the AI | Yes | Yes |
| Teaches you | No | Yes - audio, quiz, mind map, slides |
| Interactive | No | Yes - via NotebookLM |
| Works with | Claude Code | Any model, any agent |
| Time to activate | 1 minute | 15 minutes |

## Get Started in 4 Steps

### 1. Clone this repo

```bash
git clone https://github.com/Asaf-Dahan/super-skill
mv super-skill super-skill-[your-domain]
```

### 2. Connect the Learning Layer

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
notebooklm login
```

This step is what separates a Super Skill from every other
AI customization approach.

Once connected, your Super Skill generates a dedicated NotebookLM
notebook for your domain. That notebook becomes an interactive
knowledge interface that works in two directions.

**From your AI agent:**
The agent reads your domain layers, detects drift, proposes updates,
and asks NotebookLM questions about your own knowledge base.

**From you, directly in NotebookLM:**
Open your notebook and explore your domain knowledge as a human.
Ask questions. Get cited answers. See where your knowledge is strong
and where it needs updating.

**Visual and audio outputs you can generate:**

| Output | How to generate | What you get |
|---|---|---|
| Podcast | `python scripts/generate_learning.py audio` | MP3 deep dive on your domain |
| Quiz | `python scripts/generate_learning.py quiz` | Test your domain knowledge |
| Mind Map | `python scripts/generate_learning.py mindmap` | Visual domain structure |
| Slide Deck | Ask Claude: "Generate a presentation from my Super Skill" | Shareable slides |
| Study Guide | Ask NotebookLM directly | Structured learning document |
| Briefing | Ask NotebookLM directly | Executive summary of your domain |

This is not a tool for AI agents only.
It is the bridge between you and your domain knowledge.
The Super Skill teaches the agent. The outputs teach you.
As you learn, you improve the skill. As the skill improves,
the agent becomes more accurate. The loop runs in both directions.

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

## Domain Types

Super Skill works for any domain.

**Technical:** software infrastructure, database architecture, DevOps,
security, product development

**Non-technical:** investment portfolio, legal review, medical documentation,
marketing strategy, real estate, financial modeling

## License

MIT License - © 2026 Gitit Inc · AI Architecture

Fork it. Build your own. Publish your Super Skills.

---

## Created By

Super Skill was conceived and developed by Asaf Dahan.

Asaf Dahan is a Product Architect and AI Solutions Lead at
Gitit Inc and A/Z Systems. He works at the intersection of
AI-native product development, autonomous agent architecture,
and sovereign infrastructure design.

Stack OS is the first published Super Skill.

Website: asafid.com
Company: gitit-inc.com
GitHub: github.com/Asaf-Dahan

Built with Claude Code. Powered by notebooklm-py.
