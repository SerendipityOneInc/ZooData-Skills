# Product search

Find products for a specified use, keyword or category under confirmed filters.

## Task input

The confirmed search scope (all categories or one category), any product keyword, active filters and requested order. A keyword is optional.

## Endpoints and call order

1. Call `openapi_v2_products_search` (`products/search`). Check billing before the first read.

## `products/search`

### Request parameters

| Parameter | Use |
|---|---|
| `dateRange` | Omit for the latest available catalog. For a historical month, pass YYYY-MM to select its month-end record. |
| `keyword` | The search term for this request. |
| `categoryPath` | Path from the root to the target category. |
| `keywordMatchType` | Include only with a nonblank keyword. |
| `listingAge` | Maximum time since launch: `30d`, `90d`, `180d`, `1y` or `2y`. Use `180d` for the past six months. Omit for an unrestricted age. |
| `monthlySalesMax`, `fulfillments` | Purchase lower-bound cap and fulfillment types when selected. |
| `sortBy` | A supported sort field. |
| `sortOrder` | Ascending (asc) or descending (desc). |
| `page` | Page number for paged reads. |
| `pageSize` | Number of records per page. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"keyword":"small storage baskets"}
```

### Response handling

1. Retain ASINs, attributes and category paths. Distinguish total matches from the number of rows read.
2. Keep the requested period separately from the resolved data date. For a successful explicit historical month query, the catalog serves that month end. For latest data, use the returned business date if present. If the latest response has no business date, retain the rolling 30-day window and leave its exact cutoff unknown.
3. In the latest daily catalog, `salesGrowthRate` compares this ASIN’s current trailing-30-day purchase lower bound with its own same-basis lower bound recorded 30 days earlier. For its listing, pair `parentMonthlySalesFloor` with `parentSalesGrowthRate` on the same dates and retain `parentAsin`. The returned rate and its filter parameters use decimal units. A missing or zero prior base has no valid growth rate.

4. For each product, retain `ratingCount` and `monthlyRatingCount`. The latter is the current rating count minus its count 30 days earlier, in ratings. Preserve negative values, zero and null.

## Deliverable

Matching products and the coverage of the list.
