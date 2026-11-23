# Product history

Set the requested window using the [trend period rule](../../../contract/query.md#select-the-trend-period) before the read.

Track an ASIN’s observed prices, category ranks or page changes over a specified period.

## Task input

One product ASIN, measures and period.

## Endpoints and call order

1. Call `openapi_v2_products_history` (`products/history`) once per ASIN and window, grouping the requested fields in `aspects`. Check billing before the first read.

## `products/history`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | Required. One product ASIN. |
| `startDate` | Required. First date, YYYY-MM-DD. |
| `endDate` | Required. Last date, YYYY-MM-DD. |
| `aspects` | Select the requested series: `title` for the title, `imageUrl` for the main image, `price` for the price, ranks with their categories (`bsr`, `bsrCategory`, `subBsr`, `subBsrCategory`), and stars and cumulative rating counts (`rating`, `ratingCount`). Include `parentAsin` when checking a change of parent. Omit for all supported series. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14","startDate":"2026-10-01","endDate":"2026-10-31","aspects":["title","imageUrl","price"]}
```

### Response handling

1. Title (`title`) and main-image (`imageUrl`) events have a `date` and `value`. Compare consecutive known values. Label the dates of the earlier and later observations. Across a sampling gap, the effective change date is unknown. A single observation establishes a baseline. Show changed image URLs; describe visual differences only after inspecting both images.
2. Match prices (`price`), BSR, purchase lower bounds and ratings to `timestamps` by index. Calculate price differences from known prices of the same ASIN. Preserve the observed date range when there is a gap.
3. Retain observed coverage and distinguish parent/child scopes and ranking categories. Report insufficient comparable observations separately from no observed change.

## Deliverable

Dated observations and page changes for the requested measures.
