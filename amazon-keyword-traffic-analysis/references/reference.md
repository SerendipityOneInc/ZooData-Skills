# Amazon Keyword Intelligence — Reference

> Load this file when you need exact endpoint choices, field priorities, evidence boundaries, or scenario-to-endpoint mapping.

## Endpoints

| Endpoint | Use in this skill | Key fields |
|----------|-------------------|------------|
| `/openapi/v2/keywords/detail` | Weekly keyword snapshot | `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`, `marketCharacteristics`, `totalSkuCnt`, `brandCount`, `organicSkuCount`, `adCampaignCount`, `adCount` |
| `/openapi/v2/keywords/trend` | Weekly trend validation | `estimateSearchCount`, `estimateSearchChangeRate`, `abaRank`, `rankChangeCount`, `periodStartDate`, `periodEndDate` |
| `/openapi/v2/keywords/extends` | Expansion / long-tail discovery | `term`, `seedKeyword`, `relevanceScore`, `estimateSearchCountWeekly`, `abaRank`, `marketCharacteristics`, `brandCount`, `organicSkuCount`, `adCount` |
| `/openapi/v2/keywords/search-results` | SERP structure, page-1 product mix, and ad density | `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`, `title`, `brand`, `price`, `rating`, `ratingCount`, `recentSales`, `estimateImpressionPoint`, `keywordTotalEstimateImpressionPoint` |
| `/openapi/v2/keywords/competitor-product-keywords` | Keywords where ASIN appears as competitor | `keyword`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`, `trafficShare` |
| `/openapi/v2/keywords/product-traffic-terms` | Traffic-driving keywords for ASIN | `keyword`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`, `trafficShare` |
| `/openapi/v2/keywords/product-traffic-terms-overview` | All-keyword traffic changes under one ASIN versus previous period | placement-level impression points, matching `*Prev` previous-period fields, `first3PagesNewOrganicKeywords`, `first3PagesLostOrganicKeywords`, `periodStartDate`, `periodEndDate` |
| `/openapi/v2/keywords/product-traffic-terms-timeline` | ASIN + keyword anomaly timeline | `date`, `latestOrganicPosition`, `latestAdPosition`, impression-point fields, `avgOrganicObservation`, `avgAdObservation`, `keywordEstimateSearchCnt`, `keywordAbaRank`, ad activity fields |

## Keyword API Quick Reference

Use this section before selecting or calling a keyword endpoint. It is the
skill-local API reference for the keyword endpoints; `zoodata/references/openapi-reference.md`
remains the broader platform reference.

Usage accounting:
- Each CLI/API response should include `_query.endpoint` and `_query.params`; use `_query.endpoint` for API usage aggregation
- Credits are reported in response `meta.creditsConsumed`; aggregate this by endpoint for the final API Usage table and include a final `Total` row
- Credits remaining are reported in response `meta.creditsRemaining`; use the latest observed value for `Credits remaining`
- If either credit field is missing, write `not returned` in the report rather than omitting API usage
- Any report based on live API data must end with `API Usage`; omit `Data Provenance` unless the user explicitly asks for source-by-section details

Keyword-query and date rule:
- Keyword endpoints are keyword-query workflows; inputs named `keyword` or `query` should be Amazon search queries / keyword phrases
- If an endpoint requires `date` or `dateTo`, prefer T-1 or earlier and avoid the current date unless the user explicitly asks for today's lookup. Do not proactively explain the rationale unless the user asks why.
- If today's lookup is explicitly requested and data is missing, sparse, or resolves backward, label the result as potentially incomplete instead of treating it as a demand signal

### Keyword Value Boundary

- ZooData keyword endpoints provide estimated search volume, SERP visibility, rank, traffic share, and impression-point signals
- These fields are enough for directional opportunity screening and testing priority, but not enough to 100% prove a keyword's value for a specific ASIN
- Do not claim definitive profitability, conversion potential, or final budget priority from ZooData alone
- Do not claim the ASIN, listing, CTR, CVR, rank, or traffic quality is better than competitors without direct competitor evidence at the same metric, keyword/query, marketplace, date range, and comparable placement or position scope
- Prefer market-relative language when competitor-specific evidence is missing: above/below market median, ahead/behind the market midpoint, near the upper/lower band, ranking toward the front/back, or not an obvious weak point
- When a market average or median is derived from ABA/SQP screenshots, ZooData aggregates, or visible SERP samples, state the calculation basis and limitation; do not present it as external benchmark proof or competitor-specific evidence
- ABA-SQP backend location: Seller Central path `Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View`
- Recommended ABA-SQP data provision method: in Brand View, sort descending by `[Search Funnel - Impressions](https://sellercentral.amazon.com/brand-analytics/metric-glossary?linkedFrom=query-performance-brand-report-table-qp-impressions-group) -> Brand Count`, then provide a screenshot; alternatively, download the CSV and provide it for model analysis

- Before writing conclusions, check whether the user provided ABA backend Search Query Performance / ABA-SQP search conversion data for the relevant ASIN/brand/query/date range
- When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, place the seller-side SQP enrichment request in the report's opening `Data Notes` and end `Data Notes Reminder`, not inside each traffic-related conclusion or recommendation group.
- If seller-side ABA-SQP data is included, do not add the seller-side SQP enrichment request; incorporate impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate as first-party conversion evidence

### `/openapi/v2/keywords/detail`

Parameters:
- required: `keyword`, `date`
- optional: `marketplace` default `US`

Behavior:
- `date` resolves to the nearest available weekly snapshot at or before the requested date
- Prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- `success: true` may return `data: null`; treat that as no weekly snapshot, not an API failure

Response:
- single keyword snapshot object or `null`
- key fields: `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`, `marketCharacteristics`, `totalSkuCnt`, `brandCount`, `organicSkuCount`, `adCampaignCount`, `adCount`, `periodStartDate`, `periodEndDate`, `observedAt`

### `/openapi/v2/keywords/trend`

Parameters:
- required: `keyword`, `dateFrom`, `dateTo`
- optional: `marketplace` default `US`
- CLI flags: `keyword-trend --keyword "<query>" --date-from YYYY-MM-DD --date-to YYYY-MM-DD --marketplace US`
- Dates must be complete ISO strings. Do not use truncated dates, ellipses, relative dates, or natural-language dates in CLI calls.
- `dateTo - dateFrom` cannot exceed 93 days for `keywords/trend`

Behavior:
- weekly-granularity series across the requested date range
- Prefer T-1 or earlier for `dateTo`; avoid current-date lookup unless explicitly requested
- do not compare directly to daily SERP observations without stating the grain difference

Response:
- array of weekly trend points
- key fields: `observedAt`, `periodStartDate`, `periodEndDate`, `estimateSearchCount`, `estimateSearchChangeCount`, `estimateSearchChangeRate`, `abaRank`, `prevAbaRank`, `prevEstimateSearchCount`, `rankChangeCount`

### `/openapi/v2/keywords/extends`

Parameters:
- required: `query`, `date`
- optional: `marketplace` default `US`, `page`, `pageSize` max `100`, `queryType`, `sortBy`, `sortOrder`
- `queryType`: `phrase` / `fuzzy`
- `sortBy`: `relevanceScore` / `estimateSearchCount` / `abaRank` / `observedAt` / `keyword`
- `sortOrder`: `asc` / `desc`

Behavior:
- uses `query`, not `keyword`
- `date` resolves to the nearest available weekly snapshot at or before the requested date
- Prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- `data: []` is a normal success case; try both `phrase` and `fuzzy` before concluding low expandability

Response:
- array of expansion keyword rows
- key fields: `term`, `seedKeyword`, `relevanceScore`, `estimateSearchCountWeekly`, `abaRank`, `marketCharacteristics`, `brandCount`, `organicSkuCount`, `adCount`, `periodStartDate`, `periodEndDate`, `observedAt`
- market-structure fields may include `totalSkuCnt`, `observedSkuCount`, `titleDensity`, `organicRolloverRate`, `amazonChoiceSkuCount`, sponsored SKU counts, `adCampaignCount`, and top-48 organic average price/rating/sales fields

### `/openapi/v2/keywords/search-results`

Parameters:
- required: `keyword`, `date`
- optional: `marketplace` default `US`, `page`, `pageSize` max `100`, `exploreTypes`, `sortBy`, `sortOrder`
- `exploreTypes`: `ORG` / `SP` / `SB` / `SBV` / `SPR`
- `sortBy`: `absolutePosition` / `estimateImpressionPoint` / `observedAt` / `price` / `rating` / `ratingCount` / `recentSales` / `asin` / `title`

Behavior:
- daily/recent SERP observation exposed through a short sliding window, not long-retention history
- Prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- primary source for observed keyword SERP, page-1 product mix, brand mix, ad vs organic composition, and visible price-band questions
- separate `exploreType` at least into `ORG` and sponsored placements
- do not replace it with `products/search` for observed Amazon keyword SERP composition or ordering

Response:
- array of SERP product rows with absolute positions
- key fields: `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`, `title`, `brand`, `price`, `currency`, `link`, `imageLink`, `rating`, `ratingCount`, `recentSales`, `hasVideo`, `estimateImpressionPoint`, `keywordTotalEstimateImpressionPoint`

### `/openapi/v2/keywords/product-traffic-terms`

Parameters:
- required: `asin`, `date`
- optional: `marketplace` default `US`, `page`, `pageSize` max `100`, `exploreTypes`, `keywordContains`, `sortBy`, `sortOrder`
- `exploreTypes`: `ORG` / `SP` / `SB` / `SBV` / `SPR`
- `sortBy`: `estimateImpressionPoint` / `absolutePosition` / `avgPosition` / `keywordEstimateSearchCount` / `keywordAbaRank` / `observedAt` / `keyword`

Behavior:
- reverse-ASIN traffic-list endpoint for current traffic-source/share structure
- Prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- same live item shape and equivalent traffic-list functionality as `competitor-product-keywords`; choose one available endpoint instead of requiring both
- preferred choice for target-ASIN traffic-source lists
- not a substitute for `keywords/search-results` when the question is visible page-1 product composition

Response:
- array of ASIN keyword rows
- key fields: `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`, `keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`, `keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`, `keywordAbaRankChangeCount`, `trafficShare`

### `/openapi/v2/keywords/competitor-product-keywords`

Parameters:
- required: `asin`, `date`
- optional: `marketplace` default `US`, `page`, `pageSize` max `100`, `exploreTypes`, `keywordContains`, `sortBy`, `sortOrder`
- `exploreTypes`: `ORG` / `SP` / `SB` / `SBV` / `SPR`
- `sortBy`: `estimateImpressionPoint` / `absolutePosition` / `avgPosition` / `keywordEstimateSearchCount` / `keywordAbaRank` / `observedAt` / `keyword`

Behavior:
- reverse-ASIN traffic-list endpoint for competitor/overlap-framed workflows
- Prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- same live item shape and equivalent traffic-list functionality as `product-traffic-terms`; choose one available endpoint instead of requiring both
- not a substitute for `keywords/search-results` when the question is visible page-1 product composition

Response:
- array of ASIN keyword rows
- key fields match `product-traffic-terms`: `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`, `keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`, `keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`, `keywordAbaRankChangeCount`, `trafficShare`

### `/openapi/v2/keywords/product-traffic-terms-overview`

Parameters:
- required: `asin`, `date`
- optional: `marketplace` default `US`

Behavior:
- preferred core evidence for two-week / previous-period ASIN all-keyword impression traffic changes
- returns the latest weekly all-keyword traffic-change overview on or before `date`
- Prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- when reporting the overview period, use the response's `periodStartDate` and `periodEndDate` exactly; do not display the request `date` or an inferred date range as the data period
- use matching `*Prev` impression-point fields as previous-period baselines
- do not treat it as per-keyword daily rank history

Response:
- single overview object or `null`
- key fields: `periodStartDate`, `periodEndDate`, `asin`, `site`, `organicImpressionPoint`, `sponsoredProductImpressionPoint`, `sponsoredBrandImpressionPoint`, `sponsoredBrandVideoImpressionPoint`, `sponsoredRecommendImpressionPoint`, matching `*Prev` fields, `first3PagesNewOrganicKeywords`, `first3PagesLostOrganicKeywords`
- `first3PagesNewOrganicKeywords` and `first3PagesLostOrganicKeywords` items contain `keyword`, `pageIndex`, and `pagePosition`

### `/openapi/v2/keywords/product-traffic-terms-timeline`

Parameters:
- required: `asin`, `keyword`, `dateFrom`, `dateTo`
- optional: `marketplace` default `US`, `page`, `pageSize` max `100`, `sortBy`, `sortOrder`
- `dateTo - dateFrom` cannot exceed 93 days
- `sortBy`: `date`
- `sortOrder`: `asc` / `desc`

Behavior:
- preferred ASIN + exact-keyword timeline input for anomaly diagnosis
- Prefer T-1 or earlier for `dateTo`; avoid current-date lookup unless explicitly requested
- interpret three metric groups separately:
  - `keyword*` fields describe keyword traffic-forecast dependency data for `keywordPeriodStartDate` / `keywordPeriodEndDate`
  - `latest*` fields describe the ASIN's latest product/listing/rank snapshot on the row date
  - impression-point, `avg*`, ad-activity, and placement fields are rolling metrics for the most recent 7 days ending on the row date

Response:
- array of timeline rows
- product/listing fields: `date`, `asin`, `keyword`, `latestTitle`, `latestPrice`, `latestCurrency`, `latestLink`, `latestMainImageLink`, `latestBrandName`, `latestMonthlySaleCnt`, `latestRatingAmt`, `latestRatingCnt`, category BSR fields
- placement/exposure fields: `exploreTypes`, impression-point fields, `latestOrganicPosition`, organic page fields, `latestAdPosition`, ad page fields, `avgOrganicObservation`, `avgAdObservation`, `adActiveObservationCount`, `adActiveDayCoverageRate`, `adCampaignCnt`, `adCnt`
- keyword context fields: `keywordPeriodStartDate`, `keywordPeriodEndDate`, `keywordEstimateSearchCnt`, keyword growth fields, `keywordAbaRank`, ABA share fields, keyword market/SKU/ad-count fields

## Draft Callable Tool Mapping

Use these as draft full names only. Final authority is the tool surface actually
exposed in the current session.

| HTTP endpoint path | Draft callable tool name |
|----------|--------------------------|
| `/openapi/v2/keywords/detail` | `mcp__zoodata__openapi_v2_keyword_detail` |
| `/openapi/v2/keywords/trend` | `mcp__zoodata__openapi_v2_keyword_trend` |
| `/openapi/v2/keywords/extends` | `mcp__zoodata__openapi_v2_keyword_extends` |
| `/openapi/v2/keywords/search-results` | `mcp__zoodata__openapi_v2_keyword_search_results` |
| `/openapi/v2/keywords/competitor-product-keywords` | `mcp__zoodata__openapi_v2_keyword_competitor_product_keywords` |
| `/openapi/v2/keywords/product-traffic-terms` | `mcp__zoodata__openapi_v2_keyword_product_traffic_terms` |
| `/openapi/v2/keywords/product-traffic-terms-overview` | `mcp__zoodata__openapi_v2_product_traffic_terms_overview` |
| `/openapi/v2/keywords/product-traffic-terms-timeline` | `mcp__zoodata__openapi_v2_product_traffic_terms_timeline` |

Tool selection rules:
- Before selecting a tool, read the candidate tool's relevant docs/help/schema; names are hints, not proof of function
- Preferred execution path after that documentation check is `python {skill_base_dir}/scripts/zoodata.py` with the matching keyword subcommand
- Use the full callable tool name, not a shortened alias
- Do not infer a callable name from another tool such as `openapi_v2_categories`
- If the live session exposes a different full name, follow the live session
- If the local CLI path is unavailable and the live session does not expose keyword tools, report that explicitly

## Endpoint Quirks

- `keywords/detail`: top-level `data` is an object or `null`
- `keywords/trend`: `data` is an array of weekly points
- `keywords/extends`: input seed is `query`; try `queryType=phrase` first, then `fuzzy`
- `keywords/search-results`: daily-ish observation in a ~7-day sliding window
- `keywords/competitor-product-keywords` and `keywords/product-traffic-terms`: same live item shape and equivalent traffic-list functionality today; for traffic-structure analysis, choose one available endpoint instead of requiring both
- `keywords/product-traffic-terms-overview`: weekly ASIN-level all-keyword impression traffic-change overview; `data` is an object or `null`; `*Prev` fields are previous-period baselines for matching impression-point fields
- For `keywords/product-traffic-terms-overview`, report the period from response fields `periodStartDate` / `periodEndDate` only; request dates are lookup inputs, not the returned observation period
- `first3PagesNewOrganicKeywords` lists keywords newly entering the ORG first three pages; `first3PagesLostOrganicKeywords` lists keywords that dropped out of the ORG first three pages
- `keywords/product-traffic-terms-timeline`: ASIN + exact-keyword timeline; `data` is an array, requested range cannot exceed 93 days

Timeline field groups:
- `keyword*` fields are keyword traffic-forecast dependency data for the provided keyword's corresponding metric period, indicated by `keywordPeriodStartDate` / `keywordPeriodEndDate`
- `latest*` fields are the ASIN's latest product/listing/rank snapshot on the specified `date`
- impression-point fields, `avg*` fields, ad-activity fields, and placement observations are rolling metrics for the most recent 7 days ending at the given `date`
- Do not compare these groups as if they were the same time grain
- For diagnosis, use timeline data as several curves: price (`latestPrice`), BSR (`latestSmallCategoryBsr`, `latestBigCategoryBsr`), sales (`latestMonthlySaleCnt`), rating (`latestRatingAmt`, `latestRatingCnt`), and traffic estimate (impression-point fields plus `avgOrganicObservation` / `avgAdObservation`)
- Use `keyword*` fields as supporting context for traffic-estimate movement, not as direct evidence of ASIN price, BSR, sales, rating, title, or image changes
- Treat `latestTitle` and `latestMainImageLink` changes as listing events; use them as possible causes/confounders only when their timing aligns with curve movement

## SERP Product Interpretation Rule

- If the user asks what products appear on the first page for a keyword, answer that primarily from `/openapi/v2/keywords/search-results`
- This endpoint already returns product-level fields such as `asin`, `title`, `brand`, `price`, `rating`, `ratingCount`, and `recentSales`, so it is not just an ad-density endpoint
- Treat `/openapi/v2/keywords/search-results` as the default source for page-1 product mix, intent shape, brand mix, and ad vs organic composition
- Do not add `products/search` by default just to explain what appears on the keyword SERP
- Add `products/search` only as an optional supplement when the user explicitly asks for broader market winners, sales distribution, price-band structure, or best-selling variants beyond the observed keyword SERP

## `products/search` Boundary Rule

- `products/search` is a query against our own product database snapshot, not a direct Amazon live search-result page
- Its result set can help describe broader catalog winners, sales distribution, price-band structure, and variant concentration
- Do not present `products/search` output as "Amazon search results", "Amazon first-page results", or evidence of current keyword SERP ordering
- Do not classify `products/search` as a front-end keyword SERP interface
- When both endpoints are used, describe them separately:
  `keywords/search-results` = observed keyword SERP
  `products/search` = broader product-database supplement

## `webtools_search` Boundary Rule

- `webtools_search` is a crawler / web retrieval utility, not a keyword-intelligence endpoint
- Do not use `webtools_search` as a substitute for `/openapi/v2/keywords/detail`, `/trend`, `/extends`, or `/search-results`
- Use it only when the task is genuinely about web collection or when you need an explicitly labeled supplementary source outside the ZooData keyword endpoints

## Evidence Boundary Rules

- Use the endpoint that directly matches the evidence type whenever possible
- Do not substitute broader product-library evidence for observed keyword SERP evidence
- Do not substitute keyword snapshot evidence for reverse-ASIN source attribution
- Do not substitute daily observed SERP evidence for weekly demand direction
- Missing data from one endpoint type should create a boundary, not trigger cross-type invention

## Capability Verification Order

Before judging whether a question can be answered:

1. Read the relevant docs/help/schema for each plausible candidate tool before choosing one
2. Check whether the matching `zoodata.py` keyword subcommand exists and use it as the primary execution path when its docs match the evidence need
3. If needed, read the live tool schema and field descriptions for the exposed callable tool
4. Map those fields or CLI outputs to the business question
5. Use endpoint naming only as a weak hint, never as proof

If neither the CLI docs/subcommand path nor live tool schema can be verified from the current environment, report that boundary explicitly instead of inventing capability.

## Scenario Mapping

| Scenario | Must-have endpoints | Optional endpoints | Main decision output |
|----------|---------------------|--------------------|----------------------|
| Keyword expansion | `keywords/extends`, `keywords/detail` | `keywords/trend`, `keywords/search-results`, `products/search` | Candidate tiers and coarse filtering |
| Single keyword analysis | `keywords/detail`, `keywords/search-results` | `keywords/trend`, `products/search` | Worth targeting or not |
| Reverse ASIN keyword analysis | one of `keywords/product-traffic-terms` or `keywords/competitor-product-keywords` | the other ASIN traffic-list endpoint, `keywords/detail`, `keywords/search-results`, `products/search` | Traffic-source map and bid focus |
| Keyword Traffic Diagnosis | `keywords/search-results`, `keywords/detail` | `keywords/product-traffic-terms-timeline`, `keywords/product-traffic-terms-overview`, `keywords/trend`, ASIN keyword endpoints, `products/search` | Cause analysis for changes |

Availability interpretation:
- `Must-have endpoints` means the scenario should not be presented as fully executable without them
- `Optional endpoints` may enrich confidence or context, but they must not be silently substituted for missing must-have endpoints
- For reverse ASIN, `keywords/product-traffic-terms` and `keywords/competitor-product-keywords` currently provide equivalent traffic-list functionality; one available endpoint is enough for the core traffic-source map
- For reverse ASIN, `keywords/detail` and `keywords/search-results` are enrichers only; they do not replace an ASIN traffic-list endpoint
- For traffic diagnosis, `keywords/product-traffic-terms-timeline` is the preferred ASIN + keyword timeline input; if missing, keep ASIN-side position/exposure-change conclusions weak
- For traffic diagnosis, `keywords/product-traffic-terms-overview` is the preferred core evidence for two-week / previous-period all-keyword ASIN impression traffic changes; if missing, omit previous-period all-keyword traffic deltas and ORG first-3-page entry/exit conclusions
- For traffic diagnosis, if both ASIN traffic-list endpoints are missing, omit ASIN-side traffic-share conclusions instead of inferring them
- For single keyword analysis, if `keywords/trend` is missing, keep the conclusion snapshot-led and avoid strong claims about demand direction

Conclusion scope:
- `Must-have endpoints` unlock the scenario's core claim
- `Optional endpoints` can refine confidence, context, or prioritization
- Missing optional endpoints should narrow the claim scope, not redirect the task into another evidence model

## Scoring Inputs

### Demand

- Primary: `estimateSearchCountWeekly`, `keywordEstimateSearchCount`
- Secondary: `estimateSearchChangeRate`, `keywordEstimateSearchCountChangeRate`, `abaRank`
- Boundary: these are search-demand and exposure estimates, not first-party conversion or sales value; when the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep traffic/value conclusions directional and put the seller-side SQP enrichment request only in `Data Notes` and `Data Notes Reminder`; when seller-side ABA-SQP data is included, use it to refine final keyword value

### Competition

- Primary: `adCount`, `adCampaignCount`, SERP ad-slot share
- Secondary: top ASIN repetition, `avgPosition`, `trafficShare`

### Relevance

- Primary: `relevanceScore`
- Secondary: semantic closeness to seed term, alignment between keyword intent and SERP results

### Stability

- Primary: trend consistency across 4-8 weekly points
- Secondary: `daysCoverageRate`, `observationCount`

## Recommended Reporting Dimensions

### For keyword expansion

- Search demand bucket
- Competition bucket
- Relevance bucket
- Suggested usage scene: auto, broad, phrase, exact, product targeting support, or SEO observation

### For single keyword analysis

- Traffic size
- Traffic direction
- Ad crowding
- Organic room
- Head-listing strength
- Bid recommendation tier

### For reverse ASIN

- Top traffic-source keywords
- Ranking quality by keyword
- Defensive keywords vs expansion keywords
- Missing but strategically relevant competitor keywords
- Bucket labels: `Defend` / `Expand` / `Observe` / `Avoid`

### For keyword traffic diagnosis

- Position change
- Exposure change
- Search demand change
- Ad density change
- ASIN + keyword timeline movement
- Price / BSR / sales / rating curves
- Traffic-estimate curve
- Title and main image change events
- ASIN all-keyword impression traffic changes versus previous period
- ORG first-3-page keyword entries/exits
- Head competitor change
- Likely cause and urgency
