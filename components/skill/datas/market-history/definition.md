# Market history

## Task input

Confirmed category IDs, consistent sample scope and the requested period.

## Endpoints and call order

1. Before the first read check billing, then call `openapi_v2_markets_history` (`markets/history`).

## `markets/history`

### Request parameters

| Parameter | Use |
|---|---|
| `categoryIds` | Required. Array of confirmed category IDs. |
| `sampleType` | Choose the leading-product sample by unit sales or revenue. |
| `includeDescendantCategoryProducts` | Whether to include products in descendant categories. |
| `dateFrom`, `dateTo` | Required start and end dates (YYYY-MM-DD). |
| `marketplace` | Use `US` for Amazon US. |

```json
{"categoryIds": ["679399011"], "dateFrom": "2026-05-01", "dateTo": "2026-10-31"}
```

### Response handling

1. Pass category IDs, `dateFrom`, `dateTo` and consistent inclusion/sample rules. Read each returned series' category identity and `points`.
2. Align the returned month-end dates and compare the same measures from `marketSize` or `sampleProfile`. Calculate requested changes from those observations and retain sample selection at each point.
3. Use the [shared trend windows](../../../contract/query.md) when no period is given.

## Deliverable

For `marketSize.monthlySales`, identify the category for each series and the month for each observation.
