# Consumer-feedback analysis methods

## categories: Category lookup

1. Resolve the intended category name/path and retain its exact returned path for category-based analysis.

## reviews/analysis: Consumer-theme profiles

1. Use the connected consumer-aggregation tool matching this read. Select ASIN or category mode and pass the corresponding identifiers, marketplace and supported period using its current schema.
2. Read the returned review count, rating/sentiment distributions and consumer-insight dimensions. Select the needed dimensions from that response.
3. Retain each theme's dimension, element, count, mention rate and associated rating. Sort themes locally by requested count or rate within the same population.

## reviews/search: Stored review text

1. Query the identified ASIN with the supported review-date, rating or other filters needed by the question. Use the tool's page/pageSize and supported sorting for the requested coverage; theme tags returned on records are not filter parameters.
2. Preserve the returned review IDs, text, stars, dates and product/variant information. This search uses the ASIN's parent-review population; identify a particular variant only from the returned review evidence.

## realtime/reviews: Current page reviews

1. Use this source when the question requires the latest reviews currently shown on the product page. Pass the identified ASIN and marketplace. Omit the first cursor, then use the returned `nextCursor` for additional requested coverage; null means no further page.
2. Keep this page sample's actual review dates and product scope. It does not replace a requested historical review period.

## Local analysis: Theme evidence

1. Use supplied or already acquired review text for the requested theme and coverage. When it covers the request, process it locally without requiring an ASIN or querying reviews.
2. When review text is still needed, use [stored reviews](#reviewssearch-stored-review-text) with the requested review period. Use [current page reviews](#realtimereviews-current-page-reviews) for an explicit latest-page request. Request a necessary ASIN or marketplace only when context and documented defaults cannot supply it.
3. Keep review IDs, text, stars, dates and variant information. Deduplicate by source ID; when no ID is supplied, use a local row key.
4. For requested text analysis, tag text-supported sentiment and themes, cluster equivalent expressions while preserving negation/context, and count each review once per theme.
5. Local mention rate = distinct readable reviews mentioning a theme / all distinct readable reviews. Use numeric stars from supporting reviews for a local theme mean; retain supporting IDs and label these local calculations.
6. If required text cannot be obtained, report findings supported by the available text and identify the missing coverage. If no readable text is available, report that the requested text-based finding cannot be established.

## realtime/product: Rating distribution

1. Read the target ASIN's returned rating count, star score and available star breakdown using the connected product tool's actual response paths.
2. Keep this product-wide rating population separate from the text-review population used for consumer themes.

## Local analysis: Feedback comparison

1. For each designated product or review population, reuse a compatible theme report. When only ASINs or categories are given, obtain a separate report for each comparison population through [consumer-theme profiles](#reviewsanalysis-consumer-theme-profiles). For supplied review text or an explicit text-based comparison, use [theme evidence](#local-analysis-theme-evidence) to produce the missing theme findings.
2. Compare the same theme dimension within the requested period and variant scope, retaining each source and denominator. Report observed count/rate differences with available supporting text. Use text that explicitly links consumer attributes and use contexts when reporting that relationship.
3. If a population's necessary theme data cannot be obtained or aligned, report its available findings separately and identify the comparison that remains unavailable. Do not replace missing themes with zero mentions.
