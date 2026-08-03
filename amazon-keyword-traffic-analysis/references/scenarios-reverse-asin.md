# Reverse-ASIN Traffic-Structure Diagnosis Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects capabilities for “which keywords drive this ASIN's observed traffic/visibility?” and must align upward with `execution-guide.md`, `evidence-protocols.md`, `output-rules.md`, `reference.md`, and the field-semantic references; those specifications define all conclusion and action limits.

## Scenario boundary

This scenario diagnoses the ASIN's current observed traffic structure by selecting the aggregate channel metric or the keyword-level traffic-term detail required by the user's question, then validating a user-confirmed candidate set when applicable. It may describe the overview's explicitly scoped first-three-page organic Top-N entries and exits as structure context, but it does not diagnose broader temporal movement, anomalies, or causes.

- Use it for explicit traffic-structure diagnosis: `which keywords`, `traffic terms`, `traffic-source structure`, `candidate keywords`, and current observed posture.
- Do not claim a broad ASIN keyword-traffic analysis, overview, health check, or perspective request merely because it lacks change language; `SKILL.md` and the shared clarification gate must disambiguate it before this scenario is loaded.
- Do not answer `why`, drop/rise, volatility, anomaly, event attribution, or time-based explanation questions here. Route them to `scenarios-keyword-traffic-diagnosis.md`.
- Do not call `product-traffic-terms-timeline` in this scenario. Use `product-traffic-terms-overview` for its current ORG/SP/SB/SBV/SPR fields and its returned first-three-page organic entry/exit lists when the user asks for current aggregate channel or placement structure. The lists may be described only as bounded Top-N set membership changes between the returned previous and current periods; numeric `*Prev` comparisons, persistence, anomaly, and cause remain outside this scenario.
- A follow-up asking why a discovered term changed is outside this scenario; preserve compatible traffic-source evidence for top-level rerouting.

## Capability combinations

| Question | Primary capability | Add only when needed |
|---|---|---|
| Current ASIN-wide channel or placement structure | `product-traffic-terms-overview` current ORG/SP/SB/SBV/SPR fields and returned first-three-page organic entry/exit lists | Stop when the aggregate metric answers the question; do not descend to traffic-term rows merely to duplicate channel structure or the returned set changes |
| Current keyword traffic-term list | `keywords/product-traffic-terms` | Select `keywords/competitor-product-keywords` before retrieval only for competitor/overlap framing; it is not a runtime-failure fallback |
| Selected term's market context | batch `market-profile` | `trend-profile` only for keyword-market trend context; `search-results` for named current-SERP questions. Neither is used to diagnose ASIN movement here. |
| Product-specific fit for a posture label | `realtime/product` for the target ASIN, unless compatible direct product evidence is already carried | Page acquisition only when a named fit inference requires evidence absent from the structured product response |

If the aggregate overview is unavailable, do not reconstruct a complete ASIN-wide channel mix from one page of traffic-term rows. If neither ASIN traffic-list endpoint is available, do not make keyword-level reverse-ASIN traffic-source claims. `detail` and `search-results` cannot replace either contract.

## Traffic-term dimensions available

| Dimension | Returned evidence |
|---|---|
| Aggregate channel exposure | Overview current ORG/SP/SB/SBV/SPR impression points |
| Traffic contribution | `trafficShare`, `estimateImpressionPoint` |
| Rank quality | `avgPosition`, `daysCoverageRate`, `observationCount` |
| Keyword size | `keywordEstimateSearchCount`, `keywordAbaRank` |
| Market context | Selected-term `market-profile`, trend, and SERP evidence when retrieved |

## Supported report outputs

- Current aggregate channel/placement structure from the overview's current fields, plus clearly scoped first-three-page organic Top-N entries/exits between the returned periods when material.
- Current traffic-term table with contribution, position/coverage, keyword-size, and candidate-selection rationale. Traffic-term discovery does not assign posture labels or operating priority.
- Selected-term market-context enrichment without treating it as a replacement for the ASIN traffic-source map.
- Carried target-keyword observation combining compatible earlier market evidence with the ASIN's current fit, placement, and traffic posture.
- Candidate pool validated through batch market-profile and sufficient direct product-fit evidence before seller-funnel calibration.

## Posture labels

Use these labels only after Stage 2 candidate market validation. Never assign them directly from the Stage 1 traffic-source list.

- `Established posture`: the term currently contributes meaningful observed ASIN traffic or holds a comparatively strong position and has directly observed product fit.
- `Headroom validation`: product fit, ASIN observation, and candidate market validation show observable headroom but do not yet support a final product-specific priority conclusion. The label remains provisional below seller-funnel evidence.
- `Observe`: evidence is relevant but sparse, unstable, mixed, or not sufficient for a stronger conclusion at the current evidence level.
- `No current support`: current evidence shows weak fit or lacks support for further validation. Do not use this label merely because one endpoint returned empty or one observation was poor.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| 1A. Aggregate channel structure | ASIN + explicit current channel/placement-structure question | Current ORG/SP/SB/SBV/SPR fields and returned first-three-page organic entry/exit lists from `product-traffic-terms-overview`, interpreted through `traffic-observation-semantics.md` | Describe the current aggregate observed channel/placement exposure structure and bounded Top-N organic set entries/exits. Do not make numeric `*Prev` comparisons, infer per-keyword contribution, persistence, anomaly, causes, or operating priority. |
| 1B. Traffic-term discovery | ASIN + explicit traffic-term, keyword-contribution, or candidate-discovery question | Traffic-term list interpreted through `traffic-observation-semantics.md` | Describe the returned keyword-level traffic structure and identify terms that merit examination. Do not assign product-specific posture labels, infer causes, or give operating priority. |
| 2. Candidate keyword examination | User-confirmed candidate list + compatible Stage 1B evidence | Batched candidate `market-profile` evidence plus current direct product evidence; named trend/SERP evidence only for the current question | Give evidence-bounded product-specific posture labels. Do not give seller-calibrated priority, conversion, profitability, bid, or budget conclusions. |
| 3. Seller-funnel calibration | Explicit seller-funnel or product-priority request + compatible Stage 1B–2 evidence + SQP artifact for one named candidate | Compatible carried evidence plus user-provided ABA-SQP interpreted through `sqp-field-semantics.md` | Give the product-specific funnel and priority conclusion supported for that candidate. Do not give Ads economics, profitability, exact bid, or budget conclusions. |
| 4. Ads-performance calibration | Explicit Ads-performance request + compatible earlier-stage evidence + Ads artifact for one named candidate | Compatible carried evidence plus the user-provided Ads search-term report interpreted through `sqp-field-semantics.md` | Give only the attributed Ads-performance conclusion supported for the named scope. Do not infer profitability or recommend a bid or budget. |
| 5. Profitability calibration | Explicit profitability request + compatible earlier-stage and Ads evidence + seller-supplied unit economics or an economics-grounded break-even/target ACOS or ROAS | Compatible carried evidence plus the supplied Ads performance and economics interpreted through `sqp-field-semantics.md` | Give only the named profitability conclusion supported for the preserved scope. Do not give an exact bid or budget decision. |
| 6. Advertising-control decision | Explicit exact bid or budget request + compatible earlier-stage evidence + the complete controlled-target, performance, current-control, objective/economics, and validation inputs required by `diagnosis-action-protocols.md` | Compatible carried evidence plus only the seller inputs required for the named control under `diagnosis-action-protocols.md` and `sqp-field-semantics.md` | Give only the named reversible control decision when fully authorized; otherwise conclude with the exact unresolved evidence boundary and no number. |

### Stage application constraints

- Apply the shared `Interactive Stage Gate`, `Stage Handoff Closure Gate`, and `Stage-End Selection List Rule` from `execution-guide.md`. The rows above are evidence levels, not a required end-to-end traversal.
- Stages 1A and 1B are mutually exclusive active entries selected by the requested deliverable. Use Stage 1A for current aggregate channel/placement structure and Stage 1B for traffic terms, keyword contribution, or candidate discovery; do not call both merely to provide a broader report.
- When one explicit request names both aggregate structure and keyword-level terms, complete Stage 1A first under metric-first access and expose Stage 1B only as a supported continuation; do not combine both conclusions in one turn.
- Stage 1A follows metric-first access. Interpret the overview's current ORG/SP/SB/SBV/SPR fields and, when material, its returned first-three-page organic entry/exit lists. Label the lists with the returned current period, disclose the unavailable previous-period boundary, and preserve the exact set boundary; never infer the missing dates, and use numeric Top-N wording only when N is verified. Do not make numeric `*Prev` comparisons or turn set membership changes into per-keyword contribution, magnitude, persistence, anomaly, or cause. Do not call a traffic-list endpoint unless the user's named question requires keyword rows, in which case Stage 1B is the applicable entry or continuation instead.
- Stage 1B applies to explicit requests such as `map this ASIN's current traffic terms` or `which keywords merit examination`. A raw-list-only request uses only the returned-list conclusion authority and must be explicit.
- Stage 1B may use Top-N wording when the shared ranked-detail protocol verifies the exact sort field, direction, page, page size, filters, identity, period, and usable row count. Otherwise describe only the returned rows. Never use an unqualified `top keywords` label.
- Stage 1B is discovery, not keyword judgment. Its conclusion may state which keywords require examination and why, but it must not assign `Established posture`, `Headroom validation`, `Observe`, or `No current support`, declare advertising dependence, recommend SEO/listing changes, rank advertising priority, or request SQP.
- Interpret Stage 1A and Stage 1B traffic, placement, contribution, and coverage fields only through `traffic-observation-semantics.md`.
- Do not call `realtime/product` or page acquisition during Stage 1A or Stage 1B; direct product-fit retrieval belongs to Stage 2 after candidate confirmation. Retain any compatible carried product evidence without rendering or interpreting it during either stage.
- Stage 2 entry requires a candidate list explicitly supplied or confirmed by the user. Bare `continue` or `analyze these terms` satisfies that entry input only when the preceding request made the entire retained list its single unambiguous referent.
- Do not call `market-profile` before the Stage 2 candidate list is supplied or confirmed.
- Every candidate included in the Stage 2 posture conclusion must have completed market-profile validation and sufficient directly observed ASIN/product-fit evidence. Traffic share, estimated impression points, placement type, or keyword wording alone cannot replace either requirement.
- Do not present a final keyword-priority, SEO, advertising, bid, budget, or profitability conclusion before the required seller-data stage. Stage 2 provides an evidence-bounded candidate conclusion, never a `Final calibrated conclusion`.
- `Headroom validation` remains provisional below Stage 3 seller-funnel evidence for the named candidate.
- If the conversation carries a target keyword from an earlier market screen, include it in the Stage 1B discovery evidence and reuse compatible carried context. Do not retrieve new market or SERP evidence before candidate confirmation. Movement and causal conclusions remain outside this scenario.

Stage 3 requires a compatible Stage 1B–2 candidate-validation conclusion for the named candidate. At a seller-data evidence level, use `sqp-field-semantics.md` as the sole source for acquisition, sequencing, sufficiency, and field interpretation.

## Section content requirements

Use the canonical Full-Mode Stage Output template from `output-rules.md` without renaming, adding, removing, or reordering its report sections.

- For aggregate channel structure, put the current overview fields and any material, explicitly scoped first-three-page organic Top-N entries/exits in Evidence, interpret the current channel/placement mix and bounded set changes in Analysis, and state only that scoped structure conclusion in Conclusion.
- For traffic-term discovery, put the current keyword-row observations and selection basis in Evidence, interpret the returned keyword structure in Analysis, and summarize only the supported discovery conclusion in Conclusion. Do not render a separate candidate shortlist or selection keys in any report section.
- For candidate examination, put keyword-market and product-fit observations in Evidence, reconcile them in Analysis, and put only the authorized posture result in Conclusion. Do not repeat the full discovery report; carry forward only the evidence needed for the current conclusion.
- When the Stage Handoff Closure Gate supports keyword examination, place every selectable keyword and its observed selection reason directly in the single final numbered selection list. Apply the shared rule for individual items, set selection, and the select-all item without creating a separate candidate list in the report body.

Labels such as `Established posture`, `Headroom validation`, `Observe`, and `No current support` may appear only in Stage 2 or later, describe validation posture only, and remain subject to the shared Candidate Validation and action rules. Do not collapse Stage 1A, Stage 1B, or Stage 2 evidence or conclusions into one response.
