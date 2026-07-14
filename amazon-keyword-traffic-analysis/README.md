# Amazon Keyword Intelligence — ZooData Agent Skill

> Backed by Amazon Brand Analytics (ABA) data: expand seed terms into ready-to-test ad keyword tiers, judge whether a keyword deserves budget, reverse-lookup any ASIN's traffic terms, and explain rank anomalies.

## What This Skill Does

Four workflows for search-demand and keyword-traffic questions that product/category skills don't cover:

1. **Keyword expansion** — seed term → candidate ad keywords, pre-sorted into `Priority test` / `Selective test` / `Observe only` / `Exclude` tiers
2. **Single keyword analysis** — a directional bid-worthiness verdict across demand, competition, ad density, and SERP structure
3. **Reverse ASIN lookup** — which keywords drive a (competitor) ASIN's visibility, prioritized by traffic share
4. **Keyword traffic diagnosis** — watch an ASIN under a keyword and explain rank/exposure anomalies with likely causes

## Example Prompts

- "Expand keyword ideas from `wireless earbuds` and do a coarse filter"
- "Is `yoga mat` worth targeting as an ad keyword?"
- "Reverse ASIN lookup for `B0XXXXXXX` — which keywords are driving its traffic?"
- "Monitor ASIN `B0XXXXXXX` under `collagen peptides` and explain any anomalies"

## What You Get

- Candidate keyword tiers: `Priority test` / `Selective test` / `Observe only` / `Exclude`
- Single-keyword directional viability assessment across demand, competition, ad density, and SERP structure
- Reverse ASIN keyword source view with traffic-share-based prioritization
- Keyword anomaly diagnosis with likely cause analysis

## Data Source & Boundaries

All keyword signals are sourced from the **Amazon Brand Analytics (ABA)** backend — the search-demand data Amazon shows brand owners. Coverage is limited to keywords that appear in ABA; missing data means outside ABA coverage, not low demand.

Keyword value boundary: ZooData keyword endpoints provide estimated search, exposure, visibility, and rank signals. They do not prove final keyword value or conversion quality for a specific ASIN by themselves. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, traffic-related conclusions should be treated as directional. Recommended data provision: in Brand View, sort descending by Search Funnel - Impressions → Brand Count, then provide a screenshot or download the CSV for model analysis. If seller-side ABA-SQP data is included, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate as first-party conversion evidence.

Keyword date rule: keyword workflows are keyword-query lookups. When a keyword endpoint requires `date` or `dateTo`, prefer T-1 or earlier and avoid current-date lookup unless the user explicitly asks for today's data. Keep the rationale internal unless the user asks why.

## Endpoints Used

The skill is designed around these eight ZooData endpoints:

- `/openapi/v2/keywords/detail`
- `/openapi/v2/keywords/trend`
- `/openapi/v2/keywords/extends`
- `/openapi/v2/keywords/search-results`
- `/openapi/v2/keywords/competitor-product-keywords`
- `/openapi/v2/keywords/product-traffic-terms`
- `/openapi/v2/keywords/product-traffic-terms-overview`
- `/openapi/v2/keywords/product-traffic-terms-timeline`

## Agent Implementation Notes

### Draft Tool Names

To reduce agent guessing, read the relevant tool docs/help/schema before selecting a tool, then document and prefer full callable tool names.
These are draft names inferred from other ZooData tool naming patterns and
should be manually confirmed against the active session:

- `mcp__zoodata__openapi_v2_keyword_detail`
- `mcp__zoodata__openapi_v2_keyword_trend`
- `mcp__zoodata__openapi_v2_keyword_extends`
- `mcp__zoodata__openapi_v2_keyword_search_results`
- `mcp__zoodata__openapi_v2_keyword_competitor_product_keywords`
- `mcp__zoodata__openapi_v2_keyword_product_traffic_terms`
- `mcp__zoodata__openapi_v2_product_traffic_terms_overview`
- `mcp__zoodata__openapi_v2_product_traffic_terms_timeline`

### Notes

- This skill currently focuses on workflow design and endpoint orchestration.
- Before choosing or rejecting a tool, read the relevant tool documentation: CLI help/reference docs for `zoodata.py`, or live schema / field descriptions for MCP/session tools.
- If the active session has not exposed the required keyword tools and the local CLI path is unavailable, report that boundary explicitly instead of guessing or fabricating calls.
- Use endpoint names as hints only; do not infer functionality from names without checking docs/help/schema.
- Scenario docs are split one-per-file for easier routing: expansion, keyword analysis, reverse ASIN, and keyword traffic diagnosis.
