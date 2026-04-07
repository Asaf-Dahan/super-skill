# CURRENT_STATE.md
# Layer 2: Verified current state of all services and tools

Last verified: 2026-04-06

## Shared Services

| Service        | Tier/Plan  | Status | Notes                          |
|----------------|------------|--------|--------------------------------|
| Supabase       | Free       | Active | Shared instance, both products |
| Cloudflare     | Free       | Active | DNS for all domains            |
| GitHub         | Free       | Active | Personal account, 2 private repos |
| Anthropic API  | Pay-as-go  | Active | Used by both products          |

## GreenLedger

| Component      | Tier/Plan   | Status     | Notes                        |
|----------------|-------------|------------|------------------------------|
| Frontend       | Lovable     | Pre-launch | React/TypeScript             |
| Supabase       | Free (shared) | Active   | DB, Auth, Edge Functions     |
| Stripe         | Test mode   | Pre-launch | 2 subscription tiers configured |
| Resend         | Free        | Active     | 3 email templates, domain verified |

Product status: Pre-launch. Building toward first public release.

## PulseLog

| Component      | Tier/Plan        | Status  | Notes                      |
|----------------|------------------|---------|----------------------------|
| Backend        | Railway Hobby    | Active  | Python web server + worker |
| Admin UI       | Streamlit        | Dev only | Runs locally               |
| Supabase       | Free (shared)    | Active  | Persistent storage         |

Product status: Running. Operational for early users.

## Automation

| Service   | Tier/Plan | Status | Notes                          |
|-----------|-----------|--------|--------------------------------|
| Make.com  | Free      | Active | 3 scenarios, within op limits  |

## Monthly Cost Summary

| Service        | Monthly Cost |
|----------------|-------------|
| Supabase       | $0 (free)   |
| Cloudflare     | $0 (free)   |
| GitHub         | $0 (free)   |
| Anthropic API  | ~$12        |
| Railway        | ~$5         |
| Stripe         | $0 (test)   |
| Resend         | $0 (free)   |
| Make.com       | $0 (free)   |
| **Total**      | **~$17/mo** |

## Known Gaps

- No automated database backup beyond Supabase built-in daily snapshots
- No uptime monitoring for public-facing endpoints
- No error alerting pipeline -- failures are discovered manually
- No load testing performed on either product
- No disaster recovery plan documented

## Sources Used to Verify

- Supabase dashboard
- Railway dashboard
- Cloudflare dashboard
- Stripe dashboard
- Make.com dashboard
- GitHub repository list
- Anthropic Console
- Resend dashboard
