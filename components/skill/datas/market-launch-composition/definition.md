# Launch composition

## Task input

Group a category’s leading listings by their first launch dates.

## Endpoints and call order

`openapi_v2_markets_listing_launch_trend` (`markets/listing-launch-trend`).

## `markets/listing-launch-trend`

### Request parameters

Batch the category IDs in `categoryIds`. For sales rankings use `sampleType="unitSalesTop100"` and the selected descendant scope. Set `dateFrom` and `dateTo` to the inclusive first-launch dates and `granularity="month"` to group the filtered listings. This endpoint always reads the latest ranked sample.

```json
{"categoryIds":["679399011"],"sampleType":"unitSalesTop100","includeDescendantCategoryProducts":true,"dateFrom":"2026-05-04","dateTo":"2026-10-31","granularity":"month"}
```

### Response handling

Use the latest market search’s resolved ranking date as the reference. For each category sum its monthly `points[].productCount` values. Preserve explicit zeros. Treat absent categories or missing counts as unavailable.

## Deliverable

Launch composition.
