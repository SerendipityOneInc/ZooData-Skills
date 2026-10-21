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

The market contract follows the current MCP descriptions, inputSchema and outputSchema. Inspect the connected service's tools/list before live MCP use; cached tool definitions and another deployment's documentation may describe a different version. Use the configured service for verification.

All 14 market endpoints use SPU (parent-product / Amazon Listing) grain: variants of the same product are merged. Only US is supported. Money is already USD; rates are fractions. Public floating metrics are rounded to two decimals, midpoint away from zero; integers and null remain unchanged. Filtering and sorting use these same rounded values. A returned zero is a value, not missingness. `avgReviewCount` is unavailable; rating count is not written-review count.

### Search request and response

`resolvedDate` records the actual business date of returned market data. Keep it distinct from the requested `date`, which selects data and can resolve to a different business date. Launch composition instead uses its returned first-launch periods; its contract does not require an additional data-date field.

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

Distribution bucket shares use the selected sample as denominator. Top N new-product monthlySalesRate/monthlyRevenueRate use their ranked group sales/revenue denominators. Price bands use inclusive lower and exclusive upper bounds; compare actual bounds because band codes can change across markets or dates. Use documented bucket-code rules for other dimensions.

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
| Monthly Sales | `totalMonthlySales` / `sampleMonthlySales` | `monthlySalesFloor` | ❌ | ❌ | per-band avg | per-brand | historical |
| Revenue | `totalMonthlyRevenue` / `sampleMonthlyRevenue` | `monthlyRevenueFloor` | ❌ | ❌ | ❌ | ❌ | ❌ |
| Price | `medianProductPrice` | `price` | `buyboxWinner.price` | ❌ | band range | ❌ | historical |
| BSR | `avgBigBsr30d` (sample average; search filter/sort supported) | `bsr` (individual product, integer) | `bestsellersRank` (array) | ❌ | ❌ | ❌ | historical |
| Rating | `avgRating` | `rating` | `rating` | `avgRating` | ❌ | ❌ | historical |
| Rating count | `avgRatingCount` (平均评分数) | `ratingCount` | `ratingCount` | ❌ | ❌ | ❌ | ❌ |
| Written-review count | ❌ | ❌ | ❌ | `reviewCount` | ❌ | ❌ | ❌ |
| Sentiment | ❌ | ❌ | ❌ | `sentimentDistribution` | ❌ | ❌ | ❌ |
| Consumer Insights | ❌ | ❌ | ❌ | `consumerInsights` (11 dims) | ❌ | ❌ | ❌ |
| Top 10 brand sales share | `top10BrandMonthlySalesRate` | ❌ | ❌ | ❌ | ❌ | per-brand share | ❌ |
| Seller | ❌ | `buyBoxSellerName` (string) | `buyboxWinner` (object) | ❌ | ❌ | ❌ | ❌ |
| Features/Bullets | ❌ | ❌ | `features` | ❌ | ❌ | ❌ | ❌ |

## Common Field Name Mistakes

- Product rating totals use `ratingCount`; market sample averages use `avgRatingCount`. Keep the separate review-analysis `reviewCount` field in its own context.
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
