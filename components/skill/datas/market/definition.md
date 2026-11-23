# Category-market analysis

1. Analyze category markets through category discovery, market size, price and rating distributions, competition, product launch dates and historical changes.

## Identify required inputs

1. Use category IDs or a named discovery scope, marketplace, snapshot/date range, product-inclusion scope, sample selection and explicit filters.
2. Resolve names or paths with the [category lookup method](methods.md#categories-category-lookup).

## Select an analysis task

| Check | Necessary input | Standard report content | Method |
|---|---|---|---|
| Market discovery | Category scope, marketplace and explicit filters | Category list, market totals, sample indicators and criterion matches | [Method](methods.md#marketssearch-market-discovery) |
| Market profile | Category IDs, marketplace and snapshot selection | Full-market size and leading-sample prices, ratings, concentration and new-product indicators | [Method](methods.md#marketsprofile-market-profile) |
| Market price distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by price bounds | [Method](methods.md#marketsprice-distributions-price-distribution) |
| Market rating distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by star-rating bounds | [Method](methods.md#marketsrating-distributions-star-rating-distribution) |
| Market rating-count distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by rating-count bounds | [Method](methods.md#marketsrating-count-distributions-rating-count-distribution) |
| Market listing-age distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by listing-age bounds | [Method](methods.md#marketslisting-age-distributions-listing-age-distribution) |
| Market fulfillment distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by fulfillment labels | [Method](methods.md#marketsfulfillment-distributions-fulfillment-distribution) |
| Market seller-country distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by seller-country labels | [Method](methods.md#marketsseller-country-distributions-seller-country-distribution) |
| Market content distribution | Category IDs, snapshot and sample selection | Sample counts, shares and sales by returned content-type labels | [Method](methods.md#marketscontent-distributions-content-distribution) |
| Market product concentration | Category IDs, snapshot and sample selection | Top-N concentration and returned product concentration entities | [Method](methods.md#marketstop-product-concentrations-product-concentration) |
| Market brand concentration | Category IDs, snapshot and sample selection | Top-N concentration and returned brand concentration entities | [Method](methods.md#marketsbrand-concentrations-brand-concentration) |
| Market seller concentration | Category IDs, snapshot and sample selection | Top-N concentration and returned seller concentration entities | [Method](methods.md#marketsseller-concentrations-seller-concentration) |
| Launch composition | Category IDs, sample and first-launch date range | Current-sample product counts by first-launch month or year | [Method](methods.md#marketslisting-launch-trend-launch-composition) |
| Market trend | Category IDs, date range and inclusion/sample rules | Month-end market totals, sample means and comparable changes | [Method](methods.md#marketshistory-market-history) |

## Preserve object features and report findings

1. Retain category ID/name/path, marketplace, actual period, product-inclusion scope and sample selection, with the available market product count, monthly sales and revenue.
2. For discovery, report the requested candidate list and explicit criterion matches. For a profile, report the requested full-market and sample indicators.
3. For distributions and concentration, report the requested groups, counts, measures and their populations. For history or launch composition, retain the returned dates and comparison scope.
