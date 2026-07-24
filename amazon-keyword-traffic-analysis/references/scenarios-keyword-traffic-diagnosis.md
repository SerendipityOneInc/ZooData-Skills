# Keyword Traffic Diagnosis

> Load this file for keyword traffic anomaly diagnosis.

## Contents

- [Inputs](#inputs)
- [Task Constraints](#task-constraints)
- [Tool Availability Gate](#tool-availability-gate)
- [Important ASIN-Side Inputs](#important-asin-side-inputs)
- [Curves And Events](#curves-and-events)
- [Diagnosis Signals](#diagnosis-signals)
- [Output Template](#output-template)

## 4. Keyword Traffic Diagnosis

> Trigger: "diagnose keyword traffic anomalies" / "why did this keyword move" / "analyze this ASIN's keyword traffic drop"

### Inputs

- required: ASIN + keyword
- recommended: at least 2 observation dates
- recommended: date range for `keywords/product-traffic-terms-timeline` when explaining ASIN-side movement
- optional: comparison date for `keywords/product-traffic-terms-overview` when explaining all-keyword impression traffic changes for the ASIN versus the previous period
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Minimum evidence is claim-specific. Prefer `search-results-metrics` for SERP structure, `market-profile` for weekly market context, `trend-profile` for demand/rank trend judgments, `product-traffic-terms-overview` for ASIN aggregate movement, and `product-traffic-terms-timeline-review` when live for timeline evidence summary.
- Use raw `search-results`, `detail`, or timeline data only when the matching metric is unavailable or omits rows/fields/series required for a named diagnosis inference.
- A metric dimension's unsupported/unavailable status limits the conclusion; it does not automatically authorize a same-source data call.
- Two or more observations are required for anything stronger than directional movement commentary
- If `keywords/trend-profile` is unavailable, use raw `keywords/trend` only for transparent point-level interpretation; if neither is available, keep demand-change interpretation weak
- `keywords/product-traffic-terms-timeline-review` is preferred when live. Use raw `keywords/product-traffic-terms-timeline` only when the review metric is unavailable or the diagnosis needs series detail omitted by the metric.
- `keywords/product-traffic-terms-overview` is the preferred core evidence for two-week / previous-period all-keyword impression traffic changes under the ASIN; if unavailable, do not infer previous-period traffic deltas or first-3-page ORG keyword entry/exit
- `keywords/product-traffic-term-changes` is the planned source for top losing/gaining keyword contribution. If it returns 404, omit contribution claims rather than deriving them from the overview.
- `keywords/product-traffic-terms-timeline-review` is a planned evidence-summary endpoint. If unavailable and raw timeline fields can support the requested inference, inspect only the required timeline groups. Report an Agent explanation only when those fields materially distinguish it; otherwise retain the unresolved question.
- When diagnosing several keywords for one ASIN, batch them through timeline review first when live. If raw series are justified by a named inference, batch only that fallback set—up to 20—through one timeline data request and preserve each item's status.
- If both ASIN traffic-list endpoints are unavailable, do not infer ASIN-side traffic-share
- If `keywords/product-traffic-terms-overview` is unavailable, do not infer all-keyword impression traffic changes or ORG first-3-page entry/exit
- `products/search` must not be used to explain observed rank or page-1 composition changes
- Diagnosis may use any efficient call pattern, but explanations require evidence that materially distinguishes them from alternatives; an available evidence class alone does not make a cause claim valid.
- Without seller funnel data, keep traffic-change conclusions within observed visibility/placement evidence. In a staged target-keyword workflow, ask for ABA-SQP only after candidate-profile validation; in a standalone anomaly diagnosis, one end-of-report seller-data request is allowed when it directly resolves the named uncertainty.
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to locate the unresolved funnel handoff and calibrate action priority. Do not treat SQP alone as proof of the handoff's cause, and do not add the seller-side SQP enrichment request.
- Apply `execution-guide.md § Evidence-Seeking Diagnosis Protocol` before reporting explanations and `§ Evidence-to-Action Protocol` before every recommendation. Aggregate traffic or funnel movement can identify an unresolved problem domain but cannot identify a cause, defective listing asset, or operating setting by itself.
- Do not recommend rebuilding or replacing images, title, bullets, A+ content, price, offer, variation, fulfillment, keyword, bid, or campaign settings unless the exact target meets the required authorization level. If it was not directly inspected, stop at `Inspect`.

### Tool Availability Gate

- Check the metric endpoint matching each requested diagnosis claim first; there is no universal raw-endpoint minimum pair.
- Check `keywords/product-traffic-terms-timeline-review` first whenever the task includes ASIN + keyword movement across dates; descend to timeline data only for metric unavailability or an explicitly missing series-level inference.
- `keywords/product-traffic-terms-overview` should be checked whenever the task asks whether all keywords under the ASIN changed over two weeks or versus the previous period, especially ORG first-3-page entries/exits
- `keywords/product-traffic-terms` and `keywords/competitor-product-keywords` currently provide equivalent traffic-list functionality; choose one available endpoint when traffic-source/share context is needed
- If ASIN-side endpoints are unavailable, continue with a SERP-led diagnosis and label ASIN-side timeline, traffic-share, all-keyword traffic-change, and ORG first-3-page entry/exit conclusions as unavailable rather than inferred

### SERP And Product-Library Rule

- Diagnose keyword movement primarily from `keywords/search-results` because this is the observed keyword SERP
- Do not default to `products/search` to explain rank or page-1 composition changes
- Use `products/search` only if the user also wants a broader catalog context such as category-wide winners, price-band shifts, or strong-selling variants beyond the observed keyword SERP
- If `products/search` is used, state clearly that it is our product-database query result and does not equal Amazon live search ranking

### Important ASIN-Side Inputs

| Endpoint | Use for | Key fields |
|----------|---------|------------|
| `keywords/product-traffic-terms-timeline` | ASIN × keyword movement across dates | nested `asinSnapshot`, `traffic`, `placement`, `keywordMetrics`, and `adActivity` groups |
| `keywords/product-traffic-terms-overview` | All-keyword impression traffic changes under one ASIN versus previous period | `organicImpressionPoint`, sponsored impression-point fields, matching `*Prev` previous-period fields, `first3PagesNewOrganicKeywords`, `first3PagesLostOrganicKeywords`, `periodStartDate`, `periodEndDate` |
| `keywords/product-traffic-terms` | Current ASIN traffic-source keyword list; preferred choice for traffic-share context | `trafficShare`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount` |
| `keywords/competitor-product-keywords` | Equivalent ASIN traffic-list fallback or competitor/overlap-framed choice | `trafficShare`, `avgPosition`, `keywordEstimateSearchCount`, `keywordAbaRank` |

Interpretation rules:
- Prefer `keywords/product-traffic-terms-timeline` over ad hoc comparison of isolated snapshots when the question is "why did this ASIN move under this keyword?"
- Use `keywords/product-traffic-terms-overview` for all-keyword ASIN traffic changes, not as proof of one exact keyword's daily rank movement
- When presenting the overview period, copy `periodStartDate` and `periodEndDate` from the response exactly; do not use the requested lookup date or a self-inferred two-week range as the displayed period
- For current traffic-source/share structure, use either `keywords/product-traffic-terms` or `keywords/competitor-product-keywords`; do not spend calls on both unless you intentionally need a parity check
- Treat `*Prev` fields as the previous-period baseline for the matching current impression-point fields
- `first3PagesNewOrganicKeywords` lists keywords newly entering the ORG first three pages; `first3PagesLostOrganicKeywords` lists keywords that dropped out of the ORG first three pages
- Keep the three timeline metric groups separate:
  - `keywordMetrics` belongs to its nested `metricWindow`
  - `asinSnapshot` is tied to `series[].date`
  - `traffic`, `placement`, and `adActivity` cover the rolling 7-day window ending on `series[].date`
- Do not compare these three groups as if they shared the same time grain
- Use `keywordMetrics` to support interpretation of traffic movement, not as direct evidence of ASIN price/BSR/sales/rating changes

### Curves And Events

For ASIN + keyword diagnosis, inspect these curves when timeline data is available:

| Curve | Fields | Use |
|-------|--------|-----|
| Price curve | `asinSnapshot.latestPrice` | Check whether price changes align with rank, conversion, or traffic-estimate movement |
| BSR curve | `asinSnapshot.latestSubBsr`, `asinSnapshot.latestBsr` | Check whether category rank improved or weakened around the anomaly |
| Sales curve | `asinSnapshot.latestMonthlySaleCount` | Check whether sales momentum moved with traffic exposure |
| Rating curve | `asinSnapshot.latestRating`, `asinSnapshot.latestRatingCount` | Check whether rating or review-count movement is time-aligned with placement/conversion evidence; do not assign impact from co-movement alone |
| Traffic-estimate curve | `traffic.*ImpressionPoint`, `placement.avgOrganicObservation`, `placement.avgAdObservation` | Estimate exposure movement over the 7-day rolling window |

Use keyword-level fields as supporting context for traffic-estimate changes:
- `keywordMetrics.keywordEstimateSearchCount`, `keywordMetrics.keywordAbaRank`, and Top3 share fields explain whether the provided keyword's demand context changed during its metric period
- Do not use keyword-level movement alone to claim the ASIN's product performance changed

Track these timeline events:
- Title change event: `asinSnapshot.latestTitle` changed between dates
- Main image change event: `asinSnapshot.latestMainImageLink` changed between dates
- Treat title/image events as time-aligned evidence signals only when their timing aligns with traffic, BSR, sales, or rating movement. Alignment makes them candidates for further discrimination, not causes. A changed value/link does not reveal content quality and cannot authorize a content change without direct inspection.

### Diagnosis Signals

| Signal | Observed change | Evidence needed to explain it |
|--------|-----------------|-------------------------------|
| Position drop | `absolutePosition` / `pageIndex` worsened | Time-aligned SERP, placement, ad-activity, demand, and subject-event evidence needed to distinguish the driver |
| Exposure drop | `estimateImpressionPoint` fell | Demand and placement movement over the same window |
| Ad crowding rose | Sponsored share of SERP increased | Comparable ad-density observations plus target-ASIN ad activity; crowding alone does not prove bidding intensity |
| Traffic share fell | ASIN keyword share weakened | Position, coverage, impression, and all-keyword movement over the same window |
| Demand fell | Trend/search count moved down | Multiple comparable weekly points; this explains keyword demand movement, not automatically ASIN movement |
| Timeline position worsened | `placement.latestOrganicPosition`, `placement.latestAdPosition`, or `placement.avgOrganicObservation` worsened | Channel-separated placement, ad activity, demand, and time-aligned subject/market events |
| Timeline impression fell | Organic/sponsored impression-point fields fell | Placement, ad presence, and keyword demand over matching grains |
| Ad activity weakened | `adActivity.adActiveObservationCount`, `adActiveDayCoverageRate`, `adCampaignCount`, or `adCount` fell | Campaign/Ads evidence needed to distinguish pause, budget, bid, eligibility, and observation-coverage explanations |
| All-keyword traffic changed | Overview impression-point fields changed versus `*Prev` fields | Channel and keyword-row evidence needed before attributing contribution to a specific keyword |
| ORG first-3-page entry/exit changed | `first3PagesNewOrganicKeywords` or `first3PagesLostOrganicKeywords` changed | Keyword-level position/timeline evidence needed to explain why entry or exit occurred |
| Price moved | `asinSnapshot.latestPrice` changed | Time alignment plus conversion/placement evidence needed before assigning price impact |
| BSR moved | `asinSnapshot.latestSubBsr` / `latestBsr` changed | Time alignment with sales, exposure, and category movement; BSR is not a standalone cause |
| Sales moved | `asinSnapshot.latestMonthlySaleCount` changed | Time alignment with exposure and seller conversion evidence; co-movement is not causality |
| Rating moved | `asinSnapshot.latestRating` / `latestRatingCount` changed | Review-event and conversion evidence needed before assigning impact |
| Listing event occurred | `asinSnapshot.latestTitle` or `latestMainImageLink` changed | Direct asset inspection plus time-aligned relevance/CTR/conversion evidence needed before assigning impact |

### Alert Levels

- `High`
  target ASIN shows a meaningful, sustained position/share loss across comparable observations; explanation confidence is reported separately
- `Medium`
  noticeable movement but evidence is mixed
- `Low`
  small movement or single-snapshot fluctuation only

### Output Template

```markdown
# Keyword Traffic Diagnosis Report — [ASIN] × [Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> Without seller funnel data, keep conclusions within observed visibility and placement evidence. Report an explanation only when discriminating evidence supports it; if seller-side ABA-SQP data is included, integrate it directly without treating the funnel pattern itself as proof of cause.

## [Localized Data Notes title]
[Name the current evidence level and the specific diagnosis boundary. If SQP is present, name the fields used.]

## Alert Level
[High / Medium / Low]

## What Changed
| Metric | Previous | Current | Interpretation |
|--------|----------|---------|----------------|

## ASIN-Side Timeline
| Date | Price | BSR | Sales | Rating | Traffic Estimate | Key Events | Interpretation |
|------|-------|-----|-------|--------|------------------|------------|----------------|

## All-keyword Traffic Overview (period: [periodStartDate] → [periodEndDate])
[Fill from `keywords/product-traffic-terms-overview`. If endpoint unavailable, write "unavailable" and omit period-comparison conclusions.]

| Placement | Current ImpressionPoint | Previous ImpressionPoint | Change |
|-----------|-------------------------|--------------------------|--------|
| ORG | | | |
| SP | | | |
| SB | | | |
| SBV | | | |
| SPR | | | |

**Newly entered ORG first 3 pages:** [list from `first3PagesNewOrganicKeywords`, or "none" / "unavailable"]

**Dropped out of ORG first 3 pages:** [list from `first3PagesLostOrganicKeywords`, or "none" / "unavailable"]

## Explanation Status
[Report only evidence-supported explanations. For each one, name the supporting evidence and material alternatives not ruled out. If none is sufficiently supported, state the unresolved question and do not create a cause list.]

## Authorized Next Actions
[Include only actions authorized by the evidence. Label each `Inspect / Diagnose / Test / Change / Scale / Stop` and state the target plus supporting evidence. Omit this section when no action is authorized; keep the single evidence request in `Next Step`.]

## Next Step
[In a standalone diagnosis, request only the minimum evidence needed to distinguish the unresolved explanations. Omit this section when the provided evidence is sufficient.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
