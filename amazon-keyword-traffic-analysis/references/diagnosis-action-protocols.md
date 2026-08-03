# Diagnosis and Action Protocols — Amazon Keyword Intelligence

This file owns detailed causal-diagnosis and evidence-to-action procedures. It operates inside an active scenario stage and returns its result to the Gate system in `execution-guide.md`; it does not select stages, define handoff lists, or raise conclusion authority.

## Contents

- [Evidence-Seeking Diagnosis Protocol](#evidence-seeking-diagnosis-protocol)
- [Evidence-to-Action Protocol](#evidence-to-action-protocol)
- [Action authorization](#action-authorization)
- [Numeric advertising decision protocol](#numeric-advertising-decision-protocol)
- [General examples](#general-examples)
- [Asset-fidelity rule](#asset-fidelity-rule)

## Evidence-Seeking Diagnosis Protocol

Apply this protocol when the active stage asks what is wrong, why a metric moved, or what explains a funnel pattern.

1. Record the observed fact without causal language.
2. Identify the narrowest problem domain supported by that fact.
3. Convert it into an unresolved question.
4. Identify the smallest evidence that can discriminate material explanations.
5. Acquire that evidence when it is authorized, available, and inside the active stage; do not finalize while a usable discriminating source remains unchecked.
6. Form an explanation only from obtained evidence while retaining material alternatives not ruled out.
7. Return each branch to the Diagnostic Closure Gate before reporting it.
8. Apply the Evidence-to-Action Protocol before proposing a test, change, scale, or stop decision.

Use only acquisition channels whitelisted by `SKILL.md` and `reference.md`. Prefer matching structured evidence; use authorized page acquisition only for a named inference absent from structured responses. A compatible-cause inventory is an internal search map, not a diagnosis.

If discriminating evidence is unavailable, return the observed problem, exact unresolved question, and decision boundary to the guide. Do not create a generic cause list or handoff directly from this module.

## Evidence-to-Action Protocol

Apply this after scoping the conclusion and before writing a recommendation. Confidence describes evidence strength; it does not authorize a stronger action.

For every proposed action, record:

1. **Target** — exact asset, field, keyword, campaign setting, offer, or decision.
2. **Direct observation** — whether the target was inspected at sufficient fidelity.
3. **Defect signal** — the concrete issue observed on that target.
4. **Alternatives** — material explanations that must be distinguished.
5. **Validation** — comparison, experiment, series, or first-party measurement that distinguishes the target.
6. **Impact** — reversibility, cost, and downside if wrong.

## Action authorization

| Level | Minimum authorization |
|---|---|
| `Inspect` | A broad signal identifies a relevant problem domain. |
| `Diagnose` | Multiple bounded hypotheses are supported and alternatives remain explicit. |
| `Test` | The target was directly observed, a specific defect hypothesis exists, and the test is reversible with predefined criteria. |
| `Change` | Direct target evidence plus validation distinguishes the target from material alternatives. |
| `Scale` / `Stop` | Seller-real outcome evidence and thresholds justify the financial consequence. |

If a required condition is absent, downgrade the action itself. Do not preserve a stronger action merely by softening its wording.

## Numeric advertising decision protocol

A numeric bid, bid range, bid-change percentage, budget amount, or budget-allocation percentage is a `Change` action at minimum. Apply this protocol only after the General Conclusion Authority Gate has established that the user's latest request explicitly asks for that exact advertising decision. Never introduce a numeric advertising action as an unsolicited optimization.

Before producing any numeric advertising recommendation, verify all of the following:

1. **Exact controlled target** — marketplace/account profile, ad product, campaign, ad group, targeting or search-term relationship, match type, and the specific bid or budget control to be changed are resolved.
2. **Compatible performance evidence** — the named target has same-scope Ads impressions, clicks, spend, attributed orders, attributed sales, and the relevant returned or transparently derived CPC, CVR, ACOS, or ROAS for a disclosed period and attribution scope.
3. **Current control state** — the current bid or budget, bidding strategy, placement adjustments, and any other setting that materially changes the effective bid or spend ceiling are known.
4. **Seller objective and economics** — the seller supplied the optimization objective and guardrail. Profitability or break-even reasoning also requires contribution economics covering the material product costs and fees, or a seller-provided break-even/target ACOS or ROAS explicitly grounded in those economics.
5. **Observation sufficiency** — the available clicks, orders, spend, period coverage, and stability are adequate for the requested decision. Do not invent a universal sample threshold; identify sparse, zero-denominator, newly launched, promotion-distorted, stockout-affected, or otherwise atypical evidence as insufficient unless the user explicitly asks for a bounded experiment and accepts its risk.
6. **Bounded validation** — define a reversible change, downside limit, evaluation period, and success/stop criteria appropriate to the available evidence.

If any condition is missing, do not output a bid, budget, range, default amount, formula-derived amount, or percentage change. Return the exact missing evidence to the guide-owned handoff rule. Directional observations such as high ACOS, low CVR, or limited spend do not fill the missing fields and do not authorize a number.

Ads performance can support advertising-efficiency observations within its returned attribution scope. It cannot establish product profitability without the seller economics above, and a target ACOS or ROAS supplied without its intended business meaning must be treated as a seller guardrail rather than independently verified profitability.

## General examples

| Available evidence | Not authorized | Authorized direction |
|---|---|---|
| Click/cart-add evidence but weak purchases | Rebuild named images or list generic causes | Locate the unresolved post-click/purchase question and seek discriminating evidence. |
| Search-result main-image thumbnail only | Rebuild the full image set | Inspect only thumbnail-level recognition; require full-fidelity assets for asset-level conclusions. |
| High ACOS alone | Lower bids by a fixed percentage | Diagnose target-level CPC, conversion, placement, and attribution before defining a reversible test. |
| Organic-rank decline | Pause the keyword or list every compatible cause | Retrieve the smallest aligned demand, placement, subject, and market evidence needed by the named question. |
| Review deterioration | Redesign the product | Validate complaint frequency, recency, variant scope, and product causality. |

Do not open unsupported branches merely to demonstrate caution. If causal diagnosis is unnecessary for the requested decision, omit it. If it is necessary, pursue or request directly discriminating evidence through the guide-owned stage handoff.

## Asset-fidelity rule

State the representation actually observed when an asset enters diagnosis: full-resolution asset, detail-page rendering, mobile rendering, search-result thumbnail, URL/change event, or no visual observation. An asset URL or change event proves availability/change, not content defect or causality.
