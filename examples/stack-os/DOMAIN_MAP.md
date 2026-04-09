# DOMAIN_MAP.md
# Layer 1: Domain structure and sub-domain relationships

## Architecture Overview

Two SaaS products share a common services layer. Each product also has
infrastructure specific to its own stack. Automation connects both
products to external services through Make.com.

```
                    +------------------+
                    |  Shared Services |
                    |  (both products) |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
     +--------+--------+          +--------+--------+
     |   GreenLedger   |          |    PulseLog     |
     | (product-specific)         | (product-specific)
     +-----------------+          +-----------------+
```

## Pillar 1: Shared Services

These services are used by both GreenLedger and PulseLog.
Any change here requires cross-product impact analysis.

### DBHost (shared instance)
  Role: authentication, user management, shared reference data
  Used by: GreenLedger (primary database), PulseLog (persistent storage)
  Dependency level: critical -- both products depend on this instance
  Change cost: high -- affects auth flows in both products

### CDNLayer
  Role: DNS, CDN, DDoS protection, edge caching
  Used by: both products (custom domains)
  Dependency level: critical -- all traffic routes through CDNLayer
  Change cost: medium -- DNS changes propagate within hours

### GitHub
  Role: source control, CI/CD via GitHub Actions
  Used by: both products (separate repositories)
  Dependency level: critical -- all code and deployment pipelines live here
  Change cost: low for per-repo changes, high for org-level changes

### Anthropic API
  Role: AI features in both products (Claude integration)
  Used by: GreenLedger (report generation), PulseLog (incident summaries)
  Dependency level: high -- core feature differentiator
  Change cost: medium -- API version changes may affect prompts

## Pillar 2: GreenLedger (Product A)

### UIBuilder
  Role: frontend development platform (React/TypeScript)
  Dependency level: high -- all UI and DBHost migrations run through UIBuilder
  Change cost: high -- switching frontend tooling would require full rebuild

### Stripe
  Role: subscription billing, payment processing
  Dependency level: critical -- all revenue flows through Stripe
  Change cost: very high -- payment migration is complex and risky

### Resend
  Role: transactional email (receipts, onboarding, alerts)
  Dependency level: medium -- email is important but replaceable
  Change cost: low -- standard SMTP-compatible API

## Pillar 3: PulseLog (Product B)

### AppHost
  Role: Python backend hosting (API server, background jobs)
  Dependency level: critical -- the only compute platform for PulseLog
  Change cost: medium -- containerized, can move to another PaaS

### Streamlit
  Role: internal admin dashboard
  Dependency level: low -- admin-only, not user-facing
  Change cost: low -- could be replaced with any dashboard framework

## Pillar 4: Automation

### Make.com
  Role: workflow automation connecting services across both products
  Scenarios: Stripe webhook processing, DBHost event triggers,
  Resend email sequences, monitoring alert routing
  Dependency level: medium -- automations are convenient but not critical path
  Change cost: medium -- scenarios would need to be rebuilt on a new platform

## Cross-Pillar Dependencies

| If this changes...       | These are affected...                        |
|--------------------------|----------------------------------------------|
| DBHost auth config     | GreenLedger login, PulseLog login, Make.com triggers |
| CDNLayer DNS           | Both product domains, SSL certificates        |
| GitHub Actions workflow  | Deploy pipeline for the affected product only |
| Anthropic API version    | AI features in both products                  |
| Stripe webhook format    | Make.com billing scenarios, GreenLedger billing |
| AppHost region or plan   | PulseLog API latency, background job capacity |
| Make.com scenario change | Downstream service affected by that scenario  |

## Dependency Direction

Shared services flow down into products. Products do not depend on
each other directly. Automation (Make.com) sits alongside and connects
to both shared services and product-specific services.

```
  Shared Services (DBHost, CDNLayer, GitHub, Anthropic)
         |                    |
    GreenLedger           PulseLog
  (UIBuilder, Stripe,     (AppHost, Streamlit)
   Resend)
         \                   /
          --- Make.com ------
```
