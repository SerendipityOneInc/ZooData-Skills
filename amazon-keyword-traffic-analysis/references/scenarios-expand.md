# Keyword Expansion

> Load this file for keyword expansion and coarse filtering.

---

## 1. Keyword Expansion

> Trigger: "keyword expansion" / "find ad keyword ideas" / "expand from this seed keyword" / "coarse-filter keyword candidates"

### Inputs

- required: seed keyword
- optional: marketplace
- optional: snapshot date for weekly endpoints
- optional: candidate count or page-size preference
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Task Constraints

- Minimum evidence: `keywords/extends` + `keywords/detail`
- If `keywords/extends` returns empty, you may retry with `queryType=fuzzy` before concluding the seed has low expandability
- If `keywords/trend` is unavailable, keep demand interpretation snapshot-led and avoid strong growth or decline claims
- If `keywords/search-results` is unavailable, avoid strong statements about page-1 crowding, brand concentration, or intent shape
- `products/search` is supplementary only when the user explicitly wants broader market context beyond the observed keyword SERP
- Candidate scoring may be done with any efficient call pattern, as long as the evidence gate is respected
- Candidate scores are directional opportunity scores based on estimated search/exposure/visibility signals, not definitive keyword-value scores
- If the user did not provide Amazon backend ABA-SQP search conversion data, keep candidate conclusions directional and place the seller-side SQP enrichment request only in `Data Notes` and `Data Notes Reminder`
- If the user provided ABA-SQP data, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate to refine candidate priority and do not add the seller-side SQP enrichment request

### Evidence Plan

| Evidence Type | Endpoint | Purpose |
|---------------|----------|---------|
| Expansion candidates | `keywords/extends` | Get related terms and `relevanceScore` |
| Demand snapshot | `keywords/detail` | Add weekly demand, ABA, ad density, market characteristics |
| Demand direction | `keywords/trend` | Confirm whether demand is stable / rising / fading |
| SERP crowding and intent | `keywords/search-results` | Check ad crowding, who dominates, and what product types/brands/prices actually occupy page 1 |

### Candidate Scoring

Suggested 100-point opportunity model:

| Dimension | Weight | Main fields |
|-----------|--------|-------------|
| Relevance | 35 | `relevanceScore`, seed-intent fit |
| Demand | 30 | `estimateSearchCountWeekly`, `abaRank` |
| Competition | 20 | `adCount`, `adCampaignCount`, SERP ad density |
| Stability | 15 | 4-8 week trend consistency |

This model ranks testing priority. It does not prove conversion value, profitability, or final budget allocation without ABA-SQP or other first-party conversion data; when ABA-SQP is missing, keep traffic recommendation groups directional and reserve the seller-side SQP enrichment request for `Data Notes` and `Data Notes Reminder`.

### Coarse-Filter Output

For each keyword, output:

| Field | Meaning |
|-------|---------|
| Keyword | candidate term |
| Demand Tier | High / Mid / Low |
| Competition Tier | High / Mid / Low |
| Relevance Tier | Strong / Medium / Weak |
| Suggested Usage | Auto / Broad / Phrase / Exact / SEO Observe |
| Recommendation | `Priority test` / `Selective test` / `Observe only` / `Exclude` |

### Suggested Interpretation

- High demand + high relevance + manageable ad crowding → `Priority test`
- High demand + very high ad crowding → `Selective test`
- High relevance but low demand → `Observe only` or low-budget exact test
- Weak relevance regardless of traffic → `Exclude`

### Output Template

```markdown
# Keyword Expansion Report — [Seed Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> Scores are directional opportunity signals from estimated search/exposure data. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep traffic-related candidate conclusions directional and place the seller-side SQP enrichment request only in Data Notes and Data Notes Reminder. If seller-side ABA-SQP data is included, integrate it directly and omit the enrichment request.

## [Localized Data Notes title]
[Use short, natural prose, not status labels, field lists, or deficit-framed wording. If the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, first state that evidence basis; then say that if the user can provide seller-side ABA-SQP conversion funnel data, the analysis can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance; then include Seller Central path `Brand Analytics → Search Analytics → Search Query Performance → Brand View`, recommend sorting by `Search Funnel - Impressions → Brand Count`, and ask for a screenshot or CSV. If seller-private ABA-SQP data is present, name the SQP fields used and omit the seller-side SQP enrichment request.]

## Summary
[🔍 What kind of keyword pool this seed generated]

## Priority Candidates
| Keyword | Demand | Competition | Relevance | Suggested Usage | Recommendation |
|---------|--------|-------------|-----------|-----------------|----------------|

## Watchlist
| Keyword | Key reason to watch | Risk |
|---------|---------------------|------|

## Excluded Terms
| Keyword | Why excluded |
|---------|--------------|

## [Localized Data Notes Reminder title]
[Repeat the opening Data Notes body here. For Chinese output, the opening title must render from `\u6570\u636e\u8bf4\u660e`; the end reminder title must render from `\u6570\u636e\u8bf4\u660e\uff08\u518d\u6b21\u63d0\u9192\uff09`.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
