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
| categoryPath | String | Exact path lookup |
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
| mode | String | 14 preset modes (see SKILL.md) |
| keywordMatchType | String | `fuzzy` / `phrase` / `exact` |
| listingAge | **String** | Max age in days ⚠️ must be string |

Filter pairs (all optional, Min/Max): `monthlySales`, `revenue`, `salesGrowthRate`, `bsr`, `subBsr`, `bsrGrowthRate`, `price`, `rating`, `ratingCount`, `fbaShipping`, `variantCount`, `grossMargin`, `sellerCount`

Additional: `includeBrands`, `excludeBrands`, `fulfillment` (`["FBA"]`/`["FBM"]`), `badges` (`["New Release"]`/`["Best Seller"]`)

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

These endpoints were live-validated against the current OpenAPI surface.

Tool-surface note:
- API documentation and live endpoint availability do not guarantee that the current agent session exposes matching callable tools
- For skill execution, verify the live tool surface first; use this file for parameter and field confirmation after that

## 12. /openapi/v2/keywords/detail

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Keyword to inspect |
| date | String | **Yes** | Lookup date `YYYY-MM-DD`; resolves to the nearest available weekly snapshot at or before that date |
| marketplace | String | No | Marketplace code, default `US` |

⚠️ Live behavior: `success: true` may still return `data: null` when no matching weekly snapshot record is available for that keyword.

**Response:** Single keyword snapshot object **or `null`**.

Key fields: `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`,
`marketCharacteristics`, `totalSkuCnt`, `brandCount`, `organicSkuCount`, `adCampaignCount`, `adCount`,
`periodStartDate`, `periodEndDate`, `observedAt`

---

## 13. /openapi/v2/keywords/trend

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| keyword | String | **Yes** | Keyword to inspect |
| dateFrom | String | **Yes** | Start date `YYYY-MM-DD` |
| dateTo | String | **Yes** | End date `YYYY-MM-DD` |
| marketplace | String | No | Marketplace code, default `US` |

**Response:** Array of weekly-granularity trend points across the requested date range.

Interpretation note:
- `keywords/trend` is weekly series data; do not compare it to daily SERP observations as if they were the same grain

Key fields: `observedAt`, `periodStartDate`, `periodEndDate`, `estimateSearchCount`,
`estimateSearchChangeCount`, `estimateSearchChangeRate`, `abaRank`, `prevAbaRank`,
`prevEstimateSearchCount`, `rankChangeCount`

---

## 14. /openapi/v2/keywords/extends

| Parameter | Type | Required | Note |
|-----------|------|----------|------|
| query | String | **Yes** | Seed keyword |
| date | String | **Yes** | Lookup date `YYYY-MM-DD`; resolves to the nearest available weekly snapshot at or before that date |
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
| date | String | **Yes** | Daily snapshot lookup date `YYYY-MM-DD` |
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
| date | String | **Yes** | Daily snapshot lookup date `YYYY-MM-DD` |
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
| date | String | **Yes** | Daily snapshot lookup date `YYYY-MM-DD` |
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
