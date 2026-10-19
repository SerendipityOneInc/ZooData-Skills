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
| 7 | `products/history` | 30-day price/BSR/sales trend |
| 8 | `markets/profile` | SPU market profile and independent distribution routes |
| 9 | `markets/history` | Available month-end category history |

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

This is the SPU contract defined by the service schemas dated 2026-10-19. Inspect the active OpenAPI/MCP schema before live use; a deployment still exposing the older three-route market contract is incompatible. Do not silently use SKU fields or substitute the retired route.

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

`markets/search` accepts nested `category.ids` (1–100 exact IDs), `category.path` (warehouse hierarchy prefix including descendant market rows), or `category.name` (exact node name), mutually exclusive. Optional `categoryKeyword` matches a literal case-insensitive substring at any categoryPath level, including literal %, _ and quotes. It does not require category-directory expansion. Top-level `includeDescendantCategoryProducts` defaults to true and controls the product population inside each market row, independently of the selected rows. Parent and descendant rows can overlap.

`dateRange=30d` resolves the latest common SPU publication within the last seven days; `YYYY-MM` selects an exact published month end. Search does not accept `date`. The returned `snapshotDate` is authoritative. `sampleType=unitSalesTop100|revenueTop100` selects at most 100 SPUs. `topN=3|5|10|20` and `newProductPeriod=1|3|6|12` select dynamic Top N and new-product metric aliases; all fixed cutoffs/windows remain returned. `page` is 1-based, `pageSize` is 1–100, `sortOrder=asc|desc`. Filters and sorting apply before pagination. `meta.total` counts matching markets, not products.

Each of 192 numeric `filters` fields takes `{min?, max?}`, with finite inclusive bounds and min <= max. Money bounds use USD and rates use fractions. `filters.sellerCountryCodes` is a nonempty list of country codes. The same 192 numeric names are allowed in `sortBy`; default sort is `avgProductMonthlySaleAmt` descending. Old flat Min/Max filters are not accepted.

Response `data[]` contains flat Product fields, not `marketTotal` / `marketSample`: `totalProductCnt`, `totalMonthlySaleCnt`, `totalMonthlySaleAmt`; `sampleProductCnt`, `sampleMonthlySaleCnt`, `sampleMonthlySaleAmt`; `avgProductMonthlySaleCnt`, `avgProductMonthlySaleAmt`, `avgProductPrice30d`, `avgProductRatingAmt`, `avgProductRatingCnt`, `observedSellerCnt`, `sampleBrandCnt`, fulfillment/content fields, fixed `top3/5/10/20*`, fixed `totalMonth1/3/6/12NewProduct*` and `sampleMonth1/3/6/12NewProduct*`, plus selected `topN*` and `sampleNewProduct*` aliases. Identity is `categoryId`, `categoryName`, `categoryPath`, `categoryIdPath`, `includeDescendantCategoryProducts`, `sampleType`, `site`, `currency`, `snapshotDate`. Preserve missing paths instead of constructing one. SPU grain is specified by the endpoint contract; there is no `productGrain` response field.

### Profile, distributions, concentration and launch cohort

All twelve detail routes accept `categoryIds` (1–100), strict boolean `includeDescendantCategoryProducts` (default true), `sampleType`, `marketplace=US`, and optional `date`. Omitted date resolves the latest common publication in seven days; explicit date requires an exact common snapshot and does not fall back to yesterday. Responses are `data[]`, each market independent. The singular `categoryId` remains an identity alias, but `categoryScope`, `category_scope`, and nested `category.includeDescendantCategoryProducts` are rejected. Responses normalize `sampleType` to `unitSalesTop100|revenueTop100`, never warehouse enum values. Category name/ID paths are preserved across detail routes.

`profile` returns `marketSize` (productCnt, monthlySaleCnt/Amt, newProductProfile), and `sampleProfile` (productCnt, monthlySaleCnt/Amt, avgProductMonthlySaleCnt/Amt, price, rating, seller/content measures, newProductProfile and concentrationProfile). All sample totals are inside `sampleProfile`, with no top-level sample totals. Its per-SPU averages divide sample totals by productCnt before rounding; missing totals or a missing/zero count produce null. Profile windows use `windowMonths`; concentration profile arrays are `topnProductMetrics`, `topnBrandMetrics`, `topnSellerMetrics`, `topnSellerCountryMetrics`, with `topN` identities.

The seven distribution responses use `priceDistribution`, `ratingDistribution`, `ratingCountDistribution`, `listingAgeDistribution`, `fulfillmentDistribution`, `sellerCountryDistribution`, or `contentDistribution` inside each market row. Buckets use `bucketProductCnt` / `bucketProductRate`, `monthlySaleCnt` / `monthlySaleCntRate`, `monthlySaleAmt` / `monthlySaleAmtRate` as applicable; fields differ by dimension. Do not expect a universal buckets object. Content and seller-country memberships overlap. Fulfillment uses the market-representative SPU bucket; unknown fulfillment remains in the denominator.

`top-product-concentrations` and `seller-concentrations` return `topnMetrics`; brand concentration returns `topnBrandMetrics`. Detail lists are `topProducts`, `sellerList`, and `topnBrandList`, respectively, with at most 20 leading entities. All four cutoffs are returned, each with `monthlySaleCnt` and `monthlySaleAmt` totals for its ranked group under either sampleType. These are group totals, not per-product means. Entity-detail shares retain `saleCntRate` / `saleAmtRate`; those names do not apply to distribution buckets. `concentrationRate` uses quantity for unitSalesTop100 and revenue for revenueTop100.

`listing-launch-trend` additionally takes `granularity=month|year` (default month). Rows identify `snapshotDate`, `listingPeriod`, and `productCnt`: launch cohorts within the selected snapshot, not snapshots of historic demand.

`markets/structure-profile` is retired: HTTP 410 with dimension-specific migration guidance; no charge, absent from active discovery. There is no bundled `market-structure-profile` command. `markets/overview` is absent.

### History

`markets/history` takes `categoryIds`, strict boolean `includeDescendantCategoryProducts` (default true), `sampleType`, `marketplace=US`, required `dateFrom` and `dateTo` (ordered dates). It does not accept a snapshot `date` or `newProductPeriod`. Response `data[]` contains market series: `site`, `category={id,path,idPath}`, `includeDescendantCategoryProducts`, `sampleType`, `currency`, and `history[]`. Each history point has `snapshotDate`, `marketSize` and `sampleProfile`. Points are ordered by actual snapshotDate ascending. Series are separated by site, category ID and both paths, scope, sample type and currency; a path change can produce multiple series for the same category ID. Empty results return data=[].

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
- `period`: e.g. `"1m"` / `"3m"` / `"6m"` / `"1y"` / `"2y"`

⚠️ `labelType` is **not** an API request parameter. The API returns all 11 dimensions in a single call. Filter by `labelType` client-side from the `consumerInsights` array.

**labelType values (in response):** `scenarios`, `issues`, `positives`, `improvements`, `buyingFactors`, `painPoints`, `keywords`, `userProfiles`, `usageTimes`, `usageLocations`, `behaviors`

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

## 7. products/history

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
| Consumer demand | reviews/analysis | products (sales + growth) |

---

## Cross-endpoint field identity

The interfaces return **different fields**. Do NOT assume they share the same structure.

| Data | `market` | `products`/`competitors` | `realtime/product` | `reviews/analysis` | `price-band` | `brand` | `history` |
|------|----------|--------------------------|--------------------|--------------------|-------------|---------|-------------------|
| Monthly Sales | `totalMonthlySaleCnt` / `sampleMonthlySaleCnt` | `monthlySalesFloor` | ❌ | ❌ | per-band avg | per-brand | historical |
| Revenue | `totalMonthlySaleAmt` / `sampleMonthlySaleAmt` | `monthlyRevenueFloor` | ❌ | ❌ | ❌ | ❌ | ❌ |
| Price | `medianProductPrice30d` | `price` | `buyboxWinner.price` | ❌ | band range | ❌ | historical |
| BSR | ❌ | `bsr` (integer) | `bestsellersRank` (array) | ❌ | ❌ | ❌ | historical |
| Rating | `avgProductRatingAmt` | `rating` | `rating` | `avgRating` | ❌ | ❌ | historical |
| Review Count | `avgProductRatingCnt` | `ratingCount` | `ratingCount` | `reviewCount` | ❌ | ❌ | ❌ |
| Sentiment | ❌ | ❌ | ❌ | `sentimentDistribution` | ❌ | ❌ | ❌ |
| Consumer Insights | ❌ | ❌ | ❌ | `consumerInsights` (11 dims) | ❌ | ❌ | ❌ |
| Top 10 brand sales share | `top10BrandMonthlySaleCntRate` | ❌ | ❌ | ❌ | ❌ | per-brand share | ❌ |
| Seller | ❌ | `buyBoxSellerName` (string) | `buyboxWinner` (object) | ❌ | ❌ | ❌ | ❌ |
| Features/Bullets | ❌ | ❌ | `features` | ❌ | ❌ | ❌ | ❌ |

## Common Field Name Mistakes

- `reviewCount` → use `ratingCount`
- `bsr` → use `bsr` (products/competitors) or `bestsellersRank` (realtime, array)
- `monthlySales` → use `monthlySalesFloor`
- realtime price → `buyboxWinner.price`
- See `reference.md` → Shared Product Object for complete field list

## Data Structure Reminder

Many interfaces return `.data` as an **array**. Use `.data[0]` to get the first record for those responses, but inspect the actual payload shape first because some commands return non-array data inside `data`.

---

## Composite CLI commands

- `report --keyword X` → categories + market + products(top50) + realtime(top1)
- `opportunity --keyword X [--mode Y]` → categories + market + products(filtered) + realtime(top3)
