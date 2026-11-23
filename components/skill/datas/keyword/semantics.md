# Keyword metric meanings

## Search demand volume and relevance

| Metric | Meaning |
|---|---|
| Estimated search count | Estimated searches for the complete query during the returned measurement window. |
| ABA search-frequency rank | The query's search-frequency position relative to other queries for its marketplace and period; lower numbers rank ahead. Rank changes describe relative search frequency, not an absolute search-count change. |
| Expansion relevance | Returned seed-to-candidate relevance, used to order related keywords. |

## Keyword profiles

| Analysis dimension | Metric | Meaning |
|---|---|---|
| Search demand volume | Demand scale | Query search-demand volume, described by estimated search count and ABA rank. |
| Competition profile | Top-20 organic-entry difficulty | Relative difficulty of competing for the first 20 organic positions, expressed by the returned grade and interpretation. |
| Competition profile | Supply saturation | The returned combined supply assessment, supported by search-result product counts and title keyword coverage, with the observed-product count when available. The title-coverage rate is one reference measure, not the combined grade or a disclosed grading formula. |
| Competition profile | Search-result product count (`searchResultSkuCount`) | The largest source-reported search-result product count within the observation period. |
| Competition profile | Products observed (`observedSkuCount`) | Distinct products observed during the period, a different population from the source-reported search-result count. |
| Competition profile | Products whose titles contain the keyword (`titleKeywordDensity`) | The mean across valid days of distinct products whose titles contain the keyword divided by that day's eligible products, expressed as a proportion. It measures title coverage. |
| Competition profile | Leading organic products' ratings and sales | Average star ratings, review or rating counts according to the returned field definitions, and average sales (`top48OrganicAverageRecentSaleCount`) for the first 48 organic products. The sales lookback follows the source field's defined period; the observation week does not establish that lookback. These describe the products currently in those positions, not minimum requirements a new product must meet. |
| Search-structure profile | Top-3 concentration | ABA Top-3 product click and conversion shares, interpreted separately for each event type. These shares describe concentration, not a conversion rate. |
| Search-structure profile | Brand structure | How concentrated the observed competition is among brands, using the returned brand concentration and shares. |
| Search-structure profile | Advertising coverage | Distinct observed products appearing in advertising placements as a proportion of all observed products. |
| Demand seasonality | Annual seasonality | Historical annual demand patterns; returned historical peaks identify when peaks were observed. |

## Trend profiles and weekly statistics

| Metric | Meaning |
|---|---|
| Demand trend | The returned demand direction over the selected window. |
| ABA-rank trend | Improvement, stability or deterioration in search-frequency rank over the selected window. |
| Volatility | Demand fluctuations within that window. |
| Last-period window position | Whether the latest observation is near the high, middle or low part of the window's range. |
| Weekly observation | A search count, ABA rank or Top-3 share measured for one returned week, with its own start and end dates. |
| First-to-last change | Relative change between the window's first and last values. It describes those two observations; the returned trend classification also uses observations within the window. |
