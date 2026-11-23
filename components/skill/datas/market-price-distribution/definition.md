# Category price distribution

Compare the distribution of products and sales across a category’s price bands.

## Task input

Resolved categories and the requested price distribution scope.

## Endpoints and call order

1. Call `openapi_v2_markets_price_distributions` (`markets/price-distributions`). Check billing before the first read.

## `markets/price-distributions`

### Request parameters

| Parameter | Use |
|---|---|
| `categoryIds` | Required. Array of confirmed category IDs. |
| `sampleType` | Choose the leading-product sample by unit sales or revenue. |
| `includeDescendantCategoryProducts` | Whether to include products in descendant categories. |
| `date` | Observation date as YYYY-MM-DD. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"categoryIds":["679399011"]}
```

### Response handling

1. Read `priceDistribution` with its price bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.
2. Use the requested category and sample on the resolved business date. Read the returned lower-inclusive, upper-exclusive price bounds and keep the sample denominator with the shares.

## Deliverable

Product counts, sales and shares by price band.
