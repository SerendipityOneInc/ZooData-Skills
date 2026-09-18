# Market Metric Semantics

This module owns returned market-field meaning, denominator, time grain, and inference limits. `reference.md` owns where and how the fields are requested; scenarios own what decision may follow.

## Market size and selected sample

| Field family | Population and meaning | Permitted inference | Prohibited shortcut |
|---|---|---|---|
| `totalSkuCount`, `totalSpuCount` | All products in the selected category scope at the returned snapshot | Category supply size, with SKU/SPU distinction | Treat `meta.total` or Top 100 count as total products |
| `totalMonthlySales`, `totalMonthlyRevenue` | Estimated monthly units and revenue for the full category scope | Category-scale demand and revenue | Calculate revenue as price × sales or call it seller sales |
| `sampleSkuCount`, `sampleMonthlySales`, `sampleMonthlyRevenue` | Selected Top 100, possibly fewer than 100 products | Sample size and selected-sample scale | Treat a Top 100 measure as the whole category |
| `sampleSalesCoverageRate`, `sampleRevenueCoverageRate` | Selected Top 100 share of the corresponding all-category measure | Describe sample coverage | Apply sales coverage to revenue or infer an unreturned remainder's structure |
| `sampleMedianPrice` and `sampleAvgPrice` | Price measures of the selected sample with different aggregation | Describe observed price positioning | Infer margin, profit, or the price of every product |
| `sampleAvgGrossMarginRate` | Service-estimated average gross-margin rate for the selected sample | Describe this sample estimate with its source and date | Treat it as the seller's actual unit margin or contribution margin |

The sample is chosen by `sampleType`; `unitSalesTop100` and `revenueTop100` can contain different products. Every Top 100 claim carries the sample selector and returned date. A `subtree` total includes descendants; a `direct` total does not.

## Structure, entry, and concentration

- `sampleTop10ProductSalesRate`, `sampleTop10ProductRevenueRate`, `sampleTop10BrandSalesRate`, and `sampleTop10BrandRevenueRate` are concentration rates within the selected Top 100. They are not whole-category CR10 unless a separate contract explicitly says so. Keep product versus brand and sales versus revenue denominators distinct.
- `sampleBrandCount`, `sampleSellerCount`, `sampleAvgSellerCount`, `sampleAvgRating`, and `sampleAvgRatingCount` describe the selected sample. A low review count may indicate a lower observed review barrier, but it does not prove easy entry or conversion.
- `sampleFbmRate`, `sampleAPlusRate`, and `sampleVideoRate` are shares in the selected sample. They are content and fulfillment observations, not cost, margin, or compliance measures.
- `sampleNewProductCount6m`, `sampleNewProductRate6m`, `sampleNewProductMonthlySales6m`, and `sampleNewProductMonthlyRevenue6m` describe the service-defined six-month new-product subset of the selected Top 100. The rate uses the selected sample as its denominator. The response no longer names a conservative classification; do not apply thresholds or conclusions calibrated to that former definition. `newProductMetrics[]` adds period-specific observations, keyed by `periodMonths`, with the same sample boundary. These fields are not an exhaustive count of category entrants or a survival rate.
- `topNMetrics[]` reports product, brand, and seller concentration for each returned `n`; each sales or revenue rate uses the selected sample's corresponding total. A nested `productSalesRate` is not a full-category share. Keep the grouping (`product`, `brand`, `seller`) and measure (`sales`, `revenue`) explicit.
- `markets/structure-profile.data.buckets[]` partitions one selected Top 100 dimension for the returned date. Its `skuRate`, `salesRate`, and `revenueRate` have different denominators. An example ASIN is an illustration of its bucket, not proof that the entire category has that property.

## Time and product observations

- `markets/search` gives a current or requested daily market snapshot. `markets/history.points[]` gives available month-end snapshots. A daily row and a month-end point may differ because of date, coverage, or data refresh; do not label their raw difference MoM.
- History `*MomRate` and `*YoyRate` values belong to the exact metric and available point returned by the service. A missing rate means the comparable baseline is unavailable, not zero growth. `sampleSkuMomTurnoverRate` describes turnover of selected products, not a causal entry/exit explanation.
- `products/search.monthlySalesFloor` and `monthlyRevenueFloor` are product-level lower-bound estimates. They cannot be added to replace `totalMonthlySales` or `totalMonthlyRevenue` without a documented complete population.
- Market movement, a new-product share, or a price shift may guide an investigation. None identifies its cause, actual seller conversion, profitability, or a recommended launch date by itself.
