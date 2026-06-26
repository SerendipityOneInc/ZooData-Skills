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

### Workflow

1. Pull `keywords/product-traffic-terms` to get traffic-driving terms
2. Pull `keywords/competitor-product-keywords` to see where the ASIN appears as a competitor
3. Merge and deduplicate by keyword
4. Enrich top terms with `keywords/detail`
5. Spot-check SERP with `keywords/search-results`
6. Split terms into defense / expansion / observation buckets

### Tool Availability Gate

- Before running the workflow, confirm that both `keywords/product-traffic-terms` and `keywords/competitor-product-keywords` are exposed in the live tool surface
- If one or both are unavailable, stop the full reverse-ASIN chain and state the limitation explicitly
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
  high traffic share or good position on strategically important terms
- `Expand`
  decent relevance and volume, but position is still improvable
- `Observe`
  signals are promising but weak or unstable
- `Avoid`
  low share, low fit, or crowded with poor position

### Output Template

```markdown
# Reverse ASIN Keyword Report — [ASIN]

> Data is based on APIClaw keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

## Top Traffic Terms
| Keyword | Traffic Share | Avg Position | Search Count | Bucket |
|---------|---------------|--------------|--------------|--------|

## Defense Terms
[Which terms should be protected]

## Expansion Terms
[Which terms deserve more spend or SEO support]

## Risks
[Crowding, weak coverage, unstable observations]

## Data Provenance
| Data | Endpoint | Key Params | Notes |
|------|----------|------------|-------|

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|

Credits remaining: N
```
