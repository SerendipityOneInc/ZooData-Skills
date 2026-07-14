# Keyword Traffic Diagnosis

> Load this file for keyword traffic anomaly diagnosis.

---

## 4. Keyword Traffic Diagnosis

> Trigger: "diagnose keyword traffic anomalies" / "why did this keyword move" / "analyze this ASIN's keyword traffic drop"

### Inputs

- required: ASIN + keyword
- recommended: at least 2 observation dates
- recommended: date range for `keywords/product-traffic-terms-timeline` when explaining ASIN-side movement
- optional: comparison date for `keywords/product-traffic-terms-overview` when explaining all-keyword impression traffic changes for the ASIN versus the previous period
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Minimum evidence is claim-specific. Prefer `search-results-metrics` for SERP structure, `market-profile` for weekly market context, `product-traffic-terms-overview` for ASIN aggregate movement, and `product-traffic-terms-timeline-review` when live for timeline evidence summary.
- Use raw `search-results`, `detail`, or timeline data only when the matching metric is unavailable or omits rows/fields/series required for a named diagnosis inference.
- Metric calculation coverage limits the conclusion; it does not automatically authorize a same-source data call.
- Two or more observations are required for anything stronger than directional movement commentary
- If `keywords/trend` is unavailable, keep demand-change interpretation weak
- `keywords/product-traffic-terms-timeline-review` is preferred when live. Use raw `keywords/product-traffic-terms-timeline` only when the review metric is unavailable or the diagnosis needs series detail omitted by the metric.
- `keywords/product-traffic-terms-overview` is the preferred core evidence for two-week / previous-period all-keyword impression traffic changes under the ASIN; if unavailable, do not infer previous-period traffic deltas or first-3-page ORG keyword entry/exit
- `keywords/product-traffic-term-changes` is the planned source for top losing/gaining keyword contribution. If it returns 404, omit contribution claims rather than deriving them from the overview.
- `keywords/product-traffic-terms-timeline-review` is a planned evidence-summary endpoint. If unavailable and raw timeline fields can support the requested inference, inspect only the required timeline groups and label all cause ranking as Agent inference.
- When diagnosing several keywords for one ASIN, batch them through timeline review first when live. If raw series are justified by a named inference, batch only that fallback set—up to 20—through one timeline data request and preserve each item's status.
- If both ASIN traffic-list endpoints are unavailable, do not infer ASIN-side traffic-share
- If `keywords/product-traffic-terms-overview` is unavailable, do not infer all-keyword impression traffic changes or ORG first-3-page entry/exit
- `products/search` must not be used to explain observed rank or page-1 composition changes
- Diagnosis may use any efficient call pattern, but likely-cause claims must stay within the available evidence class
- Without seller funnel data, keep traffic-change conclusions and likely causes directional. In a staged target-keyword workflow, ask for ABA-SQP only after candidate-profile validation; in a standalone anomaly diagnosis, one end-of-report seller-data request is allowed when it directly resolves the diagnosed uncertainty.
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to refine traffic-change causes and action priority; do not add the seller-side SQP enrichment request

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
| Rating curve | `asinSnapshot.latestRating`, `asinSnapshot.latestRatingCount` | Check whether rating quality or review count changed enough to affect placement/conversion |
| Traffic-estimate curve | `traffic.*ImpressionPoint`, `placement.avgOrganicObservation`, `placement.avgAdObservation` | Estimate exposure movement over the 7-day rolling window |

Use keyword-level fields as supporting context for traffic-estimate changes:
- `keywordMetrics.keywordEstimateSearchCount`, `keywordMetrics.keywordAbaRank`, and Top3 share fields explain whether the provided keyword's demand context changed during its metric period
- Do not use keyword-level movement alone to claim the ASIN's product performance changed

Track these timeline events:
- Title change event: `asinSnapshot.latestTitle` changed between dates
- Main image change event: `asinSnapshot.latestMainImageLink` changed between dates
- Treat title/image events as possible causes or confounders only when their timing aligns with traffic, BSR, sales, or rating movement

### Diagnosis Signals

| Signal | What changed | Possible cause |
|--------|--------------|----------------|
| Position drop | `absolutePosition` / `pageIndex` worsened | stronger competitors, lower bid, listing weakness |
| Exposure drop | `estimateImpressionPoint` fell | lower search demand or worse placement |
| Ad crowding rose | sponsored share of SERP increased | bidding intensified |
| Traffic share fell | ASIN keyword share weakened | rank loss or all-keyword traffic shift |
| Demand fell | trend/search count moved down | keyword itself cooled off |
| Timeline position worsened | `placement.latestOrganicPosition`, `placement.latestAdPosition`, or `placement.avgOrganicObservation` worsened | ASIN lost organic/ad placement under the keyword |
| Timeline impression fell | organic/sponsored impression-point fields fell | weaker placement, lower ad presence, or lower keyword demand |
| Ad activity weakened | `adActivity.adActiveObservationCount`, `adActiveDayCoverageRate`, `adCampaignCount`, or `adCount` fell | ads stopped/paused or coverage dropped |
| All-keyword traffic changed | overview impression-point fields changed versus `*Prev` fields | ASIN gained/lost broader keyword traffic coverage |
| ORG first-3-page entry/exit changed | `first3PagesNewOrganicKeywords` or `first3PagesLostOrganicKeywords` changed | ASIN gained/lost important organic keyword visibility |
| Price moved | `asinSnapshot.latestPrice` changed | price sensitivity may affect conversion, rank, or ad efficiency |
| BSR moved | `asinSnapshot.latestSubBsr` / `latestBsr` changed | broader category momentum changed alongside keyword traffic |
| Sales moved | `asinSnapshot.latestMonthlySaleCount` changed | sales momentum changed alongside exposure or conversion |
| Rating moved | `asinSnapshot.latestRating` / `latestRatingCount` changed | review quality or review volume may affect conversion and placement |
| Listing event occurred | `asinSnapshot.latestTitle` or `latestMainImageLink` changed | listing content change may have affected relevance, CTR, or conversion |

### Alert Levels

- `High`
  target ASIN lost meaningful position/share and at least one supporting cause is observed
- `Medium`
  noticeable movement but evidence is mixed
- `Low`
  small movement or single-snapshot fluctuation only

### Output Template

```markdown
# Keyword Traffic Diagnosis Report — [ASIN] × [Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> Without seller funnel data, traffic-change causes and actions remain directional. If seller-side ABA-SQP data is included, integrate it directly.

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

## Likely Causes
1. [💡 / 🔍 only]
2. [💡 / 🔍 only]
3. [💡 / 🔍 only]

## Recommended Actions
[Observe / increase defense / inspect bids / inspect listing relevance]

## Next Step
[In a standalone diagnosis, request only the seller data needed to resolve the named uncertainty. Omit this section when the provided data is sufficient.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
