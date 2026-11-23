# Keyword statistics

## Task input

Named queries and the baseline measures requested.

## Endpoints and call order

1. Call `openapi_v2_keyword_detail` (`keywords/detail`). Check billing before the first read.

## `keywords/detail`

### Request parameters

| Parameter | Use |
|---|---|
| `keyword` / `keywords` | Supply one term or a list of 1–20 unique, trimmed lowercase terms. Batch terms sharing the same period. |
| `date` | Required lookup date (YYYY-MM-DD). For the latest completed data, use yesterday's date. Use the returned week for reporting. |
| `marketplace` / `granularity` | US / week. |

```json
{"keywords":["small storage baskets","woven baskets"],"date":"2026-11-07"}
```

### Response handling

1. Read the actual week from `data.context`. For each `data.items[]` match its `identity` and `status` with its `snapshotData`.
2. Read the requested measures: `estimateSearchCount`, `abaRank`, Top-3 click or purchase shares, product counts, title coverage or leading organic products’ averages. Keep empty items associated with their term.

## Deliverable

Requested baseline statistics per query and actual week.
