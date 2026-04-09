# DECISIONS.md
# Layer 4: Decisions log with reasoning and rejected alternatives

## How to Use This File

Every significant technical stack decision is recorded here with its
reasoning. This prevents the model from re-litigating settled questions.

Format: DEC-NNN: [short title]
Each entry includes: the decision, the reasoning, what was considered
and rejected, the date, and which products are affected.

## Decisions

### DEC-001: Single shared DBHost instance for both products
Date: 2026-03-15
Products affected: GreenLedger, PulseLog
Decision: Both products share one DBHost instance on the free tier,
with separate schemas for product-specific data and shared auth tables.
Reasoning: A solo operator managing two free-tier instances doubles the
operational surface for monitoring, backups, and auth configuration.
One instance keeps auth unified and reduces management overhead. The
free tier has sufficient capacity for both products at current scale.
Rejected alternative: Separate DBHost instances per product -- higher
operational overhead with no benefit at current scale. Can revisit if
one product outgrows free tier limits independently.
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]

### DEC-002: AppHost for PulseLog backend, not for GreenLedger
Date: 2026-03-15
Products affected: PulseLog
Decision: AppHost hosts the PulseLog Python backend. GreenLedger runs
entirely on UIBuilder and DBHost Edge Functions with no separate server.
Reasoning: GreenLedger is a React app that can run serverlessly through
DBHost Edge Functions for any backend logic. PulseLog requires a
persistent Python process for background monitoring jobs and incident
processing that Edge Functions cannot support. AppHost Hobby at $5/month
is the simplest option for a containerized Python service.
Rejected alternative: Running PulseLog backend on a local machine --
no reliability guarantees, no public API access, no persistence.
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]

### DEC-003: Frontend builds and database migrations through UIBuilder only
Date: 2026-03-18
Products affected: GreenLedger
Decision: All frontend code generation and DBHost schema migrations
are handled exclusively through UIBuilder. No other tool generates
frontend code or runs database migrations.
Reasoning: UIBuilder has a tightly integrated pipeline with DBHost that
handles migration safety, schema validation, and deployment in one flow.
Allowing migrations from multiple sources risks schema drift, conflicts,
and failed deployments. A single source of truth for schema changes
eliminates an entire category of operational risk.
Rejected alternative: Generating migrations from Claude Code or manual
SQL -- too risky without the safety checks that UIBuilder provides.
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]

### DEC-004: Free and hobby tiers until revenue justifies upgrades
Date: 2026-03-18
Products affected: All
Decision: Stay on free or lowest-cost tiers for every service until
a free tier limit is actually reached or product revenue covers the cost.
Reasoning: A bootstrapped solo operation cannot afford premature
infrastructure spend. Every dollar spent on higher tiers before they
are needed is a dollar not spent building the product. Upgrade triggers
are explicit: a tier limit is reached, or monthly revenue exceeds
the cost of the upgrade by at least 3x.
Rejected alternative: Starting on paid tiers for reliability -- the
current scale does not justify the cost.
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]

### DEC-005: Make.com free tier for automation, not a custom solution
Date: 2026-03-22
Products affected: All
Decision: Use Make.com on the free tier for all cross-service automation.
Do not build custom webhook handlers or cron jobs.
Reasoning: Make.com provides a visual, no-code way to connect Stripe
webhooks, DBHost triggers, and Resend emails without writing and
maintaining custom code. The free tier allows 1,000 operations per
month, which is sufficient for current volume. Building custom
automation would add code to maintain and debug -- the opposite of
what a solo operator needs.
Rejected alternative: Custom Node.js or Python scripts for automation --
more flexible but adds maintenance burden and deployment complexity.
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]
