# Real-time product details

Retrieve the current offer, specifications or selling-point text for a named ASIN.

## Task input

One ASIN and the current page information requested.

## Endpoints and call order

1. Call `openapi_v3_realtime_product` (`realtime/product`). Check billing before the first read.

## `realtime/product`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | Required. One product ASIN. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14"}
```

### Response handling

1. Extract the requested fields from `data`. Use `buyboxWinner.price` for the current offer and preserve the source section and variant for specifications and bullet text.
2. If the tool cannot return a section, mark that section unavailable. Retry only under the connector’s documented retry rules and the remaining budget.

## Deliverable

Current offer, specifications or page text.
