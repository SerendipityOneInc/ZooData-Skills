# Keyword market profile

## Task input

Named queries, comparison week and relevant demand or competition dimensions.

## Endpoints and call order

1. Call `openapi_v2_keyword_market_profile` (`keywords/market-profile`). Check billing before the first read.

## `keywords/market-profile`

### Request parameters

| Parameter | Use |
|---|---|
| `keyword` / `keywords` | Supply one term or a list of 1–20 unique, trimmed lowercase terms. Batch terms sharing the same period. |
| `date` | Required lookup date (YYYY-MM-DD). For the latest completed data, use yesterday's date. Use the returned week for reporting. |
| `marketplace` / `granularity` | US / week. |

```json
{"keyword":"small storage baskets","date":"2026-11-07"}
```

### Response handling

1. Read the week from `data.context` and each term’s `marketProfile` from `data.items[]`. An identity-only item has no available profile.
2. For each requested dimension, use its `level`, `interpretation` and `levelEvidence` values. `demandScale` gives estimated searches and ABA rank. `top20OrganicEntryDifficulty` describes entry into the first 20 organic positions. `supplySaturation` grades supply, with result counts, observed products and title coverage as distinct measures.
3. `organicProductBenchmark` describes average ratings, counts and sales of leading organic products. `top3Concentration` gives separate shares of clicks and purchases. `brandStructure` describes brand concentration. `adCoverage` measures the share of observed products seen in sponsored placements.
4. Read annual seasonality from `annualSeasonality`. Report peak periods only when returned.

## Deliverable

Same-week profiles with the evidence for each reported dimension.
