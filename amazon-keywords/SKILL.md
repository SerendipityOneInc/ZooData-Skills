---
name: amazon-keywords
description: >
  Use when user asks for keyword expansion or ad keyword filtering; whether a keyword is worth
  bidding on; which keywords drive traffic to an ASIN; or why an ASIN changed under a keyword.
  Requires ZOODATA_API_KEY.
metadata:
  version: "0.1.0"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Amazon Keyword Intelligence

> Amazon keyword research and traffic analysis. Respond in user's language.

## Files

| File | Purpose |
|------|---------|
| `{skill_base_dir}/references/reference.md` | Load when you need exact endpoint fields, quirks, or scoring inputs |
| `{skill_base_dir}/references/execution-guide.md` | Load for full execution protocol and monitoring rules |
| `{skill_base_dir}/references/scenarios-expand.md` | Load for keyword expansion flow |
| `{skill_base_dir}/references/scenarios-keyword-analysis.md` | Load for single-keyword evaluation flow |
| `{skill_base_dir}/references/scenarios-reverse-asin.md` | Load for reverse ASIN keyword analysis flow |
| `{skill_base_dir}/references/scenarios-keyword-traffic-diagnosis.md` | Load for keyword traffic diagnosis flow |

## Credential

Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys).

## Input

User typically provides one of:
- seed keyword
- target keyword
- ASIN
- ASIN + keyword
- marketplace and date range constraints

If marketplace is omitted, default to `US`. If date is omitted, use the latest available date window supported by the endpoint.

## Data Source

All keyword data comes from **Amazon Brand Analytics (ABA) backend**. Coverage is limited to keywords that appear in ABA — keywords with no ABA record will return `data: null` or empty results, not an API error. Do not treat missing data as a signal of low demand; it means the keyword is outside ABA coverage.

## Supported Endpoints

This skill is built around these six keyword endpoints:

1. `/openapi/v2/keywords/detail`
2. `/openapi/v2/keywords/trend`
3. `/openapi/v2/keywords/extends`
4. `/openapi/v2/keywords/search-results`
5. `/openapi/v2/keywords/competitor-product-keywords`
6. `/openapi/v2/keywords/product-traffic-terms`

## Callable Tool Names

Business endpoint paths and MCP callable tool names are not the same thing.

**MANDATORY — do this before any tool call or capability claim:**
1. Inspect the live tool surface of the current session
2. Read the live schema / field descriptions of any candidate tool
3. Only then judge capability — tool name alone is not evidence

| HTTP endpoint path | Draft callable tool name |
|-------------------|--------------------------|
| `/openapi/v2/keywords/detail` | `mcp__zoodata__openapi_v2_keyword_detail` |
| `/openapi/v2/keywords/trend` | `mcp__zoodata__openapi_v2_keyword_trend` |
| `/openapi/v2/keywords/extends` | `mcp__zoodata__openapi_v2_keyword_extends` |
| `/openapi/v2/keywords/search-results` | `mcp__zoodata__openapi_v2_keyword_search_results` |
| `/openapi/v2/keywords/competitor-product-keywords` | `mcp__zoodata__openapi_v2_keyword_competitor_product_keywords` |
| `/openapi/v2/keywords/product-traffic-terms` | `mcp__zoodata__openapi_v2_keyword_product_traffic_terms` |

The draft names above follow the naming convention seen in other ZooData skills. If the live session exposes a different name, use that name exactly.

**PROHIBITED — never do any of the following:**
- Call a keyword tool before inspecting its live schema
- Declare a keyword endpoint unavailable without first checking both the live tool surface and its schema
- Say "the keyword-volume interface is not available" because you didn't see a tool named "keyword volume"
- Use `products/search` as a substitute for keyword endpoints and label its results as keyword traffic evidence
- Treat `webtools_search` as a keyword-intelligence endpoint
- "Normalize" a live callable name back to the draft name above

**Capability signals in live schema:** If a tool exposes fields such as `estimateSearchCountWeekly`, `estimateSearchCount`, `keywordEstimateSearchCount`, or `abaRank`, treat it as having keyword-volume capability even if its name is not explicit.

**Tool boundary rules (CRITICAL — do not misclassify):**

| Tool | Role | NEVER use it as |
|------|------|-----------------|
| `/openapi/v2/keywords/*` | Keyword intelligence (snapshot, trend, SERP, ASIN traffic) | — |
| `products/search` | Product-database snapshot — broader catalog winners, price-band structure, variant distribution | Keyword SERP evidence, keyword demand proof, or a front-end search interface |
| `webtools_search` | Web crawler / retrieval utility | Keyword snapshot, trend, SERP, or keyword volume substitute |

## Core Scenarios

### 1. Keyword Expansion
Goal: start from a seed term and find candidate ad keywords for coarse filtering.

Primary endpoints:
- `keywords/extends`
- `keywords/detail`
- `keywords/search-results`
- `keywords/trend`

Tool availability note:
- This scenario is executable only when at least `keywords/extends` and `keywords/detail` are exposed
- If `keywords/trend` or `keywords/search-results` are unavailable, reduce confidence and state the missing evidence explicitly

### 2. Single Keyword Analysis
Goal: deeply assess whether one keyword is worth targeting.

Primary endpoints:
- `keywords/detail`
- `keywords/trend`
- `keywords/search-results`

Tool availability note:
- This scenario is executable only when `keywords/detail` and `keywords/search-results` are exposed
- If `keywords/trend` is unavailable, do not make strong claims about demand direction

### 3. Reverse ASIN Keyword Analysis
Goal: identify which keywords bring visibility/traffic to an ASIN and where to focus spend.

Primary endpoints:
- `keywords/product-traffic-terms`
- `keywords/competitor-product-keywords`
- `keywords/detail`
- `keywords/search-results`

Tool availability note:
- This scenario is executable only when both ASIN keyword endpoints are exposed: `keywords/product-traffic-terms` and `keywords/competitor-product-keywords`
- If either ASIN keyword endpoint is unavailable, report the boundary and do not substitute `keywords/detail` or `keywords/search-results` as a fake reverse-ASIN source map

### 4. Keyword Traffic Diagnosis
Goal: diagnose why an ASIN changed under a keyword, detect anomalies, and explain likely causes.

Primary endpoints:
- `keywords/search-results`
- `keywords/detail`
- `keywords/trend`
- `keywords/product-traffic-terms`
- `keywords/competitor-product-keywords`

Tool availability note:
- Minimum executable set: `keywords/search-results` + `keywords/detail`
- `keywords/trend` and the ASIN keyword endpoints are enrichers; if missing, keep the diagnosis SERP-led and mark those evidence gaps explicitly

## API Pitfalls (CRITICAL)

1. `keywords/extends` uses `query`, not `keyword`
2. `keywords/detail` and `keywords/extends` resolve to the nearest available weekly snapshot at or before the requested date
3. `keywords/trend` is weekly time series, not daily
4. `keywords/search-results` and both ASIN keyword endpoints are daily observations over a sliding ~7-day window, not long-retention history
5. `keywords/detail` may return `success: true` with `data: null`; treat this as "no snapshot available", not an API failure
6. `keywords/extends` may legitimately return `data: []`; try both `queryType=phrase` and `queryType=fuzzy` before concluding low expandability
7. `trafficShare` is an observed share within the endpoint's sampled window; do not present it as exact Amazon share of voice
8. SERP analysis must separate `exploreType`: `ORG` vs `SP` vs `SB` vs `SBV` vs `SPR`
9. Monitoring conclusions require comparison across at least 2 timestamps; single-day movement is directional only
10. `/openapi/v2/keywords/search-results` already returns listing-level product fields and should be the default source for answering "首页都是什么产品"
11. Do not append `products/search` by default when the user's question is only about the observed keyword SERP; use it only as an optional broader-market supplement
12. `products/search` is our own product-database query result, not Amazon live search results, so never present it as evidence of current SERP ordering
13. `webtools_search` is a crawler / web retrieval utility, not a keyword-intelligence endpoint; do not treat it as a substitute for keyword snapshot, trend, or SERP evidence unless the task is explicitly web collection rather than ZooData keyword analysis

## On 401 Invalid Key

When the API returns code 401: stop further calls, tell the user the key was rejected, and direct them to https://zoodata.ai/en/api-keys. Do not fabricate missing data.

## On 402 Credit Exhausted

When the API returns code 402: stop further calls, report partial findings already gathered, estimate remaining credits needed, and direct the user to https://zoodata.ai/en/pricing. Do not fabricate missing data.

## Decision Framework

### Keyword Fit Assessment

Judge each candidate keyword on four dimensions:

| Dimension | What to look at | Interpretation |
|-----------|------------------|----------------|
| Demand | `estimateSearchCountWeekly`, trend slope, ABA rank | Higher demand is better, but only if stable enough |
| Competition | `adCount`, `adCampaignCount`, SERP ad density, head ASIN concentration | Higher competition raises bid difficulty |
| Relevance | seed relation, `relevanceScore`, SERP title/brand fit | High relevance means better listing/ad fit |
| Accessibility | organic entry room, ad crowding, whether current leaders are entrenched | Indicates whether traffic is realistically capturable |

### Recommendation Labels

- `Priority test` — good balance of demand, relevance, and manageable competition
- `Selective test` — usable in certain ad groups or exact-match campaigns only
- `Observe only` — interesting but not ready for budget allocation
- `Exclude` — weak relevance or poor traffic efficiency

### Reverse-ASIN Labels

- `Defend` — already meaningful for traffic or position and should be protected
- `Expand` — relevant and promising, but still has room to improve visibility
- `Observe` — potentially useful but weak, unstable, or incomplete
- `Avoid` — low fit, weak position, or crowded without a clear path

## Output Spec

Sections: Findings → Recommendation / action tier → Data Provenance → API Usage → Data Notes.

### Language (required)

Output language MUST match the user's input language. Technical field names and endpoint names may remain in English.

### Disclaimer (required, at the top of every report)

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

### Confidence Labels (required, tag EVERY conclusion)

- 📊 **Data-backed** — direct API data
- 🔍 **Inferred** — logical reasoning from multiple observed fields
- 💡 **Directional** — action suggestions, hypotheses, or monitoring explanations

Rules:
- Strategy recommendations are NEVER 📊
- Single-day anomaly explanations are NEVER above 💡
- Group headers and aggregate labels must not use stronger confidence than their contents

### Data Provenance (required)

Include a table at the end of every report:

| Data | Endpoint | Key Params | Notes |
|------|----------|------------|-------|
| Keyword snapshot | `keywords/detail` | keyword, date, marketplace | Weekly snapshot at or before requested date |
| ... | ... | ... | ... |

### API Usage (required)

| Endpoint | Calls | Credits |
|----------|-------|---------|
| (each endpoint used) | N | N |
| **Total** | **N** | **N** |

End with `Credits remaining: N`.

## Limitations

This skill does not provide:
- real CPC / bid recommendation from Amazon Ads billing
- campaign structure write-back
- long-retention daily keyword history beyond the endpoint windows
- exact attribution from Amazon internal ad console

Use the outputs as directional research and combine with ad account data before final budget decisions.
