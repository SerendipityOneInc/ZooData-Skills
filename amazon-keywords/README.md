# Amazon Keyword Intelligence — ZooData Agent Skill

> Four keyword workflows built on ZooData's six keyword endpoints.

## What This Skill Does

This skill is for search-demand and keyword-traffic work that product/category skills do not cover well.

It supports four common scenarios:

1. **Keyword expansion** — start from a seed term and find candidate ad keywords
2. **Single keyword analysis** — decide whether one keyword is worth targeting
3. **Reverse ASIN keyword analysis** — inspect which keywords are driving an ASIN's visibility
4. **Keyword traffic monitoring** — watch an ASIN on a keyword and explain anomalies

## Endpoints Used

The skill is designed around these six ZooData endpoints:

- `/openapi/v2/keywords/detail`
- `/openapi/v2/keywords/trend`
- `/openapi/v2/keywords/extends`
- `/openapi/v2/keywords/search-results`
- `/openapi/v2/keywords/competitor-product-keywords`
- `/openapi/v2/keywords/product-traffic-terms`

## Draft Tool Names

To reduce agent guessing, document and prefer full callable tool names.
These are draft names inferred from other ZooData tool naming patterns and
should be manually confirmed against the active session:

- `mcp__zoodata.openapi_v2_keyword_detail`
- `mcp__zoodata.openapi_v2_keyword_trend`
- `mcp__zoodata.openapi_v2_keyword_extends`
- `mcp__zoodata.openapi_v2_keyword_search_results`
- `mcp__zoodata.openapi_v2_keyword_competitor_product_keywords`
- `mcp__zoodata.openapi_v2_keyword_product_traffic_terms`

## What You Get

- Candidate keyword tiers: `Priority test` / `Selective test` / `Observe only` / `Exclude`
- Single-keyword viability assessment across demand, competition, ad density, and SERP structure
- Reverse ASIN keyword source view with traffic-share-based prioritization
- Keyword anomaly diagnosis with likely cause analysis

## Example Prompts

- "基于 `wireless earbuds` 给我拓一批适合投放的关键词，并粗筛"
- "帮我分析 `yoga mat` 这个词值不值得投"
- "反查 ASIN `B0XXXXXXX` 的关键词流量来源"
- "监控 ASIN `B0XXXXXXX` 在 `collagen peptides` 下的异动，并解释原因"

## Notes

- This skill currently focuses on workflow design and endpoint orchestration.
- If the active session has not exposed the required keyword tools, report that boundary explicitly instead of guessing or fabricating calls.
- Use API docs only as a parameter/schema fallback after live tool-surface verification, not as a substitute for unavailable live tools.
- Scenario docs are split one-per-file for easier routing: expansion, keyword analysis, reverse ASIN, and keyword monitoring.
