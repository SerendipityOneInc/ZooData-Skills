# Keyword demand trend

## Task input

Named queries, as-of date and comparison window.

## Endpoints and call order

1. Call `openapi_v2_keyword_trend_profile` (`keywords/trend-profile`). Check billing before the first read.

## `keywords/trend-profile`

### Request parameters

| Parameter | Use |
|---|---|
| `keyword` / `keywords` | Supply one term or a list of 1–20 unique, trimmed lowercase terms. Batch terms sharing the same period. |
| `date` | Required lookup date (YYYY-MM-DD). For the latest completed data, use yesterday's date. Use the returned week for reporting. |
| `marketplace` / `granularity` | US / week. |
| `windowPeriods` | Required. Select 1–4 distinct supported week counts: 4, 8, 12 or 26. Use 12 for an unspecified weekly window. |

```json
{"keyword":"small storage baskets","date":"2026-11-07","windowPeriods":[12]}
```

### Response handling

1. In `data.items[].rows[]`, read `rowContext`, `status` and `trendProfile` separately for each window. Keep empty windows and missing dimensions distinct.
2. Read `searchDemand` and `abaRank` directions from their `trend` and supporting changes from `trendEvidence`. For demand include `volatilityLevel` and `lastPeriodWindowPosition` when relevant. A first-to-last change describes two values; the trend classification uses the series.

## Deliverable

Search demand and rank trends with their windows, observed changes and volatility.
