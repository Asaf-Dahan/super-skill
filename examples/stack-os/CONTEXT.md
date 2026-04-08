# CONTEXT.md
# Layer 0: Identity, principles, and scope

> Note: All names, companies, and projects in this example are fictional
> and used for instructional purposes only.

## Domain

Technical stack management for a solopreneur building two SaaS products
on a shared services layer (Supabase, Cloudflare, GitHub, Anthropic API)
with product-specific infrastructure per project.

## Owner

Tomer Naveh -- Raincode Labs
Solopreneur. Builds and operates all infrastructure personally.
No team. Every decision is made and executed by one person.

## Purpose

Maintain a living, verified map of the entire technical stack so that
every AI agent session starts with full context -- no re-explaining,
no wrong assumptions, no guessing at versions, tiers, or architecture.

Every technology decision must be informed by current state, cross-product
impact, and cost constraints appropriate for a bootstrapped solo operation.

## Products

GreenLedger -- a subscription-based sustainability reporting tool for
small businesses. React/TypeScript frontend built with Lovable, Supabase
backend, Stripe billing, Resend for transactional email.

PulseLog -- a lightweight uptime and incident logging dashboard for
indie developers. Python backend on Railway, Streamlit admin interface,
Supabase for persistent storage.

## Goals

- Know exactly what is running, where, on which tier, at all times
- Evaluate new tools or services against the existing stack before adoption
- Detect when dependencies drift, deprecate, or introduce breaking changes
- Prevent changes that break the shared-services boundary between products
- Keep monthly costs predictable and within solopreneur budget constraints

## Operating Principles

- No production changes without explicit approval from the owner
- Shared services (Supabase Auth, Cloudflare, GitHub) require cross-product
  impact analysis before any change
- Free and hobby tiers until revenue justifies upgrades -- no premature scaling
- Frontend builds and database migrations are handled by Lovable --
  Claude Code does not generate frontend code or run migration commands
- Every proposed change goes to PENDING.md first

## Scope Boundaries

This Super Skill covers:
- All infrastructure, hosting, and cloud services for GreenLedger and PulseLog
- CI/CD, DNS, CDN, email, payments, and automation services
- The Anthropic API integration layer shared by both products
- Cost and tier tracking across all services

This Super Skill does NOT cover:
- Application-level code, features, or UI design
- Business strategy, pricing, or go-to-market planning
- Make.com scenario design (covered by a separate Super Skill if needed)
- Supabase schema design and RLS policies (covered separately if needed)
