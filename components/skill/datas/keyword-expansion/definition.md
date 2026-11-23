# Related keywords

## Task input

A seed query and the desired coverage on Amazon US.

## Endpoints and call order

1. Call `openapi_v2_keyword_extends` (`keywords/extends`). Check billing before the first read.

## `keywords/extends`

### Request parameters

| Parameter | Use |
|---|---|
| `query` | Required. Identify the language of the seed itself. For a Chinese seed, translate it into one natural English search term before the first request, preserving the product type, stated attributes, brand and model. Pass seeds in any other language verbatim, even in a Chinese conversation. |
| `queryType` | Use fuzzy for ordinary expansion. Use phrase only for an explicit phrase-match request. |
| `sortBy` / `sortOrder` | Default for expansion: relevanceScore desc. For an explicit request use estimateSearchCount desc, abaRank asc or keyword asc. |
| `page` / `pageSize` | Start at page 1. Default page size 20, maximum 100. Page within the requested coverage and budget. |
| `marketplace` / `granularity` | US / week. |

```json
{"query":"small storage baskets","marketplace":"US","queryType":"fuzzy","sortBy":"relevanceScore","sortOrder":"desc","page":1,"pageSize":20}
```

### Response handling

1. From `data.rows[]`, read `matchData.keyword`, `site` and `relevanceScore`. From `keywordSnapshot` read `estimateSearchCount`, `abaRank` and `dataWindow.currentPeriod`.
2. This endpoint uses the latest available week. Keep an empty result empty and retain the distinction between retrieved rows and total matches.

## Deliverable

Candidate keywords with their relevance, weekly estimated searches, ABA rank, week and candidate coverage.
