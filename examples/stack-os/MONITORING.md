# MONITORING.md
# Layer 5: Drift detection sources and alert thresholds

## What Drift Means in This Domain

Technical stack drift occurs when:
- A service changes its pricing, tiers, or free tier limits
- A dependency releases a breaking version update
- A service announces deprecation or end-of-life
- A free tier approaches its usage limits
- A new Anthropic model is released that changes cost or quality tradeoffs
- A platform (Lovable, Supabase, Railway) changes its behavior

This domain moves fast. Pricing changes can happen monthly. Breaking
updates can land without warning. Free tier limits can be reduced.

## Sources to Watch

### Source 1: Supabase Changelog
Type: website
URL: https://supabase.com/changelog
Check frequency: weekly
What to look for: free tier limit changes, auth breaking changes,
edge function runtime updates, new features that affect architecture

### Source 2: Railway Changelog
Type: website
URL: https://railway.app/changelog
Check frequency: weekly
What to look for: hobby plan changes, pricing updates, Python runtime
version changes, deployment pipeline changes

### Source 3: Anthropic API Updates
Type: website
URL: https://docs.anthropic.com/en/docs/about-claude/models
Check frequency: weekly
What to look for: new model releases, deprecation notices, pricing
changes, rate limit adjustments, API breaking changes

### Source 4: Cloudflare Blog
Type: website
URL: https://blog.cloudflare.com
Check frequency: monthly
What to look for: free tier changes, DNS feature updates, CDN behavior
changes, security features relevant to both products

### Source 5: Stripe Changelog
Type: website
URL: https://stripe.com/docs/changelog
Check frequency: monthly (increase to weekly before GreenLedger launch)
What to look for: API version changes, pricing model updates, webhook
behavior changes, test mode limitations

### Source 6: Lovable Platform Updates
Type: website
URL: https://lovable.dev
Check frequency: weekly
What to look for: build pipeline changes, Supabase integration updates,
deployment behavior changes, new capabilities

### Source 7: Make.com Release Log
Type: website
URL: https://www.make.com/en/release-log
Check frequency: monthly
What to look for: free tier changes, module deprecations, rate limit
adjustments, new integrations relevant to the stack

### Source 8: Resend Changelog
Type: website
URL: https://resend.com/changelog
Check frequency: monthly
What to look for: free tier limit changes, API changes, deliverability
updates, domain verification requirements

## Drift Alert Threshold

Write to PENDING.md when:
- Any pricing or tier change affects current monthly cost
- Any breaking change affects a service currently in use
- Any deprecation notice has a deadline within 6 months
- Any free tier usage exceeds 75% of its limit
- A new Anthropic model could reduce cost or improve quality significantly
- Any change affects more than one pillar (cross-product impact)

## Drift Log

No drift detected yet. This log will be populated as monitoring runs.
