# Single Keyword Analysis

> Load this file for single-keyword evaluation.

---

## 2. Single Keyword Analysis

> Trigger: "keyword deep dive" / "is this keyword worth targeting" / "single keyword analysis"

### Inputs

- required: target keyword
- optional: marketplace
- optional: weekly snapshot date
- optional: trend lookback window, default 8-12 weeks when available
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Minimum evidence: `keywords/detail` + `keywords/search-results`
- If `keywords/trend` is unavailable, do not make strong demand-direction claims
- Page-1 product mix, brand mix, price band, and ad-vs-organic composition must come primarily from `keywords/search-results`
- `products/search` is allowed only as broader market context when the user explicitly asks for that broader view
- The analysis may use any efficient call pattern, but the final verdict must stay within the available evidence scope
- ZooData evidence is estimated search/exposure/visibility data, not the user's ASIN-specific ABA Search Query Performance funnel; without user-provided SQP data, the verdict is a directional test-priority judgment, not a definitive keyword-value judgment
- If the user did not provide Amazon backend ABA-SQP search conversion data, keep traffic-related verdicts, findings, and budget/placement recommendations directional and place the seller-side SQP enrichment request only in `Data Notes` and `Data Notes Reminder`
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to refine the verdict and do not add the seller-side SQP enrichment request

### SERP Source Rule

- When the user asks what products are showing on the first page, answer from `keywords/search-results` first
- Do not treat `keywords/search-results` as "only a SERP structure endpoint"; it already includes listing-level product fields
- Do not append `products/search` by default for this question
- Use `products/search` only if the user also asks for market-wide best sellers, sales distribution, price-band distribution, or a broader market view that goes beyond the observed keyword SERP

### Analysis Dimensions

| Dimension | Questions |
|-----------|-----------|
| Demand | Is the search volume meaningful enough? |
| Trend | Is volume stable, rising, or weakening? |
| Competition | Is the keyword ad-heavy and crowded? |
| SERP intent | Do current results match the user's product intent? |
| Organic room | Is there room outside the entrenched leaders? |
| Launch fit | Better for discovery, exact defense, or long-tail harvest? |

### Decision Logic

- Worth targeting now:
  demand is real, trend is not deteriorating, and the SERP is still contestable; without ABA-SQP data, phrase this as "priority test" rather than proven value and reserve the seller-side SQP enrichment request for `Data Notes` and `Data Notes Reminder`
- Worth selective testing:
  demand is good but competition is heavy, or intent fit is narrower
- Not worth prioritizing:
  demand is weak, trend is poor, or SERP mismatch is strong
- Do not call a keyword definitively profitable, high-converting, or fully validated unless the user provides SQP or equivalent first-party conversion data

### Output Template

```markdown
# Keyword Analysis — [Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> ZooData estimates exposure/search/visibility. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep traffic-related conclusions and recommendations directional and place the seller-side SQP enrichment request only in Data Notes and Data Notes Reminder. If seller-side ABA-SQP data is included, integrate it directly and omit the enrichment request.

## [Localized Data Notes title]
[Use short, natural prose, not status labels, field lists, or deficit-framed wording. If the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, first state that evidence basis; then say that if the user can provide seller-side ABA-SQP conversion funnel data, the analysis can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance; then include Seller Central path `Brand Analytics → Search Analytics → Search Query Performance → Brand View`, recommend sorting by `Search Funnel - Impressions → Brand Count`, and ask for a screenshot or CSV. If seller-private ABA-SQP data is present, name the SQP fields used and omit the seller-side SQP enrichment request.]

## Verdict
[Priority test / Selective test / Observe only / Exclude — directional unless SQP data is provided]

## Findings
- Demand: [📊 / 🔍]
- Trend: [📊 / 🔍]
- Competition: [📊 / 🔍]
- SERP structure: [📊 / 🔍]
- Recommended usage scene: [💡]

## Action
[💡 Budget or placement suggestion]

## [Localized Data Notes Reminder title]
[Repeat the opening Data Notes body here. For Chinese output, the opening title must render from `\u6570\u636e\u8bf4\u660e`; the end reminder title must render from `\u6570\u636e\u8bf4\u660e\uff08\u518d\u6b21\u63d0\u9192\uff09`.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
