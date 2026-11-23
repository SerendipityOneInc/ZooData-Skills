# Listing-age distribution

## Task input

Confirmed category IDs, inclusion scope, sample and observation date.

## Endpoints and call order

1. Before the first read check billing, then call `openapi_v2_markets_listing_age_distributions` (`markets/listing-age-distributions`).

## `markets/listing-age-distributions`

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

1. Read `listingAgeDistribution` with its listing-age bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.
2. Use calendar-month ages with inclusive lower and exclusive upper bounds.

## Deliverable

Listing-age distribution for the specified category sample.
