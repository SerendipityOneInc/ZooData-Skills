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
| `markets/history` | `market-history` | `data[].points[]` | Market-grouped SPU snapshots |
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

The market contract follows the current MCP descriptions, inputSchema and outputSchema. Inspect the connected service's tools/list before live MCP use; cached tool definitions and another deployment's documentation may describe a different version. Use the configured service for verification.

All 14 market endpoints use SPU (parent-product / Amazon Listing) grain: variants of the same product are merged. Only US is supported. Money is already USD; rates are fractions. Public floating metrics are rounded to two decimals, midpoint away from zero; integers and null remain unchanged. Filtering and sorting use these same rounded values. A returned zero is a value, not missingness. `avgReviewCount` is unavailable; rating count is not written-review count.

### Search request and response

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

## Bundled market commands

`market` exposes mutually exclusive `--category-id`, `--category-ids`, `--category-path`, `--category-name`, plus optional `--category-keyword`, `--date`, sample and paging options. `--no-include-descendant-category-products` selects direct product scope. Each numeric filter has its exact kebab-case metric flag with `MIN:MAX`, `MIN:`, or `:MAX`, e.g. `--avg-price 10:30`, `--top-n-brand-monthly-sales-rate :0.6`. `--seller-country-codes US CN` sends a country list. `--sort` uses the exact camelCase metric name; inspect `market --help` for all 192 names.

Every `market-<detail-route>` and `market-history` accepts either `--category-id ID` or `--category-ids ID1,ID2`, and the `--include-descendant-category-products` / `--no-include-descendant-category-products` boolean pair. Profile/distribution/concentration routes expose `--date`; history requires `--date-from` / `--date-to`; launch trend exposes optional `--date-from` / `--date-to` and `--granularity`. Descendant product inclusion defaults to true.

There is no automatic direct-child enumeration for exact ID selection. Use `categories --parent` to enumerate direct children, then send `category.ids` in one `markets/search` request for at most 100 IDs, with `--page-size 100`. Larger sets require batches and complete page coverage. `meta.total` counts matching rows after filters. `--parent` requires a nonempty JSON string array. A prefix search includes deeper descendants, so it cannot replace a direct-child-only comparison.

## Supporting product evidence

`products/search` accepts a product keyword and/or category path plus documented numeric filters, paging, and sort options. The CLI `--mode` presets are local filter expansions; `mode`, `salesMin`, and `ratingsMax` are not raw API fields. CLI `--sales-min` maps to `monthlySalesMin`; `--ratings-max` maps to `ratingCountMax`, not star-rating `ratingMax`. `monthlySalesFloor` and `monthlyRevenueFloor` are lower-bound estimates. `realtime/product` is for current listing attributes and does not return these database sales fields.

Brand and price-band results are sample observations and must be tied to the resolved category where the endpoint accepts it. `reviews/analysis` may lack sufficient observations for a small review set. Product history and market history have different subjects and time grains; they are not interchangeable. Use actual returned field names and `_query.params` rather than deriving an endpoint from a composite result key.
