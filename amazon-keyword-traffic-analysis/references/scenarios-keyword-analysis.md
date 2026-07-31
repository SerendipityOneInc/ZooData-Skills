# Target-Keyword Analysis Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects evidence combinations for a target-keyword question and must align upward with `execution-guide.md`, `reference.md`, and the field-semantic references; it does not define independent decision or action rules.

## Capability combinations

| User question / available subject | Primary capabilities | Optional capability when the named question requires it |
|---|---|---|
| Market demand, structure, or entry context for a keyword | `market-profile` + `trend-profile` | `search-results` for observed product type, intent, or placement structure; `detail` for a documented raw field absent from the metric contract |
| Official ZooData organic rollover/stability indicator | `detail.snapshotData.organicRolloverRate` | Load `serp-and-rollover.md`; do not relabel it as a Top-N turnover calculation |
| Keyword plus ASIN, without a movement or causal question | Carry compatible market evidence + `realtime/product` or compatible carried direct product evidence + current placement/traffic evidence | `search-results` for a named SERP question. Route movement, anomaly, and causal questions to `scenarios-keyword-traffic-diagnosis.md`. |
| Seller-real calibration | User-provided ABA-SQP, plus Amazon Ads data when economics or execution settings are requested | Load `sqp-field-semantics.md` before interpreting SQP fields |

## User journey

| Stage | Current input | Capability combination and user-facing outcome | Transition |
|---|---|---|---|
| 1. Market screen | Target keyword | Combine market profile and weekly trend, adding SERP evidence only for a named question; present market evidence, analysis, and a market-screen conclusion. | Unless the user explicitly requested a market-only screen, after a usable market conclusion request the target ASIN for product-specific validation; otherwise end after usage reporting. |
| 2. ASIN observation | Stage 1 conclusion + target ASIN | Combine carried market evidence with current observed product, placement, and traffic evidence; present ASIN evidence, analysis, and the current ASIN posture. | If candidate validation remains in the requested journey, present the observed or user-supplied candidate terms, request confirmation/additions/removals, and stop; otherwise end after usage reporting. |
| 3. Candidate validation | Stage 2 conclusion + user-confirmed candidate terms | Batch the applicable market-profile capability across candidates; present candidate evidence, analysis, and an evidence-bounded validation pool. | If the candidate conclusion advances any term for seller-funnel validation, render a separate mandatory SQP next-input request through `sqp-field-semantics.md`, then stop. If no term advances, end after usage reporting. |
| 4. Seller-funnel calibration | Supplied SQP artifact | Load `sqp-field-semantics.md`; combine SQP with retained earlier-stage evidence and present the seller-funnel evidence, analysis, and conclusion authorized by the supplied fields. | If the conclusion names one exact economics or execution question that requires Ads evidence, request one Ads artifact through that reference and stop; otherwise end after usage reporting. |
| 5. Ads-economics calibration | Later Ads artifact, when required | Analyze the supplied search-term report and update only the economics/execution conclusions it supports. | No further input unless one named decision remains unresolved. |

### Stage transition gate

- Apply the shared `Interactive Stage Gate` and `Stage Handoff Closure Gate` from `execution-guide.md`; each numbered stage is a separate user-decision turn.
- For natural target-keyword questions such as `worth targeting` or `worth focusing on`, treat the journey as multi-stage unless the user explicitly requests market-only analysis.
- A Stage 3 conclusion that advances any term into the validation pool makes seller-funnel calibration necessary by definition and triggers one SQP-artifact request through `sqp-field-semantics.md`; keep the pre-SQP conclusion provisional.
- After a Stage 1 advance conclusion, the scenario-defined next input is only the target ASIN.
- Do not request an ASIN until Stage 1 has produced a usable market-screen conclusion. Do not request ABA-SQP until the ASIN observation and candidate-validation conclusions are complete.
- At a seller-data boundary, load `sqp-field-semantics.md` and follow its acquisition, sequencing, sufficiency, and field-interpretation rules. Do not redefine those shared rules here.
- Do not request price, contribution margin, budget, SQP, or Ads data as a substitute for unavailable market demand, trend, structure, or SERP evidence. Those inputs cannot repair a failed Stage 1 retrieval.

## Supported report outputs

- Market-screen result: demand/trend/market-structure/SERP evidence and whether ASIN-level validation is supported.
- ASIN observation: carried market constraints plus current ASIN fit, placement, traffic, and observed posture.
- Candidate validation: a market-profile-validated pool for seller-funnel validation.
- Seller-funnel calibration: SQP-based interpretation combined with retained earlier-stage constraints.
- Ads-economics calibration: later, separately supplied Ads interpretation with evidence-authorized operating decisions.

## Report progression

- Keep the journey conversational: present the current stage's evidence, analysis, and stage conclusion first, then make the journey-defined next-input request whenever the conclusion advances a subject to the next evidence level.
- With ASIN evidence, retain compatible market constraints and add the observed subject posture without collapsing market and subject signals.

Use the shared guide for cross-metric reconciliation, evidence coverage, causal diagnosis, confidence, and output requirements.

## Output shape

After the active target-keyword stage has completed its required retrieval under the shared execution guide, use localized sections in this order: Data Notes, Evidence, Analysis, Stage Conclusion, and Next Input when defined by the journey. Put API Usage at the end of the current response when live API data was used. Do not include another stage's evidence or conclusion in that response. Keep Data Notes limited to source, returned period, and current stage; do not use it to list future missing inputs or replace Evidence or Analysis. Do not expose internal reasoning mechanics.
