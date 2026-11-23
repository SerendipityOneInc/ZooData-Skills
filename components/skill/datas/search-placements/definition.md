# Search placements

Locate named products in the observed search positions for a specified query.

## Task input

One search query, an observation week and the requested placements.

## Endpoints and call order

1. Call `openapi_v2_keyword_search_results` (`keywords/search-results`). Check billing before the first read.

## `keywords/search-results`

### Request parameters

| Parameter | Use |
|---|---|
| `keyword` | Required. The search term for this request. |
| `date` | Required. Observation date as YYYY-MM-DD. |
| `exploreTypes` | Optional placement-type filter for organic or sponsored positions. |
| `sortBy` | A supported sort field. |
| `sortOrder` | Ascending (asc) or descending (desc). |
| `page` | Page number for paged reads. |
| `pageSize` | Number of records per page. |
| `marketplace` | Use `US` for Amazon US. |

Use `absolutePosition asc` for position order or `estimateImpressionPoint desc` for exposure order.

```json
{"keyword":"small storage baskets","date":"2026-11-07"}
```

### Response handling

1. Retain ASIN, readable product identity, `exploreType`, `absolutePosition` and `estimateImpressionPoint`. Compare the selected ASINs under the same query, period and placement type, with the acquired record scope.
2. Read `keywordTotalEstimateImpressionPoint` once per query-period. For a requested within-sample exposure share, sum the selected group's row-level exposure points and divide by the same sample's total row-level points.

## Deliverable

Observed products, positions and exposure for the query.
