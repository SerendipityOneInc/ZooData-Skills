# Product-traffic analysis

1. Analyze ASIN exposure and its traffic keywords through organic and sponsored sources, trends, weekly changes, keyword exposure and search-position comparisons. Analyze seller-provided search and advertising reports for actual performance.

## Identify required inputs

1. Use ASINs, marketplace and the requested snapshot/window or date range. Named-term analysis also needs the specified query set.
2. For supporting data needed by the current traffic comparison, use the methods for [query snapshots](methods.md#keywordsdetail-query-snapshot-context), [query profiles](methods.md#keywordsmarket-profile-query-profile-context), [query trend profiles](methods.md#keywordstrend-profile-query-trend-context), [weekly query data](methods.md#keywordstrend-weekly-query-context) or [product observations](methods.md#realtimeproduct-product-observation-context).
3. Seller-performance tasks use user-provided reports, the identified product or report view, marketplace and period. Advertising reports also retain their attribution window. Apply [seller-report definitions](../../../contract/seller-evidence.md).

## Select an analysis task

| Check | Necessary input | Standard report content | Method |
|---|---|---|---|
| Traffic structure | ASIN or comparable ASIN set and snapshot date | Current/previous exposure and term coverage, channel changes and returned drivers | [Method](methods.md#keywordsproduct-traffic-structure-profile-traffic-structure-profile) |
| Traffic trend profile | ASIN set, as-of date and supported window | Returned total/organic/ad traffic and coverage trends with supporting metrics | [Method](methods.md#keywordsproduct-traffic-trend-profile-traffic-trend-profile) |
| Traffic weekly history | ASIN set and date range | Weekly exposure, term counts and returned distributions | [Method](methods.md#keywordsproduct-traffic-trend-weekly-traffic-data) |
| Traffic contributors | ASIN, snapshot and explicit list filters/order | Queries, exposure points/shares, positions, placement types and keyword baseline measures | [Method](methods.md#keywordsproduct-traffic-terms-traffic-contributors) |
| Named-term movement | ASIN, named queries and date range | Aligned ASIN exposure, search positions and query search volume or ABA rank; product/ad observations when needed | [Method](methods.md#keywordsproduct-traffic-terms-trend-named-term-weekly-data) |
| Search-placement comparison | Query, snapshot and target ASINs or comparison scope | Observed ASINs, placement types, absolute positions and estimated exposure within that scope | [Method](methods.md#keywordssearch-results-search-placement-records) |
| Seller search performance | User-provided search-performance report, identified product or report view, marketplace and period | Search-term impressions, clicks, cart adds, purchases, available shares/rates and requested period comparisons | [Method](methods.md#local-analysis-seller-search-performance) |
| Seller advertising performance | User-provided advertising report, identified product or report view, marketplace, period and attribution window | Search terms or targets, impressions, clicks, spend, attributed orders/sales and requested efficiency measures or comparisons | [Method](methods.md#local-analysis-seller-advertising-performance) |

## Preserve object features and report findings

1. Retain ASIN, marketplace and actual period. Term rows retain query text, placement type, position, exposure contribution and available search volume/ABA rank.
2. For structure and trend profiles, report the selected returned components and supporting values. For weekly data, report the requested observations and comparable changes.
3. When reporting changes for a specific ASIN-query pair, present three measures together for the same periods: the ASIN's exposure under that query, its search position and the query's search volume or ABA rank. Keep the placement type explicit. If any measure remains unavailable, identify the gap beside the comparison and limit findings to the obtained measures.
4. Retain source periods for supporting keyword and product measures. Use [keyword meanings](../keyword/semantics.md) and [product meanings](../product/semantics.md) for those fields.
5. For seller reports, retain original row identities, report view, product association and period. Report actual seller counts separately from public estimated exposure; leave unprovided measures unavailable.
