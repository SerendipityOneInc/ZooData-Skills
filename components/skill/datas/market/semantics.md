# Market metric meanings

## Market and sample populations

| Metric | Meaning |
|---|---|
| Parent-product grain | Market products are parent products/SPUs, with variants merged. |
| Product inclusion | Whether products from descendant categories are included in each category market. |
| Sample selection | Up to 100 leading SPUs selected by the specified monthly-unit-sales or revenue rule. |
| `totalProductCount`, `totalMonthlySales`, `totalMonthlyRevenue` | Whole-category SPU count and trailing-month sales/revenue for the selected coverage. Product-catalog record totals describe a separate population. |
| `sampleProductCount`, `sampleMonthlySales`, `sampleMonthlyRevenue` | Product count and sales/revenue of the selected sample. |
| Sample means | Per-product means over valid observations for the corresponding metric; each mean can have its own valid population. |
| `resolvedDate` | The actual business date of the returned snapshot. |
| Money and rates | Market money is returned in USD and rates are fractions. Public floating metrics use the interface's documented rounding. |

## Distributions and concentration

| Metric | Meaning |
|---|---|
| Bucket product rate | The share of sample products assigned to the named bucket, with its returned membership rule. |
| Sales/revenue share | The bucket or entity's sales/revenue divided by the corresponding sample total. |
| Content and seller-country groups | Memberships can overlap when a product satisfies multiple returned group definitions. |
| Top-N concentration | The leading N entities' combined share on the sample's unit-sales or revenue ranking basis. |
| Seller country | The country recorded for sellers represented in the sample. |
| Rating and rating count | A star score and the number of ratings respectively. |

## Numeric distribution boundaries

Price and listing-age intervals use **inclusive lower and exclusive upper bounds**: `lowerBound <= value < upperBound`. Star-rating intervals use **exclusive lower and inclusive upper bounds**, including the maximum valid rating of 5. Rating-count segments contain consecutive integers with **both endpoints inclusive**: `lowerBound <= value <= upperBound`. An explicitly unbounded final segment contains `value >= lowerBound`. Equality buckets contain exactly the named value; a null boundary is not zero. The intervals below define the standard convention; an explicit current-interface definition identifies the actual returned grouping.

| Dimension | lowerBound | upperBound | Interval |
|---|---:|---:|---|
| Rating | 0 | 2 | (0, 2] |
| Rating | 2 | 3 | (2, 3] |
| Rating | 3 | 3.5 | (3, 3.5] |
| Rating | 3.5 | 4 | (3.5, 4] |
| Rating | 4 | 4.3 | (4, 4.3] |
| Rating | 4.3 | 4.5 | (4.3, 4.5] |
| Rating | 4.5 | 5 | (4.5, 5] |
| Rating count | 1 | 50 | [1, 50] |
| Rating count | 51 | 100 | [51, 100] |
| Rating count | 101 | 200 | [101, 200] |
| Rating count | 201 | 300 | [201, 300] |
| Rating count | 301 | 500 | [301, 500] |
| Rating count | 501 | null | [501, +∞) |
| Listing age (calendar months) | 0 | 1 | [0, 1) |
| Listing age (calendar months) | 1 | 3 | [1, 3) |
| Listing age (calendar months) | 3 | 6 | [3, 6) |
| Listing age (calendar months) | 6 | 12 | [6, 12) |
| Listing age (calendar months) | 12 | null | [12, +∞) |

| Boundary case | Meaning |
|---|---|
| Rating validity | Valid ratings are greater than 0 and at most 5. Zero, null and out-of-range values belong to the source's other/unknown group. The final rating interval (4.5, 5] includes the valid maximum 5; values above 5 remain invalid. |
| Integer rating counts | [1, 50] contains integers 1 through 50; the next segment starts at 51. A returned eq_0 bucket contains exactly zero, separately from the positive-count segments. |
| Price bounds | Each returned price band is lower-inclusive and upper-exclusive; the final band has no upper limit. A band code alone does not fix its numeric boundaries across markets or dates. |
| Calendar-month age | With D_n = DATE_SUB(resolvedDate, INTERVAL n MONTH) and first-launch date L, age [a, b) corresponds to D_b < L <= D_a. The final age interval contains L <= D_12. These are calendar-month boundaries, not fixed 30-day multiples. |
| Same-day and unknown launch dates | A same-day launch has age zero and belongs to [0, 1). A missing launch date does not establish age of at least 12 months; a future launch date does not establish a valid nonnegative age. |

## History and launch composition

| Metric | Meaning |
|---|---|
| History point | A published month-end snapshot with that month's full-market and selected-sample measures. |
| Historical sample | The leading sample selected separately at each month end; membership can change. |
| New-product window | Products in the specified first-listing-age window, with the returned full-market or sample population. |
| Launch-composition point | The number of products in the current sample first listed in the named month or year. Its date labels the first-launch period, not a sample snapshot date; this response provides no separate snapshot-date field. |
