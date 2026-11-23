# Traffic terms

Identify the queries contributing exposure to an ASIN for the selected period.

## Task input

One ASIN, observation week and requested ordering of traffic terms.

## Endpoints and call order

1. Call `openapi_v2_product_traffic_terms` (`keywords/product-traffic-terms`). Check billing before the first read.

## `keywords/product-traffic-terms`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | Required. One product ASIN. |
| `date` | Required. Observation date as YYYY-MM-DD. |
| `sortBy` | A supported sort field. |
| `sortOrder` | Ascending (asc) or descending (desc). |
| `exploreTypes` | Optional placement-type filter for organic or sponsored positions. |
| `page` | Page number for paged reads. |
| `pageSize` | Number of records per page. |
| `marketplace` | Use `US` for Amazon US. |

| Retrieval purpose | Sort |
|---|---|
| Higher exposure contribution | `trafficShare desc` or `estimateImpressionPoint desc` |
| Better observed position within one placement type | `avgPosition asc` or `absolutePosition asc` |
| Higher query demand | `keywordEstimateSearchCount desc` |

```json
{"asin":"B0C7P89D14","date":"2026-11-07","sortBy":"trafficShare","sortOrder":"desc"}
```

### Response handling

1. Read query, `trafficShare`, `estimateImpressionPoint`, position, placement type, query search count/ABA rank and observation coverage from each row. Page for the requested coverage.


2. Each share uses that ASIN’s total observed exposure for the period. A missing position is unknown. Keep the latest observed position and average position separate.

## Deliverable

Traffic terms with exposure contributions and positions.
