# Trend Profile Metric Semantics

Load this file **after** `keywords/trend-profile` returns and **before** making a trend judgment. Use raw `keywords/trend` only when the requested conclusion requires weekly points or fields omitted by the profile.

## Interpretation order

For every requested window, inspect `rowContext`, `status`, `emptyReason`, then each dimension's `supported`, `calculationStatus`, and `unsupportedReason`. Interpret only returned evidence in a `status=ok` row. Do not combine different windows into one label without naming which window supports each statement.

## Dimension matrix

| Metric | Meaning | Direction/evidence | Directly supports | Prohibited inference | Related raw fields |
|---|---|---|---|---|---|
| `searchDemand` | Search-demand trend over the requested fixed weekly window | Higher search count = stronger demand; positive change/slope = rising demand; higher direction consistency = more aligned period pairs | Returned demand trend/pattern, volatility level, last-period window position, and strength/consistency of direction within that window | Product lifecycle, durable long-term growth, cause of movement, conversion, future forecast, or seasonality | `trend.series[].estimateSearchCount`, `periodStartDate`, `periodEndDate` |
| `abaRank` | ABA-rank trend over the requested fixed weekly window | Lower ABA rank = better; positive rank-improvement count = improvement; positive normalized rank slope = worsening | Returned ABA-rank trend/pattern and the evidence strength within that window | Search-volume growth by itself, conversion, product rank, organic rank, or cause of ABA-rank movement | `trend.series[].abaRank`, `periodStartDate`, `periodEndDate` |

## Evidence-field matrix

| Evidence field | Meaning | Boundary |
|---|---|---|
| `firstPeriod*`, `lastPeriod*` | Endpoints of the eligible window | End-to-end change alone must not replace the returned trend classification |
| `firstToLast*`, `previousToLast*` | Long-window and latest-period changes | The latest change is short-term evidence, not proof of a durable trend |
| `normalizedSlopePerPeriod` | Direction and normalized pace across eligible periods | Interpret its returned direction; do not turn it into an absolute weekly forecast |
| `directionConsistencyRate` | Share of eligible period pairs aligned with the overall direction | Higher consistency strengthens directional evidence; it is not confidence probability |
| `alignedPeriodCount`, `eligiblePeriodPairCount` | Evidence coverage counts | Small coverage limits the conclusion even when the direction is clear |
| `bestAbaRank`, `worstAbaRank` | ABA-rank range within the window | They do not identify when or why the extremes occurred without raw series points |

## Cross-window rules

- A 4-week rise with a stable or unclear 12-week profile supports “recent strengthening without confirmed medium-term growth,” not “a growing keyword.”
- If windows disagree, report the disagreement as different time horizons. Do not average them into a stronger single conclusion.
- `status=empty` ends the corresponding window/dimension conclusion; never invent missing periods or a reason when the response does not provide one.
- Point-by-point calculations from raw weekly series are Agent-derived rather than returned trend-profile metrics; label them accordingly and state the period count.
