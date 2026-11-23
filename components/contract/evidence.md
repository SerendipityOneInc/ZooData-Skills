# Data scope and conclusion support

## Preserve measurement scope

1. When extracting or grouping data, retain the object identifiers and baseline indicators required by the task, together with source, marketplace, period, units, denominators, sample boundaries and filters.
2. Before a numerical consistency check, match object scope and grain, population and sample selection, business dates and measurement windows, metric definitions, units and denominators. For Top-N summaries, also match the ranking metric and cutoff. If compatibility differs or is unestablished, report the observations separately rather than treating their difference as a data conflict.
3. A sum or local ranking of partial records describes only that sample, not a population total or global ranking. For a server-provided Top N, retain the actual query conditions and ordering basis.
4. An empty result means no matches under the query conditions; do not extend it to zero market demand, no competition or no change.

## Handle missing values and derived calculations

1. Preserve returned values and distinguish zero, false, null, absent fields and unreturned periods. Use unknown only for information not obtained; check the original response before treating locally unread or hidden fields as missing. Do not fill missing values with zero.
2. Use acquired numeric inputs for calculations and rankings, retaining missing-state labels. Mark a calculation not computable if no valid inputs remain or its denominator is zero or unavailable; exclude missing sort values from numeric rankings.
3. To aggregate a ratio, sum its corresponding numerators and denominators before dividing rather than averaging row ratios. Retain the inputs and formula for each derived calculation.
4. Calculate and label absolute differences, relative changes and percentage-point changes separately.
5. Preserve time-series gaps without interpolation. Label incomplete periods with their actual coverage rather than treating them as completed periods.

## Establish supported data findings

1. Use successful ZooData responses as the factual basis under the interface definitions. Never ask sellers to confirm, verify or provide proof for ZooData-returned data.
2. For apparently contradictory observations, compare objects, periods, units and statistical scope. Explain differing scopes separately. If the contradiction remains, retain the values, describe the specific inconsistency and seek supporting evidence through the current task's methods within the query limits; an unexplained relationship does not make a returned value unknown.
3. Tie each finding to returned observations or an explicit calculation. Do not add unreturned product attributes, buyer behavior or scoring formulas.
4. Interpret returned classifications within their measured window, scope and supporting observations; do not turn them into certain future outcomes.
5. A causal claim requires a measurement or comparison supporting that relationship. Co-movement or chronology alone supports an association, not a certain cause.
