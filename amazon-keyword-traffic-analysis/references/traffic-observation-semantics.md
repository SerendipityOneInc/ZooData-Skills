# Traffic Observation Field Semantics

Load this file after retrieving `product-traffic-terms`, `competitor-product-keywords`, `product-traffic-terms-timeline`, or `product-traffic-terms-overview`. It owns the meaning and inference limits of their returned traffic, placement, coverage, timeline, and aggregate-observation fields.

## Traffic-term rows

- `trafficShare` is the row's sampled share within the returned ASIN traffic period, not exact Amazon share of voice.
- `estimateImpressionPoint` and the ORG/SP/SB/SBV/SPR fields describe observed placement exposure. They do not establish clicks, conversion, sales attribution, or profitability.
- When the shared ranked-detail protocol verifies `sortBy`, `sortOrder`, page, page size, filters, identity, and period, returned traffic-term rows may be described as Top N by that exact field and direction. `Top N by trafficShare descending` ranks the endpoint's sampled row-level traffic share only; it is not a generic Top N keyword-value or conversion claim.
- A sponsored-only row or one selected page of returned rows does not establish overall advertising dependence, weak organic relevance, algorithmic recognition, or organic improvement potential.
- `daysCoverageRate`, `observationCount`, and returned period boundaries describe observation support. Low coverage limits confidence rather than proving instability; do not call coverage full, complete, or stable unless those fields and the resolved period directly establish it.

## Timeline observations

- `asinSnapshot` is tied to the series date. Traffic, placement, and `adActivity` belong to the returned weekly period. `keywordMetrics` belongs to its own weekly `metricWindow`; do not merge these grains into one timestamp.
- Compare like fields across aligned returned periods. One observation supports only a point-in-time description; at least two comparable observations are required to describe directional movement.
- `adActivity` counts and coverage describe observed ad participation. They do not establish CPC, auction competition, spend posture, ROI, or campaign intent.
- Product, demand, placement, traffic, and ad-activity changes are observations. Time-aligned co-movement can narrow an explanation but does not establish causality by itself.
- An ASIN appearing only in sponsored placements is a placement-posture observation, not proof of weak organic relevance or conversion.

## Aggregate overview

- Current ORG/SP/SB/SBV/SPR impression-point fields support the ASIN's aggregate observed channel/placement exposure structure for the returned current period.
- When all included current channel fields share one returned scope and have compatible non-null values, an Agent-derived current channel mix may be calculated as `channel impression points ÷ sum of included current channel impression points`. Name the included channels and missing-value handling; do not call the result exact Amazon traffic share.
- Current and matching non-null `*Prev` fields support a transparent same-channel current-versus-previous-baseline comparison. The legacy overview does not return separate previous-period date boundaries: label that boundary unavailable and never derive it from weekly cadence. If a matching `*Prev` value is null or absent, the movement comparison for that channel is unavailable.
- `first3PagesNewOrganicKeywords[]` and `first3PagesLostOrganicKeywords[]` are membership changes in the endpoint-defined first-three-page organic Top-N set between its matching previous and current returned periods. `new` means present in the current set and absent from the previous set; `lost` means absent from the current set and present in the previous set.
- Report those arrays with the returned current period, disclose that the previous-period boundary is not returned, and preserve the exact first-three-page organic set boundary. Do not infer the missing previous dates. Use a numeric `Top N` label only when returned context or a documented, verified ordering/pagination contract establishes N; otherwise retain the endpoint's `first-three-page organic Top-N` wording. Entry or exit does not establish per-keyword traffic gain/loss, a newly created or deleted market keyword, magnitude, cause, or broader trend.
- The overview has no keyword contribution rows. It cannot identify per-keyword gainers, losers, contribution, or cause.

## Cross-source limits

- Search demand falling across multiple comparable weekly points is a demand-trend concern only for that returned window.
- Timeline evidence owns ASIN × keyword movement observations; overview evidence owns current ASIN-wide aggregate channel structure and previous-period movement. Neither substitutes for keyword-level traffic-term rows.
- Keep all traffic observations below seller-funnel and Ads evidence authority defined in `execution-guide.md`.
