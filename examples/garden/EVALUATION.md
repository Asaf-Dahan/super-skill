# EVALUATION.md
# Layer 3: Framework for evaluating new plants, methods, or tools

## Purpose

Every new plant, technique, tool, or amendment must be evaluated
against this framework before adoption. The agent writes the full
evaluation to PENDING.md as EVAL-NNN. The owner decides.

## Criteria

| Criterion              | Weight | Notes                                    |
|------------------------|--------|------------------------------------------|
| Water demand           | High   | Must fit dry-summer constraint            |
| Soil compatibility     | High   | Must work with current pH and texture     |
| Crop rotation impact   | High   | Cannot conflict with rotation history     |
| Pest pressure          | Medium | Risk of attracting new pests              |
| Yield per square foot  | Medium | Space is limited                          |
| Time to harvest        | Medium | Must fit seasonal calendar                |
| Cost                   | Low    | Most amendments are low-cost              |

## Scoring

Each criterion: 1 (poor fit) to 5 (excellent fit). Weighted total
out of 100. Anything below 60 is rejected by default.

## Past Evaluations

| ID       | Subject                | Score | Decision  |
|----------|------------------------|-------|-----------|
| EVAL-001 | Drip emitters (1 GPH)  | 88    | Adopted   |
| EVAL-002 | Sweet potatoes         | 52    | Rejected (water demand too high) |
| EVAL-003 | Worm castings (bulk)   | 78    | Adopted   |

## Pareto Axes

Every evaluation is plotted on two axes, not scored on a single number.

### Primary axis: Yield per square foot
What matters most: how much food a plant or method produces per unit
of limited garden space.

### Secondary axis: Water demand
What you pay: total water consumption in gallons per week during
the dry season.

### Tradeoff rule
Accept up to 50% higher water demand only if yield per square foot
doubles or better. Never accept any plant that requires daily watering
in summer regardless of yield.

When evaluating: plot the candidate on both axes relative to current
baseline crops. Recommend only if Pareto-dominant or tradeoff rule permits.

## Red Flags

- Anything that requires daily watering in summer
- Anything in the same family as current crop on the same bed
  (rotation conflict)
- Any chemical pesticide or synthetic fertilizer
