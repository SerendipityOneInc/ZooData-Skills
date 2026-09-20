# Market Trend Scanner — API Field Reference

> Load this file only when you need exact field names or response structure.
> This is the shared ZooData endpoint field reference. This skill's workflows
> use only the subcommands listed in SKILL.md (`categories`, `market`,
> `products`, `check`); the endpoints below are documented purely for
> field-name / response-structure lookup, not as a claim that this skill
> invokes all of them.

## ZooData Endpoint Field Reference

| # | Endpoint | Purpose |
|---|----------|---------|
| 1 | `categories` | Category path lookup |
| 2 | `markets/search` | Market size, competition metrics, new product rate |
| 3 | `products/search` | Product supply (100+ via pagination), brand/price drill |

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

## Cross-Validation Matrix

| Data Point | Primary Source | Validation Source |
|-----------|---------------|-------------------|
| Market size | markets/search | products/search (total count) |
