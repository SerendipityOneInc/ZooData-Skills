# Product metric meanings

## Product identity and commerce measures

| Metric | Meaning |
|---|---|
| ASIN / parent ASIN | The product/variant identifier and the identifier grouping its variants. |
| `monthlySalesFloor` | The monthly purchase lower-bound tier carried from the page's “N+ bought in past month” observation into the selected catalog snapshot. |
| `monthlyRevenueFloor` | The independently returned monthly revenue lower bound. |
| Price | The price from the specified catalog snapshot or realtime offer, with its source and currency. |
| Star rating / rating count | The star score and accumulated number of ratings. |
| BSR / subcategory BSR | The product's position in the named ranking category; lower values are ahead. |
| Listing date / variant count | The recorded listing date and number of variants for the returned product scope. |
| New Release badge | A retained historical label that does not expire. It records a past New Release designation, not the product's current newness; listing date determines its listing age. |

## History and page content

| Metric | Meaning |
|---|---|
| History observation | Historical page measures aligned to returned timestamps; a point can carry an earlier observation forward. |
| Historical purchase tier | The page's monthly purchase lower-bound text recorded in the historical observations. |
| Monthly catalog sales/revenue point | The ASIN's and parent's purchase/revenue lower bounds from a catalog month-end snapshot, or the separately labeled current-month snapshot. This shares the catalog basis, not the page-observation history basis. |
| Completed / current month | `monthEnd` is a completed-month point; `monthToDate` is an updating current-month point. Returned completed-month growth rates do not apply to the latter. |
| Monthly catalog availability | `inCatalog=false` means no catalog product record that month; `inCatalog=true` with a null measure means the product exists but that measure is unavailable. Neither state is a measured zero. |
| Change record | A dated title, image or status value recorded when that field changes. |
| Returned product text | Product information explicitly stated in the acquired title, bullets, description or specifications. |
| Listing bullet descriptions (五点描述) | The product's selling-point descriptions. Standalone specification values mixed into returned feature text are attributes, not additional selling-point descriptions. |
| Phrase occurrence in page text | Whether a specified complete phrase appears in an acquired page section. This describes that section's wording; ASIN-query exposure and placement observations describe search visibility. |
| Image URL / inspected image | An asset reference and the visual content actually inspected, respectively. |
| A+ status | The returned flag describing recorded A+ availability; the body is separately acquired content. |

## Sample price bands and brands

| Metric | Meaning |
|---|---|
| Sample population | The product sample selected by the requested keyword and the endpoint's sampling rule. |
| Band bounds / `sampleMedianPrice` | A price bucket's lower/upper values and the median price across the returned sample. |
| `sampleSalesRate` | The band or brand's sales share within its returned sample. |
| `sampleTop3BrandSalesRate` / `sampleTop10BrandSalesRate` | The specified leading brands' sales share in the named band or whole sample, respectively. |
| `sampleOpportunityIndex` | The returned composite index for comparing price bands under its model. |
| `sampleProducts` | The example product records returned for a brand. |
