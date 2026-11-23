# Keyword analysis methods

## keywords/extends: Related-term expansion

1. Pass the seed as `query` with its marketplace. Use `queryType=fuzzy` for ordinary related-term expansion and `queryType=phrase` for a user-specified phrase match.
2. Select a supported order from the following mappings. Without a user-specified order, ordinary related-term expansion uses relevance descending. Apply the sort inputs under the [MCP sorting rule](../../../contract/query.md#apply-sorting-and-pagination).

| Retrieval purpose | Sort |
|---|---|
| Seed relevance | `relevanceScore desc` |
| Higher estimated search demand | `estimateSearchCount desc` |
| Better search-frequency rank | `abaRank asc` |
| Alphabetical order | `keyword asc` |

3. For each returned row, read the candidate from `matchData.keyword`, site from `matchData.site` and relevance from `matchData.relevanceScore`. Read estimated search count from `keywordSnapshot.estimateSearchCount`, ABA rank from `keywordSnapshot.abaRank` and the resolved period from `keywordSnapshot.dataWindow.currentPeriod`. These candidate snapshots supply the expansion report's baseline measures without a separate `keywords/detail` query for the same measures and period.
4. Retrieve further pages when needed for the requested candidate count or coverage. Deduplicate by candidate keyword, marketplace and measurement period.
5. Group candidates by the category, attributes, uses or settings expressed in the query. Name each group by its shared condition, separate neighboring product categories, and retain the selected order within groups.

## keywords/detail: Keyword details

1. For a named keyword's baseline-statistics request, query the keyword or query set with its marketplace and snapshot date.
2. Read the requested baseline metrics from each item's `snapshotData`: search count and ABA rank, Top-3 click/conversion shares, product and brand counts, title coverage, organic/advertising counts or Top-48 product benchmarks. Retain the keyword identity and the resolved measurement period from the response context.

## keywords/market-profile: Keyword profiles

1. Query the named keyword or query set with the marketplace and snapshot date. Read each keyword's `marketProfile`.
2. For each requested graded dimension, read `level`, `interpretation` and the numeric support in `levelEvidence`. Search volume and ABA rank are already included under `demandScale.levelEvidence`.
3. Read advertising coverage from `adCoverage`. Read annual-seasonality classification and any returned historical peaks from `annualSeasonality`.

## keywords/trend-profile: Trend profiles

1. Query the named keyword or query set with its marketplace, as-of date and requested supported `windowPeriods`.
2. For each returned window, read search-demand and ABA-rank directions from `trend`, and changes from `trendEvidence`.
3. Read demand volatility from `volatilityLevel` and the latest observation's position within the window from `lastPeriodWindowPosition`. Keep each result with its returned window.

## keywords/trend: Weekly trend data

1. For a weekly-history request or a chart of weekly observations, query the named keyword or query set with its marketplace and supported date range.
2. Read each item's `series`, retaining each week's boundaries, estimated search count, ABA rank and any requested Top-3 click/conversion shares.
