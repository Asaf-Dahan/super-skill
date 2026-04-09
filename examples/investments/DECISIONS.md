# DECISIONS.md
# Layer 4: Decisions log and reasoning

## Purpose

This file records every significant allocation and strategy decision.
When a decision is here, it is settled. The agent does not propose
reversing it without new information.

## Decision Log

### DEC-001: Three-fund core (VTI / VXUS / BND) as the base allocation
Date: 2024-11-15
Decision: 60% of the portfolio held in three Vanguard ETFs covering US
equities (VTI), international equities (VXUS), and US bonds (BND).
Reasoning: Low cost, broad diversification, no manager risk, easy to
rebalance. The remaining 40% is reserved for specific themes, REITs,
and cash.
Alternatives Rejected: Active funds (cost), single-name only (concentration),
target-date funds (lower customization).
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]
Impact: Sets the floor of the portfolio. Any new position must justify
itself relative to this baseline.

### DEC-002: Hard 15% cap on single-name exposure
Date: 2025-02-08
Decision: No single ticker may exceed 15% of total portfolio value.
Reasoning: Single-name risk is the most painful and most preventable
form of concentration risk. 15% leaves room for high-conviction names
without portfolio-destroying exposure.
Alternatives Rejected: 10% (too restrictive for conviction), 20% (too loose),
no cap (unacceptable).
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]
Impact: Drives the EVAL-002 rejection. Any future single-name addition
must check the current concentration before purchase.

### DEC-003: Rebalance triggered by drift, not by calendar
Date: 2025-08-22
Decision: Rebalance any time an asset class drifts more than 5% from
its target allocation. Do not rebalance on a fixed schedule.
Reasoning: Calendar rebalancing creates unnecessary tax events.
Drift-based rebalancing only acts when there is a real need.
Alternatives Rejected: Quarterly (forces unneeded trades), annual
(allows excessive drift), never (defeats the purpose of having targets).
Tested: [Not recorded -- pre-v2.7]
Held constant: [Not recorded -- pre-v2.7]
Confounds: [Not recorded -- pre-v2.7]
Impact: Requires monthly drift checks (see MONITORING.md).
