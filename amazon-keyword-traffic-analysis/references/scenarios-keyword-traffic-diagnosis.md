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

- Minimum evidence: `keywords/search-results` + `keywords/detail`
- Two or more observations are required for anything stronger than directional movement commentary
- If `keywords/trend` is unavailable, keep demand-change interpretation weak
- `keywords/product-traffic-terms-timeline` is an important input for ASIN + keyword diagnosis; if unavailable, do not make strong ASIN-side position/exposure/ad-activity timeline claims
- `keywords/product-traffic-terms-overview` is the preferred core evidence for two-week / previous-period all-keyword impression traffic changes under the ASIN; if unavailable, do not infer previous-period traffic deltas or first-3-page ORG keyword entry/exit
- If both ASIN traffic-list endpoints are unavailable, do not infer ASIN-side traffic-share
- If `keywords/product-traffic-terms-overview` is unavailable, do not infer all-keyword impression traffic changes or ORG first-3-page entry/exit
- `products/search` must not be used to explain observed rank or page-1 composition changes
- Diagnosis may use any efficient call pattern, but likely-cause claims must stay within the available evidence class
- If the user did not provide Amazon backend ABA-SQP search conversion data, keep traffic-change conclusions, likely-cause groups involving exposure/position/share, and recommended actions directional and place the seller-side SQP enrichment request only in `Data Notes` and `Data Notes Reminder`
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to refine traffic-change causes and action priority; do not add the seller-side SQP enrichment request

### Tool Availability Gate

- `keywords/search-results` and `keywords/detail` are the minimum required tools for a diagnosis pass
- If either minimum tool is unavailable, stop and report that the diagnosis workflow cannot be executed reliably
- `keywords/product-traffic-terms-timeline` should be checked whenever the task includes ASIN + keyword movement across dates
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
| `keywords/product-traffic-terms-timeline` | ASIN × keyword movement across dates | `latestOrganicPosition`, `latestAdPosition`, impression-point fields, `avgOrganicObservation`, `avgAdObservation`, `adActiveObservationCount`, `adActiveDayCoverageRate`, `keywordEstimateSearchCnt`, `keywordAbaRank` |
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
  - `keyword*` fields are keyword traffic-forecast dependency data for the provided keyword's corresponding metric period, indicated by `keywordPeriodStartDate` / `keywordPeriodEndDate`
  - `latest*` fields are the ASIN's latest product/listing/rank snapshot on the specified `date`
  - impression-point fields, `avg*` fields, ad-activity fields, and placement observations are rolling metrics for the most recent 7 days ending at the given `date`
- Do not compare `keyword*`, `latest*`, and 7-day rolling metrics as if they shared the same time grain
- Use `keyword*` fields to support interpretation of traffic-estimate movement, not as direct evidence of ASIN price/BSR/sales/rating changes

### Curves And Events

For ASIN + keyword diagnosis, inspect these curves when timeline data is available:

| Curve | Fields | Use |
|-------|--------|-----|
| Price curve | `latestPrice` | Check whether price changes align with rank, conversion, or traffic-estimate movement |
| BSR curve | `latestSmallCategoryBsr`, `latestBigCategoryBsr` | Check whether category rank improved or weakened around the anomaly |
| Sales curve | `latestMonthlySaleCnt` | Check whether sales momentum moved with traffic exposure |
| Rating curve | `latestRatingAmt`, `latestRatingCnt` | Check whether rating quality or review count changed enough to affect placement/conversion |
| Traffic-estimate curve | `organicImpressionPoint`, `sponsoredProductImpressionPoint`, `sponsoredBrandImpressionPoint`, `sponsoredBrandVideoImpressionPoint`, `sponsoredRecommendImpressionPoint`, `avgOrganicObservation`, `avgAdObservation` | Estimate exposure movement over the 7-day rolling window |

Use keyword-level fields as supporting context for traffic-estimate changes:
- `keywordEstimateSearchCnt`, `keywordEstimateSearchGrowthCnt`, `keywordAbaRank`, and related `keyword*` fields explain whether the provided keyword's own demand/competition context changed during its metric period
- Do not use keyword-level movement alone to claim the ASIN's product performance changed

Track these timeline events:
- Title change event: `latestTitle` changed between dates
- Main image change event: `latestMainImageLink` changed between dates
- Treat title/image events as possible causes or confounders only when their timing aligns with traffic, BSR, sales, or rating movement

### Diagnosis Signals

| Signal | What changed | Possible cause |
|--------|--------------|----------------|
| Position drop | `absolutePosition` / `pageIndex` worsened | stronger competitors, lower bid, listing weakness |
| Exposure drop | `estimateImpressionPoint` fell | lower search demand or worse placement |
| Ad crowding rose | sponsored share of SERP increased | bidding intensified |
| Traffic share fell | ASIN keyword share weakened | rank loss or all-keyword traffic shift |
| Demand fell | trend/search count moved down | keyword itself cooled off |
| Timeline position worsened | `latestOrganicPosition`, `latestAdPosition`, or `avgOrganicObservation` worsened | ASIN lost organic/ad placement under the keyword |
| Timeline impression fell | organic/sponsored impression-point fields fell | weaker placement, lower ad presence, or lower keyword demand |
| Ad activity weakened | `adActiveObservationCount`, `adActiveDayCoverageRate`, `adCampaignCnt`, or `adCnt` fell | ads stopped/paused or coverage dropped |
| All-keyword traffic changed | overview impression-point fields changed versus `*Prev` fields | ASIN gained/lost broader keyword traffic coverage |
| ORG first-3-page entry/exit changed | `first3PagesNewOrganicKeywords` or `first3PagesLostOrganicKeywords` changed | ASIN gained/lost important organic keyword visibility |
| Price moved | `latestPrice` changed | price sensitivity may affect conversion, rank, or ad efficiency |
| BSR moved | `latestSmallCategoryBsr` / `latestBigCategoryBsr` changed | broader category momentum changed alongside keyword traffic |
| Sales moved | `latestMonthlySaleCnt` changed | sales momentum changed alongside exposure or conversion |
| Rating moved | `latestRatingAmt` / `latestRatingCnt` changed | review quality or review volume may affect conversion and placement |
| Listing event occurred | `latestTitle` or `latestMainImageLink` changed | listing content change may have affected relevance, CTR, or conversion |

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
> When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep traffic-change conclusions, likely-cause groups involving exposure/position/share, and recommended actions directional and place the seller-side SQP enrichment request only in Data Notes and Data Notes Reminder. If seller-side ABA-SQP data is included, integrate it directly and omit the enrichment request.

## [Localized Data Notes title]
[Use short, natural prose, not status labels, field lists, or deficit-framed wording. If the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, first state that evidence basis; then say that if the user can provide seller-side ABA-SQP conversion funnel data, the analysis can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance; then include Seller Central path `Brand Analytics → Search Analytics → Search Query Performance → Brand View`, recommend sorting by `Search Funnel - Impressions → Brand Count`, and ask for a screenshot or CSV. If seller-private ABA-SQP data is present, name the SQP fields used and omit the seller-side SQP enrichment request.]

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

## [Localized Data Notes Reminder title]
[Repeat the opening Data Notes body here. For Chinese output, the opening title must render from `\u6570\u636e\u8bf4\u660e`; the end reminder title must render from `\u6570\u636e\u8bf4\u660e\uff08\u518d\u6b21\u63d0\u9192\uff09`.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
