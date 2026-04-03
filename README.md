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

## Important Disclaimers

**Regarding notebooklm-py:**
Super Skill uses notebooklm-py, an unofficial Python library
that accesses Google NotebookLM via undocumented internal APIs.

- Not affiliated with Google
- APIs may change without notice and break functionality
- Rate limits apply - heavy usage may be throttled
- Suitable for personal use, research, and internal projects
- Not recommended for production systems serving external users

See the notebooklm-py repository for full details:
github.com/teng-lin/notebooklm-py

**Regarding your data:**
The knowledge files in your Super Skill repository contain your
domain context, decisions, and operational details. Treat them
accordingly:

- Keep domain-specific Super Skills in private repositories
- Never commit API keys, tokens, or credentials to any layer file
- Use .env for all sensitive values - the .env.example is provided
- The .gitignore in this template excludes .env and notebooks/

**Regarding AI agent actions:**
Super Skill follows one operating principle:

> The model proposes. The human decides. The Super Skill records.
> The system executes.

No layer file is updated automatically. All proposed changes
are written to PENDING.md and require explicit human approval
before being committed. This applies to all agents using this skill.

---

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

## After Your First Super Skill

Once your first Super Skill is live, the recommended path is:

**One repository per Super Skill.**

Each Super Skill is an independent knowledge system with its own
domain, its own NotebookLM notebook, and its own lifecycle.
Keeping them in separate repositories ensures:

- Clean context loading for AI agents
- Independent versioning and changelog per domain
- No cross-domain noise when the agent is working in one area
- Easy sharing or publishing of individual Super Skills

**Recommended architecture:**

```
your-github/
  super-skill-stack-os/        private - technical infrastructure
  super-skill-investments/     private - portfolio management
  super-skill-[your-domain]/   private - any other domain
  super-skills-registry/       private - index of all your Super Skills
```

The registry is a simple YAML file that lists every Super Skill
you own, its repo URL, domain, and status. Any AI agent reads
it first to know which Super Skill to load for a given task.

**Starting your second Super Skill:**

1. Clone this template repo again into a new folder
2. Rename it for your new domain
3. Run Prompt 1 from ONBOARDING.md with your new domain context
4. Create a new NotebookLM notebook for that domain
5. Run the feed script

Each activation takes under 15 minutes.

---

## Domain Types

Super Skill works for any domain.

**Technical:** software infrastructure, database architecture, DevOps,
security, product development

**Non-technical:** investment portfolio, legal review, medical documentation,
marketing strategy, real estate, financial modeling

## License

MIT License - © 2026 Gitit Inc · AI Architecture

Fork it. Build your own. Publish your Super Skills.

## Security

**Session credentials:**
notebooklm-py stores Google session cookies locally at
~/.notebooklm/ after login. This file contains active session
credentials for your Google account. Protect it accordingly.

Do not share this file. Do not commit it to any repository.
If you suspect it has been exposed, log out and re-authenticate:

```
notebooklm login
```

**Repository visibility:**
This template repository is public and contains no personal data.
Your Super Skill repositories should be private unless you
intentionally choose to publish a domain as an open resource.

**Reporting issues:**
If you find a security issue in this template, open a private
issue on GitHub or contact via gitit-inc.com

---

## Created By

Super Skill was conceived and built by Asaf Dahan,
AI Solutions Architect at Gitit Inc.

He works at the intersection of AI-native product development,
autonomous agent architecture, and sovereign infrastructure design.

Stack OS is the first published Super Skill.

- Website: asafid.com
- Company: gitit-inc.com
- GitHub: github.com/Asaf-Dahan

Built with Claude Code. Powered by notebooklm-py.

---
