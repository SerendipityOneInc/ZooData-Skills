# Product analysis methods

## categories: Category lookup

1. Resolve the supplied category name/path and retain the returned ID and path. Ask the user to choose when matches identify different intended categories.

## products/search: Product discovery

1. Pass the confirmed product keyword/category and explicit filters. When the confirmed scope is all categories, omit category filters. Use the documented snapshot selection and retain the returned product/category identity.
2. Map the requested conditions to supported filters. Include the match type only with a nonblank keyword and convert percentages to the decimal units required by the tool.
3. Resolve conflicting bounds before querying. Explain any unsupported condition and obtain agreement before relaxing it.
4. Select a supported sort from the table for the requested purpose. Page through the requested coverage and deduplicate ASINs.
5. Retain the response's matching product total separately from the number of acquired rows. Group acquired products by a consistent category level and ID. An exact count or ranking of categories across all matches requires compatible category aggregates or complete matching-product coverage; this search tool does not itself supply category aggregates. Otherwise report sample category counts and sample rankings, without replacing them with unrelated market totals or launching an unbounded full scan.
6. For leading products within a category, preserve the original filters and confirmed sort order, using that category's ID/path. Limit requests to the agreed coverage and cost. Keep tied values tied; a stable ASIN order within acquired records is only a display order, not evidence of a better business result.

| Retrieval purpose | Sort |
|---|---|
| Higher purchase lower bound | `monthlySalesFloor desc` |
| Higher revenue lower bound | `monthlyRevenueFloor desc` |
| Higher sales growth | `salesGrowthRate desc` |
| Newer listing | `listingDate desc` |
| Lower price | `price asc` |
| Fewer ratings | `ratingCount asc` |
| Better rank in the same category | `bsr asc` |

## products/competitors: Competitor discovery

1. Pass the named ASIN, brand, seller or product/category scope using this tool's own input schema.
2. Read the paginated matching rows with ASINs, product facts and returned performance measures. Apply the requested supported sorting and preserve the query scope. Retain which ASINs were actually returned; a lookup returning only the input ASIN is not evidence of additional competitors or an automatic similarity search.

## realtime/product: Real-time product details

1. Query the identified ASIN and marketplace for the needed current offer, attributes, variant or page text. Extract only what the response provides.
2. Keep the catalog results. If the live read fails, follow the MCP failure rules for stopping or retrying and deliver the acquired facts with any outstanding gaps.

## products/detail: Product details

1. Use compatible supplied or acquired facts first. Read known products through either `asins` or `parentAsin`, as supported by the current MCP schema; these modes are mutually exclusive. ASIN-list mode supports up to 50 canonical ASINs in request order and does not accept pagination, filters or sorting. Parent mode enumerates that parent's members with its documented pagination and order.
2. Select the requested catalog period through `dateRange`; retain the returned context, product identity, per-item status and actual snapshot date when provided. Preserve empty items for requested ASINs rather than dropping or replacing them.
3. Extract the returned product attributes, page content, price, purchase/revenue lower bounds, ratings, seller and variant measures. Keep child and parent fields separate.

## products/history: Product history

1. Pass one ASIN, `startDate`, `endDate` and marketplace. Select supported `aspects` when only particular series are needed.
2. Align per-point price, BSR, purchase-lower-bound and rating arrays with `timestamps`. Read dated title/image/status changes as event records.
3. Compare the same source metric, ranking category and parent/child scope across observed dates; retain the returned observation coverage.

## products/sales-trend: Monthly sales and revenue

1. Pass one canonical ASIN and the requested `startMonth`/`endMonth` when specified, using the current tool's supported month range. Read monthly child and parent purchase/revenue lower bounds and the returned growth measures on the catalog-snapshot basis.
2. Retain each month's `pointKind` and `inCatalog` state. Compare completed `monthEnd` points with completed month ends. Label `monthToDate` separately; it is not a completed month or a returned completed-month growth rate.
3. An out-of-catalog month and an in-catalog month with a null measure are different availability states; retain both without filling zero. Use returned adjacent-month growth rates and retain the source's null result when no valid previous base exists.

## products/price-band-overview: Price-band overview

1. Pass the keyword defining the requested product sample. Read `sampleMedianPrice` and the returned `hottestBand` and `bestOpportunityBand` summaries.
2. For each returned band, retain its price bounds, product count, sales share and reported index.

## products/price-band-detail: Price-band statistics

1. Pass the sample keyword. Read `priceBands`, `sampleSkuCount` and `sampleTotalMonthlySales`.
2. Report each band's bounds, product/brand counts, sales share and returned means/indices as bucket statistics.

## products/brand-overview: Brand overview

1. Pass the sample keyword. Read `sampleBrandCount`, `sampleTop10BrandSalesRate`, `sampleTop10AvgRating` and `sampleTop10AvgPrice`.

## products/brand-detail: Brand statistics

1. Pass the sample keyword and read `brands` with the response's sample product, sales and brand totals.
2. Retain each brand's name, product count, sales/revenue, shares, price/rating measures and returned `sampleProducts`.

## Local analysis: Product facts

1. Reuse compatible supplied or acquired facts. For known US ASINs requiring a read, use [product details](#productsdetail-product-details) first. Use found records as returned.
2. For current product details, use [real-time product details](#realtimeproduct-real-time-product-details) only for ASINs unresolved by a catalog service failure or not found. Historical data and parent variant lists use the catalog.

## Local analysis: Product content

1. For the page sections requested, obtain or reuse the source text through [Product facts](#local-analysis-product-facts) before organizing it by section.
2. Inventory the acquired titles, bullets, descriptions, specifications and images actually inspected. Retain the original brand, material, dimensions, included items and compatibility, with the product identity and source section.
3. Classify returned text before assigning bullet numbers. Keep standalone entries that only repeat a known specification value with that attribute. Number the actual selling-point descriptions in source order, preserving their text and original source positions; do not use the returned array length as the bullet count.
4. If the bullet text is unavailable, mark the bullets unavailable. Titles and page flags support findings about their own sections only. Identify any other missing section separately and deliver the acquired content.
5. When the requested analysis includes comparing identified phrases with page text, retain each phrase, the checked section and its supporting text separately. Use [phrase-occurrence semantics](semantics.md#history-and-page-content) for that result; keep it separate from supplied traffic observations.

## Local analysis: Product comparison

1. Use [Product facts](#local-analysis-product-facts) for each product’s required attributes, offers and catalog measures. Use [monthly trends](#productssales-trend-monthly-sales-and-revenue) for monthly sales or revenue, [product history](#productshistory-product-history) for observed changes and [product content](#local-analysis-product-content) for page sections. Use only tasks allowed in the current session.
2. Compare the acquired specifications, prices, ratings, performance measures or page sections using the same definitions and measurement scope. For explicit measurable conditions, report matched, not matched or unavailable with the value used. Keep each difference with its ASIN or supplied product identity.
3. If a required value cannot be obtained, show it as unavailable for that product and deliver the supported comparisons. Do not claim a difference or a condition match that depends on the missing value.
