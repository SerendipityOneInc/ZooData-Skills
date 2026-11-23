# Weekly ASIN and query visibility

Set the requested window using the [trend period rule](../../../contract/query.md#select-the-trend-period) before the read.

Compare one ASIN’s weekly exposure and position with demand for the named queries.

## Task input

One ASIN, specified search queries and observation period.

## Endpoints and call order

1. Call `openapi_v2_product_traffic_terms_trend` (`keywords/product-traffic-terms-trend`). Check billing before the first read.

## `keywords/product-traffic-terms-trend`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | Required. One product ASIN. |
| `keyword` | The search term for this request. |
| `dateFrom` | Required. Start date for weekly records. |
| `dateTo` | Required. End date for weekly records. |
| `keywords` | An array of terms for a multi-query lookup. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14","keyword":"small storage baskets","dateFrom":"2026-08-16","dateTo":"2026-11-07"}
```

### Response handling

1. Read each query’s weekly `series`.
2. Read `totalEstimateImpressionPoint`, `trafficByExploreType`, `keywordEstimateSearchCount` and `keywordAbaRank` for each returned period. Within each placement type, compare its own exposure and positions; keep `absolutePosition` and `avgPosition` as separate measures. Read `asinSnapshot` and that placement type's `adActivity` only when needed by the question.
3. Align exposure, position and query search volume or ABA rank by the returned period boundaries. Reuse an available query series; one of search volume or ABA rank is sufficient.

## Deliverable

Weekly exposure, position and available demand for each named query.
