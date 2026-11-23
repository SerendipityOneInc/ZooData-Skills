# Keyword analysis

1. Analyze a search query or defined query set through related-keyword expansion, keyword groups, baseline statistics, keyword profiles, trend profiles and weekly history.

## Identify required inputs

1. Use a seed or named query set, marketplace, and the requested period and filtering conditions.

## Select an analysis task

| Check | Necessary input | Standard report content | Method |
|---|---|---|---|
| Keyword expansion | Seed and marketplace, with any explicit recall constraint | Related keywords, keyword groups, relevance and baseline measures from the returned candidate snapshots | [Method](methods.md#keywordsextends-related-term-expansion) |
| Keyword statistics | Named keyword or defined query set, marketplace and snapshot date | Requested snapshot statistics on search demand, Top-3 shares, product supply, organic/advertising counts and leading-product benchmarks, with the resolved measurement period | [Method](methods.md#keywordsdetail-keyword-details) |
| Keyword profile | Named keyword or defined query set, marketplace and snapshot period | Search demand volume, organic-entry difficulty, supply saturation, leading-product benchmarks, click/conversion concentration, brand structure, advertising coverage and annual seasonality | [Method](methods.md#keywordsmarket-profile-keyword-profiles) |
| Keyword trend profile | Named query set, marketplace, as-of date and supported windows | Search-demand and ABA-rank trend classifications, supporting changes, demand volatility and latest-period window position | [Method](methods.md#keywordstrend-profile-trend-profiles) |
| Keyword weekly history | Named query set, marketplace and date range | Weekly search count, ABA rank and requested Top-3 click/conversion shares, with actual period boundaries | [Method](methods.md#keywordstrend-weekly-trend-data) |

## Preserve object features and report findings

1. Retain each original query, marketplace and the available estimated search count, measurement window and ABA search-frequency rank.
2. For expansion, deliver the keyword list, estimated search count, ABA rank, relevance and keyword groups.
3. For baseline statistics, report the requested values for each keyword and their resolved snapshot period.
4. For a keyword profile, report the question's demand, competition and search-structure dimensions with supporting indicators and annual seasonality where relevant.
5. For a trend profile, report the selected windows, returned directions, supporting changes, volatility and latest-period window position where returned.
6. For weekly history, report the requested series and observed changes with the returned period boundaries and coverage.
