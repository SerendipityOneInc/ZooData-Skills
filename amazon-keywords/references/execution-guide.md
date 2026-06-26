# Execution Guide — Amazon Keyword Intelligence

This file defines the execution protocol for the four keyword scenarios.

---

## Execution Mode

| Task Type | Mode | Behavior |
|-----------|------|----------|
| Single lookup such as one snapshot field | Quick | Return the key metric with light interpretation |
| Expansion, full keyword judgment, reverse ASIN, monitoring diagnosis | Full | Run the full endpoint chain, apply scoring, and output provenance + API usage |

## Full-Mode Checklist

Before running any Full-mode keyword task:

- [ ] Inspect the active tool surface and read the live schema / field descriptions for candidate keyword tools before judging capability
- [ ] Confirm the object: seed keyword / target keyword / ASIN / ASIN + keyword
- [ ] Confirm marketplace; default to `US` if absent
- [ ] Confirm the date lens: weekly snapshot, recent 4-8 weeks, or latest sliding window
- [ ] Separate traffic facts from strategy advice using confidence labels
- [ ] Include Data Provenance and API Usage at the end

## General Rules

### Tool Naming

- Distinguish HTTP endpoint paths such as `/openapi/v2/keywords/detail` from actual callable tool names such as draft `mcp__zoodata.openapi_v2_keyword_detail`
- Never call a keyword tool from an inferred prefix alone
- Before first use, inspect the active tool surface and confirm the exact full callable name
- If the live callable name differs from the draft docs, trust the live callable name
- If no keyword tool is exposed, stop and report that the tool is unavailable instead of guessing

### Tool Discovery Fallback

- If the static tool list does not explicitly show the keyword tools, do not immediately fall back to API docs
- First confirm whether the current session actually exposes the corresponding callable tool names
- If the keyword tools are exposed, call them directly and do not use doc lookup as a prerequisite step
- Only fall back to ZooData docs for parameter confirmation when the keyword tools are not exposed or a live tool call fails
- If both direct tool access and doc-backed fallback are unavailable, report the limitation clearly and produce only a boundary-labeled substitute analysis

### Capability Inference Rule

- Do not infer endpoint capability from the tool name alone
- Determine capability in this order: live tool schema and field descriptions, then ZooData reference docs, then endpoint naming as a weak hint only
- If a tool exposes fields such as `estimateSearchCountWeekly`, `keywordEstimateSearchCount`, `estimateSearchCount`, `abaRank`, or related traffic fields, treat it as having keyword-volume or trend-analysis capability even if the tool name is not explicit
- Do not say "the keyword-volume interface is not available" unless you have checked the exposed schema/docs and confirmed the required fields are unavailable
- Prohibit reasoning such as "I do not see a tool named keyword volume, so volume cannot be analyzed"
- Prohibit capability claims such as "`products/search` proves this keyword has demand" unless the report explicitly labels that evidence as a secondary product-database signal rather than a keyword snapshot
- Prohibit classifying `products/search` as a front-end SERP tool or `webtools_search` as a keyword-intelligence endpoint; both have different evidence roles and must be named accordingly

### Date Handling

- `keywords/detail` and `keywords/extends` are weekly snapshots
- `keywords/trend` is weekly time series
- `keywords/search-results` and ASIN keyword endpoints are recent daily observations
- Never compare weekly and daily snapshots as if they were the same grain without stating the difference

### Ad vs Organic Separation

- Analyze `exploreType` separately
- At minimum, split `ORG` and sponsored placements
- Do not call a keyword "organic-friendly" if the visible page is dominated by ads

### Anomaly Standards

| Signal type | Minimum evidence | Max confidence |
|-------------|------------------|----------------|
| Weekly trend change | 2+ weekly points in same direction | 🔍 |
| SERP change | 2 timestamps showing changed rank mix | 🔍 |
| One-day movement | single snapshot difference | 💡 |

### Monitoring Explanation Rule

When explaining keyword anomalies, check causes in this order:

1. Search demand moved
2. Ad density changed
3. The target ASIN's position changed
4. New head competitors entered
5. The keyword itself became more or less concentrated

If multiple causes are plausible, rank them rather than presenting one as certain.

## Output Rules

### Candidate Tiering

For keyword expansion outputs, classify into:

- `Priority test`
- `Selective test`
- `Observe only`
- `Exclude`

For reverse-ASIN outputs, classify into:

- `Defend`
- `Expand`
- `Observe`
- `Avoid`

### Coarse Filtering Rule

A keyword can only be `Priority test` if ALL are true:

- demand is at least mid-tier for the batch
- relevance is strong
- competition is not the worst tier
- there is a plausible placement strategy

### High-Risk Flags

Flag as risk when any of these appear:

- very high `adCount`
- search demand falling across multiple weekly points
- ASIN appears only in sponsored placements, not organic
- top results repeat the same few brands or parent ASIN families
- low `daysCoverageRate` or low `observationCount`

## Monitoring Cadence Suggestion

Recommended default cadence:

- weekly for keyword opportunity watchlists
- 2-3 times per week for launched core terms
- daily only for high-spend hero keywords or incident follow-up
