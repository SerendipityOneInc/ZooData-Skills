# Market Metric Semantics

This module owns returned market-field meaning, denominator, time grain, and inference limits. `reference.md` owns where and how the fields are requested; scenarios own what decision may follow.

## Market size and selected sample

| Field family | Population and meaning | Permitted inference | Prohibited shortcut |
|---|---|---|---|
| `marketTotal.skuCount`, `marketTotal.spuCount` | All products in the selected category scope at the returned snapshot | Category supply size, with SKU/SPU distinction | Treat `meta.total` or Top 100 count as total products |
| `marketTotal.monthlySales`, `marketTotal.monthlyRevenue` | Estimated monthly units and revenue for the full category scope | Category-scale demand and revenue | Calculate revenue as price × sales or call it seller sales |
| `marketSample.skuCount`, `marketSample.monthlySales`, `marketSample.monthlyRevenue` | Selected Top 100, possibly fewer than 100 products | Sample size and selected-sample scale | Treat a Top 100 measure as the whole category |
| `marketSample.salesCoverageRate`, `marketSample.revenueCoverageRate` | Selected Top 100 share of the corresponding all-category measure | Describe sample coverage | Apply sales coverage to revenue or infer an unreturned remainder's structure |
| `marketSample.medianPrice` and `marketSample.avgPrice` | Price measures of the selected sample with different aggregation | Describe observed price positioning | Infer margin, profit, or the price of every product |
| `marketSample.avgGrossMarginRate` | Service-estimated average gross-margin rate for the selected sample | Describe this sample estimate with its source and date | Treat it as the seller's actual unit margin or contribution margin |

The sample is chosen by `sampleType`; `unitSalesTop100` and `revenueTop100` can contain different products. Every Top 100 claim carries the sample selector and returned date. A descendant-inclusive market row counts products in that category and its descendants; a direct-only row counts products assigned to that category itself. A parent row and one of its descendant rows can overlap.

## Structure, entry, and concentration

- `marketSample.productTopNMetrics[]` and `marketSample.brandTopNMetrics[]` return N=3/5/10/20 groups. Each `monthlySalesRate` or `monthlyRevenueRate` is a share of the selected Top 100 sample, not the whole category. Product and brand rows have different rank cutoffs and actual selected counts; brand averages are per product within the selected brands. There is no seller Top N array in this market response.
- `marketSample.brandCount`, `marketSample.sellerCount`, `marketSample.avgSellerCount`, `marketSample.avgRating`, and `marketSample.avgRatingCount` describe the selected sample. A low review count may indicate a lower observed review barrier, but it does not prove easy entry or conversion.
- `marketSample.fbmRate`, `marketSample.aPlusRate`, and `marketSample.videoRate` are shares in the selected sample. They are content and fulfillment observations, not cost, margin, or compliance measures.
- A product is new for `periodMonths=N` when its business launch date is later than the snapshot date minus N calendar months and no later than the snapshot date. A product without a business launch date is not counted as new but remains in the applicable product-count denominator.
- `marketTotal.newProductMetrics[]` describes each of the 1/3/6/12-month windows across the full category; `marketSample.newProductMetrics[]` describes those same windows within the selected Top 100. Each row supplies `newSkuCount`, `newSkuRate`, `newSkuMonthlySales`, and `newSkuMonthlyRevenue`; the sample row also supplies averages and sample sales/revenue shares. Identify the exact `periodMonths` row used. A broader claim about all entrants, survival, or seller success needs separate evidence.
- Search `topN` chooses the group used by Top N filters; search `newProductPeriod` chooses the window used by new-product filters and sorting. Neither limits the returned arrays. Distinguish the request selector from the returned `productTopN`/`brandTopN` or `periodMonths` identity.
- `markets/structure-profile.data.buckets[]` partitions one selected Top 100 dimension for the returned date. Its `skuRate`, `salesRate`, and `revenueRate` have different denominators. Bucket `amazonSelfOperated*` fields describe the Amazon self-operated subset inside that bucket, and bucket `newProductMetrics[]` carries all four periods. An example ASIN is an illustration of its bucket, not proof that the entire category has that property.

## Time and product observations

- `markets/search` gives a current or requested daily market snapshot. `markets/history.points[]` gives available month-end snapshots. A daily row and a month-end point may differ because of date, coverage, or data refresh; do not label their raw difference MoM.
- Before its month-end snapshot exists, the current incomplete calendar month is outside a completed-month trend population. Its absence is expected timing, not a missing history point, zero value, or table row.
- The upgraded history response has no server MoM or YoY rate fields. A derived rate requires two returned comparable points for the same metric path, category, scope, sample selector, and month-end grain. A missing comparison point is not zero growth.
- `products/search.monthlySalesFloor` and `monthlyRevenueFloor` are product-level lower-bound estimates. They cannot be added to replace `marketTotal.monthlySales` or `marketTotal.monthlyRevenue` without a documented complete population.
- Market movement, a new-product share, or a price shift may guide an investigation. None identifies its cause, actual seller conversion, profitability, or a recommended launch date by itself.
