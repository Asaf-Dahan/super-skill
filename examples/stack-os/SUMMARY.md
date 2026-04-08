# stack-os -- Summary
Generated: 2026-04-06 | Verified: 2026-04-06

> Note: All names, companies, and projects in this example are fictional
> and used for instructional purposes only.

## Domain
Technical stack management for a solopreneur building two SaaS products

## Owner
Tomer Naveh -- Raincode Labs

## Current State
- Supabase: Shared instance, both products
- Cloudflare: DNS for all domains
- GitHub: Personal account, 2 private repos
- Anthropic API: Used by both products
- Frontend: React/TypeScript

## Active Decisions
- DEC-001: Single shared Supabase instance for both products (free tier)
- DEC-002: Railway for PulseLog backend only, not for GreenLedger
- DEC-003: Frontend builds and database migrations through Lovable only
- DEC-004: Free and hobby tiers until revenue justifies upgrades
- DEC-005: Make.com free tier for automation, not a custom solution

## Open Pending
- Queue clear

## Load Protocol

Read this file first. Load full files only when the task requires it.

| If task involves       | Load this file        |
|------------------------|-----------------------|
| Architecture decision  | DECISIONS.md          |
| Tool version or state  | CURRENT_STATE.md      |
| Approval action        | PENDING.md            |
| Domain structure       | DOMAIN_MAP.md         |
| Evaluation of new tool | EVALUATION.md         |
| Learning content       | LEARNING.md           |

Default: work from this summary only.

## Drift Alerts
- No active alerts