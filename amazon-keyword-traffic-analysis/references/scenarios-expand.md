# Keyword Expansion Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects capabilities for expansion and must align upward with `execution-guide.md`, `reference.md`, and the field-semantic references; it cannot relax their evidence, conclusion, action, credit, or output requirements.

## Route selection

| Request state | Suitable capability combination | Deliverable boundary |
|---|---|---|
| Raw related terms only | `keywords/extends` | Return observed candidate recall only; do not force validation. |
| Seed keyword, candidate list not yet confirmed | `extends` | Candidate recall for user review; do not run market validation yet. |
| User-confirmed candidate list, no ASIN evidence | batch `market-profile`; add `trend-profile` or `search-results` only for a named question | Market-screen shortlist for possible ASIN validation. |
| ASIN evidence is available after market screening | `realtime/product` or compatible carried direct product evidence + carried candidate market evidence; add only named trend/SERP evidence | Product-specific candidate-validation posture. |

Use `phrase`, then `fuzzy` when a phrase expansion is empty. Use metric-first access and batch compatible candidates as defined in the shared guide and API reference.

## Labels and next evidence

- Without ASIN evidence, use only: `Advance to ASIN validation`, `Selective ASIN validation`, `Observe`, or `No current support`.
- With suitable direct ASIN/product-fit evidence, use only: `High validation priority`, `Selective validation`, `Existing-fit validation`, `Observe`, or `No current support` as provisional validation labels.
- These labels are subject to the shared Candidate Validation Rule; they never authorize operating changes.
- Request an ASIN only when product-specific prioritization is needed. Request ABA-SQP only when the unresolved decision requires seller-real evidence under the shared guide.

## User journey

| Stage | Current input | Capability and user-facing outcome | Transition |
|---|---|---|---|
| 1. Candidate recall | Seed keyword | Use `extends`; present related terms and why each belongs in the candidate set. Do not assign market or product-specific labels. | Ask the user to confirm the list or name additions/removals, then stop. A raw-term-only request ends here. |
| 2. Market screening | User-confirmed candidate list | Batch `market-profile` for confirmed terms and add only named trend/SERP evidence; present the market-screen evidence, analysis, and shortlist conclusion. | If product-specific prioritization is wanted, request the ASIN and stop. |
| 3. ASIN candidate validation | Stage 2 conclusion + user-supplied ASIN | Combine carried candidate market evidence with current direct ASIN/product-fit evidence; present product-specific evidence, analysis, and provisional validation posture. | If seller calibration is needed, request one SQP artifact and stop. |
| 4. Seller-funnel calibration | Supplied SQP artifact | Analyze SQP with retained earlier-stage evidence and give the calibrated conclusion authorized by it. | Request Ads later only if economics or execution remains unresolved. |
| 5. Ads-economics calibration | Later Ads artifact, when required | Analyze the search-term report and update only supported economics/execution conclusions. | Stop unless one named decision remains unresolved. |

Apply the shared `Interactive Stage Gate` from `execution-guide.md`; each numbered stage is a separate user-decision turn. Do not call `market-profile` before the Stage 1 candidate list is confirmed, and do not combine candidate recall, market screening, and ASIN validation into one report. A supplied candidate list, ASIN, or file counts as confirmation for the matching next stage; do not ask for duplicate confirmation.

Do not request SQP before the ASIN observation and candidate-validation conclusion. At a seller-data boundary, load `sqp-field-semantics.md` and follow its acquisition, sequencing, sufficiency, and field-interpretation rules instead of redefining them here.

## Output shape

Use the shared output rules. For a raw-term lookup, keep the response brief. Render this shape for the active stage only; never populate it with several stage conclusions in one response:

```markdown
# [Localized Keyword Expansion Report title] — [Seed Keyword]

> [Localized source and snapshot-period note]

## [Localized Data Notes title]
[State the evidence source, period, and current analysis scope.]

## [Localized Evidence title]
| [Localized Keyword header] | [Localized Seed/intent-fit header] | [Localized Demand/trend header] | [Localized Market-structure header] | [Localized ASIN-fit evidence header when available] |
|---|---|---|---|---|

## [Localized Analysis title]
[Reconcile the material evidence and limitations for the active stage.]

## [Localized Stage Conclusion title]
[State only the decision or validation-posture label authorized by the current evidence.]

## [Localized Next Step title]
[Include only when a specific next evidence request is needed.]

## [Localized API Usage title]
[Use the shared required table format when live API data was used.]
```
