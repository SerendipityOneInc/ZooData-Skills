# Star-rating distribution

## Task input

Confirmed category IDs, inclusion scope, sample and observation date.

## Endpoints and call order

1. Before the first read check billing, then call `openapi_v2_markets_rating_distributions` (`markets/rating-distributions`).

## `markets/rating-distributions`

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

1. Read `ratingDistribution` with its star-rating bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.
2. Use (lower, upper] for star scores, including 5 in the final band.

## Deliverable

Star-rating distribution for the specified category sample.
