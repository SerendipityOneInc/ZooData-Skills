# Seller concentration

## Task input

Confirmed category IDs, inclusion scope, sample and observation date.

## Endpoints and call order

1. Before the first read check billing, then call `openapi_v2_markets_seller_concentrations` (`markets/seller-concentrations`).

## `markets/seller-concentrations`

### Request parameters

| Parameter | Use |
|---|---|
| `categoryIds` | Required. Array of confirmed category IDs. |
| `sampleType` | Choose the leading-product sample by unit sales or revenue. |
| `includeDescendantCategoryProducts` | Whether to include products in descendant categories. |
| `date` | Observation date as YYYY-MM-DD. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"categoryIds": ["679399011"]}
```

### Response handling

1. Read `topnMetrics` and `topSellerList`. Retain each Top-N identity, `concentrationRate`, the sample's ranking basis and each returned entity's sales/revenue measures.

## Deliverable

Seller concentration for the specified category sample.
