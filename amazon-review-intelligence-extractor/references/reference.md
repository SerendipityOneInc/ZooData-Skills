# ZooData API Field Reference

> Load this file only when you need exact field names or response structure.

## ZooData Endpoint Field Reference

> Shared field reference. This skill's workflows use ONLY the subcommands
> listed in its SKILL.md; the endpoints below are documented for field-name /
> response-structure lookup, not as a claim that this skill invokes all of them.

| # | Endpoint | Purpose |
|---|----------|---------|
| 1 | `categories` | Category path lookup |
| 2 | `markets/search` | Paginated discovery or exact category snapshot |
| 3 | `products/search` | Product supply (100+ via pagination), brand/price drill |
| 4 | `products/competitors` | Top competitor list |
| 5 | `realtime/product` | Live product detail |
| 6 | `reviews/analysis` | Consumer pain points, buying factors |
| 7 | `products/price-band-overview` | Price-band opportunity overview |
| 8 | `products/price-band-detail` | Per-band SKU/sales/brand/rating breakdown |
| 9 | `products/brand-overview` | Brand count, CR10, top-brand avg price/rating |
| 10 | `products/brand-detail` | Per-brand SKU/sales/revenue/share ranking |
| 11 | `products/history` | 30-day price/BSR/sales trend |
| 12 | `markets/profile` | SPU market profile and independent distribution routes |
| 13 | `markets/history` | Available month-end category history |

Base URL: `https://api.zoodata.ai/openapi/v2`
Auth: `Bearer $ZOODATA_API_KEY`
Method: All POST with JSON body
All endpoints return: `{success, data, error, meta}` with `meta.creditsRemaining`

---

## 1. categories

**Request:** (mutually exclusive modes)
- No params → root categories
- `categoryKeyword`: String → search by keyword
- `categoryPath`: List<String> → exact path
- `parentCategoryPath`: List<String> → child categories

**Response:**
| Field | Type | Used For |
|-------|------|----------|
| `categoryId` | string | Category ID |
| `categoryName` | string | Category name |
| `categoryPath` | list | Full path from root |
| `hasChildren` | bool | Has subcategories |
| `level` | int | Depth (1=root) |
| `productCount` | int | Products in category |

---

## 2. Market endpoints

The market contract follows the current MCP descriptions, inputSchema and outputSchema. Inspect the connected service's tools/list before live MCP use; cached tool definitions and another deployment's documentation may describe a different version. Use the configured service for verification.

All 14 market endpoints use SPU (parent-product / Amazon Listing) grain: variants of the same product are merged. Only US is supported. Money is already USD; rates are fractions. Public floating metrics are rounded to two decimals, midpoint away from zero; integers and null remain unchanged. Filtering and sorting use these same rounded values. A returned zero is a value, not missingness. `avgReviewCount` is unavailable; rating count is not written-review count.

### Search request and response

`markets/search` accepts nested `category.ids` (1–100 exact IDs), `category.path` (1–10 hierarchy names, matching a path prefix), or `category.name` (exact name), mutually exclusive. Top-level `categoryIds` is an alternative to nested locators. `categoryKeyword` is a literal case-insensitive substring at any categoryPath level. Top-level `includeDescendantCategoryProducts` controls product coverage inside each market, independently of market-row selection; omitted/null means descendant-inclusive. Parent and child markets can overlap. Other market requests require a real boolean, default true.

Search uses optional `date` as a cutoff: omit for the latest common published snapshot, or select the most recent common snapshot on or before the supplied valid YYYY-MM-DD. Historical snapshots start at 2026-02 and are month ends; the cutoff need not be a month end. If none is available before the cutoff, data is empty. Read actual `resolvedDate`. The current inputSchema has no `dateRange`. This cutoff differs from the exact-date contract of profile/distribution/concentration routes.

`sampleType=unitSalesTop100|revenueTop100` selects up to 100 Listings. `topN=3|5|10|20` (default 10) and `newProductPeriod=1|3|6|12` (default 3) select dynamic metric aliases; fixed cutoffs/windows remain returned. Page starts at 1, pageSize is 1–100 (default 20). Filters and ordering apply before pagination; meta.total counts matching markets, not products.

`filters` has 28 numeric Min/Max pairs, expressed as flat fields, for example `{"avgPriceMin":10,"avgPriceMax":50}`. Bounds are inclusive and finite, either side may be omitted, and min must not exceed max. Nested `{min,max}` metric objects are not the canonical public schema. `sellerCountryCodes` is a list of 1–100 codes (OR); other conditions combine with AND. Sort supports 192 numeric response metrics, independently of the smaller filter set; default avgMonthlyRevenue descending. A sortable metric is not necessarily filterable.

Response `data[]` contains flat fields: `totalProductCount`, `totalMonthlySales`, `totalMonthlyRevenue` for the full market; `sampleProductCount`, `sampleMonthlySales`, `sampleMonthlyRevenue` for the sample; `avgMonthlySales`, `avgMonthlyRevenue`, prices, ratings and seller/content metrics. Fixed `top3/5/10/20*`, `totalMonth1/3/6/12NewProduct*`, `sampleMonth1/3/6/12NewProduct*` and selected dynamic aliases remain distinct. Identity is categoryId/name/path, categoryIdPath, includeDescendantCategoryProducts, sampleType, site, currency and `resolvedDate`. Preserve missing paths. No productGrain response field is required.

### Profile, distributions and concentration

The eleven profile/distribution/concentration routes accept categoryIds (1–100), includeDescendantCategoryProducts (strict boolean, default true), sampleType (default unitSalesTop100), marketplace=US and optional `date`. Omit date for the latest common publication; an explicit date requires an exact common snapshot, with empty data on an unpublished date. There is no yesterday fallback. Each ID selects an independent market in data[]. Category IDs are nonempty and at most 128 characters; the service deduplicates them. Detail/history/launch inputSchema has no categoryScope or nested scope. Search alone normalizes legacy inputs; such compatibility does not add CLI options or restore old responses. Use current MCP inputSchema when constructing MCP arguments.

`profile` returns `marketSize` (full-market productCount, monthlySales, monthlyRevenue and newProductProfile) and `sampleProfile` (sample productCount, monthlySales, monthlyRevenue, avgMonthlySales, avgMonthlyRevenue, price, rating, seller/content measures, newProductProfile and concentrationProfile). Profile has no top-level sample totals. Windows use windowMonths; concentrationProfile arrays are topnProductMetrics, topnBrandMetrics, topnSellerMetrics and topnSellerCountryMetrics, with topN identities.

The seven distributions use `priceDistribution`, `ratingDistribution`, `ratingCountDistribution`, `listingAgeDistribution`, `fulfillmentDistribution`, `sellerCountryDistribution` or `contentDistribution`. Each market also returns sampleProductCount, sampleMonthlySales, sampleMonthlyRevenue and `sampleAvgPrice`, `sampleAvgMonthlySales`, `sampleAvgMonthlyRevenue`, `sampleAvgRating`, `sampleAvgRatingCount` at the root. Bucket fields are `bucketProductCount`, `bucketProductRate`, `monthlySales`, `monthlySalesRate`, `monthlyRevenue`, `monthlyRevenueRate`, `avgPrice`, `avgMonthlySales`, `avgMonthlyRevenue`, `avgRating`, `avgRatingCount`. Dimensions have different identifiers/bounds; do not expect a universal buckets object. No bucket new-product or brand-concentration block is provided. Content and seller-country memberships overlap; fulfillment uses the representative bucket with unknowns retained in its denominator.

`top-product-concentrations` and `seller-concentrations` use `topnMetrics`; brand also uses `topnMetrics`. Entity arrays are topProductList, topSellerList and topBrandList, at most 20 leading entities. Root sample totals and means use the same sample-prefixed fields as distributions. Top N rows contain productCount, concentrationRate, monthlySales, monthlyRevenue, per-product price/sales/rating means and newProductProfile. All four cutoffs return both sales totals. New-product windows have windowMonths, productCount, monthlySales, monthlyRevenue, monthlySalesRate/monthlyRevenueRate and per-product means. Entity shares use monthlySalesRate/monthlyRevenueRate, named consistently with distribution shares; retain the entity or bucket population when interpreting them. Entity rank follows sampleType; seller-country distributionRank is display order, not a sales rank. concentrationRate follows the sample's ranking metric.

Root and nested warehouse fields are optional and nullable. A nested array can be null; an empty data array, a null metric and a real zero are distinct results.

### Listing launch composition

`listing-launch-trend` accepts the common market identity and `granularity=month|year` (default month), plus optional `dateFrom` and `dateTo`. These inclusive bounds filter first-launch dates before grouping, not sample snapshot dates; if both are provided, dateFrom must not exceed dateTo. The sample always comes from the latest available snapshot. The request has no `date` property, even date=null is rejected.

Response data[] contains site, categoryId, categoryPath/idPath, includeDescendantCategoryProducts, sampleType, granularity and `points[]`. Each point has `date` (YYYY-MM or YYYY) and productCount. There is no returned resolvedDate, snapshotDate or currency. Missing periods are not filled. These are current-sample launch cohorts, not historical market growth or all products launched in those months.

`markets/structure-profile` is retired: HTTP 410 with migration guidance, no charge and absent from active discovery. There is no bundled market-structure-profile command. `markets/overview` is absent.

### History

`markets/history` takes categoryIds, includeDescendantCategoryProducts, sampleType, marketplace=US and required `dateFrom/dateTo` (valid ordered YYYY-MM-DD). Query boundaries need not be month ends. Only published month-end snapshots inside the range are returned in ascending order. A current-month-only range can be empty because no completed month end is included. There is no date property: even `date=null` is rejected, as is newProductPeriod.

Response `data[]` contains series: site, category={id,path,idPath}, includeDescendantCategoryProducts, sampleType, currency and `points[]`. Each point has `date`, `marketSize` and `sampleProfile`. Series are separated by site, category ID and paths, scope, sample type and currency; a path change can yield multiple series for one ID. Empty results return data=[].

Both nested blocks contain productCount, monthlySales and monthlyRevenue for the full market and sample respectively. The sample additionally returns avgPrice, avgMonthlySales, avgMonthlyRevenue and avgRating, avgRatingCount. No min/max price/rating fields, new-product history, distribution history or server MoM/YoY are returned. There is no top-level data.points envelope or history[] field, and no resolvedDateFrom/To; retain requested bounds locally and read actual bounds from each nonempty series' points[].date. Missing months remain absent; old SKU history is never substituted.

### Credits

Search costs 1 credit per call, including empty data. Other market reads cost 1 credit per distinct returned market (site/category ID); empty data is free. Their admission check requires balance for the distinct requested market count at the unit price without pre-deducting credits. A batch is not a flat 1-credit call. Use actual meta.creditsConsumed/Remaining and their Exact variants when returned.

---

## 3. products/search — Shared Product Object

**Key Request Params:**
- `keyword`, `categoryPath`, `keywordMatchType` (`mode` is a CLI-only preset — `zoodata.py` expands it into the filter pairs below client-side; it is NOT an API field and returns 422 if sent raw)
- Filter pairs: `monthlySalesMin/Max`, `priceMin/Max`, `ratingMin/Max`, etc.
- `pageSize` (max 20), `page`, `sortBy`, `sortOrder`
- `includeBrands`, `excludeBrands`

**Key Response Fields (per product):**
| Field | Type | Used For |
|-------|------|----------|
| `asin` | string | Product ID |
| `title` | string | Product name |
| `brandName` | string | Brand |
| `price` | float | Price |
| `monthlySalesFloor` | int | Monthly sales (lower bound) |
| `monthlyRevenueFloor` | float | Monthly revenue lower bound |
| `rating` | float | Rating (0-5) |
| `ratingCount` | int | Rating count |
| `bsr` | int | BSR (NOT `bestsellersRank`) |
| `fbaFee` | float | FBA cost |
| `sellerCount` | int | Sellers on listing |
| `fulfillment` | string | FBA/FBM/AMZ |
| `listingDate` | string | When listed |
| `salesGrowthRate` | float | Growth rate |
| `variantCount` | int | Variants |

---

## 4. products/competitors

Same response as products/search. Different use: discovery by keyword/brand/asin.
Request params: `keyword`, `brand`, `asin`, `categoryPath`, `sortBy`, `pageSize`

---

## 5. realtime/product

**Request:**
- `asin`: String (required)
- `marketplace`: String (US/UK/DE/FR/IT/ES/JP/CA/AU/IN/MX/BR, default US)

**Response:**
| Field | Type | Used For |
|-------|------|----------|
| `asin` | string | Product ID |
| `title` | string | Full title |
| `brandName` | string | Brand |
| `rating` | float | Current rating |
| `ratingCount` | int | Current rating count |
| `ratingBreakdown` | object | Star distribution {five_star: {percentage, count}, ...} |
| `features` | list | Bullet points |
| `description` | string | Product description |
| `specifications` | object | Tech specs |
| `variants` | list | All variants with dimensions |
| `bestsellersRank` | list | BSR info [{category, rank}, ...] |
| `buyboxWinner` | object | Buy Box: {price, fulfillment, seller} |
| `images` | list | All image URLs |

⚠️ Does NOT have: monthlySalesFloor, fbaFee, sellerCount

---

## 6. reviews/analysis

**Request:**
- `mode`: `"asin"` or `"category"`
- `asins`: List<String> (when mode=asin)
- `categoryPath`: String (when mode=category)
- `labelType`: filter to specific dimensions. **⚠️ Only ONE value per call — do NOT comma-separate multiple types.** Make separate calls for each labelType needed.
- `period`: e.g. `"1m"` / `"3m"` / `"6m"` / `"1y"` / `"2y"`

**labelType values (one per call):** `scenarios`, `issues`, `positives`, `improvements`, `buyingFactors`, `painPoints`, `keywords`, `userProfiles`, `usageTimes`, `usageLocations`, `behaviors`

**Response:**
| Field | Type | Used For |
|-------|------|----------|
| `reviewCount` | int | Sample size |
| `avgRating` | float | Overall satisfaction |
| `sentimentDistribution` | object | Positive/neutral/negative ratio |
| `consumerInsights` | list | Structured insights by dimension |
| `topKeywords` | list | Trending terms |

**InsightItem:** `{element, labelType, count, reviewRate, avgRating}`

---

## 6b. realtime/reviews + Local Toolkit (fallback for `/reviews/analysis`)

When `/reviews/analysis` lacks aggregation (ASIN <50 reviews, or no daily snapshot),
use this endpoint + the local Map/Reduce toolkit to produce a compatible
`consumerInsights` structure.

**Request:**
- `asin`: String (10 chars, required)
- `marketplace`: String (US/UK only, default US)
- `cursor`: String (omit for first page; use previous response's `nextCursor`)

⚠️ Fixed 10 reviews/page; max 10 pages = **100 reviews** hard cap. 1 credit/page.

**Response:**
- `asin`, `reviews[]` (RealtimeReview), `nextCursor` (null = end)

**RealtimeReview:** `reviewId`, `title`, `body`, `bodyHtml`, `rating`, `author`, `date` (ISO 8601), `verifiedPurchase`, `vineProgram`, `helpfulVoteCount`, `unhelpfulVoteCount`, `reviewCountry`, `images`, `link`, `isGlobalReview`

### Local Toolkit Workflow

```
zoodata.py reviews-raw          → fetch raw reviews (one HTTP call per page, auto-paginates)
zoodata.py review-tag-prompt    → render Map prompt for one review (caller's LLM tags it)
zoodata.py review-reduce-prompt → render Reduce prompt for one dimension (caller's LLM clusters)
zoodata.py review-aggregate     → combine raw + tags + clusters → consumerInsights output
```

The aggregator output matches `/reviews/analysis` structure exactly:
`{reviewCount, avgRating, sentimentDistribution, consumerInsights[InsightItem], topKeywords[]}`.

See SKILL.md "Insufficient Data Fallback" section for full step-by-step usage.

---

## 6c. reviews/search

**Request:**
- `asin`: String (required)
- Optional filters: `ratingMin`/`ratingMax` (1-5), `verifiedOnly`, `vineOnly`, `helpfulVoteCountMin`, `dateStart`/`dateEnd` (YYYY-MM-DD)
- `sortBy`: `recent` (default) / `rating` / `helpfulVoteCount`
- `sortOrder`: `desc` (default) / `asc`
- `page` / `pageSize`: 1-indexed, pageSize 1-20 default 10

**Response:** Array of `TaggedReview` (RealtimeReview fields + `tags[{labelType, element}]` AI tags from offline pipeline).

Differs from `realtime/reviews`: BigQuery snapshot (T+1 delay) but already AI-tagged.

---

## 7. products/price-band-overview

**Request:** Same params as products/search (keyword, category, filters)

**Response:**
| Field | Type | Used For |
|-------|------|----------|
| `sampleSkuCount` | int | Total products analyzed |
| `sampleMedianPrice` | float | Median price point |
| `hottestBand` | object | Highest sales share band |
| `bestOpportunityBand` | object | Highest opportunity index band |

**Band object:** `{bandIdx, bandLabel, sampleBandMinPrice, sampleBandMaxPrice, sampleSkuCount, sampleSalesRate, sampleBrandCount, sampleTop3BrandSalesRate, sampleAvgRating, sampleOpportunityIndex}`

---

## 8. products/price-band-detail

**Response:**
- `sampleSkuCount`, `sampleTotalMonthlySales`
- `priceBands`: array of 5 band objects (same structure as above)

---

## 9. products/brand-overview

**Response:**
| Field | Type | Used For |
|-------|------|----------|
| `sampleBrandCount` | int | Total brands |
| `sampleTop10BrandSalesRate` | float | CR10 concentration (top 10 brands) |
| `sampleTop10AvgRating` | float | Top 10 brand avg rating |
| `sampleTop10AvgPrice` | float | Top 10 brand avg price |

---

## 10. products/brand-detail

**Response:**
- `sampleSkuCount`, `sampleTotalMonthlySales`, `sampleBrandCount`
- `brands`: array of brand objects

**BrandStats:** `{brandName, sampleSkuCount, sampleGroupMonthlySales, sampleGroupMonthlyRevenue, sampleSalesRate, sampleAvgPrice, minPrice, maxPrice, sampleAvgRating, sampleAvgRatingCount, sampleProducts}`

**sampleProducts:** List of Product objects for this brand within the sample. Each product contains the full Shared Product Object fields (asin, title, price, bsr, monthlySalesFloor, rating, ratingCount, fulfillment, etc). This enables brand-level product matrix analysis without a separate products/search call.

---

## 11. products/history

**Request:**
- `asins`: List<String> (required)
- `startDate`: String "YYYY-MM-DD" (required)
- `endDate`: String "YYYY-MM-DD" (required)
⚠️ Does NOT accept `dateRange` — must use startDate + endDate

**Response (array of daily snapshots):**
| Field | Type | Used For |
|-------|------|----------|
| `asin` | string | Product ID |
| `price` | float | Price on that day |
| `bsr` | int | BSR on that day |
| `subBsr` | int | Sub-category BSR |
| `recentSales` | int | Recent sales count |
| `updatedAt` | string | Unix timestamp (string) |
| `createdAt` | string | Unix timestamp (string) |

---

## Cross-Validation Matrix

| Data Point | Primary Source | Validation Source |
|-----------|---------------|-------------------|
| Market size | markets/search | products/search (total count) |
| Brand concentration | brand-overview (sampleTop10BrandSalesRate) | markets/search (top10BrandMonthlySalesRate) |
| Price distribution | price-band-detail | products/search (price field) |
| Competition level | markets/search (`top10ProductMonthlySalesRate`, selected Top 100 sales) | brand-detail (top brand shares) |
| Consumer demand | reviews/analysis | products (sales + growth) |
| Avg rating quality | markets/search (avgRating) | brand-overview (sampleTop10AvgRating) |
