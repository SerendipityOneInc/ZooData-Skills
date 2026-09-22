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
| 8 | `markets/structure-profile` | Selected Top 100 distribution |
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

All three endpoints support only US. Resolve a human category path through `categories` to obtain a category ID. The selected sample contains at most 100 products. Use `sampleType=unitSalesTop100` or `revenueTop100` consistently. `markets/search` uses nested `category` row selectors; structure-profile and history use a top-level `includeDescendantCategoryProducts` boolean. Search `newProductPeriod` selects a 1/3/6/12-month window for filters and sorting only; all four windows are returned, and structure-profile/history do not accept this selector.

### markets/search — discovery

Optional `category.ids` selects 1–100 market row IDs; a complete `category.path` or exact `category.name` is an alternative. `category.includeDescendantCategoryProducts` defaults to true and changes each row's product population, not the selected row list. Put metric conditions inside `filters`; they apply before pagination. Top-level `date`, `sampleType`, `topN`, `newProductPeriod`, `page`, `pageSize` (1–100), `sortBy`, and `sortOrder` control snapshots and ordering. Response `data[]` holds category identity and separate `marketTotal` (full-category) and `marketSample` (selected Top 100) objects. Both scopes return `newProductMetrics[]` for `periodMonths=1,3,6,12`; the sample also returns `productTopNMetrics[]` and `brandTopNMetrics[]` for N=3/5/10/20. There are no flat `total*`/`sample*` fields or fixed Top 10 fields. `meta.total` counts matching market rows after the category and metric filters. For one snapshot, send `category.ids=[ID]`, `pageSize=1`, and verify the returned ID. For a child-market comparison, obtain child IDs through `categories` and submit them together. Keep whole-category and Top 100 denominators separate.

### markets/structure-profile — one distribution

Required: `categoryId`, `dimension` (`brand`, `seller`, `price`, `sellerCountry`, `fulfillment`, `ratingCount`, `rating`, `listingAge`, `listingYear`, `productFeature`). Optional: `includeDescendantCategoryProducts`, `sampleType`, `date`. Response `data.buckets[]` describes the selected Top 100 only, with bucket label, SKU/sales/revenue measures and shares, Amazon self-operated measures, four-window `newProductMetrics[]`, example ASINs, and dimension-specific fields. `data.sampleSkuCount` is the product-share denominator.

### markets/history — month-end series

Required: `categoryId`, `dateFrom`, `dateTo`. Optional: `includeDescendantCategoryProducts`, `sampleType`. Response `data.points[]` is ascending available month-end snapshots; absent months are omitted. Each point contains `marketTotal` and `marketSample` size, monthly sales/revenue, averages, and four-window `newProductMetrics[]`. The upgraded response does not supply MoM/YoY fields. Check `resolvedDateFrom`/`resolvedDateTo`.

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
| Monthly Sales | `marketTotal.monthlySales` / `marketSample.monthlySales` | `monthlySalesFloor` | ❌ | ❌ | per-band avg | per-brand | historical |
| Revenue | `marketTotal.monthlyRevenue` / `marketSample.monthlyRevenue` | `monthlyRevenueFloor` | ❌ | ❌ | ❌ | ❌ | ❌ |
| Price | `marketSample.medianPrice` | `price` | `buyboxWinner.price` | ❌ | band range | ❌ | historical |
| BSR | ❌ | `bsr` (integer) | `bestsellersRank` (array) | ❌ | ❌ | ❌ | historical |
| Rating | `marketSample.avgRating` | `rating` | `rating` | `avgRating` | ❌ | ❌ | historical |
| Review Count | `marketSample.avgRatingCount` | `ratingCount` | `ratingCount` | `reviewCount` | ❌ | ❌ | ❌ |
| Sentiment | ❌ | ❌ | ❌ | `sentimentDistribution` | ❌ | ❌ | ❌ |
| Consumer Insights | ❌ | ❌ | ❌ | `consumerInsights` (11 dims) | ❌ | ❌ | ❌ |
| Top 10 brand sales share | `marketSample.brandTopNMetrics[brandTopN=10].monthlySalesRate` | ❌ | ❌ | ❌ | ❌ | per-brand share | ❌ |
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
