# Amazon Keyword Intelligence — ZooData Agent Skill

> Four staged keyword workflows built on ZooData data, metric, and aggregate endpoints.

## What This Skill Does

This skill is for search-demand and keyword-traffic work that product/category skills do not cover well.

It supports four common scenarios:

1. **Keyword expansion** — start from a seed term and find candidate ad keywords
2. **Single keyword analysis** — directionally judge whether one keyword is worth testing
3. **Reverse ASIN keyword analysis** — inspect which keywords are driving an ASIN's visibility
4. **Keyword traffic diagnosis** — watch an ASIN on a keyword, identify unresolved anomalies, and explain them only when discriminating evidence is available

## Endpoints Used

The current CLI covers these ten ZooData keyword endpoints:

- `/openapi/v2/keywords/detail`
- `/openapi/v2/keywords/market-profile` (localhost pre-release metric layer; inspect the target surface)
- `/openapi/v2/keywords/trend-profile` (localhost pre-release metric layer; inspect the target surface)
- `/openapi/v2/keywords/trend`
- `/openapi/v2/keywords/extends`
- `/openapi/v2/keywords/search-results`
- `/openapi/v2/keywords/competitor-product-keywords`
- `/openapi/v2/keywords/product-traffic-terms`
- `/openapi/v2/keywords/product-traffic-terms-overview`
- `/openapi/v2/keywords/product-traffic-terms-timeline`

## Draft Tool Names

To reduce agent guessing, read the relevant tool docs/help/schema before selecting a tool, then document and prefer full callable tool names.
These are draft names inferred from other ZooData tool naming patterns and
should be manually confirmed against the active session:

- `mcp__zoodata__openapi_v2_keyword_detail`
- `mcp__zoodata__openapi_v2_keyword_market_profile`
- `mcp__zoodata__openapi_v2_keyword_trend_profile`
- `mcp__zoodata__openapi_v2_keyword_trend`
- `mcp__zoodata__openapi_v2_keyword_extends`
- `mcp__zoodata__openapi_v2_keyword_search_results`
- `mcp__zoodata__openapi_v2_keyword_competitor_product_keywords`
- `mcp__zoodata__openapi_v2_keyword_product_traffic_terms`
- `mcp__zoodata__openapi_v2_product_traffic_terms_overview`
- `mcp__zoodata__openapi_v2_product_traffic_terms_timeline`

## What You Get

- Standalone market-screen candidate pools that request an ASIN before product-specific prioritization
- ASIN-stage candidate validation tiers: `Priority test` / `Selective test` / `Harvest` / `Observe only` / `Avoid`
- Single-keyword directional viability assessment across demand, competition, ad density, and SERP structure
- Reverse ASIN keyword source view with traffic-share-based prioritization
- Keyword anomaly diagnosis that seeks discriminating evidence before reporting bounded hypotheses or evidence-authorized actions

Core workflow rules:

- **Metric-first:** use the smallest sufficient metric response before descending to raw rows/series.
- **Batch-first:** batch compatible keyword subjects up to the live endpoint limit and preserve per-item status.
- **Evidence progression:** market evidence → subject observation → seller-real evidence.
- **Evidence-seeking diagnosis:** observed problem → unresolved question → discriminating evidence → evidence-supported explanation.
- **Evidence-to-action:** aggregate weakness can trigger inspection/diagnosis but cannot authorize a specific asset or operating change without direct target evidence.

Keyword value boundary: ZooData keyword endpoints provide estimated search, exposure, visibility, and rank signals. They do not prove final keyword value or conversion quality for a specific ASIN by themselves. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, traffic-related conclusions should be treated as directional. Recommended data provision: in Brand View, sort descending by Search Funnel - Impressions → Brand Count, then provide a screenshot or download the CSV for model analysis. If seller-side ABA-SQP data is included, use impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate as first-party conversion evidence.

Keyword date rule: keyword workflows are keyword-query lookups. When a keyword endpoint requires `date` or `dateTo`, prefer T-1 or earlier and avoid current-date lookup unless the user explicitly asks for today's data. Keep the rationale internal unless the user asks why.

## Example Prompts

- "Expand keyword ideas from `wireless earbuds` and do a coarse filter"
- "Is `yoga mat` worth targeting as an ad keyword?"
- "Reverse ASIN lookup for `B0XXXXXXX` — which keywords are driving its traffic?"
- "Monitor ASIN `B0XXXXXXX` under `collagen peptides` and explain any anomalies"

## Notes

- This skill currently focuses on workflow design and endpoint orchestration.
- Before choosing or rejecting a tool, read the relevant tool documentation: CLI help/reference docs for `zoodata.py`, or live schema / field descriptions for MCP/session tools.
- If the active session has not exposed the required keyword tools and the local CLI path is unavailable, report that boundary explicitly instead of guessing or fabricating calls.
- Use endpoint names as hints only; do not infer functionality from names without checking docs/help/schema.
- Scenario docs are split one-per-file for easier routing: expansion, keyword analysis, reverse ASIN, and keyword traffic diagnosis.
