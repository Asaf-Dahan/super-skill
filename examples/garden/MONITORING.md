# MONITORING.md
# Layer 5: Drift detection sources

## Purpose

The garden state changes constantly. This file lists what to watch
and how often to check it. Detected changes go to PENDING.md as
DRIFT-NNN. Nothing is updated automatically.

## Sources

| Source                | What to watch                       | Frequency  |
|-----------------------|-------------------------------------|------------|
| Visual bed inspection | Pest, disease, growth stage         | Daily      |
| Soil moisture (probe) | Top 4 inches per bed                | Every 2 days |
| Weather forecast      | Frost, heatwave, rain in next 5 days | Daily      |
| Rain barrel level     | Refill / overflow                   | After every rain |
| pH meter reading      | All active beds                     | Monthly    |
| Compost bin temperature | 110-140 F = active                | Weekly     |

## What Constitutes Drift

- Any pest population doubling within 7 days
- Soil moisture below 30% in any active bed
- pH outside 6.0-7.0 range in any active bed
- Compost temperature below 100 F (stalled)
- Forecast frost when frost-tender crops are in beds

## How Drift Is Reported

Each detected change becomes a DRIFT-NNN entry in PENDING.md with:
- What changed
- When it was detected
- The source of the observation
- Proposed action (the owner decides)
