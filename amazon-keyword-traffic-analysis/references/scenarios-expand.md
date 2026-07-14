# Keyword Expansion

> Load this file for keyword expansion and coarse filtering.

---

## 1. Keyword Expansion

> Trigger: "keyword expansion" / "find ad keyword ideas" / "expand from this seed keyword" / "coarse-filter keyword candidates"

### Inputs

- required: seed keyword
- optional: marketplace
- optional: snapshot date for `detail`/`trend`; `extends` itself uses the latest weekly snapshot and does not require a date
- optional: candidate count or page-size preference
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Candidate recall requires data-layer `keywords/extends` because candidate rows are the deliverable. Candidate market judgment should use metric-layer `keywords/market-profile` first when exposed; use `keywords/detail` only if the metric endpoint is unavailable or a named inference needs raw snapshot fields omitted by the metric.
- If `keywords/extends` returns empty, you may retry with `queryType=fuzzy` before concluding the seed has low expandability
- Prefer `keywords/trend-metrics` and `keywords/search-results-metrics` when live. Descend to raw trend/SERP only when the metric endpoint is unavailable or its contract omits the points/rows required for a named inference.
- Batch shortlisted candidates through `keywords/market-profile` first when exposed. Do not also batch them through `detail` by default, and do not use incomplete profile calculation coverage alone as a reason to call `detail`.
- Never use `keywords/extends` rows to fabricate `rootDemand`; only `keywords/root-aggregate` with verified `coverageType=root_universe` can support root-universe demand claims
- `products/search` is supplementary only when the user explicitly wants broader market context beyond the observed keyword SERP
- Candidate scoring may be done with any efficient call pattern, as long as the evidence gate is respected
- Candidate scores are directional opportunity scores based on estimated search/exposure/visibility signals, not definitive keyword-value scores
- Keep candidate conclusions directional without seller data. In a staged ASIN workflow, request ABA-SQP only after every recommended candidate has completed batch market-profile validation.
- Treat all candidate tiers as validation priority, not final expansion or spend priority. Do not attach fixed budgets, bid actions, or unconditional launch/stop decisions before seller-real calibration.
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to refine candidate priority and do not add the seller-side SQP enrichment request

### Evidence Plan

| Evidence Type | Endpoint | Purpose |
|---------------|----------|---------|
| Expansion candidates | `keywords/extends` | Get related terms and `relevanceScore` |
| Market structure and demand tier | Metric-layer `keywords/market-profile` batch when exposed | Primary source for covered demand scale, concentration, ad activity, entry difficulty, saturation, brand structure, and organic benchmark |
| Raw snapshot fields | `keywords/detail` batch, conditional | Use only when the metric endpoint is unavailable or a named inference requires fields omitted by `market-profile` |
| Demand direction | `keywords/trend-metrics` when live | Primary source for trend/lifecycle judgment; use raw `trend` only for unavailable metric or required weekly points |
| SERP structure and intent | `keywords/search-results-metrics` when live | Primary aggregate source; use raw `search-results` only for unavailable metric or required product/placement rows |

### Candidate Scoring

Suggested 100-point opportunity model:

| Dimension | Weight | Main fields |
|-----------|--------|-------------|
| Relevance | 35 | `relevanceScore`, seed-intent fit |
| Demand | 30 | `marketProfile.demandScale`; use raw `snapshotData.estimateSearchCount` / `abaRank` only when the scoring inference explicitly requires those omitted values |
| Competition | 20 | Covered `marketProfile` competition dimensions when available; otherwise `adCount`, `adCampaignCount`, SERP ad density |
| Stability | 15 | 4-8 week trend consistency |

This model ranks testing priority. It does not prove conversion value, profitability, or final budget allocation without ABA-SQP or other first-party conversion data.

### Coarse-Filter Output

For each keyword, output:

| Field | Meaning |
|-------|---------|
| Keyword | candidate term |
| Demand Tier | High / Mid / Low |
| Competition Tier | High / Mid / Low |
| Relevance Tier | Strong / Medium / Weak |
| Suggested Usage | Auto / Broad / Phrase / Exact / SEO Observe |
| Recommendation | `Priority test` / `Selective test` / `Harvest` / `Observe only` / `Avoid` |

### Suggested Interpretation

- High demand + high relevance + manageable ad crowding → `Priority test`
- High demand + very high ad crowding → `Selective test`
- High relevance but low demand and a credible low-cost capture path → `Harvest`
- Weak relevance regardless of traffic → `Avoid`

### Output Template

```markdown
# Keyword Expansion Report — [Seed Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> Scores are directional opportunity signals from product fit, current ASIN observations, and batch market profiles. Seller funnel data is required before final budget allocation.

## [Localized Data Notes title]
[State that these are ASIN-observation-level preliminary candidate tiers: product fit and current ASIN performance have been combined with batch keyword market profiles, but seller funnel data has not yet calibrated final budget priority.]

## Candidate-validation Preliminary Conclusion
[🔍 What kind of keyword pool this seed generated]

[State explicitly that the tiers below determine which terms deserve seller-funnel validation; they are not the final expansion or budget list.]

## Priority Candidates
| Keyword | Demand | Competition | Relevance | Suggested Usage | Recommendation |
|---------|--------|-------------|-----------|-----------------|----------------|

## Watchlist
| Keyword | Key reason to watch | Risk |
|---------|---------------------|------|

## Avoid Terms
| Keyword | Why avoid |
|---------|-----------|

## Next Step
[Request seller-side ABA-SQP now. Give the Brand View path, sorting instruction, preferred funnel fields, and screenshot/CSV option. Request Ads search-term performance only if profitability or final budget allocation is in scope.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
