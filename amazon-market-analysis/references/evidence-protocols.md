# Evidence Protocols — Amazon Market Analysis

This module owns shared evidence acquisition, identity matching, comparison, coverage, and reuse inside an active stage. The stage and conclusion ceiling come from `execution-guide.md` and the selected scenario; endpoint contracts come from `reference.md`.

## Plan the minimum evidence

1. Translate the current question into claim-sized needs and map each need to a documented endpoint and expected field.
2. Acquire the smallest response that resolves those needs. Use `market --category-id ID --page-size 1` for one current category; use bounded `market` pages for discovery; request a structure dimension only if its distribution matters; request history only for a time question.
3. After each result, apply the guide's Interface Failure Stop Gate before any next call. Separate retrieved facts from interpretations and recommendations.
4. Record source, request parameters, resolved category ID, returned date, sample type, category scope, pages/rows covered, and credit metadata in an evidence ledger.

Documentation is a contract, not an observed metric. Do not call a paid endpoint again merely to reformat a valid response.

## Market result projection

Apply the default result-isolation and cleanup procedure in `cli-contract.md` to every live market evidence command. Select projection fields from the claims planned for the active stage; the user does not need to choose fields or manage the temporary file. Always retain response success/failure identity, `_query.params`, credit metadata, coverage counts, category ID/name/path, marketplace, category scope, sample type, and returned date alongside every projected metric.

For a multi-category comparison, validate the requested ID set, returned row IDs, row count, and every ranking field against the complete raw payload before emitting the projection. Include the compatible `total*` demand measures and only the `sample*` concentration, new-product, price, rating, or content measures used by the current comparison. From `topNMetrics[]` and `newProductMetrics[]`, retain only the named `n` or `periodMonths` entries required by the question; retain the whole nested array only when the array itself is the requested evidence. Projection must preserve explicit `null` and absent-field distinctions.

The conversation-visible projection is not proof of raw-response completeness by itself. A collapsed `… +N lines` display is not truncation when the transcript or isolated result remains readable; inspect that complete result without another call. An actual token-truncation marker, omitted middle, fewer available category rows than the raw payload, or a missing required field cannot support a ranking. `success=true` and `meta.total=N` establish neither row visibility nor field availability. Re-project the already acquired raw result locally, without another paid call; if it is unavailable, suppress the affected comparison. Delete both raw and intermediate projection files through the shared cleanup path after the bounded projection has been consumed.

## Category and snapshot identity

- Resolve a human path through `categories` and preserve the returned `categoryId`. For a product keyword that has no direct category match, a product-search-derived path is only an inferred category; do not silently promote it to the user's intended market.
- For an exact market query, require one `markets/search.data[]` row whose `categoryId` equals the requested ID. For an ID batch, compare returned IDs with the requested set before claiming complete coverage. A zero-row result is no market observation. Do not substitute the first unrelated discovery row.
- Carry the search request's `category.includeDescendantCategoryProducts`, returned `categoryScope`, `sampleType`, marketplace, and the row's `date` with every market field. Directly assigned products and descendant-inclusive products, or unit-sales-selected and revenue-selected Top 100, are different populations.
- A composite's `market.data` is already a selected market object; a granular `market.data` is an array. Do not index either shape by assumption. Reuse compatible successful composite sections locally.

## Bounded discovery and candidate validation

- Declare page and credit limits before exploring a broad catalog. Rank only observed rows and disclose the filters, sort direction, page range, and `meta.total`; do not call the scanned pages the whole catalog.
- Keep candidate category identity separate from product identity. When a product candidate is requested, use a category-locked `products` call and deduplicate ASINs across modes or pages before ranking them.
- `--mode` is a CLI-local preset. Inspect the selected command's help and the returned `_query.params`; do not send the mode name to a raw API endpoint. User-supplied numeric thresholds take precedence over a preset when they conflict.
- A full composite may contain already paid market, product, price, brand, and review evidence. Reuse it when compatible; call a granular endpoint only for a named missing field, incompatible date/scope, or a new user question.

## Comparison and reconciliation

- Compare a market only with the same category ID, scope, sample type, marketplace, metric path, denominator, and compatible dates. Month-end history points and a latest daily snapshot can be shown side by side but do not form a precise same-grain period change by default.
- Use only returned available month-end points. Report `resolvedDateFrom` / `resolvedDateTo` when the requested bounds were not met; do not create missing months or extrapolate a rate. A returned MoM/YoY field is usable only for the metric and point that owns it.
- Distinguish absolute changes from percentage-point changes for rates. When calculating a derived change, state its numerator, denominator, and dates; if a baseline is zero or missing, do not calculate a growth percentage.
- Reconcile a material conflict before a verdict: for example, all-category sales may rise while Top 100 concentration also rises. Preserve both observations and narrow the conclusion. Do not average unlike fields or hide the conflict behind a single score.

## Coverage and no-data handling

- Report how many category rows, Top 100 products, distribution buckets, product candidates, reviews, and history points were actually observed when those counts materially limit a claim.
- For a category comparison, report rows validated from the complete isolated result, not rows that happened to remain visible in a tool transcript.
- `status=empty`, an empty `data[]`, empty buckets, and missing months are valid coverage boundaries. They do not prove zero demand, no competition, or a flat trend.
- Suppress a ranking or comparative verdict when the selected population, period, or required field is missing. State the exact gap and, only when the active stage allows it, acquire the documented missing evidence.
- Tag raw API facts separately from inference. A user-provided seller claim is an input, not an API-verified fact.
