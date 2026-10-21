# Market Metric Semantics

This module owns returned market-field meaning, denominator, time grain, and inference limits. `reference.md` owns where and how fields are requested; scenarios own what decision may follow.

## Market size and selected sample

Market measures count SPUs (parent products), merging same-product variants. They cannot be compared directly with older SKU counts or SKU history.

| Search field family | Population and meaning | Permitted inference | Prohibited shortcut |
|---|---|---|---|
| `totalProductCount`, `totalMonthlySales`, `totalMonthlyRevenue` | Full category scope: parent-product count, estimated monthly units and USD revenue | Category supply and demand scale | Use meta.total or sample size as category product count |
| `sampleProductCount`, `sampleMonthlySales`, `sampleMonthlyRevenue` | Selected Top 100 SPUs, possibly fewer | Sample size and totals | Call these per-product averages or whole-category totals |
| `avgMonthlySales`, `avgMonthlyRevenue` | Per-SPU monthly averages within the selected sample | Observed average product scale | Confuse with the sample totals or infer seller revenue |
| `avgPrice`, `medianProductPrice` | Different price aggregations in the selected sample | Observed price positioning | Infer profit or the price of every product |
| `avgGrossMarginRate` | Service-estimated average sample gross margin | Describe the returned estimate | Treat as seller contribution margin |
| `avgRating`, `avgRatingCount` | Sample average star rating and rating count | Observed rating and review barrier | Treat rating count as a separate unavailable review-count metric |

`marketSize` in profile carries full-category measures; `sampleProfile` alone carries the selected sample. Preserve their scope when mapping profile evidence to search fields. Revenue is returned USD, not price × sales, and must not be converted from cents again.

Monthly sales and revenue cover the trailing 30 days at the snapshot, not cumulative sales across a requested history or new-product window. Price and rating means exclude null values independently, include real zeros, and return null with no valid values; denominators can differ by metric. Do not reconstruct a returned mean as a total divided by product count unless that denominator is explicitly documented.

The sample selector determines the population. Every claim retains the actual snapshot date and product inclusion scope. Product grain comes from the endpoint contract, not a returned productGrain field. Parent subtree and descendant rows can overlap; they are not additive independent markets.

## Structure, entry, and concentration

- Each independent Top N summary returns both unit and revenue totals for the ranked group, regardless of sample selector. Group totals are not per-SPU averages.
- Fixed Top 3/5/10/20 Product, Brand and Seller concentration fields and profile arrays describe the selected sample, never the whole category. `concentrationRate` follows the sample selector: unit share for unitSalesTop100, revenue share for revenueTop100. Explicit `MonthlySalesRate` and `MonthlyRevenueRate` remain unit and revenue shares respectively.
- `sellerCount` is a distinct observed-seller count; `avgSellerCount` is a per-product mean. Seller concentration cannot be replaced by brand concentration.
- New-product windows cover 1/3/6/12 calendar months based on business launch date. Missing launch dates remain in the population denominator without being counted as new. Full-category and sample windows have separate denominators. A returned new-product share is not survival, seller success, or conversion evidence.
- Fixed search window and rank names, selected dynamic aliases, and profile `windowMonths` / `topN` identities must refer to the same cutoff for a comparison.
- Top N new-product monthlySalesRate and monthlyRevenueRate use the enclosing ranked group sales and revenue respectively, not the outer sample. Do not infer bucket-level new-product or brand concentration measures from the available distribution means.
- Price buckets use inclusive lowerBound and exclusive upperBound, with no upper limit for the final band. A band_1 code can refer to different ranges across markets or snapshots, so compare actual bounds. Other numeric dimensions use their documented bucket-code boundary rules; a null bound is not zero, and listing-age bounds are calendar months. bucketIndex and seller-country distributionRank are display order, not sales ranks. Entity rank follows the sample ranking metric.
- Distribution `bucketProductCount` and `bucketProductRate` describe the bucket population; `monthlySalesRate` and `monthlyRevenueRate` describe unit and revenue shares. Distribution product membership, unit sales and revenue rates have different denominators. Content and seller-country memberships can overlap; do not sum their rates to 100%. Countries identify sellers associated with the sales records, not buyers or delivery destinations. A Listing may belong to multiple countries, but sales and revenue are attributed to the corresponding seller-country records; they are neither full Listing sales repeated in every country nor equally split across countries.
- Fulfillment uses a market-representative bucket for each SPU; unknown fulfillment stays in the denominator. FBA/FBM/AMZ observations do not establish costs, compliance or profit.
- `aPlusProductRate`, `videoProductRate`, ratings and price structure describe observed sample characteristics. They may motivate validation but do not prove easy entry.
- Public floating values, including fractional rates, are rounded to two decimals. Preserve null and true zero; a rounded zero share does not prove the exact unrounded share is zero. Do not invent extra precision.

## Time and product observations

- History points are published month-end SPU snapshots identified by `date`, within one market-identity series. Interpret them as monthly observations. Each month independently selects its leading sample from that snapshot, so membership can change; sample trends do not measure a fixed product cohort. Missing dates remain absent; the service does not fill gaps or substitute SKU history. A latest snapshot and a completed-month observation can be shown side by side but are not automatically a comparable MoM pair.
- The current incomplete calendar month is outside a completed-month trend population. Its absence is expected timing, not zero or a missing completed-month point.
- History separates full-market totals in `marketSize` from sample totals, counts, prices and ratings in `sampleProfile`. Full-market sales and revenue trends are supported when comparable observations exist; new-product trends are not returned. Its avgMonthlySales and avgMonthlyRevenue are per-SPU monthly averages, distinct from the corresponding sample totals. A derived MoM/YoY requires two returned comparable dates, identical category, scope, sample, metric, unit and denominator. Missing baseline is not zero growth.
- Launch-trend rows group products by launch month/year within the latest sample snapshot. A first-launch date range narrows the cohorts, not the sample snapshot date. They are cohorts, not repeated demand observations or historical market growth.
- Product `monthlySalesFloor` / `monthlyRevenueFloor` are product-level lower-bound estimates; summing an incomplete product sample cannot replace market totals.
- Market movement alone does not identify a cause, seller conversion, profitability, or a recommended launch date.
