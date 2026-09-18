# Track Market Change

This scenario owns one-time trend reading and explicitly requested market watch comparisons. Use the shared stage/Gate and output contracts. It does not create a scheduler or notification from an ordinary trend question.

## Scenario boundary

Use this route when the user asks what changed in a named category, which subcategories are gaining or losing momentum, or requests a watchlist/baseline. A change signal is an observed difference or investigation priority, not proof of cause, future growth, or a launch/price decision.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| Historical trend | Resolved category ID and requested or inferable bounded period | `market-history` available month-end points; compatible exact `market` snapshot and selected `market-structure-profile` only for a named current-state question | Describe observed period movement and coverage; no cause or forecast. |
| Watch comparison | Explicit monitoring intent, category IDs, comparison cadence, and a compatible prior baseline or authorization to initialize one | Current exact `market` rows, the saved/user-provided baseline, and `market-history` only when month-end context is requested | Classify observed changes against stated thresholds; first baseline run cannot claim a change. |

The historical stage is valid without any prior discovery or entry assessment. A request to compare two supplied snapshots can enter watch comparison directly without creating a persistent watchlist.

## Historical trend application

- Request the smallest bounded month-end range that answers the question. Check the returned `resolvedDateFrom`, `resolvedDateTo`, point count, and absent months before calculating or summarizing movement.
- Compare the same category ID, `direct`/`subtree` scope, Top 100 selector, and metric path. Use server-provided MoM/YoY only for the point and measure that returned it; calculate a cross-point change only from compatible nonzero baselines and show dates.
- For multiple child markets, resolve IDs through `categories --parent` and use the same range and sample selector for each. A leaderboard ranks only returned comparable child rows; it is not a scan of every Amazon category.
- A current daily `market` row may explain current position but is not a substitute for a missing month-end point. Do not append it as another month-end observation.

## Explicit watch comparison

- Ask for or use the user's stated category set, cadence, thresholds, and notification destination. Do not schedule or persist state on a vague "what's trending?" request. If the user asks only for a one-time comparison, keep the baseline in the current task and make no recurring state.
- For an opted-in local baseline, store only category IDs/paths, scope, sample selector, returned date, selected market fields, and threshold configuration under `~/.zoodata/market-analysis/`; do not store credentials or seller private text in the snapshot. Explain where the state lives when it is created.
- If the baseline uses an old `sample*` market schema, a different scope or selector, or lacks the metric to compare, initialize a compatible baseline and suppress change alerts for that first run. Preserve any old snapshot separately if the user requested an audit trail; never compute across incompatible fields.
- Compare rates in percentage points and quantities in their own units. Treat thresholds as alert filters, not causal explanations. If a threshold is unspecified, report the measured difference without inventing RED/YELLOW/GREEN severity.
- A scheduler or external notification can be configured only when the user explicitly requests that recurring action and an available platform capability exists. Do not claim that a one-time skill run will continue unattended.

## Section content requirements

In `Evidence`, show the actual dates, available points or baseline identity, and comparable metrics. In `Analysis`, separate measured changes from hypotheses and note missing months or incompatible fields. In `Conclusion`, state the bounded trend or watch signal and any investigation priority; do not announce a cause, future opportunity, or operating decision without separate evidence.
