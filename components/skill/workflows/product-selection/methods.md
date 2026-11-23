# Assess identified candidates

## Confirm candidates for a seller-requested assessment

1. When working only from supplied figures, keep each candidate under its supplied name or identifier. Request an ASIN only for a catalog lookup or unresolved identity. Assess one candidate by default and compare at most three explicitly selected candidates. If the intended product is unclear or more than three are selected, ask which to assess before any candidate reads. Before looking up candidates, run the [scope check](assessment_scope.py) with the selected ASINs. Use `--compare` only for an explicit comparison. Assess the returned list only on `ready`. This limit applies to assessment, not screening.
2. For a general assessment, trace the product’s development across the measures below. For a focused question, such as whether a sales increase persisted, use just the relevant measures in the same assessment. Reuse available observations and respect the agreed budget.
3. Use the requested period. For a general growth assessment with no dates, use the last six complete months as the common horizon: monthly purchases, dated product history for those months, and complete traffic weeks inside that period. For a newer product start at the first available observation. Label shorter coverage and compare signals only over the overlap.

## Trace how each product grew

| Measure | Evidence and judgment |
|---|---|
| Purchase volume | Use [monthly purchases](../../datas/product-sales-trend/definition.md) to compare the selected ASIN’s monthly purchase lower bounds. Identify its starting level, when it moved up or down, and how many subsequent observed months held that level. Compare the same months for the parent listing to see whether the variant and the family moved together. |
| Price | Use [product history](../../datas/product-history/definition.md) for dated prices and [product details](../../datas/product-detail/definition.md) for pack size and current facts. Identify sustained price levels, temporary reductions and recoveries. Compare equivalent packs or unit prices across candidates. |
| Organic exposure | Read the [traffic trend profile](../../datas/traffic-trend/definition.md) for the direction and variability of organic exposure. Use the [traffic structure profile](../../datas/traffic-structure/definition.md) for the level and share at the comparison date. A rising share with falling exposure points means a larger share of a shrinking total. |
| Ad exposure | From those same profiles, assess the trend in estimated sponsored exposure and its share of total exposure. Use the returned ad total or comparable non-overlapping sponsored channels. Keep a movement in advertising visibility distinct from spend, clicks and ad-attributed sales. |
| Best Sellers Rank (BSR) | Reuse product history. Track rank in the same category node; smaller numbers mean a better position. Separate main and subcategory series and split at a category change. Compare the timing of rank gains with purchase changes. |
| Ratings | From the same history, compare cumulative rating counts over observed intervals and report the change in stars when available. Growth in rating count describes feedback accumulation. Preserve decreases, missing dates and changes in parent scope. |
| Written buyer feedback | Use the [review profile](../../datas/product-review-profile/definition.md) once per confirmed parent and period to identify recurring praise or complaints shared by its variants. For a change over time, use compatible dated [review samples](../../datas/review-search/definition.md) for separate non-overlapping periods, with the same coverage and a denominator for each. A single pooled profile supports themes only. |

1. For both category rank panels request `bsr`, `bsrCategory`, `subBsr` and `subBsrCategory` together with daily price in the same product-history read per ASIN. Include ratings when needed. Request traffic profiles for selected ASINs together when supported. The trend profile covers four weeks. For a longer growth history, a turning point or a chart, use the [weekly exposure series](../../datas/traffic-weeks/definition.md) where the profile lacks coverage. Reuse its organic and ad measures and skip a redundant profile.
2. Organize the history around observed changes: the starting position, the first meaningful shift and what persisted or reversed afterwards. Relate purchases to concurrent changes in price, exposure, BSR and ratings. State which signals moved together or diverged. Report only the current state for a single observation and keep an unavailable metric unknown.
3. Compare candidates over like periods and stages with the same market, units and product scope. Evaluate the seller’s explicit conditions with the relevant observations. A coincident price or exposure change cannot establish what drove sales. For ad efficiency use the seller’s advertising records.

## Add evidence for a specific selection question

1. For a missing comparable product, use [Competitor discovery](../../datas/product-competitors/definition.md) and compare its actual use and specifications. For a keyword-defined product sample, reuse the screened rows to summarize observed price bands or brand shares. Label the population, denominator and retained coverage. Compute sales shares only with comparable purchase measures and label lower-bound-based shares accordingly.
2. If category context affects candidate fit, select the relevant comparison from [market research](market-research.md). Keep market observations separate from the candidate sample.
3. To identify which terms generate exposure for a candidate, use [ASIN exposure terms](../../datas/traffic-terms/definition.md).
4. For a seller-specified threshold, report the figure, threshold and difference using the supplied costs, fees or operating limits. Identify any missing input needed for that comparison.
