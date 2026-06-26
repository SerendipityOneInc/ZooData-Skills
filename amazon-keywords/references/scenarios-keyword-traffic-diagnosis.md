# Keyword Traffic Diagnosis

> Load this file for keyword traffic anomaly diagnosis.

---

## 4. Keyword Traffic Diagnosis

> Trigger: "diagnose keyword traffic anomalies" / "why did this keyword move" / "analyze this ASIN's keyword traffic drop"

### Inputs

- required: ASIN + keyword
- recommended: at least 2 observation dates

### Workflow

1. Pull `keywords/search-results` for the target keyword at two or more timestamps
2. Track target ASIN position, exploreType mix, and estimated impression points
3. Pull `keywords/detail` and `keywords/trend` to check whether keyword demand changed
4. Pull `keywords/product-traffic-terms` or `keywords/competitor-product-keywords` to check ASIN-side traffic share changes
5. Compare head competitors and ad density
6. Output anomaly level, likely causes, and action priority

### Tool Availability Gate

- `keywords/search-results` and `keywords/detail` are the minimum required tools for a diagnosis pass
- If either minimum tool is unavailable, stop and report that the diagnosis workflow cannot be executed reliably
- `keywords/product-traffic-terms` and `keywords/competitor-product-keywords` are optional enrichers only when they are actually exposed
- If those ASIN keyword endpoints are unavailable, continue with a SERP-led diagnosis and label any ASIN-side traffic-share conclusion as unavailable rather than inferred

### SERP And Product-Library Rule

- Diagnose keyword movement primarily from `keywords/search-results` because this is the observed keyword SERP
- Do not default to `products/search` to explain rank or page-1 composition changes
- Use `products/search` only if the user also wants a broader catalog context such as category-wide winners, price-band shifts, or strong-selling variants beyond the observed keyword SERP
- If `products/search` is used, state clearly that it is our product-database query result and does not equal Amazon live search ranking

### Diagnosis Signals

| Signal | What changed | Possible cause |
|--------|--------------|----------------|
| Position drop | `absolutePosition` / `pageIndex` worsened | stronger competitors, lower bid, listing weakness |
| Exposure drop | `estimateImpressionPoint` fell | lower search demand or worse placement |
| Ad crowding rose | sponsored share of SERP increased | bidding intensified |
| Traffic share fell | ASIN keyword share weakened | rank loss or keyword portfolio shift |
| Demand fell | trend/search count moved down | keyword itself cooled off |

### Alert Levels

- `High`
  target ASIN lost meaningful position/share and at least one supporting cause is observed
- `Medium`
  noticeable movement but evidence is mixed
- `Low`
  small movement or single-snapshot fluctuation only

### Output Template

```markdown
# Keyword Traffic Diagnosis Report — [ASIN] × [Keyword]

> Data is based on APIClaw keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

## Alert Level
[High / Medium / Low]

## What Changed
| Metric | Previous | Current | Interpretation |
|--------|----------|---------|----------------|

## Likely Causes
1. [💡 / 🔍 only]
2. [💡 / 🔍 only]
3. [💡 / 🔍 only]

## Recommended Actions
[Observe / increase defense / inspect bids / inspect listing relevance]

## Data Provenance
| Data | Endpoint | Key Params | Notes |
|------|----------|------------|-------|

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|

Credits remaining: N
```
