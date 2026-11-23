# Category market discovery

## Task input

Find Amazon US categories under confirmed market conditions.

## Endpoints and call order

`openapi_v2_markets_search` (`markets/search`).

## `markets/search`

### Request parameters

Pass the confirmed markets together in `categoryIds` (up to 100 distinct IDs per request). Set `pageSize` to cover the batch. Set filters, sortBy and sortOrder for the requested decision. Use date, sampleType, includeDescendantCategoryProducts, page and pageSize to control scope. For new listings among sales leaders use `sampleType="unitSalesTop100"`. The supported `newProductPeriod` values ("1", "3", "6", "12") select precomputed counts. The first included launch date is the returned data date shifted back that many calendar months, plus one day. Use the count for a day-based request only if its first included date matches the requested cutoff. For a ranking by a matching count use `sortBy="sampleNewProductCount"`, `sortOrder="desc"`. Read that count alongside the actual `sampleProductCount`. A missing count is unknown.

```json
{"categoryIds": ["679399011"], "sortBy": "totalMonthlySales", "sortOrder": "desc"}
```

### Response handling

Retain category identity, path, resolved date and coverage. Distinguish totalMonthlySales and totalMonthlyRevenue from the leading sample metrics.

## Deliverable

Category market discovery.
