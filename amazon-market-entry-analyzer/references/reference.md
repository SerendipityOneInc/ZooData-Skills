# Market Entry Analyzer — API Field Reference

> Load this file only when you need exact field names or response structure.

## ZooData Endpoint Field Reference

> This skill's market-entry workflow spans all of the commerce endpoints below;
> they are documented here for field-name / response-structure lookup.

| # | Endpoint | Purpose |
|---|----------|---------|
| 1 | `categories` | Category path lookup |
| 2 | `markets/search` | Paginated category-market discovery |
| 3 | `products/search` | Product supply (100+ via pagination), brand/price drill |
| 4 | `products/competitors` | Top competitor list |
| 5 | `realtime/product` | Live product detail |
| 6 | `reviews/analysis` | Consumer pain points, buying factors |
| 7 | `products/price-band-overview` | Price-band opportunity overview |
| 8 | `products/price-band-detail` | Per-band SKU/sales/brand/rating breakdown |
| 9 | `products/brand-overview` | Brand count, CR10, top-brand avg price/rating |
| 10 | `products/brand-detail` | Per-brand SKU/sales/revenue/share ranking |
| 11 | `products/history` | 30-day price/BSR/sales trend |
| 12 | `markets/overview` | One category market snapshot |
| 13 | `markets/structure-profile` | Selected Top 100 distribution |
| 14 | `markets/history` | Available month-end category history |

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

All four endpoints support only US. Resolve a human category path through `categories` to obtain `categoryId`. `categoryScope=direct` selects the node itself; `subtree` includes descendants without duplicates. The selected sample contains at most 100 products. For new requests, use `sampleType=unitSalesTop100` or `revenueTop100`; the MCP schema still advertises `bySale100` / `byRevenue100`, and live MCP validation rejects `bySale100`. The server recognizes legacy `categoryPath`, `categoryKeyword`, and `topN` filters only in a separate compatibility mode: do not combine them with `categoryScope`. The bundled CLI uses only the new parameters; the current MCP schema requires `categoryScope` and cannot submit a pure legacy request.

### markets/search — discovery

Required: `categoryScope`. Optional exact `categoryId` or `categoryName`, `date`, `sampleType`, `page`, `pageSize` (1–100), `sortBy` (`totalMonthlySales`, `totalMonthlyRevenue`, `top100MonthlySales`, `top100MonthlyRevenue`), `sortOrder`. Filters include `totalMonthlySalesMin`, `totalMonthlyRevenueMin`, `top100MonthlySalesMin`, `top100MonthlyRevenueMin`, `top100FbmRateMin/Max`, `top100APlusRateMin/Max`, `top100AvgSellerCountMin/Max`, `newProductMonthlyRevenueMin/Max`, `newProductRatingCountMin/Max`, `newProductRatingMin/Max`, and `sellerCountry`. Response `data[]` holds category identity, full-category `total*` size/sales/revenue and a selected `top100*` summary; `meta.total` is the total matching market count. `categoryName` is exact match, not keyword search.

### markets/overview — one snapshot

Required: `categoryId`. Optional: `categoryScope`, `sampleType`, `date`. Response `data` is an object. Full category: `totalSkuCount`, `totalSpuCount`, `totalMonthlySales`, `totalMonthlyRevenue`. Selected Top 100: `top100SkuCount`, `top100MonthlySales`, `top100MonthlyRevenue`, coverage rates, `top100MedianPrice`, brand/seller counts, `top100AvgRating`, `top100AvgRatingCount`, `top100FbmRate`, `top100APlusRate`, conservative six-month new-product metrics, and Top 10 product/brand concentration rates. Keep whole-category and Top 100 denominators separate.

### markets/structure-profile — one distribution

Required: `categoryId`, `dimension` (`brand`, `seller`, `price`, `sellerCountry`, `fulfillment`, `ratingCount`, `rating`, `listingAge`, `listingYear`, `productFeature`). Optional: `categoryScope`, `sampleType`, `date`. Response `data.buckets[]` describes the selected Top 100 only, with bucket label, `skuCount`/`skuRate`, sales/revenue and their shares, plus dimension-specific fields. `data.top100SkuCount` is the denominator.

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
| Market size | markets/overview | products/search (total count) |
| Brand concentration | brand-overview (sampleTop10BrandSalesRate) | markets/overview (top100Top10BrandSalesRate) |
| Price distribution | price-band-detail | products/search (price field) |
| Competition level | markets (topSalesRate) | brand-detail (top brand shares) |
| Consumer demand | reviews/analysis | products (sales + growth) |
| Avg rating quality | markets/overview (top100AvgRating) | brand-overview (sampleTop10AvgRating) |
