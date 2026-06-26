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

### Workflow

1. Pull weekly snapshot from `keywords/detail`
2. Pull 8-12 weeks from `keywords/trend`
3. Pull current SERP from `keywords/search-results`
4. Use `keywords/search-results` itself to summarize what products dominate page 1: product type, brand mix, price band, and ad vs organic composition
5. Assess demand, ad density, brand concentration, and organic room
6. Output bid-worthiness and suitable usage scene

### SERP Source Rule

- When the user asks what products are showing on the first page, answer from `keywords/search-results` first
- Do not treat `keywords/search-results` as "only a SERP structure endpoint"; it already includes listing-level product fields
- Do not append `products/search` by default for this question
- Use `products/search` only if the user also asks for market-wide best sellers,销量分布, price-band distribution, or a broader market view that goes beyond the observed keyword SERP

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
  demand is real, trend is not deteriorating, and the SERP is still contestable
- Worth selective testing:
  demand is good but competition is heavy, or intent fit is narrower
- Not worth prioritizing:
  demand is weak, trend is poor, or SERP mismatch is strong

### Output Template

```markdown
# Keyword Analysis — [Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

## Verdict
[Priority test / Selective test / Observe only / Exclude]

## Findings
- Demand: [📊 / 🔍]
- Trend: [📊 / 🔍]
- Competition: [📊 / 🔍]
- SERP structure: [📊 / 🔍]
- Recommended usage scene: [💡]

## Action
[💡 Budget or placement suggestion]

## Data Provenance
| Data | Endpoint | Key Params | Notes |
|------|----------|------------|-------|

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|

Credits remaining: N
```
