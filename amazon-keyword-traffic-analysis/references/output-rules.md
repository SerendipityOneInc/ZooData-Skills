# Output Rules — Amazon Keyword Intelligence

This file owns keyword-specific language, report rendering, Data Notes, and API-usage presentation within the shared `analysis-constitution.md`. It does not redefine the constitutional user-facing boundary or define stage selection, conclusion authority, Gate outcomes, or the contents of the stage-end selection list.

## Contents

- [User-Facing Language Rule](#user-facing-language-rule)
- [Internal Identifier Rewrite](#internal-identifier-rewrite)
- [Interface Failure Output](#interface-failure-output)
- [Quick Mode Output](#quick-mode-output)
- [Full-Mode Stage Output](#full-mode-stage-output)
- [Data Notes Rule](#data-notes-rule)
- [Usage Accounting Rule](#usage-accounting-rule)

## User-Facing Language Rule

Localize headings, labels, human-readable statuses, table headers, disclaimers, and fixed phrases to the user's language. Preserve source spelling for exact endpoint paths, fields, enums, ASINs, queries, brands, product names, placement codes, and established abbreviations. Retain an enum such as `status=empty` exactly and add a localized explanation when needed. Remove template-language leakage before sending.

## Internal Identifier Rewrite

A user-facing rendering is invalid when any title, heading, note, table, parenthetical, evidence qualifier, conclusion, usage text, or final selection item exposes an internal workflow identifier.

- Treat `Stage` followed by a stage-table identifier as internal, including numeric, letter-suffixed, or ranged forms such as `Stage 1`, `Stage 1A`, `Stage 1B`, and `Stage 1B–2`. Apply the same rule to localized forms such as the Chinese `Stage` translation (`U+9636 U+6BB5`) followed by `1B`, and to wording that embeds the identifier inside a longer evidence label.
- Treat Gate names, scenario/module names, reference filenames, stage-entry language, and active-stage narration as internal control terminology. Exact endpoint identifiers, documented fields, enums such as `status=empty`, and user-supplied business subjects remain permitted.
- Rewrite the complete semantic phrase in user-domain language; never merely delete the identifier and leave an unexplained fragment. For example, rewrite `Stage 1B direct ASIN evidence` as `ASIN traffic-term observations`, and rewrite `Stage 2 product-fit evidence` as `candidate keyword market and product-fit evidence`.
- Omit internal control narration that has no user-domain meaning. Never explain that a Gate, scenario, module, or stage caused the rendered conclusion.

## Interface Failure Output

For any hard interface-failure stop selected by `execution-guide.md`, render exactly three non-empty plain-text lines with no blank lines, using only this localized template:

`Service is currently unavailable. Please try again later.`
`Succeeded interfaces: {comma-separated endpoint identifiers, or None}`
`Failed interfaces: {comma-separated endpoint identifiers}`

- Preserve endpoint identifiers exactly as documented.
- Populate the ledger only from calls completed in the current turn.
- The first emitted character must belong to the localized first line, and the last emitted character must belong to the failed-interface identifier on the third line. Add no content before or after the template.
- Emit the three lines as plain text. Do not add Markdown headings, emphasis, code formatting, block quotes, bullets, or separators.
- Do not add a heading, HTTP status, retry count, cause label, parameters, workflow rationale, successful-interface data, partial analysis, API-usage section, parameter warning, next-step section, suggestion to ask another question, action guidance, or stage-end list.
- Provide technical diagnostics only when explicitly requested.

## Quick Mode Output

For one exact lookup:

- Answer the requested metric directly with field name and value.
- Tag direct API values with 📊 and derived values with 🔍.
- State the returned source identifier and snapshot date inline.
- Keep interpretation light and within returned evidence.
- Include the localized API-usage table below.
- Omit scenario-stage framing.
- Do not render a stage-end selection list because Quick Mode did not complete a scenario stage.

## Full-Mode Stage Output

Render every normally completed full-mode scenario stage with exactly this canonical top-level template:

1. one localized report title naming the subject and business question;
2. `Data Notes`;
3. `Evidence`;
4. `Analysis`;
5. `Conclusion`;
6. `API Usage` when live API data was used; and
7. the non-report coded Stage-End Selection List from `execution-guide.md`.

Localize all five semantic section labels consistently into the user's language. Apply the constitutional user-facing boundary to the entire response, including titles, headings, body text, usage reporting, and the selection list. Put the active semantic scope in the report title and Data Notes instead of exposing its internal workflow identity.

Do not expose internal workflow identifiers, labels, ordinals, or progression claims. Name current scope and any continuation by their user-domain subject and action. Do not render a candidate menu, action menu, selection key, or selectable-subject list inside Evidence, Analysis, or Conclusion; place every user-selectable subject and action only in the final numbered selection list defined by `execution-guide.md`.

Do not rename `Evidence` to a scenario-specific heading such as observed change, traffic evidence, or market evidence. Put that material inside `Evidence`. Likewise, put explanation status inside `Analysis` and discovery, posture, or calibration results inside `Conclusion`. Scenario files may require tables, subsections, or content within these sections but cannot change the canonical skeleton.

Keep direct observations out of Conclusion and recommendations out of Evidence. Render only the evidence, analysis, and conclusion supplied for the active stage; do not repeat a prior report in full, expose methodology sections, or preview later-stage material.

A hard interface failure follows `Interface Failure Output` above. Credential and credit failures follow the guide-owned stop decision and the smallest applicable rendering under the constitutional user-facing boundary. Each failure route bypasses normal stage rendering and the stage-end list.

## Data Notes Rule

- Place one short localized Data Notes section immediately after the title/source line.
- Name evidence source, returned period, and current semantic scope neutrally.
- At first use, every ranked, aggregate, comparative, entry/exit, growth, or decline explanation must name its subject, metric, returned period or comparison periods, population/Top-N or returned-row coverage, and material filters/channels. When the source does not return one comparison boundary, label that boundary unavailable instead of deriving it; do not present the result as an exact-dated comparison. A ranking must also name its sort direction. Do not render unqualified labels such as `top keywords`, `traffic share`, `new/lost keywords`, or `growth/decline` when their evidence scope is not already explicit and unambiguous.
- At market level call it a market screen; at subject level name the ASIN/keyword scope; at seller level name the supplied SQP/Ads fields used.
- Do not duplicate Data Notes, put evidence requests inside findings, list future missing inputs, or use deficit-framed form blocks.
- Data Notes is context, not a replacement for Evidence or Analysis.
- Do not present ZooData exposure/search/visibility estimates as seller ABA-SQP conversion evidence.

## Usage Accounting Rule

- Every completed full-mode stage or Quick response using live API data must include a localized API Usage section.
- Do not append API Usage to the hard interface-failure ledger notice.
- Count every executed API call, including duplicate/diagnostic/discarded calls and calls followed by local parse failure.
- Aggregate by endpoint and sum returned `meta.creditsConsumed`; never infer absent credits.
- Use a markdown table:
  `| [Localized endpoint header] | [Localized calls header] | [Localized credits header] |`
  `|---|---:|---:|`
  `| [endpoint] | 1 | 1 |`
  `| [Localized total label] | 1 | 1 |`
- Render a localized `not returned` when credit fields are absent, or `partial N + not returned` when only some are known.
- End the report section with the localized credits-remaining label using the latest returned value.
- Do not add a separate Data Provenance table unless requested.
- API Usage is the final report section; the required stage-end selection list follows it as non-report interaction UI.
