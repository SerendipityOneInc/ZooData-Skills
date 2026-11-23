# Listing members

## Task input

One known parent ASIN, US marketplace and the required snapshot month.

## Endpoints and call order

Read `openapi_v2_products_detail` in parent-member mode. Check the connected tool’s billing before the read.

## Listing members · `products/detail`

### Request parameters

Pass `parentAsin` and, for historical comparisons, `dateRange` as YYYY-MM. The first member is sufficient for representative variant details. Use page 1 and pageSize 1. Omit `asins`.

```json
{"parentAsin":"B000000001","dateRange":"2026-10","marketplace":"US","page":1,"pageSize":1}
```

### Response handling

Read `data.items` and `context.resolvedDate`. Members are ordered by monthly purchase lower bound descending, then ASIN. A returned member’s title, brandName and imageUrl describe that variant. An empty result supplies no representative. For a historical request keep the requested month and any returned date; do not substitute current records.

## Deliverable

A confirmed member of the requested listing and its available identifying attributes.
