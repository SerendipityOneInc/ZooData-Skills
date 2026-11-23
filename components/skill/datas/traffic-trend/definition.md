# ASIN exposure trends

Set the requested window using the [trend period rule](../../../contract/query.md#select-the-trend-period) before the read.

Inspect exposure direction and volatility over the requested windows.

## Task input

Product ASINs, ending week and comparison windows.

## Endpoints and call order

1. Call `openapi_v2_product_traffic_trend_profile` (`keywords/product-traffic-trend-profile`). Check billing before the first read.

## `keywords/product-traffic-trend-profile`

### Request parameters

| Parameter | Use |
|---|---|
| `asin` | One product ASIN. |
| `date` | Required. Observation date as YYYY-MM-DD. |
| `windowPeriods` | The supported window is `[4]` (four weeks). |
| `asins` | An array of product ASINs for a multi-product lookup. |
| `detailLevel` | Select the supported detail level needed for the question. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"asin":"B0C7P89D14","date":"2026-11-07","windowPeriods":[4]}
```

### Response handling

1. Read each window row's status, then the available components in `trafficTrendProfile`. For each component, read `trend`, `trendEvidence`, `volatilityLevel` and `lastPeriodWindowPosition` when returned.

## Deliverable

Exposure direction, change and volatility by window.
