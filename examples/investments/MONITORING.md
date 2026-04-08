# MONITORING.md
# Layer 5: Drift detection sources

## Purpose

Markets move every day. This file lists what to watch and how often.
Detected changes go to PENDING.md as DRIFT-NNN. Nothing is updated
automatically.

## Sources

| Source                | What to watch                          | Frequency  |
|-----------------------|----------------------------------------|------------|
| Brokerage statement   | Position values and balances           | Weekly     |
| Allocation drift      | Each asset class vs target             | Monthly    |
| Sector concentration  | Tech / Financials / Healthcare / Energy | Monthly   |
| Single-name concentration | Each individual ticker             | Monthly    |
| ETF prospectus updates | Vanguard fund changes                 | Quarterly  |
| Tax law changes       | Capital gains brackets and rules       | Annually   |
| FX rates              | USD vs basket of holding currencies    | Weekly     |

## What Constitutes Drift

- Any asset class beyond +/- 5% of target (triggers rebalance review per DEC-003)
- Any single name beyond 12% (early warning, 3% before the cap)
- Any sector beyond 28% (early warning, 2% before the cap)
- Any FX exposure beyond +/- 5% of target band
- Any change to a fund's expense ratio
- Any tax law change that affects capital gains treatment

## How Drift Is Reported

Each detected change becomes a DRIFT-NNN entry in PENDING.md with:
- What changed
- When it was detected
- The source of the observation
- Proposed action (the owner decides)
