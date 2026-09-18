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

All three endpoints support only US. Resolve a human category path through `categories` to obtain `categoryId`. `categoryScope=direct` selects the node itself; `subtree` includes descendants without duplicates. The selected sample contains at most 100 products. For new requests, use `sampleType=unitSalesTop100` or `revenueTop100` consistently. The MCP `markets/search` route also accepts `bySale100` / `byRevenue100` aliases and returns normalized selectors; the MCP structure-profile and history routes reject `bySale100`. The server recognizes legacy `categoryPath`, `categoryKeyword`, and `topN` filters only in a separate compatibility mode: do not combine them with `categoryScope`. The bundled CLI uses only the new parameters; the current MCP search schema requires `categoryScope` and cannot submit a pure legacy request.

### markets/search — discovery

Required: `categoryScope`. Optional exact `categoryId` or `categoryName`, `date`, `sampleType`, `page`, `pageSize` (1–100), `sortBy` (`totalMonthlySales`, `totalMonthlyRevenue`, `sampleMonthlySales`, `sampleMonthlyRevenue`), `sortOrder`. Filters include `totalMonthlySalesMin`, `totalMonthlyRevenueMin`, `sampleMonthlySalesMin`, `sampleMonthlyRevenueMin`, `sampleFbmRateMin/Max`, `sampleAPlusRateMin/Max`, `sampleAvgSellerCountMin/Max`, `newProductMonthlyRevenueMin/Max`, `newProductRatingCountMin/Max`, `newProductRatingMin/Max`, and `sellerCountry`. Response `data[]` holds category identity, full-category `total*` size/sales/revenue, and selected `sample*` coverage, price, brand/seller, rating, new-product, and concentration metrics. `meta.total` is the total matching market count. For one market snapshot, filter by exact `categoryId` with `pageSize=1` and use the matching row; keep full-category and Top 100 denominators separate. `categoryName` is exact match, not keyword search.

### markets/structure-profile — one distribution

Required: `categoryId`, `dimension` (`brand`, `seller`, `price`, `sellerCountry`, `fulfillment`, `ratingCount`, `rating`, `listingAge`, `listingYear`, `productFeature`). Optional: `categoryScope`, `sampleType`, `date`. Response `data.buckets[]` describes the selected Top 100 only, with bucket label, `skuCount`/`skuRate`, sales/revenue and their shares, plus dimension-specific fields. `data.sampleSkuCount` is the denominator.

### markets/history — month-end series

Required: `categoryId`, `startDate`, `endDate`. Optional: `categoryScope`, `sampleType`. Response `data.points[]` is ascending available month-end snapshots; absent months are omitted. Points include full-category and Top 100 size/sales/revenue, conservative six-month new-product measures, and MoM/YoY rates when comparable baselines exist. Check `actualStartDate`/`actualEndDate`.

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
| Price | `sampleMedianPrice` | `price` | `buyboxWinner.price` | ❌ | band range | ❌ | historical |
| BSR | ❌ | `bsr` (integer) | `bestsellersRank` (array) | ❌ | ❌ | ❌ | historical |
| Rating | `sampleAvgRating` | `rating` | `rating` | `avgRating` | ❌ | ❌ | historical |
| Review Count | `sampleAvgRatingCount` | `ratingCount` | `ratingCount` | `reviewCount` | ❌ | ❌ | ❌ |
| Sentiment | ❌ | ❌ | ❌ | `sentimentDistribution` | ❌ | ❌ | ❌ |
| Consumer Insights | ❌ | ❌ | ❌ | `consumerInsights` (11 dims) | ❌ | ❌ | ❌ |
| Top 10 brand sales share | `sampleTop10BrandSalesRate` | ❌ | ❌ | ❌ | ❌ | per-brand share | ❌ |
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
