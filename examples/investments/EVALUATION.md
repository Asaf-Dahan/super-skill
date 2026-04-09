# EVALUATION.md
# Layer 3: Framework for evaluating new investment positions

## Purpose

Every new position, fund, or strategy must be evaluated against this
framework before adoption. The agent writes the full evaluation to
PENDING.md as EVAL-NNN. The owner decides.

## Criteria

| Criterion              | Weight | Notes                                       |
|------------------------|--------|---------------------------------------------|
| Allocation fit         | High   | Does it move actual closer to target?        |
| Single-name concentration | High | Does it push any name beyond 8%?            |
| Sector concentration   | High   | Does it push any sector beyond 30%?         |
| Liquidity              | High   | Can it be exited within 3 business days?    |
| Tax efficiency         | Medium | Capital gains impact, holding period        |
| Expense ratio          | Medium | Funds: 0.20% or lower preferred             |
| Currency exposure      | Medium | Stay within target FX band                  |
| Manager risk           | Low    | Active funds penalized vs index             |

## Scoring

Each criterion: 1 (poor fit) to 5 (excellent fit). Weighted total
out of 100. Anything below 70 is rejected by default.

## Past Evaluations

| ID       | Subject                  | Score | Decision  |
|----------|--------------------------|-------|-----------|
| EVAL-001 | VXUS (international ETF) | 92    | Adopted   |
| EVAL-002 | Single-stock MSFT 10%    | 48    | Rejected (concentration cap) |
| EVAL-003 | Bond ladder 3/5/7 years  | 84    | Adopted   |

## Pareto Axes

Every evaluation is plotted on two axes, not scored on a single number.

### Primary axis: Risk-adjusted return
What matters most: expected return relative to volatility and drawdown
risk over a 3-year horizon.

### Secondary axis: Liquidity and tax cost
What you pay: days to exit plus estimated capital gains tax impact
of the position.

### Tradeoff rule
Accept lower liquidity (up to 10-day exit) only if risk-adjusted return
improves by at least 1.5 percentage points annually. Never accept any
position that cannot be fully exited within 30 days.

When evaluating: plot the candidate on both axes relative to the
existing three-fund baseline. Recommend only if Pareto-dominant or
tradeoff rule permits.

## Red Flags

- Any position that pushes single-name concentration beyond 15%
- Any active fund with expense ratio above 0.50%
- Any strategy that would force a sale of a long-term holding
  with significant capital gains within the same tax year
- Any product the owner does not understand the mechanics of
