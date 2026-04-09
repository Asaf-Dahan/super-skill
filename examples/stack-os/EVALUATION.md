# EVALUATION.md
# Layer 3: Evaluation framework for assessing new tools and services

## Purpose

Every new tool, service, or method that enters this domain must be evaluated
against the existing stack before adoption. This framework ensures that
nothing is added impulsively and that every change is assessed for cost,
complexity, and cross-product impact.

## Evaluation Criteria

### C1: Stack Compatibility (weight: critical)
  Does this integrate with the existing shared services layer?
  Does it work with DBHost, CDNLayer, GitHub, and the current deployment model?
  Score 1-5:
    5 = drops in with no configuration changes
    4 = minor configuration required
    3 = moderate integration work
    2 = significant rework needed
    1 = incompatible with current architecture

### C2: Solo Operator Complexity (weight: critical)
  Can one person set it up, maintain it, and debug it without specialized expertise?
  Does it add a new language, paradigm, or operational burden?
  Score 1-5:
    5 = trivial to operate, good documentation
    4 = manageable with some learning
    3 = moderate learning curve, acceptable for the value
    2 = steep learning curve or frequent maintenance
    1 = requires dedicated operations knowledge

### C3: Cost at Scale (weight: high)
  What does this cost at free tier? At 1,000 users? At 10,000 users?
  Is pricing predictable or usage-based with surprise potential?
  Score 1-5:
    5 = free or near-free at current scale, predictable growth
    4 = affordable with clear pricing tiers
    3 = moderate cost, some unpredictability
    2 = expensive or difficult to forecast
    1 = prohibitively expensive at modest scale

### C4: Lock-in Risk (weight: high)
  How hard is it to leave this service once adopted?
  Are data exports available? Is the API standard or proprietary?
  Score 1-5:
    5 = fully portable, standard protocols, easy data export
    4 = minor friction to migrate
    3 = moderate effort, some proprietary elements
    2 = significant migration effort
    1 = effectively locked in, no practical exit path

### C5: Cross-Product Impact (weight: medium)
  Does this affect one product or both?
  Does it touch shared services?
  Score 1-5:
    5 = isolated to one product, no shared impact
    4 = minor shared impact, manageable
    3 = affects shared services, requires careful rollout
    2 = significant cross-product dependencies
    1 = high risk of cascading failures across products

### C6: Time to Value (weight: medium)
  How quickly can this be set up and delivering value?
  Is there a working free tier or trial to validate before committing?
  Score 1-5:
    5 = working in under an hour with free tier
    4 = working in a day
    3 = working in a week
    2 = multi-week setup or onboarding
    1 = requires months of integration work

## Scoring Guide

Minimum threshold for adoption consideration:
  Must score 4 or higher on the top two criteria (C1 + C2)

Recommended threshold for adoption:
  Average score of 3.5 or higher across all six criteria

Any score of 1 on any criterion is a blocking concern that must be
explicitly justified before proceeding.

## Evaluation Process

1. Agent identifies a candidate tool or service
2. Agent writes a full evaluation to PENDING.md using the criteria above
3. Agent does NOT recommend adoption -- only presents the scored analysis
4. The owner reviews, asks questions, and decides: adopt, reject, or defer
5. Outcome is recorded in the Evaluation Log below

## Pareto Axes

Every evaluation is plotted on two axes, not scored on a single number.

### Primary axis: Reliability at current scale
What matters most: uptime, data integrity, and operational simplicity
for a solo operator running two products.

### Secondary axis: Monthly cost
What you pay: total dollar cost per month including all usage-based
charges at current traffic levels.

### Tradeoff rule
Accept up to $10/month increase only if it eliminates a known
reliability risk or removes a manual operational step. Never exceed
$50/month total stack cost until monthly revenue covers 3x the spend.

When evaluating: plot the candidate on both axes relative to the
current tool it would replace. Recommend only if Pareto-dominant or
tradeoff rule permits.

## Evaluation Log

No evaluations completed yet.
