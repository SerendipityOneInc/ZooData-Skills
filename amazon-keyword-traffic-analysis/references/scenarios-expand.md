# Keyword Expansion Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects capabilities for expansion and must align upward with `execution-guide.md`, `evidence-protocols.md`, `output-rules.md`, `reference.md`, and the field-semantic references; it cannot relax their evidence, conclusion, action, credit, or output requirements.

## Route selection

| Request state | Suitable capability combination | Deliverable boundary |
|---|---|---|
| Raw related terms only | `keywords/extends` | Return observed candidate recall only; do not force validation. |
| Seed keyword, candidate list not yet confirmed | `extends` | Candidate recall for user review; do not run market validation yet. |
| User-confirmed candidate list, no ASIN evidence | batch `market-profile`; add `trend-profile` or `search-results` only for a named question | Market-screen shortlist for possible ASIN validation. |
| ASIN evidence is available after market screening | `realtime/product` or compatible carried direct product evidence + carried candidate market evidence; add only named trend/SERP evidence | Product-specific candidate-validation posture. |

Use `phrase`, then `fuzzy` when a phrase expansion is empty. Use metric-first access and batch compatible candidates as defined in `evidence-protocols.md` and the API reference.

## Conclusion labels

- Without ASIN evidence, use only: `Advance to ASIN validation`, `Selective ASIN validation`, `Observe`, or `No current support`.
- With suitable direct ASIN/product-fit evidence, use only: `High validation priority`, `Selective validation`, `Existing-fit validation`, `Observe`, or `No current support` as provisional validation labels.
- These labels are subject to the shared Candidate Validation Rule; they never authorize operating changes.
- `Advance to ASIN validation` and `Selective ASIN validation` mean only that ASIN-level evidence is warranted; they are not workflow states.
- `High validation priority`, `Selective validation`, and `Existing-fit validation` mean the current product-specific priority remains provisional below seller-funnel evidence.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| 1. Candidate recall | Seed keyword | `extends` related-term recall | Describe the returned candidate set and why terms belong to it. Do not assign market or product-specific labels. |
| 2. Market screening | User-confirmed candidate list | Batched `market-profile`; named trend/SERP evidence only when the current question requires it | Give market-screen labels and a market shortlist. Decide only whether ASIN-level evidence is warranted; do not give product-specific priority. |
| 3. ASIN candidate validation | Compatible Stage 2 evidence + target ASIN | Carried candidate-market evidence plus current direct ASIN/product-fit evidence | Give provisional product-specific validation labels. Do not give seller-calibrated priority, conversion, profitability, bid, or budget conclusions. |
| 4. Seller-funnel calibration | Explicit seller-funnel or product-priority request + compatible earlier-stage evidence + SQP artifact for one named ASIN × candidate | Compatible carried evidence plus user-provided ABA-SQP interpreted through `sqp-field-semantics.md` | Give the product-specific funnel and priority conclusion supported for that named candidate. Do not give Ads economics, profitability, exact bid, or budget conclusions. |
| 5. Ads-performance calibration | Explicit Ads-performance request + compatible earlier-stage evidence + Ads artifact for one named ASIN × candidate | Compatible carried evidence plus the user-provided Ads search-term report interpreted through `sqp-field-semantics.md` | Give only the attributed Ads-performance conclusion supported for the named scope. Do not infer profitability or recommend a bid or budget. |
| 6. Profitability calibration | Explicit profitability request + compatible earlier-stage and Ads evidence + seller-supplied unit economics or an economics-grounded break-even/target ACOS or ROAS | Compatible carried evidence plus the supplied Ads performance and economics interpreted through `sqp-field-semantics.md` | Give only the named profitability conclusion supported for the preserved scope. Do not give an exact bid or budget decision. |
| 7. Advertising-control decision | Explicit exact bid or budget request + compatible earlier-stage evidence + the complete controlled-target, performance, current-control, objective/economics, and validation inputs required by `diagnosis-action-protocols.md` | Compatible carried evidence plus only the seller inputs required for the named control under `diagnosis-action-protocols.md` and `sqp-field-semantics.md` | Give only the named reversible control decision when fully authorized; otherwise conclude with the exact unresolved evidence boundary and no number. |

Apply the shared `Interactive Stage Gate`, `Stage Handoff Closure Gate`, and `Stage-End Selection List Rule` from `execution-guide.md`. The rows above are evidence levels, not a required end-to-end traversal. Use only the stage whose entry input is available and whose conclusion authority matches the user's current question.

Do not call `market-profile` before the Stage 1 candidate list is confirmed, and do not combine candidate recall, market screening, and ASIN validation into one report. A supplied candidate list, ASIN, or file satisfies the matching stage input; do not ask for duplicate confirmation.

Do not interpret SQP before compatible market and ASIN candidate-validation evidence exists for the named candidate. At a seller-data boundary, load `sqp-field-semantics.md` and follow its acquisition, sequencing, sufficiency, and field-interpretation rules instead of redefining them here.

## Section content requirements

Use the canonical Full-Mode Stage Output template from `output-rules.md` without renaming, adding, removing, or reordering its report sections.

- Keep a related-term discovery report concise. In Evidence, show the candidate terms and only the intent-fit, demand/trend, market-structure, or ASIN-fit fields available to the active stage.
- In Analysis, reconcile the material evidence and limitations for the active stage.
- In Conclusion, state only the decision or validation-posture label authorized by the current evidence.
- Present the active stage's new evidence plus only the compatible prior-stage evidence needed for its analysis and conclusion. With ASIN evidence, retain compatible market constraints and add the observed subject posture without collapsing market and subject signals.
