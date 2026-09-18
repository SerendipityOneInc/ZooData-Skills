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

`categories --keyword` sends `categoryKeyword`; `categories --category` sends a parsed `categoryPath`; `categories --parent` sends `parentCategoryPath`. The response exposes `categoryId`, `categoryPath`, and child information. A category name match is not a product-keyword match. The CLI's keyword-to-category fallback may infer `categoryPath` from a top `products/search` result; composite metadata reports `category_source` and `resolved_category_path` so the inference can be distinguished from a direct category match. Use a returned `categoryId` for the market endpoints.

## Market search and single-category snapshot

`markets/search` requires `categoryScope=direct|subtree` for new requests. It accepts exact `categoryId` or `categoryName`, optional `date`, `sampleType`, `page` (1-based), `pageSize` (1–100), `sortBy`, `sortOrder`, and documented market filters. `categoryName` is exact matching, not keyword expansion. `direct` covers the named node; `subtree` includes descendant nodes without duplicates. US is the documented marketplace.

The bundled `market` CLI exposes `--category-id`, `--category-name`, `--scope`, `--sample-type`, `--date`, `--page`, `--page-size`, `--sort`, `--order`, and filter flags. Its supported sample values are `unitSalesTop100` and `revenueTop100`. For one market, use `market --category-id ID --scope subtree --page-size 1`; verify the returned row's `categoryId` before interpreting it. Omitted `date` requests the latest available snapshot; the returned row's `date` is authoritative.

Each row contains category identity, all-category `totalSkuCount`, `totalSpuCount`, `totalMonthlySales`, `totalMonthlyRevenue`, and selected Top 100 `sample*` size, coverage, price, estimated gross-margin rate, brand/seller, rating, content, conservative new-product, and Top 10 concentration fields. The selected sample has at most 100 products. `meta.total` counts matching markets, not products.

The MCP `markets/search` route currently accepts `sampleType=bySale100|byRevenue100` as aliases and echoes the normalized `unitSalesTop100|revenueTop100` value. The MCP structure-profile and history routes reject `bySale100`; use normalized values consistently in the bundled CLI. The listed overview tool still returns `Unknown tool`. Server-side legacy market filters are a separate compatibility mode and cannot be combined with the new `categoryScope` request.

## Market structure and history

`markets/structure-profile` requires `categoryId` and one `dimension`: `brand`, `seller`, `price`, `sellerCountry`, `fulfillment`, `ratingCount`, `rating`, `listingAge`, `listingYear`, or `productFeature`. Optional context includes `categoryScope`, `sampleType`, and `date`. `data.buckets[]` covers only the selected Top 100; `data.sampleSkuCount` is its size. Bucket rows carry counts and shares plus dimension-specific values. An empty bucket array is no distribution observation.

`markets/history` requires `categoryId`, `startDate`, and `endDate`; `categoryScope` and `sampleType` are optional. `data.points[]` contains available month-end snapshots in ascending date order. Absent months are omitted. Check `actualStartDate` and `actualEndDate`; MoM/YoY fields may be absent without a comparable baseline. The CLI commands use `--category-id`, `--scope`, `--sample-type`; history additionally uses `--start-date` and `--end-date`.

## Supporting product evidence

`products/search` accepts a product keyword and/or category path plus documented numeric filters, paging, and sort options. The CLI `--mode` presets are local filter expansions; `mode`, `salesMin`, and `ratingsMax` are not raw API fields. CLI `--sales-min` maps to `monthlySalesMin`; `--ratings-max` maps to `ratingCountMax`, not star-rating `ratingMax`. `monthlySalesFloor` and `monthlyRevenueFloor` are lower-bound estimates. `realtime/product` is for current listing attributes and does not return these database sales fields.

Brand and price-band results are sample observations and must be tied to the resolved category where the endpoint accepts it. `reviews/analysis` may lack sufficient observations for a small review set. Product history and market history have different subjects and time grains; they are not interchangeable. Use actual returned field names and `_query.params` rather than deriving an endpoint from a composite result key.
