# Market API and CLI Reference

This module owns production acquisition facts for `amazon-market-analysis`. All listed HTTP endpoints use `POST https://api.zoodata.ai/openapi/v2/<endpoint>` with `Authorization: Bearer $ZOODATA_API_KEY`. The bundled CLI is the supported local interface; inspect each command's current `--help` before invocation. Responses use `{success, data, error, meta}`. Read `meta.creditsConsumed` and `meta.creditsRemaining` when returned; composite top-level metadata accumulates internal calls.

## Endpoint availability and CLI mapping

| Endpoint | CLI command | Data shape | Market use |
|---|---|---|---|
| `categories` | `categories` | `data[]` | Resolve IDs and browse children |
| `markets/search` | `market` | `data[]` plus `meta.total` | Discover markets or retrieve one exact category snapshot |
| `markets/profile` | `market-profile` | `data[]` | SPU profile |
| `markets/price-distributions` | `market-price-distributions` | `data[]` | SPU price-distributions |
| `markets/rating-distributions` | `market-rating-distributions` | `data[]` | SPU rating-distributions |
| `markets/rating-count-distributions` | `market-rating-count-distributions` | `data[]` | SPU rating-count-distributions |
| `markets/listing-age-distributions` | `market-listing-age-distributions` | `data[]` | SPU listing-age-distributions |
| `markets/fulfillment-distributions` | `market-fulfillment-distributions` | `data[]` | SPU fulfillment-distributions |
| `markets/seller-country-distributions` | `market-seller-country-distributions` | `data[]` | SPU seller-country-distributions |
| `markets/content-distributions` | `market-content-distributions` | `data[]` | SPU content-distributions |
| `markets/top-product-concentrations` | `market-top-product-concentrations` | `data[]` | SPU top-product-concentrations |
| `markets/brand-concentrations` | `market-brand-concentrations` | `data[]` | SPU brand-concentrations |
| `markets/seller-concentrations` | `market-seller-concentrations` | `data[]` | SPU seller-concentrations |
| `markets/listing-launch-trend` | `market-listing-launch-trend` | `data[]` | SPU listing-launch-trend |
| `markets/history` | `market-history` | `data[]` | Available SPU snapshots |
| `products/search` | `products` | `data[]` | Candidate product observations |
| `products/competitors` | `competitors` | `data[]` | Competitor observations |
| `realtime/product` | `product` | `data` object | Current ASIN detail; no monthly sales estimate |
| `reviews/analysis` | `analyze` | `data` object | Aggregated consumer insights when available |
| `products/price-band-overview` | `price-band-overview` | Endpoint-specific object | Price-band summary |
| `products/price-band-detail` | `price-band-detail` | Endpoint-specific object | Price-band detail |
| `products/brand-overview` | `brand-overview` | Endpoint-specific object | Brand concentration summary |
| `products/brand-detail` | `brand-detail` | Endpoint-specific object | Brand detail |
| `products/history` | `history` | Time-series object | Product-level price/BSR/sales history |

`market-entry` and `opportunity-scan` are bundled composite commands, not API endpoints. Each fans out across several endpoints and can consume many credits; inspect its `--help` and returned `meta.apiCalls` / `meta.creditsConsumed`. The composite output's `market` section is a single matching market object, whereas the granular `market` command returns `data[]`. Reuse a successful composite's available evidence locally before deciding whether a missing dimension justifies another call.

## Category identity

`categories --keyword` sends `categoryKeyword`; `categories --category` sends a parsed `categoryPath`; `categories --parent` sends `parentCategoryPath`. `--parent` requires a nonempty JSON string array. Other category-path flags accept JSON arrays or `>`-separated names, but reject comma-bearing strings without an explicit separator instead of guessing boundaries. A parent request returns the complete direct-child `data[]` list in one response, with a full `categoryId` on every row. The response also exposes `categoryPath` and child information. A category name match is not a product-keyword match. The CLI's keyword-to-category fallback may infer `categoryPath` from a top `products/search` result; composite metadata reports `category_source` and `resolved_category_path` so the inference can be distinguished from a direct category match. Use a returned `categoryId` for the market endpoints.

## Market search and single-category snapshot

This is the SPU contract defined by the service schemas dated 2026-10-16. Inspect the active OpenAPI/MCP schema before live use; a deployment still exposing the older three-route market contract is incompatible. Do not silently use SKU fields or substitute the retired route.

All 14 market endpoints use SPU (parent-product) grain: variants of the same product are merged. Only US is supported. Money is already USD; rates are fractions. Public floating metrics are rounded to two decimals, midpoint away from zero; integers and null remain unchanged. Filtering and sorting use these same rounded values. A returned zero is a value, not missingness. `avgProductReviewCnt` is unavailable; use the documented rating-count field where appropriate, without inventing a separate review metric.

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

## Bundled market commands

`market` exposes mutually exclusive `--category-id`, `--category-ids`, `--category-path`, `--category-name`, plus optional `--category-keyword`, `--date-range`, sample and paging options. `--no-include-descendant-category-products` selects direct product scope. Each numeric filter has its exact kebab-case metric flag with `MIN:MAX`, `MIN:`, or `:MAX`, e.g. `--avg-product-price30d 10:30`, `--top-n-brand-monthly-sale-cnt-rate :0.6`. `--seller-country-codes US CN` sends a country list. `--sort` uses the exact camelCase metric name; inspect `market --help` for all 192 names.

Every `market-<detail-route>` and `market-history` accepts either `--category-id ID` or `--category-ids ID1,ID2`, and `--category-scope direct|subtree`. Detail routes expose `--date`; history requires `--date-from` / `--date-to`; launch trend exposes `--granularity`. Scope defaults to subtree.

There is no automatic direct-child enumeration for exact ID selection. Use `categories --parent` to enumerate direct children, then send `category.ids` in one `markets/search` request for at most 100 IDs, with `--page-size 100`. Larger sets require batches and complete page coverage. `meta.total` counts matching rows after filters. `--parent` requires a nonempty JSON string array. A prefix search includes deeper descendants, so it cannot replace a direct-child-only comparison.

## Supporting product evidence

`products/search` accepts a product keyword and/or category path plus documented numeric filters, paging, and sort options. The CLI `--mode` presets are local filter expansions; `mode`, `salesMin`, and `ratingsMax` are not raw API fields. CLI `--sales-min` maps to `monthlySalesMin`; `--ratings-max` maps to `ratingCountMax`, not star-rating `ratingMax`. `monthlySalesFloor` and `monthlyRevenueFloor` are lower-bound estimates. `realtime/product` is for current listing attributes and does not return these database sales fields.

Brand and price-band results are sample observations and must be tied to the resolved category where the endpoint accepts it. `reviews/analysis` may lack sufficient observations for a small review set. Product history and market history have different subjects and time grains; they are not interchangeable. Use actual returned field names and `_query.params` rather than deriving an endpoint from a composite result key.
