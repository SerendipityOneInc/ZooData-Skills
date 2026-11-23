# Product analysis

1. Analyze products or candidate sets through discovery, specifications, page content, monthly sales/revenue, historical changes, comparisons and price/brand statistics for matching product samples.

## Identify required inputs

1. Use ASINs or supplied product information, marketplace, requested dates and comparison conditions. Product discovery uses the seller’s conditions. Online candidate retrieval requires a confirmed category scope: a specified category or all categories. Retain any supplied product keyword.
2. Use [category lookup](methods.md#categories-category-lookup) to resolve a category-dependent question. Price-band and brand statistics use the keyword input supported by their tools.

## Select an analysis task

| Check | Necessary input | Standard report content | Method |
|---|---|---|---|
| Product discovery | Requested conditions, marketplace and confirmed search scope | Effective query conditions, candidate ASINs, baseline measures and condition matches | [Method](methods.md#productssearch-product-discovery) |
| Competitor discovery | Product keyword, brand, seller, category or ASIN accepted by the current lookup schema | Returned matching ASINs and product measures under those conditions | [Method](methods.md#productscompetitors-competitor-discovery) |
| Product facts | Known ASINs, a parent ASIN or identified supplied product information | Requested catalog attributes and purchase/revenue measures, or current page attributes and offers, with the actual product scope | [Method](methods.md#local-analysis-product-facts) |
| Product content | ASIN, acquired page or supplied product brief | Acquired title, selling-point bullets, product description, specifications, inspected visual content and requested phrase occurrences by section | [Method](methods.md#local-analysis-product-content) |
| Product history | ASIN and date range | Observed price, category ranks, purchase lower bounds, ratings and change logs | [Method](methods.md#productshistory-product-history) |
| Product sales trend | One ASIN and requested months | Monthly child/parent purchase and revenue lower bounds, completed/current-month status and returned month-over-month changes | [Method](methods.md#productssales-trend-monthly-sales-and-revenue) |
| Product comparison | Identified products and comparison dimensions or criteria | Comparable product facts/content, differences and explicit condition matches | [Method](methods.md#local-analysis-product-comparison) |
| Price-band overview | Keyword defining the product sample | Sample median price and returned summary bands | [Method](methods.md#productsprice-band-overview-price-band-overview) |
| Price-band statistics | Keyword defining the product sample | Price buckets, product/brand counts, sales shares and returned band indicators | [Method](methods.md#productsprice-band-detail-price-band-statistics) |
| Brand overview | Keyword defining the product sample | Sample brand count, Top-10 sales concentration and price/rating means | [Method](methods.md#productsbrand-overview-brand-overview) |
| Brand statistics | Keyword defining the product sample | Per-brand sample counts, sales/revenue, shares, price/rating measures and returned sample products | [Method](methods.md#productsbrand-detail-brand-statistics) |

## Preserve object features and report findings

1. Retain available ASIN, name/brand, marketplace, relevant specifications, price, monthly purchase lower bound, star rating and rating count, with parent/variant identity where relevant.
2. For discovery and comparison, report the requested products, values and explicit condition matches. For content, retain the acquired sections and product facts.
3. For history, report the requested series and comparable changes. Price-band and brand reports retain their keyword-defined sample, groups and returned denominators.
