# Execution Guide — Amazon Keyword Intelligence

This file defines the task-constraint protocol for the four keyword scenarios.

## Contents

- [Execution Mode](#execution-mode)
- [Evidence-Level Progression](#evidence-level-progression)
- [Evidence-Seeking Diagnosis Protocol](#evidence-seeking-diagnosis-protocol)
- [Evidence-to-Action Protocol](#evidence-to-action-protocol)
- [Seller Data Contract](#seller-data-contract)
- [Quick Mode Output](#quick-mode-output)
- [Full-Mode Checklist](#full-mode-checklist)
- [Evidence Capability Matrix](#evidence-capability-matrix)
- [General Rules](#general-rules)
- [Output Rules](#output-rules)

## Execution Mode

| Task Type | Mode | Behavior |
|-----------|------|----------|
| Single lookup such as one snapshot field | Quick | Return the key metric with light interpretation |
| Expansion, full keyword judgment, reverse ASIN, keyword traffic diagnosis | Full | Run only the evidence calls justified for the current stage, apply scoring, and output API usage |

## Evidence-Level Progression

Apply these rules to every full-mode scenario. Scenario files define their own stage sequence, inputs, and next-step prompts.

| Evidence level | Evidence scope | Maximum conclusion authority |
|----------------|----------------|------------------------------|
| Market evidence | Keyword demand, trend, market profile, and SERP observations | Market attractiveness, structure, relative difficulty, and directional opportunity |
| Subject observation evidence | Market evidence plus observed ASIN, listing, placement, traffic, or timeline signals | Subject-specific fit, current posture, movement, and evidence-supported bounded hypotheses |
| Seller-real evidence | User-provided ABA-SQP funnel and, when relevant, Amazon Ads performance | Calibrated operating decisions, subject to the fields actually provided |

### General Progression Rules

- Determine the highest evidence level currently available before selecting endpoints or drafting conclusions.
- Never allow a conclusion to exceed the authority of its supporting evidence level.
- Treat all conclusions below seller-real evidence as provisional when the request concerns product-specific priority, conversion, profitability, bids, spend, or budget.
- Request only the next evidence that resolves the named decision gap. Do not expose every possible future input at once.
- If the user already supplied higher-level evidence, skip unnecessary earlier steps. A scenario sequence is not a mandatory call chain.
- Reuse compatible evidence already obtained in the conversation. Do not repeat API calls when subject, marketplace, period, filters, and required grain are unchanged.
- Keep observed facts, Agent inference, provisional action, and final action distinct.
- If evidence required for the user's requested decision is unavailable, stop with three logical parts: current evidence-level conclusion, unresolved decision, and required next evidence. Omit unresolved branches that are not needed for that decision.

### General Conclusion Authority Gate

- Market evidence cannot support product-specific priority, measured conversion performance, profitability, bids, spend, budget allocation, or unconditional go/no-go decisions.
- Subject observation evidence cannot support measured click/conversion claims without seller funnel data, and it cannot support profitability or exact ad-budget decisions without Ads performance.
- Intermediate labels describe current posture or validation priority only; they do not authorize execution changes unless the scenario explicitly reaches seller-real calibration.
- Use bounded language before seller-real calibration: `merits further validation`, `controlled-test candidate`, `current evidence does not support advancing`, or `awaiting seller evidence`.
- Reserve `Final calibrated conclusion` for decisions supported by the relevant seller-real fields.
- Require Amazon Ads performance in addition to ABA-SQP for profitability, ACOS/ROAS, exact bid changes, or exact ad-budget allocation.

## Evidence-Seeking Diagnosis Protocol

Apply this protocol whenever the task asks what is wrong, why a metric moved, or what explains a funnel pattern.

1. Record the observed fact without causal language.
2. Identify the narrowest problem domain supported by that fact.
3. Convert the problem into an unresolved question.
4. Identify the smallest evidence that can distinguish among material explanations.
5. Acquire that evidence when it is available through authorized in-scope tools or already-provided context; do not finalize while a usable discriminating source remains unchecked.
6. Form an explanation only from the evidence actually obtained, while retaining material alternatives not yet ruled out.
7. Apply the Evidence-to-Action Protocol before recommending a test, change, scale, or stop decision.

All evidence acquisition in this protocol must use ZooData-owned acquisition channels. Use the matching structured data API first. For a known page URL, use ZooData WebTools `/scrape`; use `/scrape-interactive` only when rendering or page actions are required, and `/search` only when the URL must first be discovered. Never switch to an external interactive browser, direct Amazon navigation, or public web search. If neither ZooData channel can obtain the discriminating evidence, carry that exact gap into the single next-step request for user-provided evidence.

An anomaly is not a diagnosis. Do not fill an evidence gap with a standard inventory of possible causes. A list of compatible causes is allowed only as an internal evidence-search map or when each reported hypothesis has supporting evidence. If discriminating evidence is unavailable, report the identified problem, the unresolved question, the minimum next evidence, and the decision that cannot yet be made.

### Diagnostic Closure Gate

- Open a diagnostic branch only when the user requested a causal explanation or when the requested operating decision depends on resolving it.
- If the current evidence already supports the requested operating decision without explaining cause, state that decision and omit unused causal discussion. Do not append “this is not caused by X” or “factors Y/Z require investigation” merely to demonstrate caution.
- Every diagnostic branch mentioned in the report must end in exactly one of three states: `resolved by cited evidence`, `actively pursued with an in-scope evidence call`, or `carried into the single Next Step with directly matching evidence`.
- The requested next evidence must discriminate the exact explanations named in the unresolved question. Evidence for Ads economics/order attribution does not by itself resolve detail-page, price, promotion, offer, fulfillment, variation, or asset-quality explanations.
- If no available or requestable evidence can resolve the branch, omit the branch unless the user's explicit question requires reporting that it is unresolved.
- Do not continue the report as though a diagnostic branch were closed after writing only “further investigation is needed.”

## Evidence-to-Action Protocol

Apply this protocol after scoping the conclusion and before writing recommendations. Confidence labels describe evidentiary strength; they do not authorize a more specific action.

### Authorization checklist

For every proposed action, record:

1. **Target** — exact asset, field, keyword, campaign setting, offer, or business decision affected.
2. **Direct observation** — whether the target was inspected at sufficient fidelity.
3. **Defect signal** — the concrete issue observed on that target.
4. **Alternatives** — material alternative explanations that the evidence search must distinguish; compatibility alone does not make them findings.
5. **Validation** — comparison, experiment, time series, or first-party measurement that distinguishes the target from alternatives.
6. **Impact** — reversibility, cost, and downside if the action is wrong.

Map the evidence to the highest authorized action level:

| Level | Minimum authorization |
|-------|-----------------------|
| `Inspect` | A broad signal identifies a relevant problem domain |
| `Diagnose` | Multiple bounded hypotheses are supported and alternatives remain explicit |
| `Test` | The target was directly observed, a specific defect hypothesis exists, and the test is reversible with predefined success/failure criteria |
| `Change` | Direct target evidence plus validation distinguishes the target from material alternatives |
| `Scale` / `Stop` | Seller-real outcome evidence and thresholds justify the financial consequence |

If any required condition is absent, downgrade the action itself. Do not retain a `Change`, `Scale`, or `Stop` action by softening its wording.

### General examples

| Available evidence | Not authorized | Authorized next action |
|--------------------|----------------|------------------------|
| Clicks/cart adds but weak purchases | Rebuild the first three secondary images or list generic conversion causes | Locate the unresolved issue at the post-click/purchase handoff, then request the smallest evidence that can distinguish traffic quality from purchase-condition explanations |
| Search-result main-image thumbnail only | Rebuild the main image or secondary images | Inspect thumbnail-level subject recognition and request the full image set for asset-level review |
| High ACOS alone | Lower bids by a fixed percentage | Diagnose search-term CPC, conversion, placement, and attribution; define a reversible bid test only after target-level evidence |
| Organic rank decline | Pause the keyword or list every compatible cause | Define which movement remains unexplained, then retrieve the smallest time-aligned evidence that can distinguish demand, placement, subject, and market movement |
| Review deterioration | Redesign the product | Cluster complaint themes and validate frequency, recency, variant scope, and product causality |

Anti-pattern: `Current evidence does not support attributing this to the main image or title; detail-page persuasion, price, promotion, fulfillment, variation, and traffic source require further distinction.` This opens several unsupported branches without pursuing them. If causal diagnosis is not required, omit it and state only the supported operating implication. If it is required, retrieve or request evidence that directly resolves the named branch before continuing.

Acquisition anti-pattern: opening the Amazon detail page in an external browser because SQP shows clicks or cart adds without purchases. First use ZooData structured endpoints such as `realtime/product`; for page evidence absent from structured responses, use ZooData WebTools `/scrape` or `/scrape-interactive` as required. External browser and public-web fallback are prohibited even when those ZooData calls are incomplete or unavailable.

### Asset-fidelity rule

State what representation was actually observed when an asset enters the diagnosis: full-resolution asset, detail-page rendering, mobile rendering, search-result thumbnail, URL/change event, or no visual observation. An asset URL or detected change event proves that an asset changed, not that its content is defective or caused the performance movement.

### Seller Data Contract

When a scenario advances to seller-real evidence, request ABA-SQP from `Brand Analytics → Search Analytics → Search Query Performance → Brand View`. Recommend sorting by `Search Funnel - Impressions → Brand Count` and accept screenshot or CSV. Prefer these fields:

| Funnel stage | Fields |
|--------------|--------|
| Impressions | Total Count, Brand Count, Brand Share |
| Clicks | Total Count, Click Rate, Brand Count, Brand Share |
| Cart Adds | Total Count, Brand Count, Brand Share |
| Purchases | Total Count, Brand Count, Brand Share |

If the user also wants profitability or final ad-budget allocation, request Search term, Match type, Impressions, Clicks, Spend, Orders, Sales, CPC, CVR, and ACOS or ROAS.

When seller funnel data is available, compare `impression share → click share → cart-add share → purchase share` rather than judging from click count alone. Use share gains as evidence of funnel strength and share losses to locate the likely handoff problem. When the required SQP/Ads fields are present and the Evidence-to-Action Protocol authorizes them, a calibrated strategy may cover core defense, priority expansion, long-tail harvest, controlled tests, lower-bid/negative terms, budget, 7–14 day validation metrics, and explicit decision thresholds.

| Funnel pattern | Interpretation | Default action |
|----------------|----------------|----------------|
| Click share > impression share | The search-to-click handoff is comparatively strong; this pattern does not by itself explain which factor produced it | Consider an exposure test only after Ads economics and target-level evidence support it |
| Cart-add share rises again | Product acceptance is comparatively stronger | Upgrade the validation posture; authorize a test/change only through the Evidence-to-Action Protocol |
| Purchase share rises again | Query-level seller conversion evidence is comparatively stronger | Mark as a focused-expansion candidate; require Ads economics before scaling, match-type, bid, or budget execution |
| Click share is high but purchase share is low | The unresolved issue is in the post-click/purchase handoff; SQP alone does not identify its cause | Obtain the smallest evidence that distinguishes traffic quality from purchase-condition explanations; if unavailable, stop without enumerating generic causes |
| Impressions are high but clicks are low | The unresolved issue is in the search-to-click handoff; SQP alone does not identify its cause | Obtain the smallest evidence that distinguishes intent/placement from the visible search offer; if unavailable, stop without selecting a cause |
| Click and purchase performance are good but market difficulty is high | The query is efficient in the supplied seller funnel but may be expensive to scale | Diagnose Ads economics and define controlled scale thresholds before authorizing expansion |
| Market profile is favorable but the ASIN funnel is weak | The market may be viable while the ASIN is not capturing it; the responsible factor is unresolved | Define and acquire the minimum evidence needed to distinguish market capture, traffic quality, and purchase-handoff explanations before selecting a change or scaling |

## Quick Mode Output

For single-lookup tasks (e.g., "what's the search volume for X", "what's the ABA rank for X", "show me the SERP for Y"):

- Answer the specific metric(s) directly with field name and value
- Tag each value with one confidence label: 📊 for direct API field, 🔍 if derived
- State endpoint and snapshot date inline: e.g., `(source: keywords/detail, snapshot 2024-06-28)`
- No Data Provenance table required
- API Usage table is required, same format as Full Mode: markdown table with `Endpoint / Calls / Credits` columns, a `Total` row, and `Credits remaining: N` on the final line; if credit fields are absent, write `not returned`
- No full report disclaimer block required; if the metric is traffic-related and the current evidence set does not include ABA-SQP data, keep the answer directional and add at most one concise data-basis note after the answer, not inside each metric explanation
- Do not upgrade a Quick task to Full mode unless the user's follow-up questions expand the scope

## Full-Mode Checklist

Before running any Full-mode keyword task:

- [ ] Read the relevant tool documentation before selecting the tool: CLI help/reference docs for `zoodata.py`, or live schema / field descriptions for MCP/session tools
- [ ] Write down the required judgment/evidence type and select its metric endpoint first; do not begin from a fixed data-endpoint chain
- [ ] Inspect metric item status, period, returned scoring/profile version, each dimension's calculation status, and the fields exposed for the required inference
- [ ] If the metric satisfies the inference, stop; if it does not, determine whether data actually contains additional evidence before calling it—an unsupported/unavailable dimension alone is not a fallback reason
- [ ] Prefer `python {skill_base_dir}/scripts/zoodata.py` and choose the matching keyword subcommand after the documentation check
- [ ] If you need session tool parity or fallback, inspect the active tool surface and read the live schema / field descriptions for candidate keyword tools before selecting or judging capability
- [ ] Classify the task: seed keyword / target keyword / ASIN / ASIN + keyword
- [ ] Confirm marketplace; default to `US` if absent
- [ ] For endpoints independently justified by the inference plan, group compatible subjects into batch calls. `detail`, `market-profile`, `trend-profile`, and `trend` accept up to 20 keywords; timeline accepts one ASIN plus up to 20 keywords. Batch support does not justify calling multiple layers.
- [ ] Before the first call to a batch-capable endpoint, collect the complete compatible subject set; do not issue per-keyword calls when one batch or sequential 20-item chunks can serve the same context
- [ ] Check `reference.md § Production availability`; never route to a planned metric endpoint merely because it appears in the design.
- [ ] Confirm the date lens: weekly snapshot, recent 4-8 weeks, or latest sliding window; for keyword lookups that require `date` or `dateTo`, prefer T-1 or earlier and avoid the current date unless explicitly requested. In user-facing progress updates, simply state the selected marketplace/date without extra rationale unless the user asks why.
- [ ] Identify the current evidence level and, when applicable, the scenario-defined conversation stage before selecting conclusions or the next-step request
- [ ] Check whether the user provided Amazon backend ABA-SQP search conversion data for the relevant ASIN/brand/query/date range
- [ ] Add one standalone, localized `Data Notes` section near the top naming the evidence level and boundary; do not duplicate it near the end
- [ ] Use the next-step request defined by the active scenario; do not infer a universal fixed sequence
- [ ] Track every live API response for usage accounting: `_query.endpoint`, `_query.params`, `meta.creditsConsumed`, and `meta.creditsRemaining`
- [ ] Separate traffic facts from strategy advice using confidence labels
- [ ] Apply the Evidence-Seeking Diagnosis Protocol: state the unresolved question, acquire discriminating evidence, and do not substitute a generic cause list when evidence is missing
- [ ] Apply the Diagnostic Closure Gate: every diagnostic branch is resolved, actively pursued, or matched to the single final evidence request; omit branches irrelevant to the requested decision
- [ ] Apply the Evidence-to-Action Protocol to every recommendation; verify target observation, defect signal, alternatives, validation, and authorized action level
- [ ] Include `API Usage` as the final report section; if credit fields are missing, write `not returned` instead of omitting the section

## Evidence Capability Matrix

Before calling endpoints, identify the input shape and requested judgment so the relevant scenario rules and evidence plan are loaded. After retrieval, use this matrix to narrow conclusions to the evidence actually returned; the initial route never guarantees the final conclusion scope.

### Available Data → Conclusion Scope

| Data retrieved | Conclusions enabled | If unavailable: tell the user explicitly |
|----------------|---------------------|-----------------------------------------|
| `keywords/extends` | Expansion candidates with relevance tiers; try both `phrase` and `fuzzy` before concluding low expandability | Cannot expand from this seed; no candidate list possible |
| `keywords/detail` | Demand snapshot: weekly search volume, ABA rank, ad density, market structure | Cannot assess demand size or competition density for this keyword |
| Metric layer `keywords/market-profile` when exposed on the target surface | Server-calculated weekly demand scale, Top3 concentration, ad activity, organic-entry difficulty, supply saturation, brand structure, organic benchmark, and independent volatility/annual-seasonality evidence; interpret scores through `context.scoringSpec` and `levelEvidence.score.{value,direction}` | Require item `status=available`. Mark a dimension unavailable when `supported=false`, `calculationStatus!=complete`, `level=unknown`, score value is null, or `unsupportedReason` is present. Keep volatility and annual-seasonality conclusions separate. Use `detail` only if it exposes different raw evidence required for a named inference |
| `keywords/trend` | Demand direction across multiple weeks | Keep demand direction weak; snapshot-only; do not claim growth or decline |
| `keywords/search-results` | Observed SERP: page-1 product mix, brand concentration, ad vs organic composition, intent shape | Cannot assess page-1 crowding, brand dominance, or intent fit |
| `keywords/product-traffic-terms` or `keywords/competitor-product-keywords` | ASIN traffic-source map: which keywords drive visibility, traffic share, rank quality | Cannot build traffic-source map; do not substitute with keyword-detail or search-results |
| `keywords/product-traffic-terms-timeline` | ASIN × keyword position/exposure/ad-activity timeline across dates | Keep ASIN-side movement claims directional only; cannot trace timeline |
| `keywords/product-traffic-terms-overview` | All-keyword impression traffic changes vs previous period; ORG first-3-page keyword entries/exits | Cannot assess previous-period traffic delta or ORG first-3-page changes; omit those sections |
| `keywords/trend-profile` | Server-calculated trend shape, volatility, slope, and direction consistency by fixed weekly window | Use raw trend only for required weekly points or omitted fields; do not claim lifecycle or seasonality output |
| `keywords/search-results-metrics` when live | Server-calculated SERP structure, concentration, top ASIN/brand and target-ASIN evidence | Aggregate visible SERP rows transparently; do not invent metric objects or entry conclusions |
| `keywords/product-traffic-term-changes` when live | Keyword losers/gainers and contribution within a defined scope | Current terms + flat overview cannot prove keyword change contribution; omit contribution claims |
| `keywords/product-traffic-terms-timeline-review` when live | Drill-down evidence signals for specified ASIN + keyword items | Analyze raw timeline groups; label hypotheses as Agent inference, not API root cause |

### Partial Data Protocol

When some endpoints return data but others are unavailable:

1. Produce conclusions only from the data actually retrieved
2. For each missing evidence gap, explicitly state: "This conclusion requires [endpoint], which was not retrieved in this run, so it cannot be assessed."
3. Do not infer a missing endpoint's output from adjacent endpoints (e.g., do not use `keywords/detail` to fabricate a reverse-ASIN traffic-source map)
4. Downgrade the overall conclusion scope to match the weakest available evidence; do not frame partial data as a complete analysis

### Metric-First Fallback Protocol

1. Call the matching metric endpoint first when it exists on the target surface.
2. Map each requested conclusion to a returned metric dimension/field and verify what the metric can actually express.
3. Stop calling when all requested conclusions are supported.
4. For each unsupported conclusion, distinguish calculation-data absence from metric-contract insufficiency. Calculation-data absence normally ends that conclusion; it does not automatically trigger data access.
5. Descend only if the data contract exposes additional fields or grain required for a named Agent inference, or if the metric endpoint itself is unavailable and transparent calculation from data is valid.
6. Before descending, record the missing inference and the exact extra fields/rows/series expected from data.
7. Do not call a source data endpoint merely to duplicate or “double-check” a supported metric.
8. Direct data access is correct when rows/series are the requested deliverable or no corresponding metric exists.

### Batch Response Protocol

1. After an endpoint is justified by the inference plan, collect all subjects sharing marketplace, date/range, granularity, window, filters, and sort context; timeline subjects must also share one ASIN.
2. Prefer `--keywords` over repeated `--keyword` calls. Do not loop singles when a valid batch can carry them.
3. Deduplicate case-insensitively and preserve first-occurrence order before calling.
4. For more than 20 compatible keywords, send sequential chunks of 20 and merge `data.items[]` into global input order.
5. Use a single-subject call only for one subject, incompatible request contexts, or an endpoint without batch capability.
6. Inspect each item's `status`; retain `empty` and `error` items with their reasons.
7. Analyze only `status=ok` evidence. Outer `success=true` does not upgrade empty/error items.
8. Use `meta.creditsConsumed` from each batch response. Do not estimate billing from request size; final billing is based on successful items.
9. Do not call both metric and source data merely because both support batching.

---

## General Rules

### Preferred Execution Path

- Before selecting the execution path, read the candidate tool's docs/help/schema; do not choose from names alone
- Default to the local CLI entry after the documentation check: `python {skill_base_dir}/scripts/zoodata.py`
- Select endpoints by layer in this order: matching metric → inference-sufficiency check → verify that lower-layer data adds information → targeted data access → skill interpretation
- For the selected endpoint, prefer execution shape in this order: one compatible batch → sequential max-20 chunks → single calls only when batching is impossible
- Do not interpret the subcommand list below as a fixed call order or a requirement to call both metric and source data endpoints
- For CLI calls, use exact argparse flag names from `--help`; do not invent camelCase flags or pass truncated dates
- Dates in CLI calls must be complete `YYYY-MM-DD` strings. Never use ellipses, partial dates, or natural-language dates.
- Use these subcommands as the first choice for execution:
  - `keyword-detail`
  - `keyword-market-profile` when the target surface exposes the pre-release endpoint
  - `keyword-trend-profile`
  - `keyword-trend`
  - `keyword-extends`
  - `keyword-search-results`
  - `keyword-competitor-product-keywords`
  - `keyword-product-traffic-terms`
  - `product-traffic-terms-overview`
  - `product-traffic-terms-timeline`
- Use MCP callable tools as verification or fallback when you need to compare the live session surface or the local CLI path is unavailable
- `market-profile` and `trend-profile` are currently localhost pre-release **metric-layer** endpoints with CLI subcommands; inspect the target surface before calling and do not assume production availability.
- For `market-profile`, inspect in this order: item `status` → resolved context and `scoringSpec` → dimension support/status → `level` → `levelEvidence.score.value/direction`. A `not_found` item is an observation-coverage result, not a low-demand judgment.
- Interpret `marketCharacteristics.volatility` and `marketCharacteristics.annualSeasonality` independently. Preserve their returned classifications and evidence; do not manufacture peak periods or resolve apparent disagreement without additional discriminating evidence.
- If a `market-profile` batch returns HTTP 500, do not relabel it as an empty result and do not automatically retry all subjects individually. Perform at most one diagnostic split only when isolating a failing subject is necessary; otherwise stop that metric judgment and report the service failure.
- Other planned metric endpoints have no CLI subcommands while production returns 404. Probe them only when the task materially benefits and the live surface may have changed; otherwise use the verified data endpoints.
- Do not declare a keyword capability missing until you have checked the local CLI entry and, when relevant, the live tool surface/schema
- Do not force a fixed endpoint order when the evidence gate can be satisfied more efficiently another way

### Tool Naming

- Distinguish HTTP endpoint paths such as `/openapi/v2/keywords/detail` from actual callable tool names such as draft `mcp__zoodata__openapi_v2_keyword_detail`
- Never call a keyword tool from an inferred prefix, endpoint name, or friendly label alone
- Never select or reject a candidate tool before reading its relevant docs/help/schema
- Before first use, inspect the active tool surface and confirm the exact full callable name
- If the live callable name differs from the draft docs, trust the live callable name
- If the local CLI entry is unavailable and no keyword tool is exposed, stop and report that the tool is unavailable instead of guessing

### Tool Discovery Fallback

- If the local CLI subcommand exists, use it first and do not require live tool lookup as a prerequisite step
- If the static tool list does not explicitly show the keyword tools, do not immediately fall back to API docs
- First confirm whether the current session actually exposes the corresponding callable tool names when you need a fallback or parity check
- Only fall back to ZooData docs for parameter confirmation when the local CLI path is unavailable, or a direct CLI/live tool call fails
- If both the local CLI path and direct tool access are unavailable, report the limitation clearly. Do not substitute public knowledge, web search, products/search, or adjacent endpoints for missing keyword evidence; offer a narrower task only when it has its own valid evidence source.

### Capability Inference Rule

- Do not infer endpoint capability from the tool name alone
- Determine capability in this order: relevant tool docs/help/schema, live tool schema and field descriptions when using MCP/session tools, then endpoint naming as a weak hint only
- If a tool exposes fields such as `estimateSearchCountWeekly`, `keywordEstimateSearchCount`, `estimateSearchCount`, `abaRank`, or related traffic fields, treat it as having keyword-volume or trend-analysis capability even if the tool name is not explicit
- Do not say "the keyword-volume interface is not available" unless you have checked the exposed schema/docs and confirmed the required fields are unavailable
- Prohibit reasoning such as "I do not see a tool named keyword volume, so volume cannot be analyzed"
- Prohibit capability claims such as "`products/search` proves this keyword has demand" unless the report explicitly labels that evidence as a secondary product-database signal rather than a keyword snapshot
- Prohibit classifying `products/search` as a front-end SERP tool or any ZooData WebTools endpoint as a keyword-intelligence endpoint; these sources have different evidence roles and must be named accordingly

### Scenario Routing Rule

- Scenarios describe common input patterns and their recommended endpoint chains — they are reference guides, not mandatory pre-classification steps
- Start from input shape, not scenario label:
  - seed keyword only → use data-layer `extends` for candidate recall because rows are the deliverable; batch shortlisted terms through metric-layer `market-profile` and `trend-profile` when those judgments are required; call raw endpoints only for contract-omitted evidence or row-level requests
  - target keyword → use `market-profile` first for weekly market judgment; use `detail` only if the metric endpoint is unavailable or a named inference requires raw fields omitted by its contract; unsupported calculation dimensions end those metric conclusions unless data provides distinct evidence for a different inference
  - ASIN only → use metric-layer `product-traffic-terms-overview` first for aggregate movement; call one ASIN traffic-list data endpoint only when the task asks which keywords drive traffic; enrich selected terms with `market-profile` first and use `detail` only for explicitly required raw fields omitted by the metric
  - ASIN + keyword → choose the metric matching the requested judgment (`market-profile`, `search-results-metrics`, or timeline review when live); call raw SERP, traffic-list, or timeline data only when the metric contract omits information required for a named inference, the metric endpoint is unavailable, or row/series evidence is requested; an unsupported/unavailable metric dimension alone is not a fallback trigger
  - ASIN + keyword + date range → prefer `product-traffic-terms-timeline-review` when live; fall back to `product-traffic-terms-timeline` only for unavailable/insufficient metric evidence or requested raw series
  - ASIN + multiple keywords + date range → batch through timeline review when live; otherwise batch the narrow fallback set through one timeline data call when there are at most 20
- After data is retrieved, scope conclusions using the Evidence Capability Matrix above
- If a request spans multiple patterns, structure the report in labeled sections rather than forcing one scenario label
- Do not make reverse-ASIN conclusions unless at least one ASIN traffic-list endpoint returned data

### Evidence Gate Rule

- Every conclusion must be directly supported by the endpoint designed for that evidence type
- If an endpoint returned no data or was unavailable, state the gap explicitly; do not downgrade silently
- Do not bridge a missing evidence type with a loosely related endpoint
- After detecting a problem, seek evidence that distinguishes explanations before stating a cause; if none is available, stop at the unresolved problem and request the minimum next evidence instead of listing generic causes

### Non-Substitution Rule

- `keywords/search-results` is the primary evidence for observed keyword SERP composition
- `products/search` can supplement broader market context only when explicitly framed that way
- `keywords/detail` can support keyword demand snapshot claims, but not reverse-ASIN source attribution
- `keywords/trend` can support direction over weekly points, but not page-1 change claims

### Conclusion Scope Rule

- `Data-backed` means directly supported by the correct endpoint for that claim type
- `Inferred` means evidence-backed reasoning, not endpoint substitution
- `Directional` means evidence-bounded validation or monitoring advice. It does not permit an unsupported explanation, and it never means proven causality.
- Strong wording is not allowed when the claim depends on optional enrichers that were not available

### Comparative Claims Rule

- Do not say the product, listing, CTR, CVR, rank, or traffic quality is better than competitors unless the report has direct competitor evidence for the same metric, same keyword/query, same marketplace, comparable date range, and comparable placement or position scope
- When competitor-specific evidence is unavailable, compare to the market instead: above/below market median, ahead/behind the market midpoint, near the upper/lower band, or ranking toward the front/back
- If a market average, median, or band is calculated from ABA/SQP screenshots, ZooData aggregates, or visible SERP samples, state how it was calculated and name the limitation
- Do not treat a market-wide query average as competitor-specific proof
- If position or placement cannot be controlled, downgrade confidence and use restrained wording such as "not an obvious weak point" rather than "significantly better than competitors"

### Usage Accounting Rule

- Every full-mode report that used live API data must end with `API Usage`
- Do not include a separate `Data Provenance` table unless the user explicitly asks for source-by-section details
- `API Usage` must be a markdown table, not a bullet list
- The `API Usage` table must aggregate calls by endpoint and sum `meta.creditsConsumed` from the responses
- The final row of the `API Usage` table must be `Total`, summing all endpoint calls and all returned credits consumed
- If any endpoint's credits are `not returned`, write the total credits as `partial N + not returned` when some credits are known, or `not returned` when no credits are known
- Required table format:
  `| Endpoint | Calls | Credits |`
  `|----------|-------|---------|`
  `| keywords/detail | 1 | 1 |`
  `| Total | 1 | 1 |`
- End with `Credits remaining: N` using the latest `meta.creditsRemaining`
- If `meta.creditsConsumed` or `meta.creditsRemaining` is absent, write `not returned`; do not infer or hide credit usage
- Do not finish the response after recommendations, caveats, or limitations if API usage has not been reported

### HTTP Validation Rule

- HTTP 422 is a parameter validation error, not a retryable transient failure.
- Do not retry the same 422 request repeatedly.
- Read the returned error detail and correct the call before retrying.
- First checks for keyword workflows: exact CLI flag names from `--help`, full `YYYY-MM-DD` dates, `dateFrom <= dateTo`, all required fields present, and endpoint-specific range limits.
- `keyword-trend` accepts up to 93 days; `product-traffic-terms-timeline` accepts up to 61 days. Do not probe longer ranges just to learn the limit from HTTP 422.
- For batch endpoints, also check that exactly one of `keyword`/`keywords[]` is present, the batch has at most 20 subjects, and it contains no case-insensitive duplicates.
- For `keyword-trend`, the canonical CLI pattern is:
  `python {skill_base_dir}/scripts/zoodata.py keyword-trend --keyword "small baskets for organizing" --date-from 2026-04-01 --date-to 2026-07-02 --marketplace US`

### Data Notes Rule

- Full-mode reports use one localized `Data Notes` section immediately after the disclaimer. It names the current evidence level and what that level can and cannot decide.
- Do not duplicate a `Data Notes Reminder` near the end and do not place evidence requests inside individual findings.
- At market evidence level, state that the answer is a market-direction judgment and not a subject-specific operating decision. Use the active scenario to choose the next request.
- At subject observation level, state that the diagnosis uses observed subject signals and remains provisional without the required seller-real evidence.
- At seller-real-data level, name the provided SQP/Ads fields used and do not request them again.
- Keep the wording natural and translated to the user's language. Avoid deficit-framed language and form-like status blocks.
- Do not use ZooData estimated exposure/search/visibility signals as a substitute for user-provided ABA-SQP conversion evidence.
- For ABA-SQP backend paths, fields, and recommended data provision method, see this file's `Seller Data Contract`.

### Date Handling

- Keyword endpoints are keyword-query workflows: inputs named `keyword` or `query` should be Amazon search queries / keyword phrases, not category paths or product-search substitutes
- When a keyword endpoint requires `date` or `dateTo`, prefer T-1 or earlier; avoid using the current date unless explicitly requested. Keep this as an internal date-selection rule and do not proactively explain the rationale unless the user asks why.
- Use the current date only when the user explicitly requests today's lookup, and label it as potentially incomplete if the returned data is missing or sparse
- `keywords/detail` is a weekly snapshot. `keywords/extends` uses the latest weekly snapshot and does not require a request date.
- `keywords/trend` is weekly time series
- `keywords/search-results` and ASIN keyword endpoints are recent daily observations
- `keywords/product-traffic-terms-overview` is the preferred core evidence for two-week / previous-period ASIN all-keyword impression traffic changes; compare current placement-level impression-point fields to matching `*Prev` fields for previous-period movement
- For `keywords/product-traffic-terms-overview`, display the period from response `periodStartDate` / `periodEndDate` exactly; never substitute the request date or an inferred range as the overview period
- In `keywords/product-traffic-terms-overview`, `first3PagesNewOrganicKeywords` lists keywords newly entering ORG first three pages, and `first3PagesLostOrganicKeywords` lists keywords that dropped out of ORG first three pages
- `keywords/product-traffic-terms-timeline` is the preferred ASIN + keyword timeline input; requested ranges cannot exceed 61 days and one call may include up to 20 keywords for one ASIN
- In `keywords/product-traffic-terms-timeline`, `keywordMetrics` uses its nested `metricWindow`, `asinSnapshot` is tied to `series[].date`, and `traffic` / `placement` / `adActivity` are rolling 7-day observations ending on that date
- For timeline diagnosis, inspect price, BSR, sales, rating, and traffic-estimate curves separately; use keyword-level fields only as supporting context for traffic-estimate changes
- Treat `asinSnapshot.latestTitle` and `asinSnapshot.latestMainImageLink` changes as listing events, not continuous curves
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

When investigating keyword anomalies, check evidence domains in this order:

1. Search demand moved
2. Ad density changed
3. The target ASIN's position changed
4. Price, BSR, sales, rating, or traffic-estimate curves moved
5. Title or main image changed near the anomaly
6. New head competitors entered
7. The keyword's top-ASIN traffic concentration changed (check `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`, or head-ASIN dominance visible in SERP)
8. The ASIN's all-keyword impression traffic changed versus the previous period
9. Keywords entered or dropped out of ORG first three pages

Treat this order as an evidence-search sequence, not a cause checklist. Rank explanations only when the retrieved evidence materially supports and distinguishes them; otherwise report the unresolved question and the next evidence required.

For ASIN + keyword movement, prefer `keywords/product-traffic-terms-timeline` as the ASIN-side movement source before stitching together isolated observations. For all-keyword ASIN traffic changes and ORG first-3-page entry/exit, use `keywords/product-traffic-terms-overview`; do not infer first-3-page organic gains/losses from SERP snapshots alone.

## Output Rules

### Candidate Tiering

For keyword expansion outputs, classify validation priority into the following provisional tiers. Do not treat them as final expansion or spend tiers before seller-real calibration:

- `Priority test`
- `Selective test`
- `Harvest`
- `Observe only`
- `Avoid`

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
