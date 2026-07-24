# ZooData API Quick Reference

> Concise field reference for the currently documented Amazon commerce and keyword-intelligence endpoints. Load when you need exact parameter/field names.
>
> **OpenAPI Spec (live)**: https://zoodata.ai/api/v1/openapi-spec

Base URL: `https://api.zoodata.ai/openapi/v2`
Auth: `Bearer $ZOODATA_API_KEY`
Method: All POST with JSON body

---

## 1. categories

| Parameter | Type | Note |
|-----------|------|------|
| categoryKeyword | String | Search by keyword |
| categoryPath | List\<String\> | Exact path lookup, e.g. `["Electronics", "Computers"]` |
| parentCategoryPath | List\<String\> | Browse children |
| _(no params)_ | — | Returns root categories |

Response: `categoryId`, `categoryName`, `categoryPath`, `hasChildren`, `isRoot`, `level`, `productCount`, `link`

---

## 2. markets/search

| Parameter | Type | Note |
|-----------|------|------|
| categoryPath | List\<String\> | e.g. `["Pet Supplies", "Dogs"]` |
| categoryKeyword | String | Keyword match across levels |
| topN | **String** | `"3"` / `"5"` / `"10"` / `"20"` ⚠️ must be string |
| newProductPeriod | **String** | `"1"` / `"3"` / `"6"` / `"12"` ⚠️ must be string |
| sampleType | String | `bySale100` / `byBsr100` / `avg` |
| dateRange | String | default `30d` |
| pageSize | Integer | default 20 |
| sortBy | String | default `sampleAvgMonthlySales` |
| sortOrder | String | `asc` / `desc` |

Key response fields: `sampleAvgMonthlySales`, `sampleAvgPrice`, `sampleAvgMonthlyRevenue`, `sampleBrandCount`, `sampleSellerCount`, `sampleFbaRate`, `sampleNewSkuRate`, `topSalesRate`, `topBrandSalesRate`, `topSellerSalesRate`, `totalSkuCount`

---

## 3. products/competitors

| Parameter | Type | Note |
|-----------|------|------|
| keyword | String | Search keyword |
| brand | String | Brand filter |
| seller | String | Seller filter |
| asin | String | ASIN filter |
| categoryPath | List\<String\> | Category filter |
| sortBy | String | `monthlySalesFloor` / `monthlyRevenueFloor` / `bsr` / `price` / `rating` / `ratingCount` / `listingDate` |
| sortOrder | String | `asc` / `desc` |
| pageSize | Integer | default 20 |

---

## 4. products/search

Same as competitors, plus:

| Parameter | Type | Note |
|-----------|------|------|
| keywordMatchType | String | `fuzzy` / `phrase` / `exact` |
| listingAge | **Enum String** | One of `30d` / `90d` / `180d` / `1y` / `2y` (⚠️ bare numbers like `180` → 422) |

Filter pairs (all optional, Min/Max): `monthlySales`, `revenue`, `salesGrowthRate`, `bsr`, `subBsr`, `bsrGrowthRate`, `price`, `rating`, `ratingCount`, `fbaShipping`, `variantCount`, `grossMargin`, `sellerCount`

> `mode` is **NOT** an API parameter. The 13 CLI presets in `zoodata.py` expand client-side into the filter pairs above before the request is sent; passing `mode` in a raw request returns 422.

Additional: `includeBrands`, `excludeBrands`, `fulfillment` (`["FBA"]`/`["FBM"]`/`["AMZ"]`), `badges` — enum values `["bestSeller"]` / `["amazonChoice"]` / `["newRelease"]` / `["aPlus"]` / `["video"]` (⚠️ `"New Release"` with a space → 422)

---

## 5. realtime/product

| Parameter | Required | Note |
|-----------|----------|------|
| asin | **Yes** | Product ASIN |
| marketplace | No | `US`/`UK`/`DE`/`FR`/`IT`/`ES`/`JP`/`CA`/`AU`/`IN`/`MX`/`BR` (default: US) |

Response fields: `asin`, `title`, `brand`, `rating`, `ratingCount`, `ratingBreakdown`, `features`, `description`, `specifications`, `categories`, `variants`, `bestsellersRank` (array), `buyboxWinner` (object with price), `images`, `dimensions`, `weight`

⚠️ Does NOT have: `monthlySalesFloor`, `fbaFee`, `sellerCount`

---

## 6. reviews/analysis

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| mode | String | **Yes** | `asin` or `category` |
| asins | List\<String\> | When mode=asin | ⚠️ plural, array format |
| categoryPath | String | When mode=category | Category path |
| period | String | No | e.g. `6m` |

⚠️ `labelType` is **not** an API request parameter. The API returns all 11 dimensions in one call. Filter by `labelType` client-side from the `consumerInsights` array.

Response: `reviewCount`, `avgRating`, `verifiedRate`, `ratingDistribution`, `sentimentDistribution`, `consumerInsights` (list of InsightItem), `topKeywords`

InsightItem: `element`, `labelType`, `count`, `reviewRate`, `avgRating`

labelType values (in response): `scenarios`, `issues`, `positives`, `improvements`, `buyingFactors`, `painPoints`, `keywords`, `userProfiles`, `usageTimes`, `usageLocations`, `behaviors`

---

## 6b. realtime/reviews

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Product ASIN (10 chars) |
| marketplace | String | No | `US`/`UK` only (default: US) |
| cursor | String | No | Pagination token from previous response's `nextCursor`. Omit for first page. |

⚠️ No `pageSize` parameter — server returns 10 reviews/page fixed. Hard cap = **100 reviews / 10 pages**. Cost = **1 credit/page**.

Response: `asin`, `reviews` (array of RealtimeReview), `nextCursor` (null = no more pages).

RealtimeReview: `reviewId`, `title`, `body`, `bodyHtml`, `rating`, `author`, `date` (ISO 8601), `verifiedPurchase`, `vineProgram`, `helpfulVoteCount`, `unhelpfulVoteCount`, `reviewCountry`, `images`, `link`, `isGlobalReview`

Use cases:
- ASIN has <50 reviews so `/reviews/analysis` aggregation is empty
- Brand-new product with no daily snapshot
- Need fresh raw text for local LLM analysis (Map/Reduce → consumerInsights)

See `zoodata.py reviews-raw / review-tag-prompt / review-reduce-prompt / review-aggregate` for the local toolkit that consumes this endpoint.

---

## 6c. reviews/search

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Product ASIN |
| ratingMin / ratingMax | Number | No | 1-5 inclusive |
| verifiedOnly | Boolean | No | Default false |
| vineOnly | Boolean | No | Default false |
| helpfulVoteCountMin | Integer | No | Filter low-engagement reviews |
| dateStart / dateEnd | Date (YYYY-MM-DD) | No | Inclusive range |
| sortBy | String | No | `recent` (default) / `rating` / `helpfulVoteCount` |
| sortOrder | String | No | `desc` (default) / `asc` |
| page | Integer | No | 1-indexed, default 1 |
| pageSize | Integer | No | 1-20, default 10 |

Response: array of TaggedReview with AI-generated `tags[{labelType, element}]` derived from the offline analysis pipeline (BigQuery daily snapshot).

TaggedReview vs RealtimeReview: `reviews/search` uses snapshot data with AI tags (T+1 delay); `realtime/reviews` is live raw text (no tags). Use `reviews/search` when daily snapshot exists and you want pre-tagged data; use `realtime/reviews` for fresh data or new products.

---

## 7. products/price-band-overview

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Search keyword |

⚠️ Only accepts `keyword` — does NOT support `categoryPath`.

**Response (top-level):**

| Field | Type | Note |
|-------|------|------|
| sampleMedianPrice | Float | Median price across sampled products |
| hottestBand | BandObject | Band with highest sales rate |
| bestOpportunityBand | BandObject | Band with highest opportunity index |

**BandObject:**

| Field | Type | Note |
|-------|------|------|
| bandIdx | Integer | Band index (0-4) |
| bandLabel | String | e.g. "$10-$20" |
| sampleBandMinPrice | Float | Band minimum price |
| sampleBandMaxPrice | Float | Band maximum price |
| sampleSkuCount | Integer | Number of SKUs in this band |
| sampleSalesRate | Float | Share of total sales in this band |
| sampleBrandCount | Integer | Number of brands in this band |
| sampleTop3BrandSalesRate | Float | Top 3 brands' share within this band |
| sampleAvgRating | Float | Average rating in this band |
| sampleOpportunityIndex | Float | Composite opportunity score |

---

## 8. products/price-band-detail

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Search keyword |

⚠️ Only accepts `keyword` — does NOT support `categoryPath`.

**Response:**

| Field | Type | Note |
|-------|------|------|
| sampleSkuCount | Integer | Total sampled SKUs |
| sampleTotalMonthlySales | Integer | Total monthly sales across all bands |
| priceBands | Array\<BandObject\> | Array of 5 band objects (same structure as §7) |

---

## 9. products/brand-overview

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Search keyword |

⚠️ Only accepts `keyword` — does NOT support `categoryPath`.

**Response:**

| Field | Type | Note |
|-------|------|------|
| sampleBrandCount | Integer | Total number of brands found |
| sampleTop10BrandSalesRate | Float | CR10 — top 10 brands' share of total sales |
| sampleTop10AvgRating | Float | Average rating of top 10 brands |
| sampleTop10AvgPrice | Float | Average price of top 10 brands |

---

## 10. products/brand-detail

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Search keyword |

⚠️ Only accepts `keyword` — does NOT support `categoryPath`.

**Response (top-level):**

| Field | Type | Note |
|-------|------|------|
| sampleSkuCount | Integer | Total sampled SKUs |
| sampleTotalMonthlySales | Integer | Total monthly sales |
| sampleBrandCount | Integer | Total brands found |
| brands | Array\<BrandObject\> | Per-brand breakdown |

**BrandObject:**

| Field | Type | Note |
|-------|------|------|
| brandName | String | Brand name |
| sampleSkuCount | Integer | SKUs for this brand |
| sampleGroupMonthlySales | Integer | Monthly unit sales |
| sampleGroupMonthlyRevenue | Float | Monthly revenue |
| sampleSalesRate | Float | Share of total sales |
| sampleAvgPrice | Float | Average price |
| minPrice | Float | Lowest price product |
| maxPrice | Float | Highest price product |
| sampleAvgRating | Float | Average rating |
| sampleAvgRatingCount | Integer | Average review count |
| sampleProducts | Array\<ProductObject\> | Sample products from this brand |

**ProductObject** (within sampleProducts): Same fields as Shared Product Object below.

---

## 11. products/history

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Single ASIN (one per call) |
| startDate | String | **Yes** | Start date `YYYY-MM-DD` |
| endDate | String | **Yes** | End date `YYYY-MM-DD` |
| marketplace | String | No | Marketplace code, default `US` |

⚠️ `asin` is a **single string** — NOT an array. For multiple ASINs, make separate calls.
⚠️ Does NOT support `page`/`pageSize` — returns full date range in one response.
⚠️ Uses `startDate`/`endDate` — NOT `dateRange`.

**Response:** Single time series object (NOT an array of snapshots).

| Field | Type | Note |
|-------|------|------|
| asin | String | Product ASIN |
| timestamps | List\<String\> | Dates (YYYY-MM-DD) |
| price | List\<Float\> | Price on each date |
| bsr | List\<Integer\> | BSR on each date |
| subBsr | List\<Integer\> | Sub-category BSR |
| monthlySalesFloor | List\<Integer\> | Monthly sales lower bound |
| rating | List\<Float\> | Rating on each date |
| ratingCount | List\<Integer\> | Review count on each date |
| sellerCount | List\<Integer\> | Seller count |
| title | List\<ChangeLog\> | Title changes `{date, value}` |
| imageUrl | List\<ChangeLog\> | Main image changes `{date, value}` |
| bestSeller | List\<ChangeLog\> | Best Seller badge `{date, value}` |
| amazonChoice | List\<ChangeLog\> | Amazon's Choice badge `{date, value}` |
| newRelease | List\<ChangeLog\> | New Release badge `{date, value}` |
| aPlus | List\<ChangeLog\> | A+ content status `{date, value}` |
| inventoryStatus | List\<ChangeLog\> | Stock status `{date, value}` |
| currency | String | e.g. `USD` |

---

## Keyword Intelligence Endpoints

Published endpoints were live-validated against the current OpenAPI surface. `keywords/market-profile` is a localhost pre-release exception documented below.

Tool-surface note:
- API documentation and live endpoint availability do not guarantee that the current agent session exposes matching callable tools
- For skill execution, verify the live tool surface first; use this file for parameter and field confirmation after that

## 12. /openapi/v2/keywords/detail

Keyword value boundary for all keyword endpoints:
- The keyword endpoints expose estimated search, SERP visibility, rank, traffic-share, and impression-point signals.
- Keyword endpoints are keyword-query workflows; parameters named `keyword` or `query` expect Amazon search query / keyword phrases.
- For keyword endpoints that require `date` or `dateTo`, prefer T-1 or earlier and avoid the current date unless the user explicitly asks for today's lookup.
- These signals support directional screening and testing priority, but do not 100% prove a keyword's value for a specific ASIN.
- ABA-SQP backend location: Chinese Seller Central path `品牌分析 -> 搜索分析 -> 搜索查询绩效 -> 品牌视图`; English Seller Central path `Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View`.
- Recommended ABA-SQP data provision method: in Brand View, sort descending by `[Search Funnel - Impressions](https://sellercentral.amazon.com/brand-analytics/metric-glossary?linkedFrom=query-performance-brand-report-table-qp-impressions-group) -> Brand Count` / `搜索漏斗-展示次数 -> 品牌数量`, then provide a screenshot; alternatively, download the CSV and provide it for model analysis.
- If the user has not provided Amazon backend ABA-SQP search conversion data, every traffic-related conclusion or recommendation group should include: "建议结合 Amazon 后台 ABA-SQP 的搜索转化数据做更精确分析（中文路径：品牌分析 -> 搜索分析 -> 搜索查询绩效 -> 品牌视图；英文路径：Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View）."
- If the user provided ABA-SQP data, combine the endpoint output with impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate as first-party conversion evidence and omit that caveat.

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Keyword to inspect |
| date | String | **Yes** | Lookup date `YYYY-MM-DD`; prefer T-1 or earlier; resolves to the nearest available weekly snapshot at or before that date |
| marketplace | String | No | Marketplace code, default `US` |

⚠️ Live behavior: `success: true` may still return `data: null` when no matching weekly snapshot record is available for that keyword.

**Response:** Single keyword snapshot object **or `null`**.

Key fields: `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`,
`marketCharacteristics`, `totalSkuCnt`, `brandCount`, `organicSkuCount`, `adCampaignCount`, `adCount`,
`periodStartDate`, `periodEndDate`, `observedAt`

---

## 12b. /openapi/v2/keywords/market-profile (metric layer, localhost pre-release)

Availability: exposed on `http://localhost:8080` as of 2026-07-14; not yet published to production.

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | Conditional | One keyword; exactly one of `keyword` / `keywords` |
| keywords | List\<String\> | Conditional | Batch of 1–20 keywords; preserves request order |
| date | String | **Yes** | Lookup date `YYYY-MM-DD`; resolves to the latest weekly snapshot on or before this date |
| marketplace | String | No | `US` / `UK`, default `US` |
| granularity | String | No | `week` only |

**Response:** `data.context + data.items[]` for both single and batch requests.

Context fields: `marketplace`, `site`, `requestedDate`, `resolvedDate`, `granularity`, `dataWindow.currentPeriod`, and `scoringSpec` (`id`, `version`, `scoreType`, `scoreRange`, `referenceScope`).

Each item has `identity`, `status=available|not_found`, `marketProfile`, and `unavailableReason`. `marketProfile` contains `marketCharacteristics`, `demandScale`, `top3Concentration`, `adActivity`, `top20OrganicEntryDifficulty`, `supplySaturation`, `brandStructure`, and `organicProductBenchmark`.

Use returned scores only with `context.scoringSpec`. Each scored dimension exposes `supported`, `level`, `interpretation`, `calculationStatus`, `unsupportedReason`, and `levelEvidence.score.{value,direction}`; evaluate it independently and treat any explicit unavailable signal as a conclusion boundary. `marketCharacteristics.volatility` exposes type and mapping-confidence evidence. `marketCharacteristics.annualSeasonality` separately exposes classification, year-over-year correlation, eligible-pair count, peak-pattern detection, and peak periods. Do not merge the two classifications or invent peak periods. This endpoint returns deterministic weekly snapshot evidence, not trend, root cause, recommendations, or seller-private ABA-SQP conversion data.

An unmatched keyword returns `status=not_found`, `marketProfile=null`, `unavailableReason=keyword_not_observed`, zero consumed credits, and may return null resolved context / scoring spec. A subject-specific calculation error can currently return HTTP 500 for the entire batch; treat that as a service failure rather than an empty item, and do not automatically fan out the batch. Use returned `meta.creditsConsumed` / `meta.creditsConsumedExact`.

Three-layer boundary: `keywords/detail` is the traceable data layer; `keywords/market-profile` is the stable deterministic metric layer; the Agent + skill layer combines evidence and produces confidence, explanations, limitations, and recommendations.

Metric-first rule: use `market-profile` before `detail` for supported market judgments. Do not descend merely because a metric dimension has incomplete calculation coverage; both are source-related, so the missing metric input will usually remain missing. Descend only when a named Agent inference requires raw fields omitted by the metric contract, the metric endpoint is unavailable, or the user requests source evidence.

Batch-first rule: once an endpoint is selected, prefer its batch form for all subjects sharing marketplace, date/range, granularity, window, filters, and sort context. Deduplicate while preserving order, chunk at 20, and use single calls only for one subject or incompatible contexts.

CLI: `zoodata.py keyword-market-profile --keywords "yoga mat,pilates mat" --date 2026-06-29 --marketplace US`

---

## 13. /openapi/v2/keywords/trend

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Keyword to inspect |
| dateFrom | String | **Yes** | Start date `YYYY-MM-DD` |
| dateTo | String | **Yes** | End date `YYYY-MM-DD`; prefer T-1 or earlier |
| marketplace | String | No | Marketplace code, default `US` |

**Response:** Array of weekly-granularity trend points across the requested date range.

Interpretation note:
- `keywords/trend` is weekly series data; do not compare it to daily SERP observations as if they were the same grain

Key fields: `observedAt`, `periodStartDate`, `periodEndDate`, `estimateSearchCount`,
`estimateSearchChangeCount`, `estimateSearchChangeRate`, `abaRank`, `prevAbaRank`,
`prevEstimateSearchCount`, `rankChangeCount`

---

## 13b. /openapi/v2/keywords/trend-profile (metric layer, localhost pre-release)

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | Conditional | Exactly one of `keyword` / `keywords` |
| keywords | String[] | Conditional | 1–20, mutually exclusive with `keyword` |
| date | String | **Yes** | As-of date `YYYY-MM-DD` |
| windowPeriods | Integer[] | **Yes** | 1–4 unique values from `4`, `8`, `12`, `26` |
| marketplace | String | No | `US` / `UK`, default `US` |
| granularity | String | No | `week` only |

**Response:** `data.context + data.items[].rows[]`. Each keyword has one row per requested window. Rows return `status=available|unavailable|not_found`, `rowContext`, `unavailableReason`, and `trendProfile`. Available profiles expose guarded `searchDemand` and `abaRank` dimensions. Their `trendEvidence` values include an explicit direction plus slope and consistency evidence, so do not infer the server label from endpoint movement alone. Preserve null unavailable reasons without inventing one.

Use this metric endpoint first for trend shape and volatility; call raw `keywords/trend` only when weekly points or omitted fields are required.

---

## 14. /openapi/v2/keywords/extends

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| query | String | **Yes** | Seed keyword |
| date | String | **Yes** | Lookup date `YYYY-MM-DD`; prefer T-1 or earlier; resolves to the nearest available weekly snapshot at or before that date |
| marketplace | String | No | Marketplace code, default `US` |
| page | Integer | No | default 1 |
| pageSize | Integer | No | default 20, max 100 |
| queryType | String | No | `phrase` / `fuzzy` (default `phrase`) |
| sortBy | String | No | `relevanceScore` / `estimateSearchCount` / `abaRank` / `observedAt` / `keyword` |
| sortOrder | String | No | `asc` / `desc` |

⚠️ Uses `query`, NOT `keyword`.
⚠️ Live behavior: empty `data: []` is a normal success case.

**Response:** Array of expansion keywords.

Key fields per item: `term` (expanded keyword), `seedKeyword`, `relevanceScore`,
`estimateSearchCountWeekly`, `abaRank`, `marketCharacteristics`, `brandCount`,
`organicSkuCount`, `adCount`, `periodStartDate`, `periodEndDate`, `observedAt`

Additional market-structure fields may appear on each item, including `totalSkuCnt`,
`observedSkuCount`, `titleDensity`, `organicRolloverRate`, `amazonChoiceSkuCount`,
`sponsoredProductSkuCount`, `sponsoredBrandSkuCount`, `sponsoredBrandVideoSkuCount`,
`sponsoredRecommendSkuCount`, `adCampaignCount`, `top48OrganicSkuAvgPrice`,
`top48OrganicSkuAvgRating`, `top48OrganicSkuAvgRatingsTotal`, and
`top48OrganicSkuAvgRecentSaleCnt`.

---

## 15. /openapi/v2/keywords/search-results

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Keyword to inspect |
| date | String | **Yes** | Daily snapshot lookup date `YYYY-MM-DD`; prefer T-1 or earlier |
| marketplace | String | No | Marketplace code, default `US` |
| page | Integer | No | default 1 |
| pageSize | Integer | No | default 20, max 100 |
| exploreTypes | Array\<String\> | No | `ORG` / `SP` / `SB` / `SBV` / `SPR` |
| sortBy | String | No | `absolutePosition` / `estimateImpressionPoint` / `observedAt` / `price` / `rating` / `ratingCount` / `recentSales` / `asin` / `title` |
| sortOrder | String | No | `asc` / `desc` |

⚠️ This endpoint behaves like a daily-observation feed exposed through a recent sliding ~7-day window, not a long-retention historical snapshot archive.
⚠️ Use this endpoint as the primary source for "what products are currently showing on the keyword SERP/page 1" because it already returns listing-level product fields.
⚠️ Do not replace it with `products/search` when the question is about observed Amazon keyword SERP composition or ordering.
⚠️ When analyzing this endpoint, separate `exploreType` at least into `ORG` and sponsored placements instead of collapsing all rows together.

**Response:** Array of SERP products with absolute positions.

Key fields from live response: `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`,
`title`, `brand`, `price`, `currency`, `link`, `imageLink`, `rating`, `ratingCount`, `recentSales`,
`hasVideo`, `estimateImpressionPoint`, `keywordTotalEstimateImpressionPoint`

Interpretation rule:
- `keywords/search-results` = observed keyword SERP snapshot
- It can answer page-1 product mix, brand mix, ad vs organic composition, and visible price band questions
- If you also use `products/search`, present it as a broader catalog supplement, not as the same thing

---

## 16. /openapi/v2/keywords/competitor-product-keywords

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Target ASIN |
| date | String | **Yes** | Daily snapshot lookup date `YYYY-MM-DD`; prefer T-1 or earlier |
| marketplace | String | No | Marketplace code, default `US` |
| page | Integer | No | default 1 |
| pageSize | Integer | No | default 20, max 100 |
| exploreTypes | Array\<String\> | No | `ORG` / `SP` / `SB` / `SBV` / `SPR` |
| keywordContains | String | No | Optional substring filter on returned keywords |
| sortBy | String | No | `estimateImpressionPoint` / `absolutePosition` / `avgPosition` / `keywordEstimateSearchCount` / `keywordAbaRank` / `observedAt` / `keyword` |
| sortOrder | String | No | `asc` / `desc` |

**Response:** Array of keyword rows for an ASIN.

Key fields from live response: `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`,
`keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`, `avgPosition`,
`daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`,
`keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`,
`keywordAbaRankChangeCount`, `trafficShare`

⚠️ Live validation indicates this endpoint also behaves like a daily-observation feed exposed through a recent sliding ~7-day window.
⚠️ In skill workflows, this endpoint is a reverse-ASIN source endpoint, not a substitute for `keywords/search-results` when the question is about visible page-1 product composition.

---

## 17. /openapi/v2/keywords/product-traffic-terms

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Target ASIN |
| date | String | **Yes** | Daily snapshot lookup date `YYYY-MM-DD`; prefer T-1 or earlier |
| marketplace | String | No | Marketplace code, default `US` |
| page | Integer | No | default 1 |
| pageSize | Integer | No | default 20, max 100 |
| exploreTypes | Array\<String\> | No | `ORG` / `SP` / `SB` / `SBV` / `SPR` |
| keywordContains | String | No | Optional substring filter on returned keywords |
| sortBy | String | No | `estimateImpressionPoint` / `absolutePosition` / `avgPosition` / `keywordEstimateSearchCount` / `keywordAbaRank` / `observedAt` / `keyword` |
| sortOrder | String | No | `asc` / `desc` |

⚠️ Live validation showed the same item shape as `keywords/competitor-product-keywords`; do not assume
the semantic label implies a different wire schema.
⚠️ Live validation indicates this endpoint also behaves like a daily-observation feed exposed through a recent sliding ~7-day window.
⚠️ In skill workflows, this endpoint is a reverse-ASIN source endpoint, not a substitute for `keywords/search-results` when the question is about visible page-1 product composition.

**Response:** Array of keyword rows for an ASIN.

Key fields from live response: `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`,
`keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`, `avgPosition`,
`daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`,
`keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`,
`keywordAbaRankChangeCount`, `trafficShare`

---

## 18. /openapi/v2/keywords/product-traffic-terms-overview

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Target ASIN |
| date | String | **Yes** | Lookup date `YYYY-MM-DD`; prefer T-1 or earlier; returns the latest weekly all-keyword impression traffic-change overview on or before this date |
| marketplace | String | No | Marketplace code, default `US` |

**Response:** Single overview object **or `null`**.

Purpose:
- Shows estimated impression traffic changes across all keywords under the ASIN versus the previous period
- Current placement-level impression-point fields are paired with matching `*Prev` previous-period fields
- Lists keywords newly entering ORG first three pages and keywords dropping out of ORG first three pages

Key fields from live localhost MCP response:
`periodStartDate`, `periodEndDate`, `asin`, `site`, `organicImpressionPoint`,
`sponsoredProductImpressionPoint`, `sponsoredBrandImpressionPoint`,
`sponsoredBrandVideoImpressionPoint`, `sponsoredRecommendImpressionPoint`,
`organicImpressionPointPrev`, `sponsoredProductImpressionPointPrev`,
`sponsoredBrandImpressionPointPrev`, `sponsoredBrandVideoImpressionPointPrev`,
`sponsoredRecommendImpressionPointPrev`, `first3PagesNewOrganicKeywords`,
`first3PagesLostOrganicKeywords`.

`*Prev` fields are previous-period baselines for the matching current impression-point fields.

`first3PagesNewOrganicKeywords` and `first3PagesLostOrganicKeywords` items contain
`keyword`, `pageIndex`, and `pagePosition`.

`first3PagesNewOrganicKeywords` lists keywords newly entering ORG first three pages;
`first3PagesLostOrganicKeywords` lists keywords that dropped out of ORG first three pages.

Live validation source: `http://localhost:8080/mcp` tool
`openapi_v2_product_traffic_terms_overview`, request
`{"asin":"B01CGLCGRA","date":"2026-06-29","marketplace":"US"}`.

---

## 19. /openapi/v2/keywords/product-traffic-terms-timeline

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| asin | String | **Yes** | Target ASIN |
| keyword | String | **Yes** | Exact keyword filter |
| dateFrom | String | **Yes** | Start date `YYYY-MM-DD` |
| dateTo | String | **Yes** | End date `YYYY-MM-DD`; prefer T-1 or earlier; requested range cannot exceed 93 days |
| marketplace | String | No | Marketplace code, default `US` |
| page | Integer | No | default 1 |
| pageSize | Integer | No | default 20, max 100 |
| sortBy | String | No | `date` |
| sortOrder | String | No | `asc` / `desc` |

**Response:** Array of timeline rows.

Metric groups:
- `keyword*` fields are keyword traffic-forecast dependency data for the provided keyword's corresponding metric period, indicated by `keywordPeriodStartDate` / `keywordPeriodEndDate`
- `latest*` fields are the ASIN's latest product/listing/rank snapshot on the specified `date`
- impression-point fields, `avg*` fields, ad-activity fields, and placement observations are rolling metrics for the most recent 7 days ending at the given `date`

Diagnosis curves and events:
- Price curve: `latestPrice`
- BSR curve: `latestSmallCategoryBsr`, `latestBigCategoryBsr`
- Sales curve: `latestMonthlySaleCnt`
- Rating curve: `latestRatingAmt`, `latestRatingCnt`
- Traffic-estimate curve: impression-point fields plus `avgOrganicObservation` / `avgAdObservation`
- Keyword fields: use `keyword*` fields only as supporting context for traffic-estimate changes
- Listing events: `latestTitle` and `latestMainImageLink` changes indicate title/main-image change events

Key fields from live localhost MCP response:
`date`, `site`, `asin`, `keyword`, `latestTitle`, `latestPrice`, `latestCurrency`,
`latestLink`, `latestMainImageLink`, `latestBrandName`, `latestProductBadges`,
`latestMonthlySaleCnt`, `latestRatingAmt`, `latestRatingCnt`,
`latestSmallCategoryName`, `latestSmallCategoryBsr`, `latestBigCategoryName`,
`latestBigCategoryBsr`, `latestProductHasVideo`, `exploreTypes`,
`exploreRecommendTypes`, `organicImpressionPoint`, `sponsoredProductImpressionPoint`,
`sponsoredBrandImpressionPoint`, `sponsoredBrandVideoImpressionPoint`,
`sponsoredRecommendImpressionPoint`, `latestOrganicPosition`,
`latestOrganicPageIndex`, `latestOrganicPageSize`, `latestOrganicPageSizeReal`,
`latestOrganicPagePosition`, `latestOrganicObservedAt`, `latestAdPosition`,
`latestAdPageIndex`, `latestAdPageSize`, `latestAdPageSizeReal`,
`latestAdPagePosition`, `latestAdObservedAt`, `avgOrganicObservation`,
`avgAdObservation`, `keywordPeriodStartDate`, `keywordPeriodEndDate`,
`keywordEstimateSearchCnt`, `keywordEstimateSearchGrowthCnt`, `keywordEstimateShowCnt`,
`keywordEstimateShowGrowthCnt`, `keywordEstimateClickCnt`,
`keywordEstimateClickGrowthCnt`, `keywordEstimatePurchaseCnt`,
`keywordEstimatePurchaseGrowthCnt`, `keywordAbaRank`, `keywordAbaRankGrowthCnt`,
`keywordAbaTopClickShareRate`, `keywordAbaTopClickShareGrowthAmt`,
`keywordAbaTopConversionShareRate`, `keywordAbaTopConversionShareGrowthAmt`,
`keywordMarketCharacteristics`, `keywordTitleDensity`,
`keywordTitleDensityGrowthAmt`, `keywordTotalSkuCnt`, `keywordTotalSkuGrowthCnt`,
`keywordObservedSkuCnt`, `keywordObservedSkuGrowthCnt`, `keywordOrganicSkuCnt`,
`keywordOrganicSkuGrowthCnt`, `keywordAmazonChoiceSkuCnt`,
`keywordAmazonChoiceSkuGrowthCnt`, `keywordSponsoredProductSkuCnt`,
`keywordSponsoredProductSkuGrowthCnt`, `keywordSponsoredBrandSkuCnt`,
`keywordSponsoredBrandSkuGrowthCnt`, `keywordSponsoredBrandVideoSkuCnt`,
`keywordSponsoredBrandVideoSkuGrowthCnt`, `keywordSponsoredRecommendSkuCnt`,
`keywordSponsoredRecommendSkuGrowthCnt`, `adActiveObservationCount`,
`adActiveDayCoverageRate`, `adCampaignCnt`, `adCnt`.

Live validation source: `http://localhost:8080/mcp` tool
`openapi_v2_product_traffic_terms_timeline`, request
`{"asin":"B01CGLCGRA","keyword":"yoga mat","dateFrom":"2026-06-23","dateTo":"2026-06-29","marketplace":"US","page":1,"pageSize":20,"sortBy":"date","sortOrder":"asc"}`.

---

## Shared Product Object (products/search, competitors & brand-detail sampleProducts)

Boundary note:
- `products/search` is a query against ZooData's product-database snapshot
- It is useful for broader catalog analysis such as market winners, sales distribution, price bands, and variant concentration
- It does NOT represent Amazon live keyword SERP ordering
- Do not describe `products/search` output as "Amazon search results" or "Amazon首页结果" unless you are explicitly talking about the ZooData product database rather than the observed Amazon keyword SERP

| Field | Type | Note |
|-------|------|------|
| asin | String | |
| title | String | |
| brand | String | |
| price | Float | Top-level (unlike realtime) |
| bsr | Integer | BSR rank (NOT `bsr` or `bestsellersRank`) |
| monthlySalesFloor | Integer | Lower-bound monthly sales |
| monthlyRevenueFloor | Float | Monthly revenue lower bound |
| salesGrowthRate | Float | Growth rate |
| rating | Float | 0-5 |
| ratingCount | Integer | NOT `reviewCount` |
| fbaFee | Float | |
| sellerCount | Integer | |
| variantCount | Integer | |
| fulfillment | String | FBA/FBM/AMZ |
| listingDate | String | |
| buyBoxSellerName | String | |
