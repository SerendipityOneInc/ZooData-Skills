# Category review profile

Retrieve an Amazon US category review profile covering use cases, purchase drivers, buyer complaints and requested improvements.

## Task input

One resolved category path and an optional review period.

## Endpoints and call order

1. Query the review profile using `openapi_v2_voc_analysis` (`voc/analysis`).

## `voc/analysis`

### Request parameters

| Parameter | Required | Use |
|---|---|---|
| `mode` | Yes | Use `category`. |
| `categoryPath` | Yes | Array of category names from root to target. |
| `marketplace` | No | Use `US` for Amazon US. |
| `period` | No | Send `1y` (last 12 months) unless requested otherwise. Supported: `1m`, `3m`, `6m`, `1y`, `2y`. |

```json
{"mode":"category","categoryPath":["Home & Kitchen","Storage & Organization"],"marketplace":"US","period":"1y"}
```

### Response handling

Use `data` as the profile. Finish on a populated profile, preserving unavailable fields, absent themes and observed zeroes.

Report the requested category and period if its profile is unavailable.

## Deliverable

Deliver one review profile in the following order. Use business labels in reports and the API field names for structured results.

1. **Population**: `mode`, `asins` or `categoryPath`, coverage dates `dateRangeStart` / `dateRangeEnd`, and `reviewCount`.
2. **Rating and sentiment summary**: overall `avgRating`, verified purchase rate `verifiedRate`, star counts `ratingDistribution`, and sentiment shares `sentimentDistribution`.
3. **Themes and top terms**: `consumerInsights` and `topKeywords` use the same item fields: `labelType`, `element`, `count`, `reviewRate` and theme `avgRating`. Use the profile's review count as the mention-rate denominator. Keep `issues`, `painPoints`, `positives` and `improvements` in separate dimensions. Rank within a dimension by count and keep tied values tied.
