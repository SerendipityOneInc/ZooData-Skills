# Track Market Change

This scenario owns one-time trend reading and explicitly requested persistent market monitoring. Use the shared stage/Gate and output contracts. It does not create a scheduler or notification from an ordinary trend question.

## Scenario boundary

Use this route when the user asks what changed in a named category, which subcategories are gaining or losing momentum, or requests a watchlist/baseline. A change signal is an observed difference or investigation priority, not proof of cause, future growth, or a launch/price decision.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| Historical trend | Resolved category ID and requested or inferable bounded period; alternatively, two supplied compatible snapshots for a one-time comparison | `market-history` observations or the supplied snapshots; compatible exact `market` snapshot and selected `market-structure-profile` only for a named current-state question | Describe observed period movement and coverage; no cause or forecast. |
| Persistent watch | Explicit monitoring intent, category IDs, cadence, thresholds, and a compatible prior baseline or authorization to initialize one | Current exact `market` rows, the saved or user-provided baseline, and `market-history` only when month-end context is requested | Classify observed changes against stated thresholds; first baseline run cannot claim a change. |

The historical stage is valid without any prior discovery or entry assessment. A one-time comparison of supplied snapshots remains a historical trend task and creates no watch state.

## Historical trend application

- Acquire the smallest bounded historical evidence that answers the question and apply the time-grain and comparison rules owned by `market-metric-semantics.md` and `evidence-protocols.md`.
- For a one-time comparison of supplied snapshots, validate their category, scope, selector, metric identity, and dates before describing change. Keep the evidence in the current task and create no persistent baseline.
- For multiple child markets, require the same bounded period and compatible evidence identity for each. A leaderboard is limited to the validated child set.
- Add current-state evidence only when the user asks a current-state question; do not let it replace the historical population defined by the metric semantics.

## Persistent monitoring

- Require the user's stated category set, cadence, and thresholds before initializing watch state. Require a notification destination only when the user requests external notifications. Do not schedule or persist state on a vague "what's trending?" request.
- For an opted-in local baseline, store only category IDs/paths, scope, sample selector, returned date, selected market fields, and threshold configuration under `~/.zoodata/market-analysis/`; do not store credentials or seller private text in the snapshot. Explain where the state lives when it is created.
- If the baseline uses the former flat market schema, a different scope or selector, or lacks the metric to compare, initialize a compatible baseline and suppress change alerts for that first run. Preserve any old snapshot separately if the user requested an audit trail; never compute across incompatible fields.
- Apply the comparison calculations owned by `evidence-protocols.md`. Treat user thresholds as alert filters, not causal explanations; without a threshold, report the measured difference without inventing severity.
- A scheduler or external notification can be configured only when the user explicitly requests that recurring action and an available platform capability exists. Do not claim that a one-time skill run will continue unattended.

## Section content requirements

In `Evidence`, show the dates, observed periods or baseline identity, and comparable metrics needed by the active stage. In `Analysis`, separate measured changes from hypotheses and identify only gaps that limit the requested comparison. In `Conclusion`, state the bounded trend or persistent-watch signal and any investigation priority; do not announce a cause, future opportunity, or operating decision without separate evidence. Render history rows and missing-period treatment only through `output-rules.md`.
