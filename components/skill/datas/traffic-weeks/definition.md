# Weekly ASIN exposure

Set the requested window using the [trend period rule](../../../contract/query.md#select-the-trend-period) before the read.

Read weekly exposure and placement measures for selected ASINs.

## Task input

Product ASINs and the observation period.

## Endpoints and call order

1. Call `openapi_v2_product_traffic_trend` (`keywords/product-traffic-trend`). Check billing before the first read.

## `keywords/product-traffic-trend`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | One product ASIN. |
| `dateFrom` | Required. Start date for weekly records. |
| `dateTo` | Required. End date for weekly records. |
| `asins` | An array of product ASINs for a multi-product lookup. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14","dateFrom":"2026-08-16","dateTo":"2026-11-07"}
```

### Response handling

1. Read the returned status and weekly `series` for each ASIN.
2. Retain weekly boundaries, total/organic/ad exposure points, term counts and the returned placement and demand-rank distributions. Compare like measures across the requested weeks.

3. Each request supports up to 26 complete Sunday–Saturday weeks. Use the weekly organic, ad and total estimated exposure points. Compute shares only with a positive total.

## Deliverable

Comparable weekly exposure records for each product.
