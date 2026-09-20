# Output Rules — Amazon Market Analysis

This module owns market-specific language, confidence labels, report shape, provenance, and credit accounting. The shared `analysis-constitution.md` owns the universal user-facing boundary and progress discipline. The execution guide and scenario determine which conclusion is allowed; this module only renders it.

## Language and interface failure

Use the user's language for the entire report. Keep API field names, endpoint identifiers, ASINs, and standard units unchanged when translation would obscure identity. Do not show internal stage names, Gate labels, module names, tool retries, raw error payloads, or analysis-control instructions in the report.

On a terminal interface failure selected by `execution-guide.md`, return one concise localized notice that the market analysis could not be completed, followed by succeeded and failed endpoint identifiers from the current turn. Do not attach a market verdict, ranking, trend claim, API-usage table, or next-stage prompt. Give technical error details only if the user requests diagnostics.

## Quick lookup

Answer the requested metric or distribution directly. State its category, `direct`/`subtree` scope, selected Top 100 type when relevant, returned date or month-end period, source endpoint, and material limitation. Mark a direct API value 📊 and a calculated value 🔍. Include the API usage table below when a live call was made. Do not turn a one-field lookup into a multi-stage report.

## Full report shape

For one normally completed full stage, use this localized top-level order:

1. Title naming the category or observed candidate set and the current business question;
2. `Data Notes` — source, returned dates, scope, sample selector, pages/rows or history-point coverage;
3. `Evidence` — observed facts with units and source identity;
4. `Analysis` — compatible comparisons, uncertainty, and labeled inference;
5. `Conclusion` — only the active stage's authorized judgment;
6. `API Usage` — calls and credits; and
7. one final numbered selection list rendered from the guide's handoff decisions, after the report body.

Scenario files may require a table or a subsection *inside* these headings; they do not rename or reorder the skeleton. Apply the constitutional user-facing boundary to the whole rendering. A prose sentence in the conclusion does not replace the final selection list. Do not repeat a previous report or present an unvisited stage as completed. A user-supplied seller figure must be labeled as user-provided.

## Confidence and evidence labels

- 📊 Direct returned API observation, with endpoint, subject, and period.
- 🔍 Derived or interpretive claim whose source fields and assumptions are shown.
- 💡 Directional suggestion or validation priority; never mark it as a measured API fact.

A section, score, table header, or group label that contains mixed confidence must not wear a stronger label than its least certain component. Do not use the three symbols as decorative prefixes. Report a score only with its actual components and the scenario's stated method; do not use a numeric score to conceal missing dimensions. Explain when a valid empty response narrows the conclusion.

## Provenance and usage

Within `Data Notes` or `Evidence`, identify the relevant endpoint and actual returned `_query.params` when available. For `markets/search`, distinguish a broad discovery page, a batch of `category.ids`, and an exact one-ID snapshot. State the page range, filter/sort, requested `category.includeDescendantCategoryProducts`, `sampleType`, and returned date that materially constrain the claim. For history, state requested and actual period bounds when different.

Use a localized API-usage table when live calls were made:

| Endpoint | Calls | Credits consumed |
|---|---:|---:|
| Actual endpoint identifier | N | Returned amount or unavailable |
| **Total** | **N** | **Sum of returned amounts, or unavailable** |

Count every executed call, including a call whose data was discarded. Use `meta.creditsConsumed` or composite accumulated metadata; do not add the composite total to its internal calls again. If a returned credit figure is absent, say it is unavailable rather than estimating it. Report remaining credits only when returned.
