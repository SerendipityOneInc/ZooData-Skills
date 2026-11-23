# Weekly search demand

Set the requested window using the [trend period rule](../../../contract/query.md#select-the-trend-period) before the read.

Read weekly search volume or ABA rank for specified queries.

## Task input

Named search queries and the observation period.

## Endpoints and call order

1. Call `openapi_v2_keyword_trend` (`keywords/trend`). Check billing before the first read.

## `keywords/trend`

### Request parameters

| Parameter | Use |
|---|---|
| `keyword` | The search term for this request. |
| `dateFrom` | Required. Start date for weekly records. |
| `dateTo` | Required. End date for weekly records. |
| `keywords` | Use exactly one of `keyword` or `keywords`. Batch 1–20 unique lowercase, trimmed terms. Each date range covers at most 93 days. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"keyword":"small storage baskets","dateFrom":"2026-08-16","dateTo":"2026-11-07"}
```

### Response handling

1. Read each term’s `series` with its returned week boundaries, `estimateSearchCount`, `abaRank` and any requested `abaTop3ClickShareRate` or `abaTop3ConversionShareRate`. When used alongside ASIN exposure and position, align observations by week.

## Deliverable

Weekly observations of the requested measures for each term, with actual week boundaries.
