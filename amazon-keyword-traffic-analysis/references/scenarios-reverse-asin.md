# Reverse ASIN Keyword Analysis

> Load this file for reverse ASIN keyword analysis.

## Contents

- [Inputs](#inputs)
- [Task Constraints](#task-constraints)
- [Tool Availability Gate](#tool-availability-gate)
- [Analysis Dimensions](#analysis-dimensions)
- [Decision Buckets](#decision-buckets)
- [Output Template](#output-template)

## 3. Reverse ASIN Keyword Analysis

> Trigger: "reverse ASIN" / "which keywords drive traffic to this ASIN" / "traffic-source keywords for this ASIN"

### Inputs

- required: ASIN
- optional: marketplace
- optional: top-N focus for returned keywords
- optional: spot-check keywords to inspect with `keywords/search-results`
- optional: target keyword carried forward from a market-screening step
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Minimum evidence: one ASIN traffic-list endpoint, either `keywords/product-traffic-terms` or `keywords/competitor-product-keywords`
- These two endpoints currently provide equivalent functionality and the same live item shape for traffic-structure analysis; choose one available endpoint instead of requiring both
- Prefer `keywords/product-traffic-terms` for the target ASIN's traffic-source list; use `keywords/competitor-product-keywords` as an equivalent fallback or when the workflow is competitor/overlap framed
- If neither ASIN traffic-list endpoint is available, do not output reverse-ASIN traffic-source conclusions
- `product-traffic-terms-overview` is aggregate evidence. Production currently returns a legacy flat object; calculate simple channel totals/shares/changes transparently and do not claim grouped `trafficStructure`, `aggregateChanges`, or `keywordConcentration` were returned.
- `keywords/product-traffic-term-changes` is the planned source for keyword losers/gainers and contribution. If it is unavailable, do not infer keyword-level change contribution from the current traffic list or flat overview.
- Use metric-layer `product-traffic-terms-overview` first when the request is aggregate movement/structure. Call one ASIN traffic-list data endpoint only when keyword rows are the requested deliverable; no current metric replaces that row list.
- Enrich selected traffic terms through metric-layer `keywords/market-profile` first and use `keywords/trend-profile` for trend judgments. Call `detail` or raw `trend` only when a named inference needs fields or weekly points omitted by the matching profile.
- Do not descend from `market-profile` merely because a dimension is unsupported/unavailable; same-source data is unlikely to restore the missing metric input.
- Enrichment requires `market-profile status=available` and complete evidence for the dimension used. `not_found` leaves that term unvalidated rather than proving weak demand. Keep volatility and annual-seasonality evidence separate, and do not fan out a batch HTTP 500 automatically.
- `keywords/detail` and `keywords/search-results` may enrich prioritization and SERP context, but they cannot replace ASIN keyword evidence
- `products/search` is supplementary only when the user explicitly asks for broader market context beyond observed keyword SERP behavior
- Term bucketing may use any efficient call pattern, as long as the traffic-source map is grounded in one of the ASIN traffic-list endpoints
- Reverse-ASIN traffic terms show visibility and estimated traffic contribution, not definitive commercial value or conversion quality
- When this follows a target-keyword market screen, diagnose the ASIN × target keyword first: semantic/product-form fit, price/rating/reviews/sales basis, organic and sponsored positions, target-term share of observed ASIN traffic, organic/ad exposure mix, recent changes, listing events, and distance from the market barrier.
- Classify the target term as `Defend`, `Expand`, `Observe`, or `Avoid`. Identify a constraint only when discriminating evidence supports it; otherwise state the unresolved question and the minimum next evidence. A visibility pattern alone must not be converted into a generic exposure, ad-dependence, organic-capture, relevance, or click/conversion cause list.
- Candidate terms may be formed from ASIN traffic terms, target-term extensions, attributes/scenes, user-provided SQP queries, and competitor terms. Do not publish them as recommendations until they have passed batch `keywords/market-profile` validation.
- Keep traffic-source conclusions and spend/value recommendations directional without seller data. Ask for ABA-SQP only after candidate-profile validation, not at the start of the ASIN diagnosis.
- Apply the General Conclusion Authority Gate: `Defend` / `Expand` / `Observe` / `Avoid` is an observed posture, not permission to change bids or budgets. Keep final focus, expansion, or pause decisions unresolved until seller calibration.
- Apply `execution-guide.md § Evidence-Seeking Diagnosis Protocol` before explaining a constraint, then apply `§ Evidence-to-Action Protocol` to every action. Traffic rows and posture labels alone do not authorize a cause claim, match type, bids, budgets, scaling, pausing, negatives, or uninspected listing changes.
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to refine each traffic-source bucket and do not add the seller-side SQP enrichment request

### Tool Availability Gate

- Before choosing the execution tool, read the relevant docs/help/schema for the candidate path
- Before running the workflow, confirm that at least one of `keywords/product-traffic-terms` or `keywords/competitor-product-keywords` is available through the selected path, either local CLI or live tool surface
- If both are unavailable, stop the full reverse-ASIN chain and state the limitation explicitly
- In that case, do not fabricate reverse-ASIN traffic-source conclusions from `keywords/detail` or `keywords/search-results` alone
- If the user still wants help, offer only a boundary-labeled substitute such as single-keyword SERP analysis for manually provided keywords

### SERP And Product-Library Rule

- When explaining what products/brands dominate a keyword tied to this ASIN, use `keywords/search-results` first because it reflects the observed keyword SERP
- Do not default to `products/search` for that question
- Use `products/search` only as an optional supplement when the user explicitly wants broader catalog winners, price bands, or market-wide best-selling variants around those keywords
- If `products/search` is used, explicitly label it as our product-database query result, not Amazon live search results

### Analysis Dimensions

| Dimension | What to inspect |
|-----------|-----------------|
| Traffic contribution | `trafficShare`, `estimateImpressionPoint` |
| Rank quality | `avgPosition`, `daysCoverageRate`, `observationCount` |
| Keyword size | `keywordEstimateSearchCount`, `keywordAbaRank` |
| Growth | `keywordEstimateSearchCountChangeRate` |
| Competition | SERP ad density and head-ASIN overlap |

### Decision Buckets

- `Defend`
  high traffic share or good position on strategically important terms; budget impact remains directional without seller data
- `Expand`
  decent relevance and volume, but position is still improvable; treat as a testing priority without ABA-SQP
- `Observe`
  signals are promising but weak or unstable
- `Avoid`
  low share, low fit, or crowded with poor position

### Output Template

```markdown
# Reverse ASIN Keyword Report — [ASIN]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> Traffic-source signals estimate visibility and exposure contribution, not final keyword value.

## [Localized Data Notes title]
[State that this is an ASIN-observation-level diagnosis. It can judge observed fit, visibility, and preliminary action class, but not measured seller conversion or final budget.]

## ASIN-observation Preliminary Conclusion
[State the current observed posture and explicitly list which final decisions remain unresolved.]

## Top Traffic Terms
| Keyword | Traffic Share | Avg Position | Search Count | Bucket |
|---------|---------------|--------------|--------------|--------|

## Defense Terms
[Which terms currently show a defend posture; do not prescribe protection actions without the required seller/Ads evidence.]

## Expansion Terms
[Which terms are expansion candidates for validation; show only the highest evidence-authorized `Inspect / Diagnose / Test` level and do not force a test when discriminating target evidence is absent.]

## ORG First-3-Page Changes
[Fill from `keywords/product-traffic-terms-overview` when available. If unavailable, omit this section.]

**Newly entered:** [keywords from `first3PagesNewOrganicKeywords` with pageIndex / pagePosition, or "no data"]

**Dropped out:** [keywords from `first3PagesLostOrganicKeywords` with pageIndex / pagePosition, or "no data"]

## Risks
[Crowding, weak coverage, unstable observations]

## Candidate Validation
[Show only candidates that completed batch market-profile validation. Use `Priority test` / `Selective test` / `Harvest` / `Observe only` / `Avoid`.]

## Next Step
[After candidate validation, request ABA-SQP using `execution-guide.md § Seller Data Contract`. Request Ads search-term fields only when profitability, match-type execution, exact bids, or final budget is requested.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
