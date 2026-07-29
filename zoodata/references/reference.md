# ZooData API Field Reference

> Load this file only when you need exact field names or response structure.

## ZooData Endpoint Field Reference

> Shared field reference. This skill's workflows use ONLY the subcommands
> listed in its SKILL.md; the endpoints below are documented for field-name /
> response-structure lookup, not as a claim that this skill invokes all of them.

| # | Endpoint | Purpose |
|---|----------|---------|
| 1 | `categories` | Category path lookup |
| 2 | `markets/search` | Market size, competition metrics, new-product rate |
| 3 | `products/search` | Product supply (100+ via pagination), brand/price drill |
| 4 | `products/competitors` | Top competitor list |
| 5 | `realtime/product` | Live product detail |
| 6 | `reviews/analysis` | Consumer pain points, buying factors |
| 7 | `products/price-band-overview` | Price-band opportunity overview |
| 8 | `products/price-band-detail` | Per-band SKU/sales/brand/rating breakdown |
| 9 | `products/brand-overview` | Brand count, CR10, top-brand avg price/rating |
| 10 | `products/brand-detail` | Per-brand SKU/sales/revenue/share ranking |
| 11 | `products/history` | 30-day price/BSR/sales trend |

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

## 2. markets/search

**Key Request Params:**
- `categoryPath`: List<String> (e.g. `["Pet Supplies", "Dogs"]`)
- `categoryKeyword`: String
- `topN`: **String** (`"10"` not `10`)
- `sampleType`: `by_sale_100` / `by_bsr_100` / `avg`
- `pageSize`: Integer (max 20)

**Key Response Fields:**
| Field | Type | Used For |
|-------|------|----------|
| `totalSkuCount` | int | Market size |
| `sampleAvgMonthlySales` | float | Demand level |
| `sampleAvgMonthlyRevenue` | float | Market value |
| `sampleAvgPrice` | float | Price benchmark |
| `sampleAvgRating` | float | Quality benchmark |
| `sampleBrandCount` | int | Brand diversity |
| `sampleSellerCount` | int | Seller diversity |
| `sampleFbaRate` | float | FBA adoption (decimal) |
| `sampleNewSkuRate` | float | New entrant rate (decimal) |
| `topSalesRate` | float | Product concentration (CR_topN) |
| `topBrandSalesRate` | float | Brand concentration |
| `topSellerSalesRate` | float | Seller concentration |
| `sampleAPlusRate` | float | Margin benchmark |

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

## 6b. realtime/reviews

**Request:**
- `asin`: String (10 chars, required)
- `marketplace`: String (US/UK only, default US)
- `cursor`: String (pagination token; omit for first page)

⚠️ Fixed 10 reviews/page; max 10 pages = **100 reviews** hard cap. 1 credit/page. Cursor-based pagination.

**Response:**
| Field | Type | Used For |
|-------|------|----------|
| `asin` | string | Product ID |
| `reviews` | list | Array of RealtimeReview |
| `nextCursor` | string\|null | Next page token (null = end) |

**RealtimeReview:** `reviewId`, `title`, `body`, `bodyHtml`, `rating`, `author`, `date` (ISO 8601 UTC), `verifiedPurchase`, `vineProgram`, `helpfulVoteCount`, `unhelpfulVoteCount`, `reviewCountry`, `images`, `link`, `isGlobalReview`

**Use cases:** ASIN <50 reviews (fallback for `/reviews/analysis`), brand-new product without snapshot, freshest possible raw text. Feeds the local Map/Reduce toolkit (`zoodata.py reviews-raw / review-tag-prompt / review-reduce-prompt / review-aggregate`).

---

## 6c. reviews/search

**Request:**
- `asin`: String (required)
- Optional filters: `ratingMin`/`ratingMax` (1-5), `verifiedOnly`, `vineOnly`, `helpfulVoteCountMin`, `dateStart`/`dateEnd` (YYYY-MM-DD)
- `sortBy`: `recent` (default) / `rating` / `helpfulVoteCount`
- `sortOrder`: `desc` (default) / `asc`
- `page`: 1-indexed (default 1)
- `pageSize`: 1-20 (default 10)

**Response:** Array of `TaggedReview` — same fields as `RealtimeReview` + `tags[{labelType, element}]` (AI tags from offline pipeline).

**Differs from realtime/reviews:** uses BigQuery daily snapshot (T+1 delay) but already has AI tags applied. Prefer `reviews/search` when snapshot exists; prefer `realtime/reviews` for live data or new products.

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
- `asin`: String (required) — Single ASIN (one per call, NOT an array)
- `startDate`: String "YYYY-MM-DD" (required)
- `endDate`: String "YYYY-MM-DD" (required)
- `marketplace`: String (optional, default "US")
⚠️ `asin` is a **single string** — NOT an array. For multiple ASINs, make separate calls.
⚠️ Does NOT support `page`/`pageSize` — returns full date range in one response.
⚠️ Does NOT accept `dateRange` — must use startDate + endDate.

**Response (single time series object, NOT an array of snapshots):**
| Field | Type | Used For |
|-------|------|----------|
| `asin` | string | Product ASIN |
| `timestamps` | List\<string\> | Dates (YYYY-MM-DD) |
| `price` | List\<float\> | Price on each date |
| `bsr` | List\<int\> | BSR on each date |
| `subBsr` | List\<int\> | Sub-category BSR |
| `monthlySalesFloor` | List\<int\> | Monthly sales lower bound |
| `rating` | List\<float\> | Rating on each date |
| `ratingCount` | List\<int\> | Review count on each date |
| `sellerCount` | List\<int\> | Seller count |
| `title` | List\<ChangeLog\> | Title changes `{date, value}` |
| `imageUrl` | List\<ChangeLog\> | Main image changes `{date, value}` |
| `bestSeller` | List\<ChangeLog\> | Best Seller badge `{date, value}` |
| `amazonChoice` | List\<ChangeLog\> | Amazon's Choice badge `{date, value}` |
| `newRelease` | List\<ChangeLog\> | New Release badge `{date, value}` |
| `aPlus` | List\<ChangeLog\> | A+ content status `{date, value}` |
| `inventoryStatus` | List\<ChangeLog\> | Stock status `{date, value}` |
| `currency` | string | e.g. "USD" |

---

## Cross-Validation Matrix

| Data Point | Primary Source | Validation Source |
|-----------|---------------|-------------------|
| Market size | markets/search | products/search (total count) |
| Brand concentration | brand-overview (sampleTop10BrandSalesRate) | markets/search (topBrandSalesRate) |
| Price distribution | price-band-detail | products/search (price field) |
| Competition level | markets (topSalesRate) | brand-detail (top brand shares) |
| Consumer demand | reviews/analysis | products (sales + growth) |
| Avg rating quality | markets (sampleAvgRating) | brand-overview (sampleTop10AvgRating) |
