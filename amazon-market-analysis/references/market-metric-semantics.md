# Market Metric Semantics

This module owns returned market-field meaning, denominator, time grain, and inference limits. `reference.md` owns where and how fields are requested; scenarios own what decision may follow.

## Market size and selected sample

Market measures count SPUs (parent products), merging same-product variants. They cannot be compared directly with older SKU counts or SKU history.

| Search field family | Population and meaning | Permitted inference | Prohibited shortcut |
|---|---|---|---|
| `totalProductCnt`, `totalMonthlySaleCnt`, `totalMonthlySaleAmt` | Full category scope: parent-product count, estimated monthly units and USD revenue | Category supply and demand scale | Use meta.total or sample size as category product count |
| `sampleProductCnt`, `sampleMonthlySaleCnt`, `sampleMonthlySaleAmt` | Selected Top 100 SPUs, possibly fewer | Sample size and totals | Call these per-product averages or whole-category totals |
| `avgProductMonthlySaleCnt`, `avgProductMonthlySaleAmt` | Per-SPU monthly averages within the selected sample | Observed average product scale | Confuse with the sample totals or infer seller revenue |
| `avgProductPrice30d`, `medianProductPrice30d` | Different price aggregations in the selected sample | Observed price positioning | Infer profit or the price of every product |
| `avgProductGrossMarginRate` | Service-estimated average sample gross margin | Describe the returned estimate | Treat as seller contribution margin |
| `avgProductRatingAmt`, `avgProductRatingCnt` | Sample average star rating and rating count | Observed rating and review barrier | Treat rating count as a separate unavailable review-count metric |

`marketSize` in profile carries full-category measures; top-level sample totals and `sampleProfile` carry the selected sample. Preserve their scope when mapping profile evidence to search fields. Revenue is returned USD, not price × sales, and must not be converted from cents again.

The sample selector determines the population. Every claim retains the actual snapshot date and category scope. Parent subtree and descendant rows can overlap; they are not additive independent markets.

## Structure, entry, and concentration

- Fixed Top 3/5/10/20 Product, Brand and Seller concentration fields and profile arrays describe the selected sample, never the whole category. `concentrationRate` follows the sample selector: unit share for unitSalesTop100, revenue share for revenueTop100. Explicit `MonthlySaleCntRate` and `MonthlySaleAmtRate` remain unit and revenue shares respectively.
- `observedSellerCnt` is a distinct observed-seller count; `avgProductSellerCnt` is a per-product mean. Seller concentration cannot be replaced by brand concentration.
- New-product windows cover 1/3/6/12 calendar months based on business launch date. Missing launch dates remain in the population denominator without being counted as new. Full-category and sample windows have separate denominators. A returned new-product share is not survival, seller success, or conversion evidence.
- Fixed search window and rank names, selected dynamic aliases, and profile `windowMonths` / `topN` identities must refer to the same cutoff for a comparison.
- Distribution product membership, unit sales and revenue rates have different denominators. Content and seller-country memberships can overlap; do not sum their rates to 100%. Countries describe observed membership, not exclusive seller origin.
- Fulfillment uses a market-representative bucket for each SPU; unknown fulfillment stays in the denominator. FBA/FBM/AMZ observations do not establish costs, compliance or profit.
- `aPlusProductRate`, `videoProductRate`, ratings and price structure describe observed sample characteristics. They may motivate validation but do not prove easy entry.
- Public floating values, including fractional rates, are rounded to two decimals. Preserve null and true zero; a rounded zero share does not prove the exact unrounded share is zero. Do not invent extra precision.

## Time and product observations

- History rows are actual published SPU snapshots identified by `dt`. Preserve the actual returned time grain; do not presume every row is month-end. Missing dates remain absent; the service does not fill gaps or substitute SKU history. A latest snapshot and a completed-month observation can be shown side by side but are not automatically a comparable MoM pair.
- The current incomplete calendar month is outside a completed-month trend population. Its absence is expected timing, not zero or a missing completed-month point.
- History has core sample totals, counts, prices and ratings; it does not establish full-category sales or new-product trends. A derived MoM/YoY requires two returned comparable dates, identical category, scope, sample, metric, unit and denominator. Missing baseline is not zero growth.
- Launch-trend rows group products by launch month/year within one selected snapshot. They are cohorts, not repeated demand observations or historical market growth.
- Product `monthlySalesFloor` / `monthlyRevenueFloor` are product-level lower-bound estimates; summing an incomplete product sample cannot replace market totals.
- Market movement alone does not identify a cause, seller conversion, profitability, or a recommended launch date.
