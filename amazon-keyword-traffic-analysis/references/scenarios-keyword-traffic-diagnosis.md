# ASIN × Keyword Diagnosis Capability Guide

Use this downstream scenario after loading the applicable top-level references. It selects evidence for a named ASIN × keyword movement or anomaly and must align upward with `execution-guide.md`, `reference.md`, and the field-semantic references; it does not authorize causal or operating conclusions beyond them.

## Scenario boundary

This scenario owns temporal movement, anomaly, and causal questions for an ASIN × keyword and the initial aggregate triage of an ASIN-wide keyword-traffic anomaly.

- Use it for `why`, drop/rise, volatility, anomaly, event attribution, and time-based explanation questions.
- Do not produce a full current traffic-term map, candidate pool, or `Established posture` / `Headroom validation` / `Observe` / `No current support` classification. Those belong to `scenarios-reverse-asin.md`.
- For an ASIN-wide anomaly without a named keyword, use aggregate overview evidence only to locate the changed channel/scope. Do not infer per-keyword contribution or cause; ask the user to select a target keyword or confirm a separate reverse-ASIN discovery stage.
- A follow-up from reverse ASIN that names a keyword and asks why it moved enters this scenario directly; reuse compatible prior evidence without repeating traffic-term discovery.

## Capability combinations

| Question | Primary capability | Supporting capability when needed |
|---|---|---|
| ASIN-wide keyword-traffic anomaly without a named keyword | `product-traffic-terms-overview` | Aggregate channel movement and ORG first-three-page entries/exits only; no per-keyword attribution |
| ASIN × keyword movement over time | `product-traffic-terms-timeline` | At least two observations are needed for more than directional movement commentary |
| Market demand / ABA-rank trend | `trend-profile` | `trend` only for explicitly required weekly points absent from the profile |
| Observed keyword SERP structure | `search-results` | Keep placement/exposure sample boundaries explicit |
| Current market context | `market-profile` | `detail` only for a named raw field not exposed by the metric contract |

Use the shared diagnostic protocol: state the observation, identify the unresolved question, retrieve the smallest discriminating evidence, then give only an evidence-supported explanation or request the exact missing evidence.

## Diagnostic dimensions available

| Dimension | Returned fields / comparison |
|---|---|
| Placement and exposure | Organic/sponsored positions, pages, `traffic.*ImpressionPoint`, and placement averages across returned weeks |
| Demand and ABA rank | Weekly `trend-profile` or required raw trend points |
| Product events | `asinSnapshot` price, BSR, sales, rating/review count, title, and main-image-link changes |
| Ad activity | Timeline `adActivity` counts and coverage, kept separate from bid/CPC economics |
| ASIN-wide movement | Overview current versus matching `*Prev` placement impression points and first-three-page ORG entries/exits |

## Observable signal patterns

Report position, exposure, traffic-share, demand, ad-activity, price, BSR, sales, rating, listing-event, and ORG-entry/exit changes when returned. Treat each as an observation; use time-aligned evidence to discriminate explanations rather than turning co-movement into causality.

For an ASIN × keyword anomaly, combine only the domains needed by the reported movement: keyword demand, SERP/ad density, ASIN placement, product-event curves, head-competitor or concentration observations, ASIN aggregate movement, and ORG first-three-page entries/exits. Use timeline evidence for ASIN × keyword movement and overview evidence for ASIN-wide previous-period movement; neither replaces the other.

## Supported report outputs

- Change table comparing returned periods and fields.
- ASIN-side timeline covering available product, placement, traffic, and event signals.
- All-keyword traffic overview by placement when retrieved.
- An evidence-bounded alert level for the observed movement, with its contributing returned signals shown alongside it.
- Explanation status that distinguishes confirmed evidence, bounded hypotheses, and the exact unresolved question.
- Evidence-authorized next action and, only when needed, the smallest next evidence.

## Alert-level meaning

Alert level describes the magnitude and persistence of the observed movement, not confidence in its cause.

- `High`: a material movement persists across comparable observations and is supported by multiple aligned movement signals.
- `Medium`: movement is notable but shorter-lived, mixed across signals, or limited by coverage.
- `Low`: movement is small or visible only in a single snapshot/observation.

Always show the contributing returned signals next to the label. Do not upgrade the alert level to imply a confirmed explanation or operating action.

## User journey

| Stage | Current input | Capability and user-facing outcome | Transition |
|---|---|---|---|
| 1A. ASIN-wide anomaly triage | ASIN + change/anomaly question, no target keyword | Use `product-traffic-terms-overview` to show aggregate channel movement and any returned ORG first-three-page entries/exits. Present the bounded scope conclusion without a per-keyword cause. | Ask the user to select a target keyword for diagnosis or confirm a separate reverse-ASIN discovery stage, then stop. |
| 1B. ASIN × keyword diagnosis | ASIN + keyword + relevant observation range | Use the timeline, market, SERP, and aggregate evidence needed to show what changed and resolve the narrowest reported uncertainty; present evidence, analysis, explanation status, and the stage conclusion. | If the stage conclusion identifies seller-funnel evidence as the exact next evidence for a named unresolved question, render a separate mandatory SQP next-input request through `sqp-field-semantics.md`, then stop. Otherwise end the completed diagnosis after usage reporting. |
| 2. Seller-funnel calibration | Supplied SQP artifact | Analyze the current funnel evidence with retained Stage 1 constraints and present the seller-funnel conclusion. | Request Ads separately only when economics or execution remains unresolved. |
| 3. Ads-economics calibration | Later Ads artifact, when required | Analyze the supplied search-term report and update only supported economics/execution conclusions. | Stop unless one named decision remains unresolved. |

Apply the shared `Interactive Stage Gate` and `Stage Handoff Closure Gate` from `execution-guide.md`; each numbered stage is a separate user-decision turn. Multiple timeline/market/SERP calls needed to resolve the same Stage 1B diagnosis are within one stage, but SQP and Ads are later stages and must never be interpreted in the same turn as the preceding stage.

Stage 1A ends only with a target-keyword selection request or confirmation to enter a separate reverse-ASIN discovery stage; do not request SQP there. At later seller-data boundaries, load `sqp-field-semantics.md` and follow its acquisition, sequencing, sufficiency, and field-interpretation rules instead of redefining them here.

For Stage 1B, conditional acquisition is allowed only until the explanation status is written. Once that conclusion names SQP as the exact missing evidence, the next-input request is mandatory and must use a direct acquisition-and-upload instruction. Do not phrase it as `if wanted` or `if needed`, or append it as an optional suggestion.

## Report shape

After the active diagnostic stage has completed its required retrieval under the shared execution guide, use localized sections in this order: Data Notes, observed change/evidence, analysis or explanation status, stage conclusion, one required next input when the conclusion carries a named unresolved question forward, and API usage. Omit the next-input section only when the diagnosis is complete at the current evidence level. Do not include a generic list of possible causes, repeat a prior-stage report, or append later-stage analysis to the same response.
