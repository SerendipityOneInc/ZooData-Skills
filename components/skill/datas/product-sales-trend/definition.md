# Monthly purchases and revenue for one Amazon US product

Set the requested window using the [trend period rule](../../../contract/query.md#select-the-trend-period) before the read.

Read monthly purchase and revenue lower bounds and changes for one Amazon US ASIN. A single read provides both the selected ASIN and parent series. Reuse observations covering the requested months.

## Task input

One ASIN, requested months and purchase or revenue measures.

## Endpoints and call order

Use the connected ZooData operation `openapi_v2_products_sales_trend` for logical read `products/sales-trend`. Inspect its current schema on first use. A request costs 1 credit for one ASIN regardless of the number of months.

## `products/sales-trend`

### Request parameters

| Argument | How to supply it |
|---|---|
| `asin` | Required. One canonical identifier of ten uppercase letters or digits. |
| `marketplace` | `US` only, also the default. |
| `startMonth` | First included month in YYYY-MM, from 2026-02. If omitted, the API starts eleven months before the end. Pass the start month explicitly for the selected trend period. |
| `endMonth` | Last included month in YYYY-MM. Default is the month containing the UTC date two days ago. The whole range can cover up to 24 months. |

For the latest finalized months, end one month before the month containing the UTC date two days ago. Pass explicit bounds. If the seller names a month, retain that month. If part of the requested period precedes coverage, query the supported overlap and label the earlier months unavailable. If the user requests more than 24 months, agree on the window or additional reads within their budget before querying.

Example arguments for three specified months:

```json
{"asin":"B000000001","marketplace":"US","startMonth":"2026-08","endMonth":"2026-10"}
```

### Response handling

1. Return observations in month order. For each month retain the ASIN and its purchase lower bound, the parent ASIN and its corresponding lower bound, and the returned revenue lower bounds in USD when requested.
2. Retain `pointKind`. Compare completed months (`monthEnd`) with each other. Treat `monthToDate` as provisional for the returned `month`. On the first two UTC days of a month, the previous month can still be provisional. For an explicitly requested month retain its identity and status. Use returned adjacent-month growth rates. A partial month or a missing, null or nonpositive prior base has no valid completed-month growth rate.
3. Distinguish `inCatalog=false` (no catalog record) from `inCatalog=true` with a null measure (record present, measure unavailable). Preserve numeric zeroes. Pass the same labeled observations to the calling workflow.
4. WorkBuddy handles authentication. If setup is needed, direct the user to the ZooData connector. After a failed read, keep available observations and identify the missing period. Correct invalid inputs when the error specifies how. Avoid repeat reads for an empty month or an uncertain charge.

## Deliverable

Monthly purchase lower bounds for the selected ASIN and its listing, with revenue lower bounds when requested.
