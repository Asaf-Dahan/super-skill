# LEARNING.md
# Layer 6: NotebookLM learning module plan

## NotebookLM Notebook
Name: Stack Management -- Super Skill
Notebook ID: [Set in .env file as NOTEBOOK_ID]

## Learning Modules Planned

### Module 1: DBHost Free Tier Limits and Upgrade Paths
Priority: high
Purpose: Understand exactly where the free tier walls are for database
size, auth users, edge function invocations, and bandwidth. Know what
the upgrade path looks like and what it costs before it becomes urgent.
Status: planned

### Module 2: Anthropic API Cost Optimization
Priority: high
Purpose: Understand model selection tradeoffs (Haiku vs Sonnet vs Opus)
for different use cases across both products. How to estimate and control
monthly spend as usage grows. When to use each model tier.
Status: planned

### Module 3: AppHost Hobby Plan -- Constraints and Scaling Options
Priority: medium
Purpose: Know the resource limits, sleep behavior, and scaling options
on the AppHost Hobby plan. What happens when background jobs exceed
memory or CPU limits. When to consider upgrading.
Status: planned

### Module 4: SaaS Pre-Launch Infrastructure Checklist
Priority: high
Purpose: A complete checklist of infrastructure requirements before
accepting paying users. Covers payment processing, email deliverability,
SSL configuration, security headers, error handling, and monitoring.
Status: planned

### Module 5: Backup and Disaster Recovery for Solo Operators
Priority: medium
Purpose: Practical backup strategies when running on free and hobby
tiers. What can be recovered automatically, what requires manual steps,
and how to restore from a complete service failure.
Status: planned

### Module 6: Cross-Service Failure Scenarios
Priority: medium
Purpose: Map what happens when each shared service experiences an outage.
Which products are affected, what breaks visibly for users, what keeps
working, and what manual workarounds exist for each scenario.
Status: planned

## How to Generate a Module
Use Prompt 4 from ONBOARDING.md with any topic from this list.
The output goes to notebooks/[topic]-learning.md
Then run: python scripts/feed_notebook.py

## How to Generate Audio
python scripts/generate_learning.py audio

## How to Generate a Quiz
python scripts/generate_learning.py quiz

## How to Generate a Mind Map
python scripts/generate_learning.py mindmap
