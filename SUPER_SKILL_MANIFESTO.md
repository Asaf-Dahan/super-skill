# Super Skill - Founding Document

Version: 2.3.1
Status: Canonical
Language: English
Author: Asaf Dahan
Date: April 2026

---

## The Definition

A Skill is a file.
A Super Skill is a living knowledge architecture.

A Skill tells an AI how to perform a task.
A Super Skill gives an AI a complete, current, layered understanding of a domain - including how to verify its own knowledge, how to detect when that knowledge is outdated, how to generate learning materials from it, and how to remain the most accurate and useful version of itself over time.

```
A Super Skill is a portable, AI-native intelligence layer that gives
any language model full context, methodology, and operational capability
over a defined domain.

A Super Skill is the new Domain Expert for you and your AI.
```

---

## Why This Is Different From Everything That Exists

Every existing approach to AI personalization is static at its core.

Custom instructions are written once and forgotten.
RAG retrieves documents but does not understand them.
RAG (Retrieval-Augmented Generation) is a method where an AI searches a
document collection before answering. It retrieves but does not understand.
Agent Skills define how to perform a task but not how to understand a field.
Fine-tuning burns knowledge into a model that cannot update itself.
Fine-tuning permanently modifies an AI model using training data.
The changes cannot be updated without retraining the entire model.

A Super Skill is none of these things.

It is a growing repository of structured knowledge, organized in layers, connected to live sources, capable of generating learning artifacts, and designed to be operated by any language model on behalf of any human who defines their domain and their context.

The model that reads a Super Skill does not just know what to do.
It knows why things are done this way, what has been decided and why, what is being watched, what is uncertain, and what needs human approval before anything changes.

---

## The Landscape: Where Super Skill Fits

```
2022    Custom Instructions
        Static. Manual. Single-session. No memory.

2023    System Prompts and RAG
        Documents fed into context. Better, but not portable.
        Not self-updating. Not evaluative.

2024    Model Context Protocol (MCP)
        MCP is a standard that lets AI agents connect to external tools and services.
        Standardized tool connectivity. The agent can act.
        But it still does not know what it is.

Oct 2025  Agent Skills
          SKILL.md files. Modular instructions. Portable.
          Adopted by 16+ tools. A genuine open standard.
          Tells the agent HOW to perform a specific task.

Dec 2025  Agent Skills Open Standard (Anthropic)
          Released to the ecosystem. VS Code, Cursor, GitHub,
          OpenAI, Microsoft all adopted within weeks.

Apr 2026  Super Skill
          The layer above.
          Tells the agent what the DOMAIN is, how it works,
          what has been decided, what to watch, what to learn,
          and how to keep growing.
```

The gap that exists today: Agent Skills define capability per task.
No standard exists for domain-level intelligence across a whole field.
Super Skill fills that gap.

---

## The Layer Architecture

Every Super Skill, regardless of domain, contains the same structural layers.
The layers are pre-built. The content inside them is domain-specific and user-defined.

This is what makes every Super Skill both universal in structure and unique in content.

```
LAYER 0: IDENTITY
  Who this Super Skill belongs to.
  What domain it covers.
  What the user is building or managing within that domain.
  The operating principles that govern all decisions.
  The boundaries of the domain.

LAYER 1: DOMAIN MAP
  The full map of the domain and its sub-domains.
  The relationships between sub-domains.
  Why each sub-domain is included.
  What the domain explicitly does not cover and why.

LAYER 2: CURRENT STATE
  The actual state of the domain right now.
  Versions, tools, methods, entities, positions - depending on type.
  When each piece of information was last verified.
  The sources used to verify it.

LAYER 3: EVALUATION FRAMEWORK
  How to assess anything new entering the domain.
  Scoring criteria: compatibility, complexity, lock-in risk, cost.
  A log of everything evaluated and the outcome.
  A gate requiring human approval before any change is recorded as accepted.

LAYER 4: DECISIONS AND REASONING
  Every significant decision made within this domain.
  The reasoning behind each decision.
  What was considered and rejected, and why.
  This layer prevents the model from re-litigating settled questions.

LAYER 5: MONITORING AND DRIFT DETECTION
  What sources are watched for changes in the domain.
  What constitutes a meaningful change requiring attention.
  Where detected changes are written for human review.
  Nothing is updated automatically. Everything is proposed first.

LAYER 6: LEARNING GENERATION
  Structured summaries ready for NotebookLM ingestion.
  Audio overview generation from domain content.
  Quiz, flashcard, and mind map generation.
  The Super Skill teaches the AI agent and teaches the human.

LAYER 7: PENDING APPROVALS
  Nothing changes in a Super Skill without human approval.
  All proposed changes, evaluations, and updates live here.
  The human reviews and decides.
  The model executes only after explicit approval.

LAYER X: EXPERT COUNCIL
  Real domain experts selected by the user during activation.
  Each expert assigned to a primary layer they contribute most to.
  Expert profiles contain methodology, frameworks, red lines,
  and domain-specific questions.
  Disagreements between experts surface as debates in COUNCIL.md.
  Expert positions that conflict with DECISIONS.md go to PENDING.md
  for human review.
  Claude Code surfaces expert perspectives only when genuine
  friction exists, not on routine tasks.
  NotebookLM sources per expert load into the domain notebook.
```

---

## Why Layers and Sub-Domains Matter

This is the architectural insight that separates Super Skill from every existing approach.

Every domain has sub-domains. Every sub-domain has its own context, cost of change, rate of drift, and relationship to every other sub-domain.

In a technical stack domain, changing the database layer affects authentication, API design, edge behavior, and monthly cost. A model without this map gives advice that is locally correct and systemically wrong.

In an investment portfolio domain, a change in one asset class affects liquidity, tax position, risk exposure, and rebalancing requirements across the whole portfolio. A model that sees each holding in isolation will always miss the full picture.

In a medical documentation domain, a change in regulatory language in one sub-domain affects every template, every workflow, and every compliance checkpoint connected to it.

The layer architecture forces the model to understand these connections before it acts.

When a user defines their domain and activates their Super Skill, they give the model:
- A structured map of how everything in the domain relates
- Which choices have been made at each layer
- What the real cost of changing any piece actually is

This is why a Super Skill produces advice that a Skill cannot.

A Skill knows how.
A Super Skill knows why, what else changes if you do, and whether you should.

---

## The NotebookLM Integration: The Memory Layer

A Super Skill does not only serve the AI agent.
It serves the human.

Every layer of a Super Skill can be converted into structured learning content and pushed into NotebookLM as a source. The human receives:

- Audio overviews of their own domain knowledge
- Quizzes generated from their own decisions log
- Mind maps of their own domain structure
- Flashcards generated from their own current state

This creates a feedback loop no existing system offers.

```
The Super Skill teaches the AI agent.
The Super Skill also teaches the human.
As the human learns, they make better decisions.
Better decisions improve the Super Skill.
A better Super Skill makes the AI agent more accurate.
A more accurate agent produces better outputs.
Better outputs are recorded in the decisions log.
The decisions log becomes a richer learning source.
The loop continues.
```

Knowledge does not sit in one place. It circulates.

---

## The Activation Process

A Super Skill is not configured by a developer.
It is activated by any user, through any AI agent, in under 15 minutes (with prerequisites installed).

```
Step 1  Clone or fork the Super Skill repository.
        The repository contains the layer structure, empty and ready.

Step 2  Paste the Activation Prompt into any AI agent.
        The agent reads the layer structure.
        The agent asks the minimum number of questions needed to fill it.
        Maximum 3 questions. The agent infers everything it can first.

Step 3  Answer the agent's questions.
        The agent generates the complete configured Super Skill.
        All layers populated for your specific domain and context.

Step 4  Review and commit the generated files.
        The Super Skill is live.
```

From that point, any AI agent that reads this Super Skill has full domain context.
The model does not need to be re-explained.
It does not start from zero.
It starts from a complete, current, layered understanding of exactly what you defined.

---

## Activation

All activation prompts live in ONBOARDING.md.
Clone the repository and open ONBOARDING.md to begin.

The full prompt sequence is maintained there and kept current.
The MANIFESTO describes the framework -- ONBOARDING.md runs it.

---

## The Operating Principle

```
The model proposes.
The human decides.
The Super Skill records.
The system executes.
```

This principle is structural, not optional.
It is encoded into Layer 7 of every Super Skill.
No change to any layer is accepted without passing through the human approval gate.

This is what makes a Super Skill safe to run continuously.
The model monitors, evaluates, detects, and proposes at any frequency.
The human controls what actually changes.

---

## What a Super Skill Produces

A user who activates and maintains a Super Skill will have an AI agent that:

- Knows every element of their defined domain and how those elements relate
- Knows what has been decided, why, and what was rejected
- Knows the current verified state and when it was last confirmed
- Detects drift and surfaces it for human review before it causes problems
- Evaluates new entrants against established criteria
- Generates learning content that keeps the human growing alongside the model
- Never acts on a proposed change without explicit human approval

There is no existing system that produces all of these properties together.

This is the Domain Expert the next generation of AI users needs:
Not a model that knows everything about everything.
A model that knows everything about your specific domain, your specific context,
your specific decisions, and your specific goals.

---

## Domain Types

Super Skill is universal. The layer architecture applies across all domains.

Technical domains:
- Software infrastructure and stack management
- Database architecture and data modeling
- Security and compliance frameworks
- DevOps and deployment pipelines
- Product development methodology

Non-technical domains:
- Investment portfolio management
- Legal due diligence and contract review
- Medical documentation and clinical protocols
- Marketing strategy and brand management
- Real estate analysis and acquisition
- Educational curriculum design
- Financial modeling and forecasting
- Operations and supply chain management

The structure is identical across all of these.
Only the content of each layer changes.

---

## Repository Structure for Every Super Skill

Note: paths marked with (*) are created during activation,
not present in the cloned template.

```
super-skill-[domain]/
  SUPER_SKILL_MANIFESTO.md    this document
  SKILL.md                    agent skills format entry point
  CLAUDE.md                   Claude Code specific instructions
  AGENTS.md                   instructions for any other agent
  CONTEXT.md                  layer 0: identity
  DOMAIN_MAP.md               layer 1: domain structure
  CURRENT_STATE.md            layer 2: verified current state
  EVALUATION.md               layer 3: evaluation framework
  DECISIONS.md                layer 4: decisions log
  MONITORING.md               layer 5: drift detection
  LEARNING.md                 layer 6: NotebookLM structure
  PENDING.md                  layer 7: approval queue
  experts/COUNCIL.md          layer X: expert council and debates
  experts/[name].md           individual expert profiles
  template/experts/EXPERT_TEMPLATE.md  template for expert profiles
  notebooks/                  notebooklm-ready learning files
  template/SCHEDULE.md        scheduled maintenance tasks
  scripts/                    automation for monitoring and feeding
  .claude/commands/ (*)       slash commands for Claude Code
  .claude/agents/domain-agent.md (*)  domain-specific agent definition
  experts/debates/ (*)        parallel expert debate sessions
```

---

## Starting Your First Super Skill

Clone the repository. Then follow the Bootstrap instructions
in README.md -- they will guide you through the full activation
sequence including environment checks, domain setup, and first commit.

The MANIFESTO describes the framework.
README.md runs it.

---

*Super Skill - Version 2.3.1 - April 2026*
*Authored by Asaf Dahan*
*MIT License - Fork it. Build your own.*
