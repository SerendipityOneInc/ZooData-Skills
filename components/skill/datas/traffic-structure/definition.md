# ASIN traffic sources

Compare organic and sponsored exposure for the selected ASINs.

## Task input

Product ASINs and the observation week.

## Endpoints and call order

1. Call `openapi_v2_product_traffic_structure_profile` (`keywords/product-traffic-structure-profile`). Check billing before the first read.

## `keywords/product-traffic-structure-profile`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | One product ASIN. |
| `date` | Required. Observation date as YYYY-MM-DD. |
| `asins` | An array of product ASINs for a multi-product lookup. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14","date":"2026-11-07"}
```

### Response handling

1. Read each ASIN’s `productTrafficTermsProfile` and its current and previous periods.
2. Read `summary`, `trafficStructureChange`, `organicStructureChange` and `termChangeDrivers` as returned. Retain channel keys and the actual fields of any supplied driver records.

## Deliverable

Traffic sources and channel shares for each product.
