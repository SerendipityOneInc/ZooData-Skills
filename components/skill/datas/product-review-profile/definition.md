# Product review profile

Retrieve an aggregate review profile for one or more Amazon US ASINs, including problems, praise, requested improvements and mention rates.

## Task input

One or more product ASINs and an optional review period.

## Endpoints and call order

1. Query the review profile using `openapi_v2_voc_analysis` (`voc/analysis`).
2. Only if no profile is available, read the original text via `openapi_v2_realtime_reviews` (`realtime/reviews`) and build the profile.

## `voc/analysis`

### Request parameters

| Parameter | Required | Use |
|---|---|---|
| `mode` | Yes | Use `asin`. |
| `asins` | Yes | 1–100 product ASINs per combined profile. Each supplied ASIN selects its parent’s review population. ASINs sharing a parent contribute one population. |
| `marketplace` | No | Use `US` for Amazon US. |
| `period` | No | Send `1y` (last 12 months) unless requested otherwise. Supported: `1m`, `3m`, `6m`, `1y`, `2y`. |

```json
{"mode":"asin","asins":["B0C7P89D14"],"marketplace":"US","period":"1y"}
```

### Response handling

Retain the requested ASINs, confirmed parent identities when available, and the reviewed population. A parent aggregate supports family-level findings. Attribute feedback to a specific variant only when review records identify that variant. Use `data` as the profile. Finish on a populated profile, preserving unavailable fields, absent themes and observed zeroes.

Use the real-time endpoint when the lookup yields no profile or `reviewCount=0`. Stop on authentication, connection or budget failures.

## `realtime/reviews`

### Request parameters

| Parameter | Required | Use |
|---|---|---|
| `asin` | Yes | One product ASIN per fallback request. |
| `marketplace` | No | Use the original marketplace, `US`. |
| `cursor` | No | Omit on the first page. Use the previous `nextCursor` for later pages and stop at null. |

```json
{"asin":"B0C7P89D14","marketplace":"US"}
```

### Response handling

1. Within budget, use dated, readable reviews from the same requested period. Deduplicate across pages and ASINs; count each review once per theme.
2. Build the profile in the format below. Average numeric stars only in the corresponding overall or theme population. Compute distributions and rates where supported; mark unavailable measures accordingly. Identify the observed products, dates and page-review sample. If there is no usable text, report the profile as unavailable.

## Deliverable

Deliver one review profile in the following order. Use business labels in reports and the API field names for structured results.

1. **Population**: `mode`, `asins` or `categoryPath`, coverage dates `dateRangeStart` / `dateRangeEnd`, and `reviewCount`.
2. **Rating and sentiment summary**: overall `avgRating`, verified purchase rate `verifiedRate`, star counts `ratingDistribution`, and sentiment shares `sentimentDistribution`.
3. **Themes and top terms**: `consumerInsights` and `topKeywords` use the same item fields: `labelType`, `element`, `count`, `reviewRate` and theme `avgRating`. Use the profile's review count as the mention-rate denominator. Keep `issues`, `painPoints`, `positives` and `improvements` in separate dimensions. Rank within a dimension by count and keep tied values tied.
