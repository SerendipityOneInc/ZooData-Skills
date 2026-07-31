# Reverse-ASIN Keyword Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects capabilities for “which keywords drive this ASIN's observed traffic/visibility?” and must align upward with `execution-guide.md`, `reference.md`, and the field-semantic references; those specifications define all conclusion and action limits.

## Scenario boundary

This scenario maps the ASIN's current observed traffic terms and validates a user-confirmed candidate set. It does not diagnose temporal movement, anomalies, or causes.

- Use it for `which keywords`, `traffic terms`, `traffic-source structure`, `candidate keywords`, and current observed posture.
- Do not answer `why`, drop/rise, volatility, anomaly, event attribution, or time-based explanation questions here. Route them to `scenarios-keyword-traffic-diagnosis.md`.
- Do not call `product-traffic-terms-timeline` or `product-traffic-terms-overview` in this scenario. Their movement evidence belongs to diagnosis.
- If the user selects a discovered term and asks why it changed, the follow-up itself confirms transition to diagnosis; reuse compatible traffic-source evidence and load only the diagnosis scenario in that turn.

## Capability combinations

| Question | Primary capability | Add only when needed |
|---|---|---|
| Current keyword traffic-term list | `keywords/product-traffic-terms` | Select `keywords/competitor-product-keywords` before retrieval only for competitor/overlap framing; it is not a runtime-failure fallback |
| Selected term's market context | batch `market-profile` | `trend-profile` only for keyword-market trend context; `search-results` for named current-SERP questions. Neither is used to diagnose ASIN movement here. |
| Product-specific fit for a posture label | `realtime/product` for the target ASIN, unless compatible direct product evidence is already carried | Page acquisition only when a named fit inference requires evidence absent from the structured product response |

If neither ASIN traffic-list endpoint is available, do not make reverse-ASIN traffic-source claims. `detail` and `search-results` cannot replace a traffic-source map.

## Traffic-term dimensions available

| Dimension | Returned evidence |
|---|---|
| Traffic contribution | `trafficShare`, `estimateImpressionPoint` |
| Rank quality | `avgPosition`, `daysCoverageRate`, `observationCount` |
| Keyword size | `keywordEstimateSearchCount`, `keywordAbaRank` |
| Market context | Selected-term `market-profile`, trend, and SERP evidence when retrieved |

## Supported report outputs

- Current traffic-term table with contribution, position/coverage, keyword-size, and candidate-selection rationale. Stage 1 does not assign posture labels or operating priority.
- Selected-term market-context enrichment without treating it as a replacement for the ASIN traffic-source map.
- Carried target-keyword observation combining compatible earlier market evidence with the ASIN's current fit, placement, and traffic posture.
- Candidate pool validated through batch market-profile and sufficient direct product-fit evidence before seller-funnel calibration.

## Posture labels

Use these labels only after Stage 2 candidate market validation. Never assign them directly from the Stage 1 traffic-source list.

- `Established posture`: the term currently contributes meaningful observed ASIN traffic or holds a comparatively strong position and has directly observed product fit.
- `Headroom validation`: product fit, ASIN observation, and candidate market validation support further seller-funnel validation while current position or contribution still has observable headroom. Assigning this label means seller-funnel calibration is the required next stage before any final product-specific priority conclusion.
- `Observe`: evidence is relevant but sparse, unstable, mixed, or not yet sufficient to advance.
- `No current support`: current evidence shows weak fit or lacks support for further validation. Do not use this label merely because one endpoint returned empty or one observation was poor.

## User journey

| Stage | Current input | Required capability and user-facing outcome | Transition |
|---|---|---|---|
| 1. Traffic-term discovery | ASIN | Retrieve the traffic-term list. Present the current observed traffic structure and a clearly labeled list of keywords requiring examination, with each selection tied to sampled contribution, semantic cluster, placement/coverage gap, or a carried target keyword. | For the staged workflow, render one concise confirmation request and stop; a raw-list-only request ends without a confirmation request. |
| 2. Candidate keyword examination | User-confirmed Stage 1 candidate list | Batch every confirmed candidate that may appear in the stage conclusion through `market-profile`, and inspect current direct product evidence before assigning a product-specific posture label. Add trend or SERP evidence only for a named question. Present keyword-market and product-fit evidence, analysis, and an evidence-bounded candidate/posture conclusion. Candidates with valid empty/unsupported market evidence or without sufficient direct product-fit evidence remain unvalidated and receive no posture label. | If any candidate receives `Headroom validation`, render a separate mandatory SQP next-input request through `sqp-field-semantics.md`, then stop. If no candidate advances and the user's requested posture decision is complete, end after usage reporting. |
| 3. Seller-funnel calibration | Supplied SQP artifact requested after Stage 2 | Analyze SQP and combine it with the retained Stage 1–2 evidence before giving the seller-calibrated conclusion authorized by those fields. | If the conclusion names one exact profitability or execution question that requires Ads evidence, request one Ads artifact and stop; otherwise end after usage reporting. |
| 4. Ads-economics calibration | Later Ads artifact, when required | Follow `sqp-field-semantics.md`; analyze the supplied search-term report and update only the economics/execution conclusions it supports. | No further input unless one named decision remains unresolved. |

### Stage transition gate

- Apply the shared `Interactive Stage Gate` and `Stage Handoff Closure Gate` from `execution-guide.md`; the rules below define this scenario's stage boundaries.
- Treat natural requests such as `analyze this ASIN's keyword traffic` or `reverse-ASIN analysis` as the full staged workflow. A raw-list-only request must be explicit.
- Stage 1 is discovery, not keyword judgment. Its conclusion may state which keywords require examination and why, but it must not assign `Established posture`, `Headroom validation`, `Observe`, or `No current support`, declare advertising dependence, recommend SEO/listing changes, rank advertising priority, or request SQP.
- Stage 1 may describe a term's returned ORG/SP/SB/SBV/SPR records and sampled contribution, but a sponsored-only row or selected Top-N subset does not establish overall advertising dependence, weak organic relevance, algorithmic recognition, or organic improvement potential. Do not call coverage `full`, `complete`, or `stable` unless the returned coverage fields and resolved period directly establish that claim.
- Do not call `realtime/product` or page acquisition during Stage 1; direct product-fit retrieval belongs to Stage 2 after candidate confirmation. Retain any compatible carried product evidence without rendering or interpreting it during Stage 1.
- A generic full-analysis request does not authorize automatic progression. After Stage 1, ask the user to confirm the candidate list or name additions/removals, then stop the turn. Do not call `market-profile` before that confirmation.
- Advance to Stage 2 only when the candidate list was explicitly confirmed or supplied by the user in the current conversation. A reply such as `confirm`, `continue`, or `analyze these terms` is sufficient; do not ask a second confirmation.
- Every candidate included in the Stage 2 posture conclusion must have completed market-profile validation and sufficient directly observed ASIN/product-fit evidence. Traffic share, estimated impression points, placement type, or keyword wording alone cannot replace either requirement.
- Do not present a final keyword-priority, SEO, advertising, bid, budget, or profitability conclusion before the required seller-data stage. Stage 2 provides an evidence-bounded candidate conclusion, never a `Final calibrated conclusion`.
- In the full staged workflow, assigning `Headroom validation` makes seller-funnel calibration necessary by definition. After the Stage 2 conclusion, render the scenario-defined SQP next-input section through `sqp-field-semantics.md` and stop.
- If the conversation carries a target keyword from an earlier market screen, include it in the Stage 1 discovery evidence and reuse compatible carried context. Do not retrieve new market or SERP evidence before candidate confirmation. If the user asks about movement or cause, transition to diagnosis instead of calling a timeline here.

Do not request SQP before the candidate-validation conclusion. At a seller-data boundary, use `sqp-field-semantics.md` as the sole source for acquisition, sequencing, sufficiency, and field interpretation.

## Report shape

After the required Stage 1 traffic-term retrieval has produced usable evidence under the shared execution guide, render localized sections in this order and then stop:

1. Data Notes.
2. Stage 1 traffic evidence.
3. Stage 1 analysis.
4. `Keywords to Examine`, listing the candidate, observed reason for selection, and evidence still required; this is not a recommendation table.
5. Stage 1 discovery conclusion.
6. For the staged workflow only, a separate next-input section asking the user to confirm the list or name additions/removals; omit it for a raw-list-only request.
7. API usage.

After confirmation, render Data Notes, Stage 2 keyword-market/product-fit evidence, a separate analysis section, the Stage 2 candidate/posture conclusion, and API usage. If any candidate receives `Headroom validation`, include the mandatory separate SQP next-input section immediately after the stage conclusion and before API usage. Follow `sqp-field-semantics.md` for the acquisition path and upload action. Do not repeat the full Stage 1 report; carry forward only the evidence needed to explain the Stage 2 conclusion.

Labels such as `Established posture`, `Headroom validation`, `Observe`, and `No current support` may appear only in Stage 2 or later, describe validation posture only, and remain subject to the shared Candidate Validation and action rules. Do not collapse the two stages into one response, auto-run Stage 2, or move the SQP request directly after the traffic-source table.
