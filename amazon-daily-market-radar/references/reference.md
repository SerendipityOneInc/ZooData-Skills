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

This is the SPU contract defined by the service schemas dated 2026-10-16. Inspect the active OpenAPI/MCP schema before live use; a deployment still exposing the older three-route market contract is incompatible. Do not silently use SKU fields or substitute the retired route.

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

`markets/search` accepts nested `category.ids` (1–100 exact IDs), `category.path` (warehouse hierarchy prefix including descendant market rows), or `category.name` (exact node name), mutually exclusive. Optional `categoryKeyword` matches a literal case-insensitive substring at any categoryPath level, including literal %, _ and quotes. It does not require category-directory expansion. `category.includeDescendantCategoryProducts` defaults to true and controls the product population inside each market row, independently of the selected rows. Parent and descendant rows can overlap.

`dateRange=30d` resolves the latest common SPU publication within the last seven days; `YYYY-MM` selects an exact published month end. Search does not accept `date`. The returned `dt` is authoritative. `sampleType=unitSalesTop100|revenueTop100` selects at most 100 SPUs. `topN=3|5|10|20` and `newProductPeriod=1|3|6|12` select dynamic Top N and new-product metric aliases; all fixed cutoffs/windows remain returned. `page` is 1-based, `pageSize` is 1–100, `sortOrder=asc|desc`. Filters and sorting apply before pagination. `meta.total` counts matching markets, not products.

Each of 192 numeric `filters` fields takes `{min?, max?}`, with finite inclusive bounds and min <= max. Money bounds use USD and rates use fractions. `filters.sellerCountryCodes` is a nonempty list of country codes. The same 192 numeric names are allowed in `sortBy`; default sort is `avgProductMonthlySaleAmt` descending. Old flat Min/Max filters are not accepted.

Response `data[]` contains flat Product fields, not `marketTotal` / `marketSample`: `totalProductCnt`, `totalMonthlySaleCnt`, `totalMonthlySaleAmt`; `sampleProductCnt`, `sampleMonthlySaleCnt`, `sampleMonthlySaleAmt`; `avgProductMonthlySaleCnt`, `avgProductMonthlySaleAmt`, `avgProductPrice30d`, `avgProductRatingAmt`, `avgProductRatingCnt`, `observedSellerCnt`, `sampleBrandCnt`, fulfillment/content fields, fixed `top3/5/10/20*`, fixed `totalMonth1/3/6/12NewProduct*` and `sampleMonth1/3/6/12NewProduct*`, plus selected `topN*` and `sampleNewProduct*` aliases. Identity is `categoryId`, `categoryName`, `categoryPath`, `categoryIdPath`, `categoryScope`, `sampleType`, `site`, `currency`, `dt`, `productGrain=SPU`. Preserve missing paths instead of constructing one.

### Profile, distributions, concentration and launch cohort

All twelve detail routes accept `categoryIds` (1–100), `categoryScope=direct|subtree` (default subtree), `sampleType`, `marketplace=US`, and optional `date`. Omitted date resolves the latest common publication in seven days; explicit date requires an exact common snapshot and does not fall back to yesterday. Responses are `data[]`, each market independent. Legacy `categoryId` and `includeDescendantCategoryProducts` are accepted by the service as identity aliases; new CLI calls send the canonical form.

`profile` returns `marketSize` (productCnt, monthlySaleCnt/Amt, newProductProfile), top-level sample totals, and `sampleProfile` (price, rating, seller/content measures, newProductProfile and concentrationProfile). Profile windows use `windowMonths`; concentration profile arrays are `topnProductMetrics`, `topnBrandMetrics`, `topnSellerMetrics`, `topnSellerCountryMetrics`, with `topN` identities.

The seven distribution responses use `priceDistribution`, `ratingDistribution`, `ratingCountDistribution`, `listingAgeDistribution`, `fulfillmentDistribution`, `sellerCountryDistribution`, or `contentDistribution` inside each market row. Buckets use `membershipProductCnt` / `productMembershipRate`, `monthlySaleCnt` / `saleCntRate`, `monthlySaleAmt` / `saleAmtRate` as applicable; fields differ by dimension. Do not expect a universal buckets object. Content and seller-country memberships overlap. Fulfillment uses the market-representative SPU bucket; unknown fulfillment remains in the denominator.

`top-product-concentrations` and `seller-concentrations` return `topnMetrics`; brand concentration returns `topnBrandMetrics`. Detail lists are `topProducts`, `sellerList`, and `topnBrandList`, respectively, with at most 20 leading entities. All four cutoffs are returned. `concentrationRate` uses quantity for unitSalesTop100 and revenue for revenueTop100.

`listing-launch-trend` additionally takes `granularity=month|year` (default month). Rows identify `snapshotDt`, `listingPeriod`, and `productCnt`: launch cohorts within the selected snapshot, not snapshots of historic demand.

`markets/structure-profile` is retired: HTTP 410 with dimension-specific migration guidance; no charge, absent from active discovery. There is no bundled `market-structure-profile` command. `markets/overview` is absent.

### History

`markets/history` takes `categoryIds`, `categoryScope`, `sampleType`, `marketplace=US`, required `dateFrom` and `dateTo` (ordered dates). It does not accept a snapshot `date` or `newProductPeriod`. Returns flat `data[]` rows with actual `dt`, category identity, `totalProductCnt`, `sampleProductCnt`, `sampleMonthlySaleCnt/Amt`, price and rating core fields. It has no points envelope, resolvedDateFrom/To, full-market sales, new-product history, distributions, or server MoM/YoY. Missing SPU snapshots stay absent; old SKU history is never substituted.

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
