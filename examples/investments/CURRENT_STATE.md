# CURRENT_STATE.md
# Layer 2: Verified current state of the portfolio

Last verified: 2026-04-06

## Asset Allocation (Target vs Actual)

| Asset Class      | Target | Actual | Drift |
|------------------|--------|--------|-------|
| US Equities      | 40%    | 42%    | +2%   |
| International    | 20%    | 18%    | -2%   |
| Bonds            | 25%    | 26%    | +1%   |
| REITs            | 5%     | 4%     | -1%   |
| Cash             | 10%    | 10%    | 0%    |

Drift threshold: rebalance triggered when any class drifts beyond +/- 5%.
Current drift is within tolerance.

## Holdings

| Ticker | Class           | Position    | Cost Basis | Status |
|--------|-----------------|-------------|------------|--------|
| VTI    | US Equities     | 30%         | n/a        | Hold   |
| VXUS   | International   | 18%         | n/a        | Hold   |
| BND    | Bonds           | 26%         | n/a        | Hold   |
| VNQ    | REITs           | 4%          | n/a        | Hold   |
| AAPL   | US Equities     | 6%          | logged     | Hold   |
| MSFT   | US Equities     | 6%          | logged     | Hold   |
| Cash   | Money Market    | 10%         | n/a        | Reserve |

(Specific dollar amounts intentionally omitted in this example.)

## Liquidity

- Money market reserve covers 12 months of essential expenses
- Bond ladder partially staggered (3-year, 5-year, 7-year rungs)
- No locked positions; all holdings can be liquidated within 3 business days

## Risk Posture

- Single-name concentration: AAPL + MSFT = 12% of portfolio (cap: 15%)
- Sector concentration: Tech weight = 24% (cap: 30%)
- Currency exposure: 82% USD, 18% non-USD (within target band)

## Known Gaps

- No tax-loss harvesting automation in place
- No documented rebalancing cadence (currently ad-hoc)
- No exposure tracking for fund overlap (e.g., VTI vs AAPL/MSFT double counting)

## Sources Used to Verify

- Brokerage statement (2026-04-01)
- ETF fact sheets (Vanguard)
- Personal tracking spreadsheet
