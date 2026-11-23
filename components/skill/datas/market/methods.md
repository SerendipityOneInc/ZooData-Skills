# Market analysis methods

1. Profile, distribution and concentration reads share the selected category IDs, product-inclusion scope and sample selection. For a specified snapshot, use its published business date; to follow a discovery result, use that response's `resolvedDate`.
2. For numeric distributions, retain each returned bucket code, bounds and measures. If the source defines a different inclusion rule, preserve that returned grouping rather than moving its counts to a new interval. Without an established inclusion rule, report the returned group and measures without assigning interval brackets or deriving threshold totals.

## categories: Category lookup

1. Look up the supplied category name/path, or enumerate a named parent with `parentCategoryPath`. Read `categoryId`, `categoryName` and `categoryPath` from each returned row.
2. For a direct-child comparison, use the returned child IDs as the market scope. Ask the user to select a category when matches lead to different intended markets.

## markets/search: Market discovery

1. Apply the named category scope, inclusion rule, sample selection and explicit filters using the connected schema. An omitted date selects the latest publication; read `resolvedDate` from the response.
2. Use a supported sort from the table when the question specifies the corresponding order. Continue pagination for the requested coverage, retaining the category identity and flat market/sample fields in each row.

| Retrieval purpose | Sort |
|---|---|
| Higher market unit demand | `totalMonthlySales desc` |
| Higher market revenue | `totalMonthlyRevenue desc` |
| Higher average revenue per sampled product | `avgMonthlyRevenue desc` |
| Lower Top-3 product monthly-unit-sales share | `top3ProductMonthlySalesRate asc` |

## markets/profile: Market profile

1. Read whole-market measures from `marketSize` and sample measures from `sampleProfile`. Select the price, rating, new-product and concentration blocks needed by the question.

## markets/price-distributions: Price distribution

1. Read `priceDistribution` with its price bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/rating-distributions: Star-rating distribution

1. Read `ratingDistribution` with its star-rating bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/rating-count-distributions: Rating-count distribution

1. Read `ratingCountDistribution` with its rating-count bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/listing-age-distributions: Listing-age distribution

1. Read `listingAgeDistribution` with its listing-age bounds. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/fulfillment-distributions: Fulfillment distribution

1. Read `fulfillmentDistribution` with its fulfillment labels. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/seller-country-distributions: Seller-country distribution

1. Read `sellerCountryDistribution` with its seller-country labels. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/content-distributions: Content distribution

1. Read `contentDistribution` with its returned content-type labels. Retain bucket product counts/rates, sales/revenue totals and shares, and the sample totals returned with this distribution.

## markets/top-product-concentrations: Product concentration

1. Read `topnMetrics` and `topProductList`. Retain each Top-N identity, `concentrationRate`, the sample's ranking basis and each returned entity's sales/revenue measures.

## markets/brand-concentrations: Brand concentration

1. Read `topnMetrics` and `topBrandList`. Retain each Top-N identity, `concentrationRate`, the sample's ranking basis and each returned entity's sales/revenue measures.

## markets/seller-concentrations: Seller concentration

1. Read `topnMetrics` and `topSellerList`. Retain each Top-N identity, `concentrationRate`, the sample's ranking basis and each returned entity's sales/revenue measures.

## markets/listing-launch-trend: Launch composition

1. Pass category IDs, inclusion/sample rules and the requested first-launch date range and month/year granularity.
2. Read `points[].date` and `productCount` for the current leading sample. Preserve the first-launch grouping and the periods actually returned.

## markets/history: Market history

1. Pass category IDs, `dateFrom`, `dateTo` and consistent inclusion/sample rules. Read each returned series' category identity and `points`.
2. Align the returned month-end dates and compare the same measures from `marketSize` or `sampleProfile`. Calculate requested changes from those observations and retain sample selection at each point.
