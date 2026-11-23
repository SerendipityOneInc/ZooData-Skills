# Product concentration

## Task input

Confirmed category IDs, inclusion scope, sample and observation date.

## Endpoints and call order

1. Before the first read check billing, then call `openapi_v2_markets_top_product_concentrations` (`markets/top-product-concentrations`).

## `markets/top-product-concentrations`

### Request parameters

| Parameter | Use |
|---|---|
| `categoryIds` | Required. Send up to 100 distinct category IDs together for the same date and scope. Each returned market costs 1 credit at the current endpoint rate. |
| `sampleType` | Choose the leading-product sample by unit sales or revenue. |
| `includeDescendantCategoryProducts` | Whether to include products in descendant categories. |
| `date` | Observation date as YYYY-MM-DD. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"categoryIds": ["679399011"]}
```

### Response handling

1. Read `topnMetrics` and `topProductList`. Retain each Top-N identity, `concentrationRate`, the sample's ranking basis and each returned entity's sales/revenue measures.

## Deliverable

Product concentration for the specified category sample.
