---
name: amazon-keyword-traffic-analysis
description: >
  Use when user asks for keyword expansion or ad keyword filtering; single keyword analysis or
  keyword deep dive; whether a keyword is worth bidding on; which keywords drive traffic to an ASIN;
  ASIN keyword health, keyword traffic changes, or why an ASIN changed under a keyword. Supports
  batch keyword snapshot, multidimensional market profile, trend, and ASIN-keyword timeline
  workflows. Requires ZOODATA_API_KEY.
metadata:
  version: "0.1.3"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Amazon Keyword Intelligence

> Amazon keyword research and traffic analysis. Respond in user's language.

## Files

| File | Purpose |
|------|---------|
| `{skill_base_dir}/references/reference.md` | Load before tool selection; authoritative live-vs-planned endpoint status, batch contracts, exact parameters, response fields, and metric boundaries |
| `{skill_base_dir}/references/execution-guide.md` | Load before any full-mode task — contains input-to-endpoint routing, Evidence Capability Matrix, and full execution protocol |
| `{skill_base_dir}/references/scenarios-expand.md` | Load for keyword expansion output template |
| `{skill_base_dir}/references/scenarios-keyword-analysis.md` | Load for single-keyword analysis output template |
| `{skill_base_dir}/references/scenarios-reverse-asin.md` | Load for reverse ASIN output template |
| `{skill_base_dir}/references/scenarios-keyword-traffic-diagnosis.md` | Load for keyword traffic diagnosis output template |

## Credential

Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys).

## Capabilities & Data Flow

- **Network**: only `https://api.zoodata.ai` (Bearer `ZOODATA_API_KEY`). Setting `ZOODATA_BASE_URL` to any other host triggers a CLI warning — do not point it at hosts you don't trust.
- **Execution**: bundled shared ZooData CLI `{skill_base_dir}/scripts/zoodata.py` (Python 3, stdlib-only). The shared CLI exposes ALL ZooData endpoints as subcommands; this skill's workflows use: `keyword-detail`, `keyword-market-profile`, `keyword-trend`, `keyword-trend-profile`, `keyword-extends`, `keyword-search-results`, `keyword-competitor-product-keywords`, `keyword-product-traffic-terms`, `product-traffic-terms-overview`, `product-traffic-terms-timeline`, `check`. Do not invoke unrelated subcommands for this skill's tasks.
- **Local files**: none; reads the optional credential store `~/.zoodata/config.json`.
- **Sent to the API**: keywords, category paths, ASINs, marketplace/date and numeric filter values only. **Never sent**: budget, experience level, risk tolerance, or any other user-profile text — profile inputs map client-side to numeric filters.
- **Credits**: every API call consumes account credits. For broad or ambiguous requests, state the estimated credit cost and confirm with the user before running multi-call scans.

## Input

User typically provides one of:
- seed keyword
- target keyword
- ASIN
- ASIN + keyword
- marketplace and date range constraints

If marketplace is omitted, default to `US`. Keyword endpoints are keyword-query workflows: treat user-provided terms as search queries/keywords, not category paths or product search substitutes. If a keyword request requires `date` or `dateTo`, prefer T-1 or earlier instead of the current date; only use the current date when the user explicitly asks for today's data. In user-facing updates, state the selected marketplace/date without extra rationale unless the user asks why that date was selected.

## Data Source

Keyword demand and ABA-share fields come from Amazon Brand Analytics-derived snapshots; SERP, listing, placement, and ASIN traffic fields come from ZooData observations built around those keywords. Coverage is limited to observed keywords and ASIN placements. An item with `status=empty` means no matching observation in that snapshot/window, not proven low demand and not an API failure.

ZooData keyword endpoints provide search-demand, SERP, rank, and estimated-impression signals. They do **not** provide the seller's own ABA **Search Query Performance** conversion funnel, including ASIN-specific impressions, clicks, cart adds, purchases, conversion rate, or sales share. Therefore, keyword value judgments from this skill are directional prioritization, not 100% proof of commercial value.

ABA-SQP backend location: `Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View`

Recommended ABA-SQP data provision method:
- In Brand View, sort descending by `[Search Funnel - Impressions](https://sellercentral.amazon.com/brand-analytics/metric-glossary?linkedFrom=query-performance-brand-report-table-qp-impressions-group) -> Brand Count`, then provide a screenshot
- Alternatively, download the CSV and provide it for model analysis

Before writing traffic-related conclusions, identify the current evidence level and keep the reply inside that level:

- **Market evidence** — keyword market profile, trend, and SERP observations. It supports market structure and directional opportunity, not product-specific execution decisions.
- **Subject observation evidence** — market evidence plus observed ASIN, listing, placement, traffic, or timeline signals. It supports subject-specific fit, posture, movement, and evidence-supported bounded hypotheses, not measured seller conversion.
- **Seller-real evidence** — user-provided ABA-SQP and optionally Amazon Ads performance. It supports calibrated operating decisions within the fields provided.

### Conclusion Authority Gate (MANDATORY)

- Treat conclusions below seller-real evidence as provisional when the request concerns product-specific priority, conversion, profitability, bids, spend, or budget.
- Intermediate labels describe current posture or validation priority only; they do not authorize budget or bid changes.
- Prohibit fixed budget percentages, bid changes, pause decisions, unconditional `GO` / `NO-GO`, or profitability claims before the required seller-real evidence is present.
- If the next evidence level is required for the user's requested decision and unavailable, stop with `current evidence-level conclusion + unresolved decision + required next evidence`. Do not surface unrelated unresolved branches merely because later evidence could theoretically enrich them.
- Require Amazon Ads performance in addition to ABA-SQP for profitability, ACOS/ROAS, exact bid changes, or exact ad-budget allocation.

Use one short, localized `Data Notes` section near the top to name the current evidence level and conclusion boundary. Do not repeat it near the end and do not scatter the same caveat through individual findings. Use the scenario file to select the next evidence request; do not expose every possible future input at once.

When seller-private ABA-SQP data is present, name the provided fields used, such as impressions, clicks, cart adds, purchases, click share, purchase share, or conversion rate. Avoid deficit-framed wording; describe the next evidence level as the way to make the next decision more product-specific.

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
| `/openapi/v2/keywords/market-profile` | `keyword-market-profile` | `mcp__zoodata__openapi_v2_keyword_market_profile` |
| `/openapi/v2/keywords/trend-profile` | `keyword-trend-profile` | `mcp__zoodata__openapi_v2_keyword_trend_profile` |
| `/openapi/v2/keywords/trend` | `keyword-trend` | `mcp__zoodata__openapi_v2_keyword_trend` |
| `/openapi/v2/keywords/extends` | `keyword-extends` | `mcp__zoodata__openapi_v2_keyword_extends` |
| `/openapi/v2/keywords/search-results` | `keyword-search-results` | `mcp__zoodata__openapi_v2_keyword_search_results` |
| `/openapi/v2/keywords/competitor-product-keywords` | `keyword-competitor-product-keywords` | `mcp__zoodata__openapi_v2_keyword_competitor_product_keywords` |
| `/openapi/v2/keywords/product-traffic-terms` | `keyword-product-traffic-terms` | `mcp__zoodata__openapi_v2_keyword_product_traffic_terms` |
| `/openapi/v2/keywords/product-traffic-terms-overview` | `product-traffic-terms-overview` | `mcp__zoodata__openapi_v2_product_traffic_terms_overview` |
| `/openapi/v2/keywords/product-traffic-terms-timeline` | `product-traffic-terms-timeline` | `mcp__zoodata__openapi_v2_product_traffic_terms_timeline` |

### Layer and availability boundary

- Treat `detail`, `trend`, `extends`, `search-results`, both ASIN traffic-list endpoints, and `product-traffic-terms-timeline` as data endpoints: preserve their `items[]`, `rows[]`, or `series[]` evidence.
- Treat `market-profile` explicitly as a **metric-layer endpoint** derived from the same weekly snapshot source as the data-layer `detail` endpoint. Preserve `context`, per-item `status`, `unavailableReason`, `marketProfile`, and `context.scoringSpec`; never present scores without the returned scoring model/version/range/reference scope. Current item statuses are `available` and `not_found`. Check every scored dimension's `supported`, `calculationStatus`, `unsupportedReason`, `level`, and `levelEvidence.score.{value,direction}` independently—there is no aggregate `calculationCoverage` object. `marketCharacteristics.volatility` and `marketCharacteristics.annualSeasonality` are independent evidence objects and must not overwrite each other.
- Treat `trend-profile` as the metric layer for weekly demand and ABA-rank trend judgments. Preserve each keyword's `rows[]` by requested window, `status`, `rowContext`, both profile dimensions, and every `trendEvidence.value` / `direction` pair. Rows can be `available`, `unavailable`, or `not_found`; do not invent a reason when `unavailableReason` is null.
- Treat `product-traffic-terms-overview` as an aggregate endpoint. The live response is currently the legacy flat overview object with current and `*Prev` impression points plus first-3-page keyword entry/exit lists; do not assume the planned grouped metric objects exist.
- The design also defines `search-results-metrics`, `root-aggregate`, `product-traffic-term-changes`, and `product-traffic-terms-timeline-review`. These are planned metric endpoints, not currently callable on the verified production surface. Do not invent a separate `detail-metrics`; `market-profile` is the metric-layer profile sourced from `detail`-family snapshot data.
- Before using a metric endpoint, probe or inspect the live schema. If it returns 404, continue from the live data endpoints, calculate only transparent task-local aggregates, label them as Agent calculations, and name the missing server-side metric capability. Never fabricate `trendMetrics`, `demandLifecycle`, `competitionMetrics`, `keywordChanges`, or `timelineReview` as API-returned objects.
- Keep explanations, diagnoses, confidence, limitations, `nextBestCalls`, and recommended actions in the Agent/skill layer. Never claim that an API returned a root cause or strategy recommendation.

### Metric-First Access Gate (MANDATORY)

Keep these concepts separate:

- **Calculation coverage**: whether the service had enough source inputs to calculate a metric dimension. It limits the conclusion; it does not trigger data access.
- **Metric contract scope**: which indicators, summaries, reasons, and grains the metric endpoint intentionally returns.
- **Inference sufficiency**: whether that contract output is enough for the Agent's requested judgment. Only an inference-sufficiency gap can justify descending—and only when the data contract is known to add the missing information.

1. Define the exact judgment and evidence type before calling an endpoint.
2. Inspect the target surface for the matching metric endpoint and call the smallest sufficient metric request first.
3. Inspect item status, resolved period, the returned scoring/profile version, each dimension's calculation status, and the metric fields actually returned. For `market-profile`, require `status=available` before interpreting the profile; `status=not_found` means the keyword was not observed, not low demand.
4. If the metric fully supports the requested judgment, stop at the metric layer. Do not automatically call its source data endpoint for confirmation, enrichment, or completeness.
5. Treat each dimension's calculation status as a conclusion boundary, not an automatic fallback trigger. When metric and data are derived from the same source, missing metric inputs usually mean the data layer cannot restore that metric. Mark the dimension unavailable unless the data contract is known to contain different evidence that supports a different, valid Agent inference.
6. Access the data layer only when at least one condition holds:
   - no metric endpoint exists for the required capability, such as candidate recall or a current ASIN traffic-term list;
   - the metric endpoint is not deployed or fails for a metric-specific reason, and the data endpoint can transparently support the requested judgment;
   - the metric contract omits an indicator, row grain, time point, placement, or source field that the data contract explicitly provides and the Agent needs for the requested inference;
   - the user explicitly asks for raw rows, products, time-series points, field-level audit, or traceable source evidence;
   - the required claim depends on detail that the metric contract intentionally omits.
7. Do not descend merely because a metric item is `empty`, or a dimension is `unsupported`, `unknown`, or `unavailable`. First determine whether the data layer contains additional—not merely identical upstream—evidence.
8. When descending, call only the data endpoint and scope needed to fill the named inference gap. Do not rerun the whole lower-layer chain.
9. Record which required inference was not expressible from the metric and which additional data fields/grain are expected to resolve it. A metric-first run must not silently become a metric-plus-data run.

### Batch-First Request Gate (MANDATORY)

Apply this gate after endpoint/layer selection:

1. Collect all requested or shortlisted subjects that share the selected endpoint's non-subject parameters.
2. If the endpoint supports batch, send the largest valid batch instead of looping over single-subject calls.
3. Batch compatibility requires the same marketplace, date or date range, granularity, lookback/window, filters, and sort context. Timeline batches must also share one ASIN.
4. Deduplicate subjects case-insensitively while preserving first-occurrence order.
5. Use batches of at most 20. For 21+ compatible subjects, send sequential chunks of 20 and merge `data.items[]` back into global input order.
6. Use a single-subject call only when there is one subject, request contexts differ, or the endpoint has no batch contract.
7. Do not split a batch merely to simplify parsing. Inspect each item's `status`, retain `empty`/`error` items, and continue with successful items.
8. Batch capability improves execution efficiency; it never justifies calling an otherwise unnecessary endpoint or both metric and data layers.

### Batch contract

- `keyword-detail`: pass exactly one of `--keyword` or `--keywords "term one,term two"`; API fields are `keyword` / `keywords[]`.
- `keyword-market-profile`: use the same single-or-batch subject contract as `keyword-detail`; up to 20 keywords share the snapshot date, marketplace, and weekly granularity.
- `keyword-trend-profile`: use exactly one of `--keyword` or `--keywords` plus `--date` and `--window-periods`; up to 20 keywords share 1–4 unique windows selected from `4,8,12,26`, marketplace, and weekly granularity.
- `keyword-trend`: pass exactly one of `--keyword` or `--keywords`; all items share `dateFrom`, `dateTo`, marketplace, and weekly granularity.
- `product-traffic-terms-timeline`: pass one ASIN and exactly one of `--keyword` or `--keywords`; up to 20 keywords share the same range and 7-day rolling window.
- Preserve `data.items[]` input order. Read each item's `identity`, `status`, `emptyReason`, `errorCode`, `errorMessage`, and evidence object independently; outer `success=true` does not mean every item succeeded.
- Do not drop empty/error items from the user's requested set. Report their per-item reason and continue with successful items.
- Batch billing is per successful item: preflight may check the full subject count, but final credits correspond to `status=ok`; `empty` and `error` items are not billed. Use returned `meta.creditsConsumed`, never infer charges.
- For 21+ keywords, chunk into batches of at most 20 and preserve global input order when merging. Deduplicate case-insensitively before calling because duplicate batch subjects return 422.

If the live session exposes a different name, use that name exactly.

**PROHIBITED — never do any of the following:**
- Choose or reject a tool from its name alone before reading the relevant docs/help/schema
- Declare a keyword endpoint unavailable without first checking `zoodata.py`, and then the live tool surface/schema if needed
- Say "the keyword-volume interface is not available" because you didn't see a tool named "keyword volume"
- Use `products/search` as a substitute for keyword endpoints and label its results as keyword traffic evidence
- Treat any ZooData WebTools endpoint, including callable `webtools_search`, as a keyword-intelligence endpoint
- Bypass ZooData data/crawler APIs by opening an external or built-in interactive browser tool, navigating directly to Amazon outside ZooData, or using public web search
- Use browser or public-web access after a ZooData call fails, returns empty data, lacks a field, or cannot be reached
- "Normalize" a live callable name back to the draft name above

**Capability signals in live schema:** If a tool exposes fields such as `estimateSearchCountWeekly`, `estimateSearchCount`, `keywordEstimateSearchCount`, or `abaRank`, treat it as having keyword-volume capability even if its name is not explicit.

**Tool boundary rules (CRITICAL — do not misclassify):**

| Tool | Role | NEVER use it as |
|------|------|-----------------|
| `/openapi/v2/keywords/*` | Keyword intelligence (snapshot, trend, SERP, ASIN traffic) | — |
| `products/search` | Product-database snapshot — broader catalog winners, price-band structure, variant distribution | Keyword SERP evidence, keyword demand proof, or a front-end search interface |
| `/openapi/v2/webtools/scrape` and `/scrape-interactive` | ZooData page extraction, including rendered or interaction-dependent page content | Keyword snapshot, trend, observed Amazon SERP, traffic, or seller-private data |
| `/openapi/v2/webtools/search` (`webtools_search` when exposed under that callable name) | ZooData web-search and optional result-page extraction | Keyword snapshot, trend, observed Amazon SERP, traffic, or seller-private data |

### ZooData Acquisition Channel Gate (MANDATORY)

ZooData data APIs and ZooData crawler/retrieval APIs are the authorized acquisition channels for this skill. Tool choice may move between these channel types according to the evidence required, but it must not bypass ZooData and access a browser, Amazon page, or public web-search tool directly.

1. Use the ZooData data endpoint designed for the required evidence first, including `realtime/product` for live ASIN/product fields and `/openapi/v2/keywords/*` for keyword evidence.
2. When a known page URL contains evidence absent from the structured data endpoints, use ZooData WebTools `/scrape`; use `/scrape-interactive` only when rendering or page actions are required. Use WebTools `/search` only when the URL itself must first be discovered. Label all three as crawler/retrieval evidence and keep them within their evidence boundary.
3. Do not invoke an external or built-in interactive browser tool, browser automation outside ZooData WebTools, direct Amazon-page navigation outside ZooData, or a general/public web-search tool as a fallback, supplement, confirmation step, or workaround.
4. A failed, empty, unavailable, or incomplete ZooData endpoint does not authorize browser or public-web fallback. Check the documented ZooData data and crawler surfaces; if neither can obtain the required evidence, stop at the supported conclusion and request the minimum user-provided evidence.
5. Do not confuse acquisition priority with evidence equivalence: all ZooData WebTools results remain crawler/retrieval evidence and must not be presented as keyword snapshot, trend, observed Amazon SERP, traffic, or seller-private conversion data.

## Task Constraints

These constraints are higher priority than any suggested workflow wording in reference files.

### Evidence Gate

- Do not produce a conclusion unless the scenario's minimum evidence is available
- If minimum evidence is missing, stop or downgrade the answer and name the missing evidence explicitly
- Do not silently backfill a missing keyword endpoint with another non-equivalent interface
- Apply the Metric-First Access Gate before every evidence call; scenario endpoint lists describe capabilities, not a requirement to call every listed endpoint

### Non-Substitution Rules

- `products/search` must not be used as a substitute for keyword snapshot, keyword trend, keyword SERP, or reverse-ASIN traffic evidence
- No ZooData WebTools endpoint may substitute for any `/openapi/v2/keywords/*` endpoint
- `keywords/detail` and `keywords/search-results` must not be used to fabricate reverse-ASIN traffic-source maps when neither ASIN traffic-list endpoint is available
- `keywords/trend` must not be treated as daily history; `keywords/search-results` and ASIN keyword endpoints must not be treated as long-retention weekly trend series

### Confidence Gate

- `Data-backed` conclusions require direct support from the endpoint actually designed for that evidence type
- `Inferred` conclusions require multiple supporting fields that materially discriminate the explanation from alternatives and must stay within the endpoint boundary
- `Directional` conclusions may frame validation or monitoring advice, but they do not authorize an action that fails the Evidence-to-Action Authorization Gate and must not be phrased as proven causality
- If a required evidence type is absent, lower the confidence instead of strengthening the wording
- Keyword-value judgments such as "worth targeting", "high value", "profitable", or "conversion potential" are never 100% supported by ZooData alone because the available data is estimated exposure/search/visibility data, not the user's ABA Search Query Performance funnel
- Without Search Query Performance data, phrase keyword-value and traffic-related conclusions as directional testing priority. Use the active scenario file to determine the next evidence request.
- If user-provided ABA-SQP data is available, use it to refine traffic and keyword-value conclusions and do not add the seller-side SQP enrichment request

### Evidence-Seeking Reasoning Gate (MANDATORY)

Apply this gate to every diagnosis, regardless of scenario or evidence level:

`observed fact → identified problem → unresolved question → required discriminating evidence → evidence acquisition → evidence-supported explanation → authorized action`

Hard rules:

- Detecting an anomaly, weak funnel stage, movement, or mismatch identifies a problem; it does not explain the cause.
- After identifying a problem, define the unresolved question and seek the smallest available evidence that can distinguish among material explanations before answering why it happened.
- Do not replace missing evidence with a generic list of plausible causes. Compatibility with a pattern is not evidence for a cause.
- Name alternative explanations only when they define the evidence search or when existing evidence supports them as bounded hypotheses. Do not present unsupported alternatives as findings.
- A cause, diagnosis, test, or corrective action requires direct or sufficiently discriminating evidence for that explanation. Apply the Evidence-to-Action Authorization Gate separately afterward.
- Open a causal-diagnosis branch only when the user asked for it or when resolving it is necessary for the requested decision. If the supported operating decision does not require a causal explanation, omit the unused diagnostic branch instead of adding a disclaimer or a list of factors to investigate.
- Once a diagnostic branch is opened, close it in the same run: acquire the discriminating evidence when it is available through authorized in-scope tools or already-provided context. Do not stop at “further investigation is needed” while usable evidence remains.
- If required evidence must come from the user or is genuinely unavailable, carry that exact unresolved question into the single end-of-report next step. Request only evidence that directly distinguishes the named explanations and state which decision it unlocks.
- Do not name an unresolved question in the findings and then request evidence for a different question at the end. If the next evidence cannot resolve the diagnostic branch, omit that branch from the report.
- When an unresolved explanation is necessary to the user's requested decision and evidence is unavailable, stop at `identified problem + unresolved question + minimum next evidence + decision that remains unresolved`. When it is not necessary, answer the supported decision and omit the unresolved explanation.
- Do not insert defensive disclaimers about specific assets or settings that have not entered the evidence chain. State the evidence boundary at the problem-domain level instead.

### Evidence-to-Action Authorization Gate (MANDATORY)

The specificity and consequence of an action must not exceed the specificity and strength of its evidence. Apply this gate separately from confidence labels; cautious wording does not authorize an unsupported action.

Before proposing an action, identify the exact target, whether that target was directly observed at sufficient fidelity, the specific defect signal, material alternative explanations, available validation, and the action's reversibility/impact.

- `Inspect`: allowed when a broad signal identifies a relevant problem domain.
- `Diagnose`: allowed when evidence supports multiple bounded hypotheses; retain alternatives and do not select an unproven root cause.
- `Test`: requires direct observation of the target, a specific defect hypothesis, a reversible test, and predefined success/failure criteria.
- `Change`: requires direct target evidence and stronger validation that distinguishes it from material alternatives.
- `Scale` / `Stop`: requires seller-real outcome evidence and decision thresholds proportionate to the financial impact.

Hard rules:

- If the target was not directly inspected, stop at `Inspect` for that target.
- Broad funnel weakness can identify a handoff/problem domain but cannot authorize changes to a specific listing asset, keyword, campaign setting, offer, price, variation, or fulfillment setting.
- Low-fidelity evidence authorizes only conclusions at that fidelity. A search-result thumbnail cannot support claims about full-size detail, secondary images, mobile readability, texture, dimensions, or image sequence.
- If an asset was not inspected, recommend auditing it rather than modifying, replacing, removing, or rebuilding it.
- When evidence is insufficient, downgrade the action itself—not merely its confidence label or wording. Words such as `consider`, `possibly`, and `directionally` do not upgrade authorization.
- Preserve the chain `observed fact → identified problem → unresolved question → discriminating evidence → evidence-supported explanation → authorized action`; never skip evidence acquisition or replace it with generic candidate causes.

See `references/execution-guide.md § Evidence-to-Action Protocol` for the operational checklist and examples.

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
- When ZooData crawler/retrieval or other ZooData enrichment endpoints are used, state their role precisely and do not blur their evidence class
- If any live ZooData API call was made, the final report must end with `API Usage`; do not omit it even when the user did not ask for it explicitly
- Track endpoint usage while calling APIs: read `_query.endpoint` and `_query.params` when returned; otherwise record the ZooData endpoint and request parameters actually invoked. Read `meta.creditsConsumed` and `meta.creditsRemaining` when present.
- In `API Usage`, use a markdown table, not a bullet list; aggregate calls and `meta.creditsConsumed` by endpoint; include a final `Total` row that sums calls and credits; use the latest returned `meta.creditsRemaining` for credits remaining
- If a response omits `meta.creditsConsumed` or `meta.creditsRemaining`, write `not returned` for that field rather than dropping the usage section
- Avoid competitor-superiority wording in findings and recommendations unless the Comparative Claims Gate is satisfied
- Do not interrupt individual findings with evidence requests. Put exactly one scenario-appropriate next-step request at the end of the reply.
- If the user has provided ABA-SQP search conversion data, do not repeat the seller-side SQP enrichment request; instead, cite the relevant SQP signal in the conclusion when it changes precision or confidence
- In full-mode reports, include one standalone `Data Notes` section near the top that names the evidence level and conclusion boundary. Do not add a duplicated end reminder.

## API Pitfalls (CRITICAL)

1. `keywords/extends` uses `query`, not `keyword`
2. `keywords/detail` resolves to the nearest available weekly snapshot at or before the requested date. `keywords/extends` uses the latest available weekly snapshot; legacy `date` is optional and ignored by the service.
3. Keyword endpoints are keyword-query interfaces; for inputs named `keyword` or `query`, use the Amazon search query / keyword phrase being analyzed
4. When a keyword endpoint requires `date` or `dateTo`, prefer T-1 or earlier and avoid using the current date unless the user explicitly asks for today's lookup; do not proactively explain the reason unless asked
5. `keywords/trend` is weekly time series, not daily. CLI usage must use full ISO dates with these exact flags: `keyword-trend --keyword "small baskets for organizing" --date-from 2026-04-01 --date-to 2026-07-02 --marketplace US`; never send truncated dates, ellipses, natural-language dates, reversed ranges, or ranges longer than 93 days.
6. `keywords/search-results` and ASIN keyword endpoints are recent `lately_day` observations with `lookbackDays=7`, not long-retention history. `keyword-trend` accepts up to 93 days; `product-traffic-terms-timeline` accepts up to 61 days.
7. `keywords/detail` returns `data.context + data.items[]`; an unmatched keyword is an item with `status=empty` and `emptyReason`, not a top-level API failure.
8. `keywords/market-profile` returns `data.context + data.items[]`; use its server-calculated dimensions as snapshot evidence only. Require `status=available`, read `context.scoringSpec`, and inspect each dimension's `supported`, `calculationStatus`, `unsupportedReason`, `level`, and `levelEvidence.score.{value,direction}` independently. Treat any unavailable signal as a conclusion boundary. The endpoint does not provide history, recommendations, root cause, or seller-private conversion data. It is currently pre-release on localhost; check the live surface before calling it elsewhere.
9. `keywords/extends` returns `data.context + data.rows[]`; an empty `rows[]` is valid. Try both `queryType=phrase` and `queryType=fuzzy` before concluding low expandability.
10. `trafficShare` is an observed share within the endpoint's sampled window; do not present it as exact Amazon share of voice
11. SERP analysis must separate `exploreType`: `ORG` vs `SP` vs `SB` vs `SBV` vs `SPR`
12. Monitoring conclusions require comparison across at least 2 timestamps; single-day movement is directional only
13. `/openapi/v2/keywords/search-results` already returns listing-level product fields and should be the default source for "what products appear on page 1 for this keyword"
14. `keywords/market-profile` uses `marketCharacteristics`. Scored dimensions expose `levelEvidence.score.value` and `.direction`. Treat `volatility.type` and `annualSeasonality.classification` as separate results; never invent peak periods or collapse them into one seasonality label.
15. A `market-profile` batch HTTP 500 is a service failure, not `not_found`. Do not automatically retry every subject individually. At most one diagnostic split is allowed when isolating the failing subject is necessary; otherwise stop at the failed metric request and report the missing judgment.
14. Do not append `products/search` by default when the user's question is only about the observed keyword SERP; use it only as an optional broader-market supplement
15. `products/search` is our own product-database query result, not Amazon live search results, so never present it as evidence of current SERP ordering
16. ZooData WebTools endpoints are crawler/retrieval utilities, not keyword-intelligence endpoints. Use `/scrape` for a known page URL, `/scrape-interactive` only when rendering/actions are necessary, and `/search` only to discover URLs; never treat any of them as a substitute for keyword snapshot, trend, observed Amazon SERP, traffic, or seller-private evidence.
17. `keywords/product-traffic-terms-overview` returns weekly all-keyword impression traffic changes under one ASIN versus the previous period, with placement-level `*ImpressionPoint` fields and matching `*Prev` baselines; `first3PagesNewOrganicKeywords` lists keywords newly entering ORG first three pages, and `first3PagesLostOrganicKeywords` lists keywords that dropped out; do not treat it as per-keyword daily rank history
18. For `keywords/product-traffic-terms-overview`, display the returned `periodStartDate` / `periodEndDate` as the overview period; do not use the request date or an inferred date range as the period shown in the report
19. `keywords/product-traffic-terms-timeline` returns `data.context + data.items[].series[]`; interpret each series point's nested groups separately:
    - `keywordMetrics` belongs to `metricWindow.keywordPeriodStartDate/keywordPeriodEndDate`
    - `asinSnapshot` is the product/listing/rank snapshot on `series[].date`
    - `traffic`, `placement`, and `adActivity` describe the 7-day rolling window ending on `series[].date`
20. HTTP 422 means request validation failed, not a transient network error. Do not retry the same request repeatedly. Read the returned error detail and fix parameters first, especially full `YYYY-MM-DD` date strings, required fields, date range order, and endpoint-specific range limits.

## On Missing Key

When `ZOODATA_API_KEY` is not set, verify with `python {skill_base_dir}/scripts/zoodata.py check` (credentials-only, no endpoint calls or credit usage; exits non-zero if no key is found in the supported config locations). Then STOP before any endpoint call, direct the user to https://zoodata.ai/en/api-keys, and do not substitute public knowledge, web search, or a boundary-labeled "partial analysis" for missing ZooData evidence.

## On 401 Invalid Key

When the API returns code 401: stop further calls, tell the user the key was rejected, and direct them to https://zoodata.ai/en/api-keys. Do not fabricate missing data.

## On 402 Credit Exhausted

When the API returns code 402: stop further calls, report partial findings already gathered, estimate remaining credits needed, and direct the user to https://zoodata.ai/en/pricing. Do not fabricate missing data.

## Decision Framework

### Keyword Fit Assessment

Judge each candidate keyword on four dimensions:

| Dimension | What to look at | Interpretation |
|-----------|------------------|----------------|
| Demand | `snapshotData.estimateSearchCount`, trend `series[].estimateSearchCount`, ABA rank | Higher demand is better, but only if stable enough |
| Competition | `marketProfile` difficulty/saturation/ad dimensions when covered; otherwise `adCount`, `adCampaignCount`, SERP ad density, head ASIN concentration | Higher competition raises bid difficulty |
| Relevance | seed relation, `relevanceScore`, SERP title/brand fit | High relevance means better listing/ad fit |
| Accessibility | organic entry room, ad crowding, whether current leaders are entrenched | Indicates whether traffic is realistically capturable |

Important boundary:
- These dimensions estimate search opportunity and visibility accessibility, not actual keyword commercial value for the user's ASIN
- Do not claim a keyword is definitively profitable, high-converting, or worth full budget from ZooData alone
- When only market-level evidence is present, keep value conclusions directional and request an ASIN at the end. After ASIN observation and batch candidate validation, request seller-side SQP. If SQP is included, use query-level impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate as first-party conversion evidence.

### Recommendation Labels

These are candidate-validation labels only. They rank which terms deserve seller-funnel validation and must not be presented as final expansion or spend decisions.

- `Priority test` — good balance of demand, relevance, and manageable competition
- `Selective test` — deserves narrow seller-funnel validation; this label does not select an ad group or match type
- `Harvest` — lower demand but strong product relevance; deserves controlled long-tail validation without prescribing bids or match type
- `Observe only` — interesting but not ready for budget allocation
- `Avoid` — weak relevance, poor market structure, or no credible entry path

### Reverse-ASIN Labels

- `Defend` — observed defend posture because the term is already meaningful for traffic or position; not permission to change bids/budgets
- `Expand` — observed expansion-candidate posture with room to improve visibility; not permission to scale
- `Observe` — potentially useful but weak, unstable, or incomplete
- `Avoid` — low fit, weak position, or crowded without a clear path

## Output Spec

Use the stage-specific structure in `execution-guide.md § Evidence-Level Progression` and the active scenario's journey/template. Do not force later-stage sections into an earlier-stage reply. Any report that used live API data must still end with `API Usage`.

### Language (required)

Output language MUST match the user's input language. Technical field names and endpoint names may remain in English.

### Disclaimer (required at the top of every Full-mode report)

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.

Quick-mode lookups follow `execution-guide.md § Quick Mode Output` and may use a concise inline source/date note instead of this block.

For keyword-value reports, add this note:

> ZooData provides estimated exposure/search/visibility signals. State the current evidence level and keep conclusions within that boundary; use the next-step request defined by the conversational evidence ladder.

### Confidence Labels (required for every substantive judgment or recommendation)

- 📊 **Data-backed** — direct API data
- 🔍 **Inferred** — reasoning from multiple observed fields that materially discriminate the conclusion from alternatives
- 💡 **Directional** — evidence-bounded validation or monitoring advice; hypotheses still require supporting evidence and must retain unresolved alternatives

Rules:
- Strategy recommendations are NEVER 📊
- Keyword-value verdicts without user-provided Search Query Performance data are NEVER above 💡
- Traffic-related conclusions without user-provided ABA-SQP search conversion data are NEVER above 💡 when they imply spend/value priority; do not repeat the seller-side SQP enrichment request inside the conclusion body
- Single-day anomaly explanations are NEVER above 💡
- Group headers and aggregate labels must not use stronger confidence than their contents
- Pure status fields such as resolved dates, unavailable evidence, or lists of unresolved decisions do not need a confidence tag

For API Usage format and credit tracking rules, see `execution-guide.md § Usage Accounting Rule`.

## Limitations

This skill does not provide:
- real CPC / bid recommendation from Amazon Ads billing
- campaign structure write-back
- long-retention daily keyword history beyond the endpoint windows
- exact attribution from Amazon internal ad console
- first-party ABA Search Query Performance conversion funnel unless the user provides it

Use the outputs as directional research and combine with ad account data and/or ABA Search Query Performance before final budget decisions.
