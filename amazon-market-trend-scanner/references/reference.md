# Market Trend Scanner — API Field Reference

> Load this file only when you need exact field names or response structure.
> This is the shared ZooData endpoint field reference. This skill's workflows
> use only the subcommands listed in SKILL.md (`categories`, `market`,
> `market`, `market-structure-profile`, `market-history`, `products`,
> `check`); the endpoints below are documented purely for
> field-name / response-structure lookup, not as a claim that this skill
> invokes all of them.

## ZooData Endpoint Field Reference

| # | Endpoint | Purpose |
|---|----------|---------|
| 1 | `categories` | Category path lookup |
| 2 | `markets/search` | Paginated discovery or exact category snapshot |
| 3 | `products/search` | Product supply (100+ via pagination), brand/price drill |
| 4 | `markets/structure-profile` | Selected Top 100 distribution |
| 5 | `markets/history` | Available month-end category history |

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

All three endpoints support only US. Resolve a human category path through `categories` to obtain `categoryId`. `categoryScope=direct` selects the node itself; `subtree` includes descendants without duplicates. The selected sample contains at most 100 products. For new requests, use `sampleType=unitSalesTop100` or `revenueTop100`; the MCP schema still advertises `bySale100` / `byRevenue100`, and live MCP validation rejects `bySale100`. The server recognizes legacy `categoryPath`, `categoryKeyword`, and `topN` filters only in a separate compatibility mode: do not combine them with `categoryScope`. The bundled CLI uses only the new parameters; the current MCP schema requires `categoryScope` and cannot submit a pure legacy request.

### markets/search — discovery

Required: `categoryScope`. Optional exact `categoryId` or `categoryName`, `date`, `sampleType`, `page`, `pageSize` (1–100), `sortBy` (`totalMonthlySales`, `totalMonthlyRevenue`, `top100MonthlySales`, `top100MonthlyRevenue`), `sortOrder`. Filters include `totalMonthlySalesMin`, `totalMonthlyRevenueMin`, `top100MonthlySalesMin`, `top100MonthlyRevenueMin`, `top100FbmRateMin/Max`, `top100APlusRateMin/Max`, `top100AvgSellerCountMin/Max`, `newProductMonthlyRevenueMin/Max`, `newProductRatingCountMin/Max`, `newProductRatingMin/Max`, and `sellerCountry`. Response `data[]` holds category identity, full-category `total*` size/sales/revenue, and selected `top100*` coverage, price, brand/seller, rating, new-product, and concentration metrics. `meta.total` is the total matching market count. For one market snapshot, filter by exact `categoryId` with `pageSize=1` and use the matching row; keep full-category and Top 100 denominators separate. `categoryName` is exact match, not keyword search.

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

## Cross-Validation Matrix

| Data Point | Primary Source | Validation Source |
|-----------|---------------|-------------------|
| Market size | markets/search | products/search (total count) |
