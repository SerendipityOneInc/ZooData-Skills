# ASIN Keyword Traffic-Change Diagnosis Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects evidence for ASIN-wide or named ASIN × keyword movement and anomaly questions and must align upward with `execution-guide.md`, `evidence-protocols.md`, `diagnosis-action-protocols.md`, `output-rules.md`, `reference.md`, and the field-semantic references; it does not authorize causal or operating conclusions beyond them.

## Scenario boundary

This scenario owns traffic-change diagnosis: temporal movement, anomaly, and causal questions for an ASIN × keyword plus initial aggregate triage for an ASIN-wide change diagnosis.

- Use it for explicit traffic-change diagnosis: `why`, drop/rise, volatility, anomaly, event attribution, and time-based explanation questions.
- Do not produce a full current traffic-term map, candidate pool, or `Established posture` / `Headroom validation` / `Observe` / `No current support` classification. Those belong to `scenarios-reverse-asin.md`.
- For an ASIN-wide traffic-change diagnosis without a named keyword, use aggregate overview evidence only to locate the changed channel/scope. Do not infer per-keyword contribution or cause. A keyword-level explanation belongs to Stage 1B and requires one named keyword as its entry input.
- A follow-up from reverse ASIN that names a keyword and asks why it moved enters this scenario directly; reuse compatible prior evidence without repeating traffic-term discovery.

## Capability combinations

| Question | Primary capability | Supporting capability when needed |
|---|---|---|
| ASIN-wide traffic-change diagnosis without a named keyword | `product-traffic-terms-overview` | Returned aggregate channels and ORG first-three-page entries/exits |
| ASIN × keyword movement over time | `product-traffic-terms-timeline` | Returned weekly series for the named ASIN × keyword |
| Market demand / ABA-rank trend | `trend-profile` | `trend` only for explicitly required weekly points absent from the profile |
| Observed keyword SERP structure | `search-results` | Current returned placement/exposure records |
| Current market context | `market-profile` | `detail` only for a named raw field not exposed by the metric contract |

Apply the shared diagnostic procedure from `diagnosis-action-protocols.md` within the active evidence level, then return every reported branch to the `Diagnostic Closure Gate` in `execution-guide.md`.

## Diagnostic dimensions available

| Dimension | Returned fields / comparison |
|---|---|
| Placement and exposure | Organic/sponsored positions, pages, `traffic.*ImpressionPoint`, and placement averages across returned weeks |
| Demand and ABA rank | Weekly `trend-profile` or required raw trend points |
| Product events | `asinSnapshot` price, BSR, sales, rating/review count, title, and main-image-link changes |
| Ad activity | Timeline `adActivity` counts and coverage |
| ASIN-wide movement | Overview current versus matching `*Prev` placement impression points and first-three-page ORG entries/exits |

Interpret timeline, aggregate movement, placement, traffic, coverage, and ad-activity observations only through `traffic-observation-semantics.md`. Combine only the evidence domains needed for the named movement question.

## Supported report outputs

- Change table comparing returned periods and fields.
- ASIN-side timeline covering available product, placement, traffic, and event signals.
- All-keyword traffic overview by placement when retrieved.
- An evidence-bounded description of the observed movement's magnitude and persistence, with the contributing returned signals shown alongside it.
- Explanation status that distinguishes confirmed evidence, bounded hypotheses, and the exact unresolved question.
- Evidence-authorized next action and, when the current diagnosis still requires authorized validation, the smallest directly matching next evidence.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| 1A. ASIN-wide change triage | ASIN + traffic-change question without a named keyword | `product-traffic-terms-overview` interpreted through `traffic-observation-semantics.md` | Describe aggregate channel movement and returned ORG first-three-page entries/exits. Do not attribute per-keyword contribution or cause. |
| 1B. ASIN × keyword diagnosis | ASIN + keyword + relevant observation range | Timeline plus only the market, SERP, product-event, or aggregate evidence required by the named movement question | Give the movement description and explanation status permitted by `traffic-observation-semantics.md` and the shared conclusion gates. Do not infer seller conversion, profitability, bids, or budget. |
| 2. Seller-funnel calibration | Explicit seller-funnel or conversion request + compatible Stage 1 evidence + SQP artifact for the named ASIN × keyword question | Compatible carried evidence plus user-provided ABA-SQP interpreted through `sqp-field-semantics.md` | Update only the funnel or conversion conclusion supported by the supplied seller fields. Do not give Ads economics, profitability, exact bid, or budget conclusions. |
| 3. Ads-performance calibration | Explicit Ads-performance request + compatible earlier-stage evidence + Ads artifact for the named ASIN × keyword | Compatible carried evidence plus the user-provided Ads search-term report interpreted through `sqp-field-semantics.md` | Give only the attributed Ads-performance conclusion supported for the named scope. Do not infer profitability or recommend a bid or budget. |
| 4. Profitability calibration | Explicit profitability request + compatible earlier-stage and Ads evidence + seller-supplied unit economics or an economics-grounded break-even/target ACOS or ROAS | Compatible carried evidence plus the supplied Ads performance and economics interpreted through `sqp-field-semantics.md` | Give only the named profitability conclusion supported for the preserved scope. Do not give an exact bid or budget decision. |
| 5. Advertising-control decision | Explicit exact bid or budget request + compatible earlier-stage evidence + the complete controlled-target, performance, current-control, objective/economics, and validation inputs required by `diagnosis-action-protocols.md` | Compatible carried evidence plus only the seller inputs required for the named control under `diagnosis-action-protocols.md` and `sqp-field-semantics.md` | Give only the named reversible control decision when fully authorized; otherwise conclude with the exact unresolved evidence boundary and no number. |

Apply the shared `Interactive Stage Gate`, `Stage Handoff Closure Gate`, and `Stage-End Selection List Rule` from `execution-guide.md`. The rows above are evidence levels, not a required end-to-end traversal. Multiple timeline/market/SERP calls needed for the same Stage 1B conclusion remain within that evidence level; seller artifacts belong to their own later evidence levels.

Stage 1A does not authorize SQP interpretation. At seller-data evidence levels, load `sqp-field-semantics.md` and follow its acquisition, sequencing, sufficiency, and field-interpretation rules instead of redefining them here.

## Section content requirements

Use the canonical Full-Mode Stage Output template from `output-rules.md` without renaming, adding, removing, or reordering its report sections.

- Put observed movement and its supporting signals in Evidence.
- Put explanation status, bounded hypotheses, and unresolved diagnostic boundaries in Analysis.
- Put only the diagnostic result authorized by the active stage's new evidence and compatible prior-stage evidence in Conclusion.
- Do not include a generic list of possible causes, repeat a prior-stage report, or append later-stage analysis to the same response.
