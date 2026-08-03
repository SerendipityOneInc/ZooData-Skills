# Output Rules — Amazon Keyword Intelligence

This file owns user-facing language, progress updates, report rendering, Data Notes, and API-usage presentation. It does not define stage selection, conclusion authority, Gate outcomes, or the contents of the stage-end selection list.

## Contents

- [User-Facing Language Rule](#user-facing-language-rule)
- [User-Facing Output Boundary](#user-facing-output-boundary)
- [Internal Identifier Rewrite](#internal-identifier-rewrite)
- [CLI Error Isolation](#cli-error-isolation)
- [Interface Failure Output](#interface-failure-output)
- [Retrieval Progress Updates](#retrieval-progress-updates)
- [Quick Mode Output](#quick-mode-output)
- [Full-Mode Stage Output](#full-mode-stage-output)
- [Data Notes Rule](#data-notes-rule)
- [Usage Accounting Rule](#usage-accounting-rule)

## User-Facing Language Rule

Localize headings, labels, human-readable statuses, table headers, disclaimers, and fixed phrases to the user's language. Preserve source spelling for exact endpoint paths, fields, enums, ASINs, queries, brands, product names, placement codes, and established abbreviations. Retain an enum such as `status=empty` exactly and add a localized explanation when needed. Remove template-language leakage before sending.

## User-Facing Output Boundary

Keep execution control separate from user communication.

- Include only evidence, analysis, conclusion, limitation, usage, and the stage-end choices needed by the user.
- Do not expose rule names, ownership, Gate decisions, internal checklists, retries, parameter-mutation policy, commands, or maintainer rationale.
- Do not expose internal workflow identifiers, labels, ordinals, or progression claims anywhere in user-facing text. Name current scope and any continuation by their user-domain subject and action, using neutral next-step wording when a transition must be described.
- A user-visible action statement may say only what is being done for the user's question. It must not say which internal condition fired, which instruction selected the action, or how the action complies with policy.
- Rewrite every internal `observation → control decision → action` narrative as a direct user-domain action statement before sending. If the rewritten sentence has no user value, omit it.
- Do not render a candidate menu, action menu, selection key, or selectable-subject list inside Evidence, Analysis, or Conclusion. Discuss evidence and named subjects naturally there, then place every user-selectable subject and action only in the single final numbered selection list defined by `execution-guide.md`.
- Surface technical diagnostics only when the user asks or when one exact identifier is necessary to correct user-controlled input.
- Scenario section-content requirements may narrow what appears inside a canonical section but cannot rename, add, remove, or reorder top-level report sections, expose internal execution state, or weaken this boundary.

## Internal Identifier Rewrite

A user-facing rendering is invalid when any title, heading, note, table, parenthetical, evidence qualifier, conclusion, usage text, or final selection item exposes an internal workflow identifier.

- Treat `Stage` followed by a stage-table identifier as internal, including numeric, letter-suffixed, or ranged forms such as `Stage 1`, `Stage 1A`, `Stage 1B`, and `Stage 1B–2`. Apply the same rule to localized forms such as the Chinese `Stage` translation (`U+9636 U+6BB5`) followed by `1B`, and to wording that embeds the identifier inside a longer evidence label.
- Treat Gate names, scenario/module names, reference filenames, stage-entry language, and active-stage narration as internal control terminology. Exact endpoint identifiers, documented fields, enums such as `status=empty`, and user-supplied business subjects remain permitted.
- Rewrite the complete semantic phrase in user-domain language; never merely delete the identifier and leave an unexplained fragment. For example, rewrite `Stage 1B direct ASIN evidence` as `ASIN traffic-term observations`, and rewrite `Stage 2 product-fit evidence` as `candidate keyword market and product-fit evidence`.
- Omit internal control narration that has no user-domain meaning. Never explain that a Gate, scenario, module, or stage caused the rendered conclusion.

### CLI Error Isolation

- Treat CLI/tool error payloads as Agent-only diagnostics. Do not quote or paraphrase internal `message`, `action`, server detail, parameters, retry logs, or control tokens by default.
- Use structured error facts only to select the applicable guide-owned Gate and output template. The CLI never owns final prose.
- When no specific template exists, state the smallest localized outcome and user action.
- Disclose only requested diagnostic detail.

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

## Retrieval Progress Updates

- Complete internal preparation silently. Never announce the loading, selection, or application of internal instructions or resources.
- When user input is required before work can continue, request it directly without a progress preamble.
- When an update is useful, use one short natural sentence naming only the subject and user-domain question.
- Do not expose execution mechanics, internal state, control vocabulary, or planned downstream routing.
- Keep intermediate control flow silent. Do not narrate how an observation, tool result, contract, rule, or internal classification caused the next method, parameter, source, scope, or action to be selected or changed.
- An intermediate result may appear user-facing only when it is requested evidence, materially affects the completed answer, or requires user action. Never use it as process justification for the next internal action.
- When work continues, either omit the update or state only the direct user-domain action. Do not explain why that action was internally selected.
- Do not expose partial judgments or narrate every retrieval call.

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

Localize all five semantic section labels consistently into the user's language. Apply the User-Facing Output Boundary to the entire response, including titles, headings, body text, usage reporting, and the selection list. Put the active semantic scope in the report title and Data Notes instead of exposing its internal workflow identity.

Do not rename `Evidence` to a scenario-specific heading such as observed change, traffic evidence, or market evidence. Put that material inside `Evidence`. Likewise, put explanation status inside `Analysis` and discovery, posture, or calibration results inside `Conclusion`. Scenario files may require tables, subsections, or content within these sections but cannot change the canonical skeleton.

Keep direct observations out of Conclusion and recommendations out of Evidence. Render only the evidence, analysis, and conclusion supplied for the active stage; do not repeat a prior report in full, expose methodology sections, or preview later-stage material.

A hard interface failure follows `Interface Failure Output` above. Credential and credit failures follow the guide-owned stop decision and the smallest applicable rendering under the User-Facing Output Boundary. Each failure route bypasses normal stage rendering and the stage-end list.

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
