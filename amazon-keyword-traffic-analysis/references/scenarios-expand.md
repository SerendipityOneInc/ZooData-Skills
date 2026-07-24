# Keyword Expansion

> Load this file for keyword expansion and coarse filtering.

## Contents

- [Inputs and route](#inputs-and-route)
- [Shared evidence rules](#shared-evidence-rules)
- [Route A: standalone expansion](#route-a-standalone-expansion)
- [Route B: staged ASIN candidate validation](#route-b-staged-asin-candidate-validation)
- [Output templates](#output-templates)

## Inputs and route

- required: seed keyword
- optional: marketplace, snapshot date, candidate count/page size
- optional staged inputs: ASIN observation evidence and/or seller ABA-SQP
- date rule: if an endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

Choose the route before calling endpoints:

- **Route A — standalone expansion:** the user provides a seed keyword but no ASIN observation evidence. Produce a market-level candidate pool. Do not claim product fit/current-ASIN performance and do not request SQP; request the ASIN as the next evidence when product-specific prioritization is wanted.
- **Route B — staged ASIN candidate validation:** ASIN observation evidence already exists in the conversation or request. Combine product fit/current ASIN posture with candidate market profiles. After every recommended candidate is validated, request SQP when final product-specific priority is in scope.

If the user asks only for raw related terms, stop after candidate recall and do not force either scoring route.

## Shared evidence rules

- Use data-layer `keywords/extends` because candidate rows are the deliverable. Try `queryType=fuzzy` after an empty phrase result before concluding low expandability.
- Use batch `keywords/market-profile` first for candidate market judgment when exposed. Use `detail` only when the metric is unavailable or a named inference needs raw fields omitted by its contract.
- Prefer `trend-profile` and `search-results-metrics` when live. Descend only for unavailable metrics or contract-omitted points/rows required for a named inference.
- Never use `extends` rows to fabricate `rootDemand`; only a verified `root-aggregate` root-universe response can support that claim.
- Treat market-profile unsupported dimensions as unavailable; do not call same-source detail merely to repair missing metric inputs.
- Publish a candidate tier only when its market-profile item is `available` and the required dimensions have complete `levelEvidence`. Treat `not_found` as unvalidated coverage, not low demand or an avoid signal.
- Keep `marketCharacteristics.volatility` separate from `annualSeasonality`; do not invent peak periods when the returned list is empty. A batch HTTP 500 does not authorize automatic per-candidate fan-out.
- Deduplicate candidates case-insensitively, batch compatible subjects up to 20, preserve input order/status, and retain empty/error items.
- Candidate labels are validation priority, not final expansion, match-type, bid, budget, launch, pause, or negative-keyword decisions.
- Do not output `Auto / Broad / Phrase / Exact` recommendations from market evidence alone. Match type is a campaign-setting hypothesis that requires the Evidence-to-Action Protocol and relevant seller/Ads evidence.

## Route A: standalone expansion

### Evidence level and scoring

This route stays at **market evidence**. A transparent market-screen score may use:

| Dimension | Suggested weight | Evidence |
|-----------|-----------------:|----------|
| Seed relation / intent | 35 | `relevanceScore`, lexical/semantic seed-intent fit |
| Demand | 30 | covered `marketProfile.demandScale`; raw demand fields only when explicitly required and justified |
| Competition/accessibility | 20 | covered market-profile dimensions; targeted SERP evidence when required |
| Stability | 15 | trend metric or transparent 4–8 week raw-series calculation when justified |

Call the result a **market-screen shortlist**, not an ASIN candidate-validation tier. It answers which terms merit product-specific validation, not which terms the seller should launch or fund.

Suggested market-screen labels:

- `Advance to ASIN validation`
- `Selective ASIN validation`
- `Observe`
- `No current support`

### Next step

Request the user's ASIN only when they want product-specific prioritization. Do not request ABA-SQP at this route because ASIN observation has not occurred.

## Route B: staged ASIN candidate validation

### Evidence level and scoring

This route requires **subject observation evidence**. Rank candidates from:

```text
product fit × current ASIN performance/posture × keyword market profile
```

Every candidate published in a recommendation tier must have completed batch market-profile validation. Title relevance or an occasional observed position is insufficient by itself.

Use these provisional labels:

- `Priority test`
- `Selective test`
- `Harvest`
- `Observe only`
- `Avoid`

The labels select terms for seller-funnel validation. They do not authorize match type, bids, budget, scaling, pausing, or negatives.

### Next step

After candidate validation, request seller-side ABA-SQP using `execution-guide.md § Seller Data Contract` if the user wants final product-specific priority. Request Ads search-term performance only for profitability, match-type execution, exact bids, or final budget allocation.

## Output templates

### Route A — standalone expansion

```markdown
# Keyword Expansion Report — [Seed Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

## [Localized Data Notes title]
[State that this is a market-evidence candidate pool. It has not used an ASIN or seller funnel and cannot decide product-specific priority, match type, bids, or budget.]

## Market-screen Conclusion
[💡 State what kind of candidate pool was found and what merits ASIN validation.]

| Keyword | Demand | Competition | Seed/intent fit | Market-screen label | Evidence note |
|---------|--------|-------------|-----------------|---------------------|---------------|

## Next Step
[If product-specific prioritization is wanted, request the user's ASIN. Otherwise omit.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Credits remaining: [latest returned value or `not returned`]
```

### Route B — staged ASIN candidate validation

```markdown
# ASIN Candidate Validation — [ASIN] × [Seed Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

## [Localized Data Notes title]
[State that these are subject-observation-level tiers combining product fit/current ASIN evidence with batch market profiles; seller funnel has not calibrated final execution priority.]

## Candidate-validation Preliminary Conclusion
[💡 State which terms deserve seller-funnel validation; do not present a final expansion or budget list.]

| Keyword | Product fit | ASIN posture | Market profile | Validation tier | Evidence note |
|---------|-------------|--------------|----------------|-----------------|---------------|

## Next Step
[Request ABA-SQP using `execution-guide.md § Seller Data Contract` when final product-specific priority is requested. Request Ads fields only for profitability or execution settings.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Credits remaining: [latest returned value or `not returned`]
```

For either route, include every live call in usage accounting and preserve `not returned` metadata rather than estimating it.
