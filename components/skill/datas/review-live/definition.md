# Current page reviews

Read the latest reviews displayed on a named product page.

## Task input

One ASIN and the requested coverage of current page reviews.

## Endpoints and call order

1. Call `openapi_v2_realtime_reviews` (`realtime/reviews`). Check billing before the first read.

## `realtime/reviews`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | Required. One product ASIN. |
| `cursor` | Omit on the first page; use the returned nextCursor for the next page. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14"}
```

### Response handling

1. Read review text and dates from `data.reviews`; use `nextCursor` to determine whether another page is available.
2. Keep this page sample's actual review dates and product scope. It does not replace a requested historical review period.

## Deliverable

Retrieved review text and dates.
