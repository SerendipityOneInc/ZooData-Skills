# Launch composition

## Task input

Group a category’s leading listings by their first launch dates.

## Endpoints and call order

`openapi_v2_markets_listing_launch_trend` (`markets/listing-launch-trend`).

## `markets/listing-launch-trend`

### Request parameters

Supply categoryIds, sampleType, includeDescendantCategoryProducts and granularity (month or year). Optional dateFrom and dateTo filter first launch dates.

```json
{"categoryIds": ["679399011"], "granularity": "month"}
```

### Response handling

Read points[].date and productCount for the selected leading sample. Estimating entry success requires the full launch cohort.

## Deliverable

Launch composition.
