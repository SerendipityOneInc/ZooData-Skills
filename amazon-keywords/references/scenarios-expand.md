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

### Workflow

1. Pull expansion candidates from `keywords/extends`
2. If result count is low, retry with `queryType=fuzzy`
3. Enrich shortlisted terms with `keywords/detail`
4. Validate demand direction with `keywords/trend`
5. Sample SERP structure for top candidates with `keywords/search-results`
6. Score and tier candidates

### Endpoint Plan

| Step | Endpoint | Purpose |
|------|----------|---------|
| 1 | `keywords/extends` | Get related terms and `relevanceScore` |
| 2 | `keywords/detail` | Add weekly demand, ABA, ad density, market characteristics |
| 3 | `keywords/trend` | Confirm whether demand is stable / rising / fading |
| 4 | `keywords/search-results` | Check ad crowding, who dominates, and what product types/brands/prices actually occupy page 1 |

### Candidate Scoring

Suggested 100-point model:

| Dimension | Weight | Main fields |
|-----------|--------|-------------|
| Relevance | 35 | `relevanceScore`, seed-intent fit |
| Demand | 30 | `estimateSearchCountWeekly`, `abaRank` |
| Competition | 20 | `adCount`, `adCampaignCount`, SERP ad density |
| Stability | 15 | 4-8 week trend consistency |

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

> Data is based on APIClaw keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

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

## Data Provenance
| Data | Endpoint | Key Params | Notes |
|------|----------|------------|-------|

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|

Credits remaining: N
```
