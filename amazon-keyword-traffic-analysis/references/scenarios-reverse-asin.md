# Reverse ASIN Keyword Analysis

> Load this file for reverse ASIN keyword analysis.

---

## 3. Reverse ASIN Keyword Analysis

> Trigger: "reverse ASIN" / "which keywords drive traffic to this ASIN" / "traffic-source keywords for this ASIN"

### Inputs

- required: ASIN
- optional: marketplace
- optional: top-N focus for returned keywords
- optional: spot-check keywords to inspect with `keywords/search-results`
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Minimum evidence: one ASIN traffic-list endpoint, either `keywords/product-traffic-terms` or `keywords/competitor-product-keywords`
- These two endpoints currently provide equivalent functionality and the same live item shape for traffic-structure analysis; choose one available endpoint instead of requiring both
- Prefer `keywords/product-traffic-terms` for the target ASIN's traffic-source list; use `keywords/competitor-product-keywords` as an equivalent fallback or when the workflow is competitor/overlap framed
- If neither ASIN traffic-list endpoint is available, do not output reverse-ASIN traffic-source conclusions
- `keywords/detail` and `keywords/search-results` may enrich prioritization and SERP context, but they cannot replace ASIN keyword evidence
- `products/search` is supplementary only when the user explicitly asks for broader market context beyond observed keyword SERP behavior
- Term bucketing may use any efficient call pattern, as long as the traffic-source map is grounded in one of the ASIN traffic-list endpoints
- Reverse-ASIN traffic terms show visibility and estimated traffic contribution, not definitive commercial value or conversion quality
- If the user did not provide Amazon backend ABA-SQP search conversion data, keep traffic-source conclusions, buckets, and spend/value recommendations directional and place the seller-side SQP enrichment request only in `Data Notes` and `Data Notes Reminder`
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
  high traffic share or good position on strategically important terms; if ABA-SQP is missing, keep budget impact directional and reserve the seller-side SQP enrichment request for `Data Notes` and `Data Notes Reminder`
- `Expand`
  decent relevance and volume, but position is still improvable; treat as a testing priority without ABA-SQP and reserve the seller-side SQP enrichment request for `Data Notes` and `Data Notes Reminder`
- `Observe`
  signals are promising but weak or unstable
- `Avoid`
  low share, low fit, or crowded with poor position

### Output Template

```markdown
# Reverse ASIN Keyword Report — [ASIN]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> Traffic-source signals estimate visibility and exposure contribution, not final keyword value. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep traffic-source conclusions, buckets, and recommendations directional and place the seller-side SQP enrichment request only in Data Notes and Data Notes Reminder. If seller-side ABA-SQP data is included, integrate it directly and omit the enrichment request.

## [Localized Data Notes title]
[Use short, natural prose, not status labels, field lists, or deficit-framed wording. If the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, first state that evidence basis; then say that if the user can provide seller-side ABA-SQP conversion funnel data, the analysis can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance; then include Seller Central path `Brand Analytics → Search Analytics → Search Query Performance → Brand View`, recommend sorting by `Search Funnel - Impressions → Brand Count`, and ask for a screenshot or CSV. If seller-private ABA-SQP data is present, name the SQP fields used and omit the seller-side SQP enrichment request.]

## Top Traffic Terms
| Keyword | Traffic Share | Avg Position | Search Count | Bucket |
|---------|---------------|--------------|--------------|--------|

## Defense Terms
[Which terms should be protected]

## Expansion Terms
[Which terms deserve testing, SQP validation, or SEO support]

## ORG First-3-Page Changes
[Fill from `keywords/product-traffic-terms-overview` when available. If unavailable, omit this section.]

**Newly entered:** [keywords from `first3PagesNewOrganicKeywords` with pageIndex / pagePosition, or "no data"]

**Dropped out:** [keywords from `first3PagesLostOrganicKeywords` with pageIndex / pagePosition, or "no data"]

## Risks
[Crowding, weak coverage, unstable observations]

## [Localized Data Notes Reminder title]
[Repeat the opening Data Notes body here. For Chinese output, the opening title must render from `\u6570\u636e\u8bf4\u660e`; the end reminder title must render from `\u6570\u636e\u8bf4\u660e\uff08\u518d\u6b21\u63d0\u9192\uff09`.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
