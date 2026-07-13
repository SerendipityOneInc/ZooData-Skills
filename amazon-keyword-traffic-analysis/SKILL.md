---
name: amazon-keyword-traffic-analysis
description: >
  Use when user asks for keyword expansion or ad keyword filtering; single keyword analysis or
  keyword deep dive; whether a keyword is worth bidding on; which keywords drive traffic to an ASIN;
  or why an ASIN changed under a keyword. Requires ZOODATA_API_KEY.
metadata:
  version: "0.1.2"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Amazon Keyword Intelligence

> Amazon keyword research and traffic analysis. Respond in user's language.

## Files

| File | Purpose |
|------|---------|
| `{skill_base_dir}/references/reference.md` | Load before tool selection and when you need exact endpoint parameters, response fields, quirks, or scoring inputs |
| `{skill_base_dir}/references/execution-guide.md` | Load before any full-mode task — contains input-to-endpoint routing, Evidence Capability Matrix, and full execution protocol |
| `{skill_base_dir}/references/scenarios-expand.md` | Load for keyword expansion output template |
| `{skill_base_dir}/references/scenarios-keyword-analysis.md` | Load for single-keyword analysis output template |
| `{skill_base_dir}/references/scenarios-reverse-asin.md` | Load for reverse ASIN output template |
| `{skill_base_dir}/references/scenarios-keyword-traffic-diagnosis.md` | Load for keyword traffic diagnosis output template |

## Credential

Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys).

## Input

User typically provides one of:
- seed keyword
- target keyword
- ASIN
- ASIN + keyword
- marketplace and date range constraints

If marketplace is omitted, default to `US`. Keyword endpoints are keyword-query workflows: treat user-provided terms as search queries/keywords, not category paths or product search substitutes. If a keyword request requires `date` or `dateTo`, prefer T-1 or earlier instead of the current date; only use the current date when the user explicitly asks for today's data. In user-facing updates, state the selected marketplace/date without extra rationale unless the user asks why that date was selected.

## Data Source

All keyword data comes from **Amazon Brand Analytics (ABA) backend**. Coverage is limited to keywords that appear in ABA — keywords with no ABA record will return `data: null` or empty results, not an API error. Do not treat missing data as a signal of low demand; it means the keyword is outside ABA coverage.

ZooData keyword endpoints provide search-demand, SERP, rank, and estimated-impression signals. They do **not** provide the seller's own ABA **Search Query Performance** conversion funnel, including ASIN-specific impressions, clicks, cart adds, purchases, conversion rate, or sales share. Therefore, keyword value judgments from this skill are directional prioritization, not 100% proof of commercial value.

ABA-SQP backend location: `Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View`

Recommended ABA-SQP data provision method:
- In Brand View, sort descending by `[Search Funnel - Impressions](https://sellercentral.amazon.com/brand-analytics/metric-glossary?linkedFrom=query-performance-brand-report-table-qp-impressions-group) -> Brand Count`, then provide a screenshot
- Alternatively, download the CSV and provide it for model analysis

Before writing traffic-related conclusions, determine whether Amazon backend ABA-SQP search conversion data is included in the current user-provided evidence. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, state the data basis in the opening `Data Notes` section and repeat it near the end in `Data Notes Reminder`. Do not insert this data-basis note inside each traffic conclusion, traffic-source bucket, or recommendation group.

If the user did provide ABA-SQP data, incorporate it as first-party conversion evidence and do not add the seller-side SQP enrichment request.

Every full-mode report that contains keyword value, traffic-source, exposure movement, ranking visibility, bidding, budget, or spend-priority conclusions must include a standalone `Data Notes` section immediately after the opening disclaimer and before `Findings` / `Summary` / `Top Traffic Terms` / `Alert Level`.

`Data Notes` must use natural prose, not status labels or similar form-like wording.

Repeat the opening data-basis message once near the end of full-mode reports, immediately before `API Usage`, using a `Data Notes Reminder` section translated to the user's language. The end reminder exists so users who skipped the opening note still see the seller-side SQP enrichment request; it must not be inserted inside business findings or replace the opening `Data Notes` section.

When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep `Data Notes` short and direct. First state that evidence basis; then say that if the user can provide seller-side ABA-SQP conversion funnel data, the analysis can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance; then give the Seller Central path `Brand Analytics → Search Analytics → Search Query Performance → Brand View`, instruct the user to sort by `Search Funnel - Impressions → Brand Count`, and ask for a screenshot or CSV.

For Chinese output, this message should naturally convey: if the user can provide seller-side ABA-SQP data, we can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance. Prefer simple wording equivalent to "If you can provide seller-side ABA-SQP data, we can tailor for you a more exclusive operating strategy that better fits your product's actual conversion performance" and avoid long phrases, field lists, or "later/follow-up" wording.

Avoid deficit-framed wording in user-facing `Data Notes`. Do not imply fault or omission by the user; frame seller-side ABA-SQP as an optional enrichment that enables a more bespoke strategy.

When seller-private ABA-SQP data is present, name the provided SQP fields used, such as impressions, clicks, cart adds, purchases, click share, purchase share, or conversion rate, and do not repeat the seller-side SQP enrichment request.

The `Data Notes` section is mandatory. Translate the section title and body to the user's language at output time; do not leave section titles in English when the report body is Chinese. For Chinese output, render the opening title exactly as the Unicode escape `\u6570\u636e\u8bf4\u660e` and the end reminder title exactly as `\u6570\u636e\u8bf4\u660e\uff08\u518d\u6b21\u63d0\u9192\uff09`. Decode these escapes into visible Chinese characters in the final report. Avoid SQP-specific status titles.

The end-of-report `Data Notes Reminder` is also mandatory for full-mode reports with keyword value, traffic-source, exposure movement, ranking visibility, bidding, budget, or spend-priority conclusions. Its body should repeat the opening `Data Notes` message, not merely summarize it, so users who miss the opening note still see the same data basis and seller-side SQP data request.

## Endpoints

Use `python {skill_base_dir}/scripts/zoodata.py` as the default execution entry.

**MANDATORY — tool selection and capability claims must follow this gate:**
1. Before choosing any tool, read the relevant documentation:
   - local CLI path: read `references/reference.md` plus `zoodata.py --help` / subcommand help
   - MCP/session tools: inspect the live tool surface and read the live schema / field descriptions
2. Prefer the local CLI entry after the documentation check; use MCP names as fallback only
3. Only then select the execution tool and judge capability — tool name alone is not evidence

| HTTP endpoint path | CLI subcommand | Draft MCP tool name |
|-------------------|----------------|---------------------|
| `/openapi/v2/keywords/detail` | `keyword-detail` | `mcp__zoodata__openapi_v2_keyword_detail` |
| `/openapi/v2/keywords/trend` | `keyword-trend` | `mcp__zoodata__openapi_v2_keyword_trend` |
| `/openapi/v2/keywords/extends` | `keyword-extends` | `mcp__zoodata__openapi_v2_keyword_extends` |
| `/openapi/v2/keywords/search-results` | `keyword-search-results` | `mcp__zoodata__openapi_v2_keyword_search_results` |
| `/openapi/v2/keywords/competitor-product-keywords` | `keyword-competitor-product-keywords` | `mcp__zoodata__openapi_v2_keyword_competitor_product_keywords` |
| `/openapi/v2/keywords/product-traffic-terms` | `keyword-product-traffic-terms` | `mcp__zoodata__openapi_v2_keyword_product_traffic_terms` |
| `/openapi/v2/keywords/product-traffic-terms-overview` | `product-traffic-terms-overview` | `mcp__zoodata__openapi_v2_product_traffic_terms_overview` |
| `/openapi/v2/keywords/product-traffic-terms-timeline` | `product-traffic-terms-timeline` | `mcp__zoodata__openapi_v2_product_traffic_terms_timeline` |

If the live session exposes a different name, use that name exactly.

**PROHIBITED — never do any of the following:**
- Choose or reject a tool from its name alone before reading the relevant docs/help/schema
- Declare a keyword endpoint unavailable without first checking `zoodata.py`, and then the live tool surface/schema if needed
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

## Task Constraints

These constraints are higher priority than any suggested workflow wording in reference files.

### Evidence Gate

- Do not produce a conclusion unless the scenario's minimum evidence is available
- If minimum evidence is missing, stop or downgrade the answer and name the missing evidence explicitly
- Do not silently backfill a missing keyword endpoint with another non-equivalent interface

### Non-Substitution Rules

- `products/search` must not be used as a substitute for keyword snapshot, keyword trend, keyword SERP, or reverse-ASIN traffic evidence
- `webtools_search` must not be used as a substitute for any `/openapi/v2/keywords/*` endpoint
- `keywords/detail` and `keywords/search-results` must not be used to fabricate reverse-ASIN traffic-source maps when neither ASIN traffic-list endpoint is available
- `keywords/trend` must not be treated as daily history; `keywords/search-results` and ASIN keyword endpoints must not be treated as long-retention weekly trend series

### Confidence Gate

- `Data-backed` conclusions require direct support from the endpoint actually designed for that evidence type
- `Inferred` conclusions require multiple supporting fields and must stay within the endpoint boundary
- `Directional` conclusions may recommend actions, but must not be phrased as proven causality
- If a required evidence type is absent, lower the confidence instead of strengthening the wording
- Keyword-value judgments such as "worth targeting", "high value", "profitable", or "conversion potential" are never 100% supported by ZooData alone because the available data is estimated exposure/search/visibility data, not the user's ABA Search Query Performance funnel
- When the current evidence set does not include Search Query Performance data, phrase keyword-value and traffic-related conclusions as directional testing priority; keep the seller-side SQP enrichment request in `Data Notes` and `Data Notes Reminder`, not inside individual findings
- If user-provided ABA-SQP data is available, use it to refine traffic and keyword-value conclusions and do not add the seller-side SQP enrichment request

### Comparative Claims Gate

- Avoid saying the product, listing, CTR, CVR, rank, or traffic quality is "better than competitors", "outperforming competitors", or "superior to competitors" unless there is direct evidence for the same metric, same keyword/query, same marketplace, comparable date range, and comparable placement or position scope
- Prefer market-relative wording when competitor-specific evidence is unavailable: above/below market midpoint, ahead/behind the market median, near the upper/lower band, ranking toward the front/back, or not an obvious weak point
- When deriving a market average or median from ABA/SQP screenshots, ZooData aggregates, or visible SERP samples, state the calculation basis and the limitation; do not present it as an external benchmark or competitor proof
- If placement or position cannot be controlled, downgrade confidence and avoid strong superiority wording; for example, use "listing exposure appeal is not obviously weak" rather than "CTR is significantly better than competitors"
- CTR/CVR comparisons must distinguish market-wide query averages from competitor-specific comparisons

### Execution Flexibility

- You do not need to follow a fixed endpoint order if the task can be completed within the evidence gate
- You may choose the most efficient call pattern for the task
- You must still satisfy the evidence gate before making its core conclusion

### Output Discipline

- Separate observed facts from interpretation and from action advice
- Explicitly label unavailable evidence instead of implying it
- When supplementary tools are used, state their role precisely and do not blur their evidence class
- If any live ZooData API call was made, the final report must end with `API Usage`; do not omit it even when the user did not ask for it explicitly
- Track endpoint usage while calling APIs: for every response, read `_query.endpoint`, `_query.params`, `meta.creditsConsumed`, and `meta.creditsRemaining` when present
- In `API Usage`, use a markdown table, not a bullet list; aggregate calls and `meta.creditsConsumed` by endpoint; include a final `Total` row that sums calls and credits; use the latest returned `meta.creditsRemaining` for credits remaining
- If a response omits `meta.creditsConsumed` or `meta.creditsRemaining`, write `not returned` for that field rather than dropping the usage section
- Avoid competitor-superiority wording in findings and recommendations unless the Comparative Claims Gate is satisfied
- When the current evidence set does not include Amazon backend ABA-SQP search conversion data, do not interrupt individual traffic-related conclusions, traffic-source buckets, "worth targeting/worth bidding" verdicts, or budget/spend recommendation groups with the seller-side SQP enrichment request; place that message only in `Data Notes` and `Data Notes Reminder`
- If the user has provided ABA-SQP search conversion data, do not repeat the seller-side SQP enrichment request; instead, cite the relevant SQP signal in the conclusion when it changes precision or confidence
- In full-mode reports, include the standalone `Data Notes` section near the top before any traffic or recommendation section, so the data basis and optional seller-side SQP enrichment path are visible without scanning the whole report
- In full-mode reports, repeat the opening `Data Notes` body near the end, immediately before `API Usage`, so the same data basis remains visible after recommendations

## API Pitfalls (CRITICAL)

1. `keywords/extends` uses `query`, not `keyword`
2. `keywords/detail` and `keywords/extends` resolve to the nearest available weekly snapshot at or before the requested date
3. Keyword endpoints are keyword-query interfaces; for inputs named `keyword` or `query`, use the Amazon search query / keyword phrase being analyzed
4. When a keyword endpoint requires `date` or `dateTo`, prefer T-1 or earlier and avoid using the current date unless the user explicitly asks for today's lookup; do not proactively explain the reason unless asked
5. `keywords/trend` is weekly time series, not daily. CLI usage must use full ISO dates with these exact flags: `keyword-trend --keyword "small baskets for organizing" --date-from 2026-04-01 --date-to 2026-07-02 --marketplace US`; never send truncated dates, ellipses, natural-language dates, reversed ranges, or ranges longer than 93 days.
6. `keywords/search-results` and ASIN keyword endpoints are daily/recent observations over short windows, not long-retention history; date-range keyword endpoints such as `keyword-trend` and `product-traffic-terms-timeline` accept up to a 93-day requested range
7. `keywords/detail` may return `success: true` with `data: null`; treat this as "no snapshot available", not an API failure
8. `keywords/extends` may legitimately return `data: []`; try both `queryType=phrase` and `queryType=fuzzy` before concluding low expandability
9. `trafficShare` is an observed share within the endpoint's sampled window; do not present it as exact Amazon share of voice
10. SERP analysis must separate `exploreType`: `ORG` vs `SP` vs `SB` vs `SBV` vs `SPR`
11. Monitoring conclusions require comparison across at least 2 timestamps; single-day movement is directional only
12. `/openapi/v2/keywords/search-results` already returns listing-level product fields and should be the default source for "what products appear on page 1 for this keyword"
13. Do not append `products/search` by default when the user's question is only about the observed keyword SERP; use it only as an optional broader-market supplement
14. `products/search` is our own product-database query result, not Amazon live search results, so never present it as evidence of current SERP ordering
15. `webtools_search` is a crawler / web retrieval utility, not a keyword-intelligence endpoint; do not treat it as a substitute for keyword snapshot, trend, or SERP evidence unless the task is explicitly web collection rather than ZooData keyword analysis
16. `keywords/product-traffic-terms-overview` returns weekly all-keyword impression traffic changes under one ASIN versus the previous period, with placement-level `*ImpressionPoint` fields and matching `*Prev` baselines; `first3PagesNewOrganicKeywords` lists keywords newly entering ORG first three pages, and `first3PagesLostOrganicKeywords` lists keywords that dropped out; do not treat it as per-keyword daily rank history
17. For `keywords/product-traffic-terms-overview`, display the returned `periodStartDate` / `periodEndDate` as the overview period; do not use the request date or an inferred date range as the period shown in the report
18. `keywords/product-traffic-terms-timeline` is the preferred endpoint for ASIN + keyword anomaly timelines; interpret its three metric groups separately:
    - `keyword*` fields are keyword traffic-forecast dependency data for the provided keyword's corresponding metric period (`keywordPeriodStartDate` / `keywordPeriodEndDate`)
    - `latest*` fields are the ASIN's latest product/listing/rank snapshot on the specified `date`
    - impression-point fields, `avg*` fields, ad-activity fields, and placement observations are rolling metrics for the most recent 7 days ending at the given `date`
19. HTTP 422 means request validation failed, not a transient network error. Do not retry the same request repeatedly. Read the returned error detail and fix parameters first, especially full `YYYY-MM-DD` date strings, required fields, date range order, and endpoint-specific range limits.

## On Missing Key

When `ZOODATA_API_KEY` is not set (verify via `python {skill_base_dir}/scripts/zoodata.py check` — credentials-only, no endpoint calls and no credit usage; exits non-zero if no key in env or `~/.zoodata/config.json`): follow the **"On Missing Key"** protocol in `zoodata/SKILL.md` — STOP before any call, link the user to https://zoodata.ai/en/api-keys, and DO NOT produce a "partial analysis from public knowledge" / "for reference only" fallback as a substitute.

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

Important boundary:
- These dimensions estimate search opportunity and visibility accessibility, not actual keyword commercial value for the user's ASIN
- Do not claim a keyword is definitively profitable, high-converting, or worth full budget from ZooData alone
- When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep traffic or spend/value recommendations directional and put the seller-side SQP enrichment request only in `Data Notes` and `Data Notes Reminder`; if seller-side ABA-SQP data is included, use those query-level impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate fields as first-party conversion evidence

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

Sections: Findings → Recommendation / action tier → API Usage.

### Language (required)

Output language MUST match the user's input language. Technical field names and endpoint names may remain in English.

### Disclaimer (required, at the top of every report)

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

For keyword-value reports, add this note:

> ZooData provides estimated exposure/search/visibility signals. When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, traffic-related conclusions below should be read directionally; seller-side ABA-SQP conversion funnel data can further refine the analysis into a more tailored, account-specific operating strategy.

### Confidence Labels (required, tag EVERY conclusion)

- 📊 **Data-backed** — direct API data
- 🔍 **Inferred** — logical reasoning from multiple observed fields
- 💡 **Directional** — action suggestions, hypotheses, or monitoring explanations

Rules:
- Strategy recommendations are NEVER 📊
- Keyword-value verdicts without user-provided Search Query Performance data are NEVER above 💡
- Traffic-related conclusions without user-provided ABA-SQP search conversion data are NEVER above 💡 when they imply spend/value priority; do not repeat the seller-side SQP enrichment request inside the conclusion body
- Single-day anomaly explanations are NEVER above 💡
- Group headers and aggregate labels must not use stronger confidence than their contents

For API Usage format and credit tracking rules, see `execution-guide.md § Usage Accounting Rule`.

## Limitations

This skill does not provide:
- real CPC / bid recommendation from Amazon Ads billing
- campaign structure write-back
- long-retention daily keyword history beyond the endpoint windows
- exact attribution from Amazon internal ad console
- first-party ABA Search Query Performance conversion funnel unless the user provides it

Use the outputs as directional research and combine with ad account data and/or ABA Search Query Performance before final budget decisions.
