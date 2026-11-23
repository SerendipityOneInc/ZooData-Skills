# Product-traffic analysis methods

## keywords/product-traffic-structure-profile: Traffic structure profile

1. Pass the ASIN set, marketplace and snapshot date. Read each identity and `productTrafficTermsProfile` with its current/previous periods.
2. Read `summary`, `trafficStructureChange`, `organicStructureChange` and `termChangeDrivers` as returned. Retain channel keys and the actual fields of any supplied driver records.

## keywords/product-traffic-trend-profile: Traffic trend profile

1. Pass ASINs, marketplace, date and the supported window. Select the supported detail level required by the question.
2. Read each window row's status, then the available components in `trafficTrendProfile`. For each component, read `trend`, `trendEvidence`, `volatilityLevel` and `lastPeriodWindowPosition` when returned.

## keywords/product-traffic-trend: Weekly traffic data

1. Pass ASINs, marketplace and the supported `dateFrom`/`dateTo` range. Read each item's status and `series`.
2. Retain weekly boundaries, total/organic/ad exposure points, term counts and the returned placement and demand-rank distributions. Compare like measures across the requested weeks.

## keywords/product-traffic-terms: Traffic contributors

1. Pass the ASIN, marketplace, snapshot and explicit placement/keyword filters. Use a supported sort from the table for the requested order.
2. Read query, `trafficShare`, `estimateImpressionPoint`, position, placement type, query search count/ABA rank and observation coverage from each row. Page for the requested coverage.

| Retrieval purpose | Sort |
|---|---|
| Higher exposure contribution | `trafficShare desc` or `estimateImpressionPoint desc` |
| Better observed position within one placement type | `avgPosition asc` or `absolutePosition asc` |
| Higher query demand | `keywordEstimateSearchCount desc` |

## keywords/product-traffic-terms-trend: Named-term weekly data

1. Pass one ASIN, the named query set, marketplace and supported date range. Read each query's weekly `series`.
2. Read `totalEstimateImpressionPoint`, `trafficByExploreType`, `keywordEstimateSearchCount` and `keywordAbaRank` for each returned period. Within each placement type, compare its own exposure and positions; keep `absolutePosition` and `avgPosition` as separate measures. Read `asinSnapshot` and that placement type's `adActivity` only when needed by the question.
3. Align exposure, position and query search volume or ABA rank by the returned period boundaries. Reuse an available query series; one of search volume or ABA rank is sufficient. If neither supplies the comparison's query context, obtain the missing periods through [weekly query context](#keywordstrend-weekly-query-context) within the query limits.

## keywords/search-results: Search-placement records

1. Pass the query, marketplace, snapshot and requested placement types. For position order use supported `absolutePosition asc`; for exposure order use supported `estimateImpressionPoint desc`.
2. Retain ASIN, readable product identity, `exploreType`, `absolutePosition` and `estimateImpressionPoint`. Compare the selected ASINs under the same query, period and placement type, with the acquired record scope.
3. Read `keywordTotalEstimateImpressionPoint` once per query-period. For a requested within-sample exposure share, sum the selected group's row-level exposure points and divide by the same sample's total row-level points.

## keywords/detail: Query snapshot context

1. When the requested traffic comparison includes query-level snapshot measures absent from the traffic response, read the named queries' `snapshotData` for the matching marketplace and date. Keep these measures with their keyword identity and period.

## keywords/market-profile: Query profile context

1. For a requested comparison with keyword demand or competition, read the named queries' `marketProfile` and the required dimensions' `level`, `interpretation` and `levelEvidence`, retaining the query snapshot.

## keywords/trend-profile: Query trend context

1. For a requested comparison of ASIN exposure and query-demand direction, read the named queries' requested trend windows and returned `trend`/`trendEvidence`. Retain both the traffic and keyword windows.

## keywords/trend: Weekly query context

1. For weekly query context not already available, read the named queries' `series` with the matching marketplace and supported date range. Extract search volume or ABA rank and align the returned period boundaries with the ASIN-query exposure and position data.

## realtime/product: Product observation context

1. When the requested traffic comparison needs a missing current product fact, read the target ASIN's actual returned attribute or offer field. Keep this current observation's date separate from historical traffic windows.

## Local analysis: Seller search performance

1. Process the user-provided search-performance file locally to identify its marketplace, period, brand/ASIN view and row dimensions. Map the source columns to the reported search terms and available impressions, clicks, cart adds, purchases and shares for that view.
2. Calculate requested rates and differences under [seller-report definitions](../../../contract/seller-evidence.md), using compatible counts and denominators. Compare periods only when the corresponding reports have been supplied.
3. Report the requested term-level measures, changes and explicit condition matches with the supporting row identities. Use only the seller report for actual performance, keeping unprovided fields unavailable instead of filling them from public estimates.

## Local analysis: Seller advertising performance

1. Process the user-provided advertising file locally to identify its marketplace, period, attribution window, product association and row dimensions. Preserve whether a row describes a shopper search term or an advertiser target.
2. Extract available impressions, clicks, spend, attributed orders and attributed sales. Calculate requested CPC, CVR, ACOS or ROAS using [seller-report definitions](../../../contract/seller-evidence.md); retain unavailable results where inputs do not support the calculation.
3. Report requested row-level or grouped measures and comparable changes. Keep campaign/ad-group identities and product associations so a report-wide result is not assigned to an ASIN that the report does not identify.
