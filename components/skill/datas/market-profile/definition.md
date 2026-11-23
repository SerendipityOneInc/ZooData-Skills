# Category profile

Compare category-wide demand and the leading-product sample for a named market.

## Task input

Resolved categories and the market measures requested.

## Endpoints and call order

1. Call `openapi_v2_markets_profile` (`markets/profile`). Check billing before the first read.

## `markets/profile`

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

1. Read whole-market measures from `marketSize` and sample measures from `sampleProfile`. Select the price, rating, new-product and concentration blocks needed by the question.
2. Use the returned business date. Category totals cover parent products (SPUs); sample measures cover only the selected leading SPUs. Compare the same descendant scope and sample selection across categories.

## Deliverable

Category size and a profile of its leading products.
