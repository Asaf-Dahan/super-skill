# MONITORING.md
# Layer 5: Drift detection sources and alert thresholds

## What Drift Means in This Domain

Technical stack drift occurs when:
- A service changes its pricing, tiers, or free tier limits
- A dependency releases a breaking version update
- A service announces deprecation or end-of-life
- A free tier approaches its usage limits
- A new AI model is released that changes cost or quality tradeoffs
- A platform (frontend builder, database host, app host) changes its behavior

This domain moves fast. Pricing changes can happen monthly. Breaking
updates can land without warning. Free tier limits can be reduced.

## Sources to Watch

### Source 1: Database Host Changelog
Type: website
URL: https://db.example.com/changelog
Check frequency: weekly
What to look for: free tier limit changes, auth breaking changes,
edge function runtime updates, new features that affect architecture

### Source 2: App Host Changelog
Type: website
URL: https://api.example.com/changelog
Check frequency: weekly
What to look for: hobby plan changes, pricing updates, Python runtime
version changes, deployment pipeline changes

### Source 3: AI Provider API Updates
Type: website
URL: https://ai-provider.example.com/docs/models
Check frequency: weekly
What to look for: new model releases, deprecation notices, pricing
changes, rate limit adjustments, API breaking changes

### Source 4: CDN Provider Blog
Type: website
URL: https://cdn.example.com/blog
Check frequency: monthly
What to look for: free tier changes, DNS feature updates, CDN behavior
changes, security features relevant to both products

### Source 5: Payment Processor Changelog
Type: website
URL: https://payments.example.com/docs/changelog
Check frequency: monthly (increase to weekly before product launch)
What to look for: API version changes, pricing model updates, webhook
behavior changes, test mode limitations

### Source 6: Frontend Builder Updates
Type: website
URL: https://app.example.com
Check frequency: weekly
What to look for: build pipeline changes, database integration updates,
deployment behavior changes, new capabilities

### Source 7: Automation Platform Release Log
Type: website
URL: https://automation.example.com/release-log
Check frequency: monthly
What to look for: free tier changes, module deprecations, rate limit
adjustments, new integrations relevant to the stack

### Source 8: Email Service Changelog
Type: website
URL: https://email.example.com/changelog
Check frequency: monthly
What to look for: free tier limit changes, API changes, deliverability
updates, domain verification requirements

## Drift Alert Threshold

Write to PENDING.md when:
- Any pricing or tier change affects current monthly cost
- Any breaking change affects a service currently in use
- Any deprecation notice has a deadline within 6 months
- Any free tier usage exceeds 75% of its limit
- A new AI model could reduce cost or improve quality significantly
- Any change affects more than one pillar (cross-product impact)

## Drift Log

No drift detected yet. This log will be populated as monitoring runs.
