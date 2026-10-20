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

This is the SPU contract defined by the service schemas dated 2026-10-20. Inspect the active OpenAPI/MCP schema before live use; a deployment still exposing the older three-route market contract is incompatible. Do not silently use SKU fields or substitute the retired route.

All 14 market endpoints use SPU (parent-product) grain: variants of the same product are merged. Only US is supported. Money is already USD; rates are fractions. Public floating metrics are rounded to two decimals, midpoint away from zero; integers and null remain unchanged. Filtering and sorting use these same rounded values. A returned zero is a value, not missingness. `avgProductReviewCnt` is unavailable; use the documented rating-count field where appropriate, without inventing a separate review metric.

| Endpoint | CLI command |
|---|---|
| `markets/profile` | `market-profile` |
| `markets/price-distributions` | `market-price-distributions` |
| `markets/rating-distributions` | `market-rating-distributions` |
| `markets/rating-count-distributions` | `market-rating-count-distributions` |
| `markets/listing-age-distributions` | `market-listing-age-distributions` |
| `markets/fulfillment-distributions` | `market-fulfillment-distributions` |
| `markets/seller-country-distributions` | `market-seller-country-distributions` |
| `markets/content-distributions` | `market-content-distributions` |
| `markets/top-product-concentrations` | `market-top-product-concentrations` |
| `markets/brand-concentrations` | `market-brand-concentrations` |
| `markets/seller-concentrations` | `market-seller-concentrations` |
| `markets/listing-launch-trend` | `market-listing-launch-trend` |

### Search request and response

`markets/search` accepts nested `category.ids` (1–100 exact IDs), `category.path` (1–10 warehouse hierarchy names, a prefix including descendant market rows), or `category.name` (exact node name), mutually exclusive. Optional `categoryKeyword` takes 1–200 characters and matches a literal case-insensitive substring at any categoryPath level, including literal %, _ and quotes. It does not require category-directory expansion. Top-level `includeDescendantCategoryProducts` defaults to true and controls the product population inside each market row, independently of the selected rows. Parent and descendant rows can overlap. Canonical search also accepts top-level categoryIds, mutually exclusive with nested locators. All search conditions are ANDed except sellerCountryCodes (OR). Search filters and its inclusion boolean may be null; the effective omitted/null inclusion scope is descendant-inclusive. Detail/history inclusion must be a real boolean and cannot be null.

`dateRange=30d` resolves the latest common SPU publication within the last seven days; `YYYY-MM` selects an exact published month end. Canonical search uses dateRange. Legacy `date` / `snapshotDate` are translated to latest-current-month or historical month-end selection; they do not request an arbitrary exact daily snapshot. The returned `snapshotDate` is authoritative. `sampleType=unitSalesTop100|revenueTop100` selects at most 100 SPUs. `topN=3|5|10|20` (default 10) and `newProductPeriod=1|3|6|12` (default 3) select dynamic Top N and new-product metric aliases; all fixed cutoffs/windows remain returned. `page` is 1-based (default 1), `pageSize` is 1–100 (default 20), `sortOrder=asc|desc` (default desc). Filters and sorting apply before pagination. `meta.total` counts matching markets, not products.

Each of 192 numeric `filters` fields takes `{min?, max?}`, with finite inclusive bounds and min <= max. Money bounds use USD and rates use fractions. `filters.sellerCountryCodes` is a list of 1–100 country codes. The same 192 numeric names are allowed in `sortBy`; default sort is `avgProductMonthlySaleAmt` descending. The service also translates known legacy flat/grouped Min/Max filters into these ranges, rejecting conflicting old/new values. New CLI requests use canonical ranges only.

Response `data[]` contains flat Product fields, not `marketTotal` / `marketSample`: `totalProductCnt`, `totalMonthlySaleCnt`, `totalMonthlySaleAmt`; `sampleProductCnt`, `sampleMonthlySaleCnt`, `sampleMonthlySaleAmt`; `avgProductMonthlySaleCnt`, `avgProductMonthlySaleAmt`, `avgProductPrice30d`, `avgProductRatingAmt`, `avgProductRatingCnt`, `observedSellerCnt`, `sampleBrandCnt`, fulfillment/content fields, fixed `top3/5/10/20*`, fixed `totalMonth1/3/6/12NewProduct*` and `sampleMonth1/3/6/12NewProduct*`, plus selected `topN*` and `sampleNewProduct*` aliases. Identity is `categoryId`, `categoryName`, `categoryPath`, `categoryIdPath`, `includeDescendantCategoryProducts`, `sampleType`, `site`, `currency`, `snapshotDate`. Preserve missing paths instead of constructing one. SPU grain is specified by the endpoint contract; there is no `productGrain` response field.

### Profile, distributions, concentration and launch cohort

All twelve detail routes accept `categoryIds` (1–100), strict boolean `includeDescendantCategoryProducts` (default true), `sampleType` (default unitSalesTop100), `marketplace=US`, and optional `date`. Omitted date resolves the latest common publication in seven days; explicit date requires an exact common snapshot and does not fall back to yesterday. Responses are `data[]`, each market independent. Each ID must be nonempty and at most 128 characters. The singular `categoryId` remains an identity alias. Detail/history do not accept `categoryScope` or a nested category scope. Search alone normalizes legacy top-level categoryId/categoryPath/categoryName, category.id/scope, nested category.includeDescendantCategoryProducts, categoryScope, legacy metric/sort names and sample aliases before validation; conflicts fail validation. Positive legacy Nd date ranges select the latest snapshot. A legacy date selector takes precedence over a 30d window; conflicting explicit historical-month selectors are rejected. These compatibility inputs are not additional CLI flags or legacy response shapes. Responses normalize `sampleType` to `unitSalesTop100|revenueTop100`, never warehouse enum values. Category name/ID paths are preserved across detail routes.

`profile` returns `marketSize` (productCnt, monthlySaleCnt/Amt, newProductProfile), and `sampleProfile` (productCnt, monthlySaleCnt/Amt, avgProductMonthlySaleCnt/Amt, price, rating, seller/content measures, newProductProfile and concentrationProfile). All sample totals are inside `sampleProfile`, with no top-level sample totals. Its per-SPU averages divide sample totals by productCnt before rounding; missing totals or a missing/zero count produce null. Profile windows use `windowMonths`; concentration profile arrays are `topnProductMetrics`, `topnBrandMetrics`, `topnSellerMetrics`, `topnSellerCountryMetrics`, with `topN` identities.

The seven distribution responses use `priceDistribution`, `ratingDistribution`, `ratingCountDistribution`, `listingAgeDistribution`, `fulfillmentDistribution`, `sellerCountryDistribution`, or `contentDistribution` inside each market row. Buckets use `bucketProductCnt` / `bucketProductRate`, `monthlySaleCnt` / `monthlySaleCntRate`, `monthlySaleAmt` / `monthlySaleAmtRate` as applicable; fields differ by dimension. Root and nested warehouse response fields are optional and nullable; response data is an array, not a guarantee that every nested array is present. Do not expect a universal buckets object. Content and seller-country memberships overlap. Fulfillment uses the market-representative SPU bucket; unknown fulfillment remains in the denominator.

`top-product-concentrations` and `seller-concentrations` return `topnMetrics`; brand concentration returns `topnBrandMetrics`. Detail lists are `topProducts`, `sellerList`, and `topnBrandList`, respectively, with at most 20 leading entities. All four cutoffs are returned, each with `monthlySaleCnt` and `monthlySaleAmt` totals for its ranked group under either sampleType. These are group totals, not per-product means. Entity-detail shares retain `saleCntRate` / `saleAmtRate`; those names do not apply to distribution buckets. `concentrationRate` uses quantity for unitSalesTop100 and revenue for revenueTop100.

`listing-launch-trend` additionally takes `granularity=month|year` (default month). Rows identify `snapshotDate`, `listingPeriod`, and `productCnt`: launch cohorts within the selected snapshot, not snapshots of historic demand.

`markets/structure-profile` is retired: HTTP 410 with dimension-specific migration guidance; no charge, absent from active discovery. There is no bundled `market-structure-profile` command. `markets/overview` is absent.

### History

`markets/history` takes `categoryIds`, strict boolean `includeDescendantCategoryProducts` (default true), `sampleType`, `marketplace=US`, required `dateFrom` and `dateTo` (ordered dates). Its request schema has no `date` property: even `date=null` is rejected, as is `newProductPeriod`. Legacy startDate/endDate map to dateFrom/dateTo; supplying both old and new date names is rejected. Response `data[]` contains market series: `site`, `category={id,path,idPath}`, `includeDescendantCategoryProducts`, `sampleType`, `currency`, and `history[]`. Each history point has `snapshotDate`, `marketSize` and `sampleProfile`. Points are ordered by actual snapshotDate ascending. Series are separated by site, category ID and both paths, scope, sample type and currency; a path change can produce multiple series for the same category ID. Empty results return data=[].

History `marketSize` and `sampleProfile` each expose `productCnt`, `monthlySaleCnt`, `monthlySaleAmt`, respectively for the full market and selected sample. The sample additionally has minPrice30d / avgProductPrice30d / maxPrice30d, minProductRatingAmt / avgProductRatingAmt / maxProductRatingAmt, and minProductRatingCnt / avgProductRatingCnt / maxProductRatingCnt. It does not expose profile's monthly per-SPU averages. Nested blocks can be null. There is no points envelope, resolvedDateFrom/To, new-product history, distribution, or server MoM/YoY. Missing SPU snapshots stay absent; old SKU history is never substituted.

Market reads cost 1 credit per call in this contract, including a batch of IDs. Read actual `meta.creditsConsumed` and `meta.creditsRemaining` when returned.

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
| `ratingCount` | int | Review count |
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
| `ratingCount` | int | Current review count |
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
| Brand concentration | brand-overview (sampleTop10BrandSalesRate) | markets/search (top10BrandMonthlySaleCntRate) |
| Price distribution | price-band-detail | products/search (price field) |
| Competition level | markets/search (`top10ProductMonthlySaleCntRate`, selected Top 100 sales) | brand-detail (top brand shares) |
| Consumer demand | reviews/analysis | products (sales + growth) |
| Avg rating quality | markets/search (avgProductRatingAmt) | brand-overview (sampleTop10AvgRating) |
