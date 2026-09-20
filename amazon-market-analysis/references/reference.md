# Market API and CLI Reference

This module owns production acquisition facts for `amazon-market-analysis`. All listed HTTP endpoints use `POST https://api.zoodata.ai/openapi/v2/<endpoint>` with `Authorization: Bearer $ZOODATA_API_KEY`. The bundled CLI is the supported local interface; inspect each command's current `--help` before invocation. Responses use `{success, data, error, meta}`. Read `meta.creditsConsumed` and `meta.creditsRemaining` when returned; composite top-level metadata accumulates internal calls.

## Endpoint availability and CLI mapping

| Endpoint | CLI command | Data shape | Market use |
|---|---|---|---|
| `categories` | `categories` | `data[]` | Resolve IDs and browse children |
| `markets/search` | `market` | `data[]` plus `meta.total` | Discover markets or retrieve one exact category snapshot |
| `markets/structure-profile` | `market-structure-profile` | `data.buckets[]` | Selected Top 100 distribution |
| `markets/history` | `market-history` | `data.points[]` | Available month-end market snapshots |
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

`markets/search` takes a nested `category` object: `ids` (1–100 exact IDs), a complete `path`, or an exact `name` are alternative row selectors. `category.includeDescendantCategoryProducts` defaults to `true` and controls whether **each returned market row's product measures** include its descendant categories. It does not select extra market rows. The `filters` object holds market metric conditions and is applied before pagination. `sampleType`, `topN`, `newProductPeriod`, `date`, `page` (1-based), `pageSize` (1–100), `sortBy`, and `sortOrder` are top-level request fields. `topN` selects `3`, `5`, `10`, or `20` for dynamic Top N filters and sorting. `newProductPeriod` selects a `1`, `3`, `6`, or `12` calendar-month business launch window for new-product filters, sorting, and returned fields. US is the documented marketplace.

There is no automatic parent-to-children market-row expansion. Use `categories --parent` to enumerate all direct child IDs, then send them as `category.ids` in one `markets/search` request when there are at most 100. Pagination and sorting operate on those ID-selected rows; `meta.total` counts matching rows after filters. Larger ID sets require batches, each with its own `meta.total`. Do not treat the returned `categoryScope` row field as a row selector; it describes the product aggregation used for that row. Parent and child rows may overlap when descendant products are included.

The bundled `market` CLI exposes mutually exclusive `--category-id`, `--category-ids` (comma-separated), `--category-path`, and `--category-name`. `--no-include-descendant-category-products` switches each row to directly assigned products only; inclusion is the default. It also exposes `--sample-type`, `--top-n`, `--new-product-period`, `--date`, `--page`, `--page-size`, `--sort`, `--order`, and exact kebab-case forms of every current filter field, such as `--sample-avg-monthly-sales-min`, `--top-brand-sales-rate-max`, and `--sample-new-sku-rate-min`. Its supported sample values are `unitSalesTop100` and `revenueTop100`. For one market, use `market --category-id ID --page-size 1`; verify the returned row's `categoryId` before interpreting it. Omitted `date` requests the latest available snapshot; the returned row's `date` is authoritative.

Each row contains category identity, all-category `totalSkuCount`, `totalSpuCount`, `totalMonthlySales`, `totalMonthlyRevenue`, and selected Top 100 `sample*` size, coverage, per-product average, package, price, estimated gross-margin, brand/seller, rating, fulfillment, content, selected-period new-product, and fixed Top 10 concentration fields. `newProductPeriod` identifies the active business launch window; `totalNewProduct*` uses the full category population and `sampleNewProduct*` uses the selected Top 100. `topNMetrics[]` returns `n=3,5,10,20` product/brand/seller sales and revenue measures. The former `sampleNewProduct*6m` and `newProductMetrics[]` fields are not current. The selected sample has at most 100 products. `meta.total` counts matching markets, not products; a nested concentration rate is still sample-scoped.

The MCP `markets/search` route also lists `sampleType=bySale100|byRevenue100` as aliases; use normalized `unitSalesTop100|revenueTop100` values consistently in the bundled CLI and other market routes. The active MCP tool list contains search, structure-profile, and history only; `markets/overview` is absent. Legacy flat market requests remain accepted separately, while the bundled CLI sends the published nested form only.

## Market structure and history

`markets/structure-profile` requires `categoryId` and one `dimension`: `brand`, `seller`, `price`, `sellerCountry`, `fulfillment`, `ratingCount`, `rating`, `listingAge`, `listingYear`, or `productFeature`. Optional context includes `includeDescendantCategoryProducts`, `sampleType`, `newProductPeriod`, and `date`. `data.buckets[]` covers only the selected Top 100; `data.sampleSkuCount` is its size. Bucket rows carry product/sales/revenue counts and shares, Amazon self-operated measures, selected-period new-product measures, example ASINs, and dimension-specific values. An empty bucket array is no distribution observation. The CLI uses `--no-include-descendant-category-products` for a direct-only request; it does not accept the former `--scope`.

`markets/history` requires `categoryId`, `dateFrom`, and `dateTo`; optional context includes `includeDescendantCategoryProducts`, `sampleType`, and `newProductPeriod`. `data.points[]` contains available month-end snapshots in ascending date order. Absent months are omitted. Check `resolvedDateFrom` and `resolvedDateTo`; each point uses the echoed `newProductPeriod` and may include full-category and sample `*NewProduct*` counts, rates, sales, and revenue. MoM/YoY fields may be absent without a comparable baseline. The CLI uses `--category-id`, `--date-from`, `--date-to`, `--sample-type`, `--new-product-period`, and the descendant-product boolean flag; it does not accept the former `--scope`, `--start-date`, or `--end-date`.

## Supporting product evidence

`products/search` accepts a product keyword and/or category path plus documented numeric filters, paging, and sort options. The CLI `--mode` presets are local filter expansions; `mode`, `salesMin`, and `ratingsMax` are not raw API fields. CLI `--sales-min` maps to `monthlySalesMin`; `--ratings-max` maps to `ratingCountMax`, not star-rating `ratingMax`. `monthlySalesFloor` and `monthlyRevenueFloor` are lower-bound estimates. `realtime/product` is for current listing attributes and does not return these database sales fields.

Brand and price-band results are sample observations and must be tied to the resolved category where the endpoint accepts it. `reviews/analysis` may lack sufficient observations for a small review set. Product history and market history have different subjects and time grains; they are not interchangeable. Use actual returned field names and `_query.params` rather than deriving an endpoint from a composite result key.
