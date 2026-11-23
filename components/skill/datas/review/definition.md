# Consumer-feedback analysis

1. Analyze buyer reviews for a selected category or specified ASIN list, covering purchase reasons, use cases, praise, complaints, supporting product-review text, star-rating distribution and feedback differences.

## Identify required inputs

1. Use ASINs or a resolved category, marketplace, relevant period and the requested consumer question. Supplied review text retains its source, product identity and coverage.
2. Use [category lookup](methods.md#categories-category-lookup) when a category-based analysis needs its exact path.

## Select an analysis task

| Check | Necessary input | Standard report content | Method |
|---|---|---|---|
| Consumer-theme profile | ASIN set or category, marketplace and period | Buyer concerns, purchase reasons, use cases, opinions expressed in reviews, mention counts/rates and review scope | [Method](methods.md#reviewsanalysis-consumer-theme-profiles) |
| Theme evidence | ASIN or supplied review text and a named theme question | Acquired review text/IDs, supported theme labels and local statistics when requested | [Method](methods.md#local-analysis-theme-evidence) |
| Rating distribution | ASIN and marketplace | Returned rating count, star score and star distribution | [Method](methods.md#realtimeproduct-rating-distribution) |
| Feedback comparison | Identified review populations and comparison dimension | Same-theme counts/rates, supporting text and population differences | [Method](methods.md#local-analysis-feedback-comparison) |

## Preserve object features and report findings

1. Retain ASINs or category, eligible written-review count, period, source and relevant variant selection.
2. For a theme profile, report selected dimensions with mention counts/rates and associated ratings when returned. For text evidence, retain source IDs and distinguish excerpts from summaries.
3. Rating reports present the returned star distribution. Feedback comparisons preserve each population's own denominator and the requested common themes.
