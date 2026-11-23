# Amazon US product details

Look up Amazon US product details by ASIN, including the title, brand, category, listing date, price, Best Sellers Rank (BSR), monthly purchase lower bound and ratings.

## Task input

One or more Amazon US product ASINs.

## Endpoints and call order

1. First use `openapi_v2_products_detail` (`products/detail`) to read the latest stored snapshot for the specified products.
2. For a snapshot miss, call `openapi_v3_realtime_product` (`realtime/product`) directly for that product.

## Product details · `products/detail`

### Request parameters

| Parameter | Required | Value |
|---|---|---|
| `asins` | Yes | 1–50 distinct product ASINs, each 10 uppercase letters or digits. |
| `marketplace` | No | Defaults to `US`, the only supported marketplace. |
| `dateRange` | No | Omit to read the latest snapshot. |

```json
{"asins":["B000000001","B000000002"],"marketplace":"US"}
```

### Response handling

1. Read `data.items` in request order. Each item identifies the requested product in `identity.asin`. Use `data.context.resolvedDate` as the data date when present.
2. For `status=ok`, use the returned `product` and finish the lookup for that ASIN even if some fields are empty. Each successful item costs one credit.
3. An item with `status=empty` and `emptyReason=asin_not_found` is a snapshot miss. Use the real-time endpoint for that ASIN. If the snapshot service fails, look up only unresolved products.
4. Correct invalid parameters on a 422 response. Stop on authentication, connection or budget failures and identify the affected ASINs.

## Real-time product details · `realtime/product`

### Request parameters

| Parameter | Required | Value |
|---|---|---|
| `asin` | Yes | One unresolved product ASIN per request. |
| `marketplace` | No | Use the same US marketplace as the original request. Defaults to `US`. |

```json
{"asin":"B000000002","marketplace":"US"}
```

### Response handling

1. Read the current product from `data`. Use only the requested fields present, such as the title, specifications or the current offer price in `buyboxWinner.price`.
2. If the real-time lookup fails, or a requested field is missing, mark the affected information unavailable and retain the records already obtained.

## Deliverable

1. Preserve numeric zeroes. Label prices in USD, monthly purchase and revenue lower bounds as such, and each rank with its category. Keep variant measures separate from parent totals.
2. Keep specifications separate from selling points. Preserve the order and source section of any bullet text returned.
