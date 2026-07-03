# Execution Guide — Amazon Keyword Intelligence

This file defines the task-constraint protocol for the four keyword scenarios.

---

## Execution Mode

| Task Type | Mode | Behavior |
|-----------|------|----------|
| Single lookup such as one snapshot field | Quick | Return the key metric with light interpretation |
| Expansion, full keyword judgment, reverse ASIN, keyword traffic diagnosis | Full | Run the full endpoint chain, apply scoring, and output provenance + API usage |

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
- [ ] Prefer `python {skill_base_dir}/scripts/zoodata.py` and choose the matching keyword subcommand after the documentation check
- [ ] If you need session tool parity or fallback, inspect the active tool surface and read the live schema / field descriptions for candidate keyword tools before selecting or judging capability
- [ ] Classify the task: seed keyword / target keyword / ASIN / ASIN + keyword
- [ ] Confirm marketplace; default to `US` if absent
- [ ] Confirm the date lens: weekly snapshot, recent 4-8 weeks, or latest sliding window; for keyword lookups that require `date` or `dateTo`, prefer T-1 or earlier and avoid the current date unless explicitly requested. In user-facing progress updates, simply state the selected marketplace/date without extra rationale unless the user asks why.
- [ ] Check whether the user provided Amazon backend ABA-SQP search conversion data for the relevant ASIN/brand/query/date range
- [ ] Add a standalone `Data Notes` section near the top of any full-mode keyword-value, traffic, ranking, bidding, budget, or spend-priority report
- [ ] Repeat the opening `Data Notes` body near the end, immediately before `API Usage`
- [ ] Track every live API response for usage accounting: `_query.endpoint`, `_query.params`, `meta.creditsConsumed`, and `meta.creditsRemaining`
- [ ] Separate traffic facts from strategy advice using confidence labels
- [ ] Include `API Usage` as the final report section; if credit fields are missing, write `not returned` instead of omitting the section

## Evidence Capability Matrix

Do not classify the request into a scenario before calling endpoints. Instead, determine which inputs are available, call the most relevant endpoints, then use this matrix to scope conclusions to the evidence returned.

### Available Data → Conclusion Scope

| Data retrieved | Conclusions enabled | If unavailable: tell the user explicitly |
|----------------|---------------------|-----------------------------------------|
| `keywords/extends` | Expansion candidates with relevance tiers; try both `phrase` and `fuzzy` before concluding low expandability | Cannot expand from this seed; no candidate list possible |
| `keywords/detail` | Demand snapshot: weekly search volume, ABA rank, ad density, market structure | Cannot assess demand size or competition density for this keyword |
| `keywords/trend` | Demand direction across multiple weeks | Keep demand direction weak; snapshot-only; do not claim growth or decline |
| `keywords/search-results` | Observed SERP: page-1 product mix, brand concentration, ad vs organic composition, intent shape | Cannot assess page-1 crowding, brand dominance, or intent fit |
| `keywords/product-traffic-terms` or `keywords/competitor-product-keywords` | ASIN traffic-source map: which keywords drive visibility, traffic share, rank quality | Cannot build traffic-source map; do not substitute with keyword-detail or search-results |
| `keywords/product-traffic-terms-timeline` | ASIN × keyword position/exposure/ad-activity timeline across dates | Keep ASIN-side movement claims directional only; cannot trace timeline |
| `keywords/product-traffic-terms-overview` | All-keyword impression traffic changes vs previous period; ORG first-3-page keyword entries/exits | Cannot assess previous-period traffic delta or ORG first-3-page changes; omit those sections |

### Partial Data Protocol

When some endpoints return data but others are unavailable:

1. Produce conclusions only from the data actually retrieved
2. For each missing evidence gap, explicitly state: "This conclusion requires [endpoint], which was not retrieved in this run, so it cannot be assessed."
3. Do not infer a missing endpoint's output from adjacent endpoints (e.g., do not use `keywords/detail` to fabricate a reverse-ASIN traffic-source map)
4. Downgrade the overall conclusion scope to match the weakest available evidence; do not frame partial data as a complete analysis

---

## General Rules

### Preferred Execution Path

- Before selecting the execution path, read the candidate tool's docs/help/schema; do not choose from names alone
- Default to the local CLI entry after the documentation check: `python {skill_base_dir}/scripts/zoodata.py`
- For CLI calls, use exact argparse flag names from `--help`; do not invent camelCase flags or pass truncated dates
- Dates in CLI calls must be complete `YYYY-MM-DD` strings. Never use ellipses, partial dates, or natural-language dates.
- Use these subcommands as the first choice for execution:
  - `keyword-detail`
  - `keyword-trend`
  - `keyword-extends`
  - `keyword-search-results`
  - `keyword-competitor-product-keywords`
  - `keyword-product-traffic-terms`
  - `product-traffic-terms-overview`
  - `product-traffic-terms-timeline`
- Use MCP callable tools as verification or fallback when you need to compare the live session surface or the local CLI path is unavailable
- Do not declare a keyword capability missing until you have checked the local CLI entry and, when relevant, the live tool surface/schema
- Do not force a fixed endpoint order when the evidence gate can be satisfied more efficiently another way

### Tool Naming

- Distinguish HTTP endpoint paths such as `/openapi/v2/keywords/detail` from actual callable tool names such as draft `mcp__zoodata.openapi_v2_keyword_detail`
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
- If both the local CLI path and direct tool access are unavailable, report the limitation clearly and produce only a boundary-labeled substitute analysis

### Capability Inference Rule

- Do not infer endpoint capability from the tool name alone
- Determine capability in this order: relevant tool docs/help/schema, live tool schema and field descriptions when using MCP/session tools, then endpoint naming as a weak hint only
- If a tool exposes fields such as `estimateSearchCountWeekly`, `keywordEstimateSearchCount`, `estimateSearchCount`, `abaRank`, or related traffic fields, treat it as having keyword-volume or trend-analysis capability even if the tool name is not explicit
- Do not say "the keyword-volume interface is not available" unless you have checked the exposed schema/docs and confirmed the required fields are unavailable
- Prohibit reasoning such as "I do not see a tool named keyword volume, so volume cannot be analyzed"
- Prohibit capability claims such as "`products/search` proves this keyword has demand" unless the report explicitly labels that evidence as a secondary product-database signal rather than a keyword snapshot
- Prohibit classifying `products/search` as a front-end SERP tool or `webtools_search` as a keyword-intelligence endpoint; both have different evidence roles and must be named accordingly

### Scenario Routing Rule

- Scenarios describe common input patterns and their recommended endpoint chains — they are reference guides, not mandatory pre-classification steps
- Start from input shape, not scenario label:
  - seed keyword only → call `extends` + `detail`; add `trend` and `search-results` for depth
  - ASIN only → call `product-traffic-terms`; add `detail` + `search-results` for per-keyword context
  - ASIN + keyword → call `search-results` + `detail`; call `product-traffic-terms` (with `keywordContains` filter) for the ASIN's traffic-share and position under that keyword; add `product-traffic-terms-timeline` for timeline depth
  - ASIN + keyword + date range → prefer `product-traffic-terms-timeline` + `search-results` + `detail`
- After data is retrieved, scope conclusions using the Evidence Capability Matrix above
- If a request spans multiple patterns, structure the report in labeled sections rather than forcing one scenario label
- Do not make reverse-ASIN conclusions unless at least one ASIN traffic-list endpoint returned data

### Evidence Gate Rule

- Every conclusion must be directly supported by the endpoint designed for that evidence type
- If an endpoint returned no data or was unavailable, state the gap explicitly; do not downgrade silently
- Do not bridge a missing evidence type with a loosely related endpoint

### Non-Substitution Rule

- `keywords/search-results` is the primary evidence for observed keyword SERP composition
- `products/search` can supplement broader market context only when explicitly framed that way
- `keywords/detail` can support keyword demand snapshot claims, but not reverse-ASIN source attribution
- `keywords/trend` can support direction over weekly points, but not page-1 change claims

### Conclusion Scope Rule

- `Data-backed` means directly supported by the correct endpoint for that claim type
- `Inferred` means evidence-backed reasoning, not endpoint substitution
- `Directional` means advice or plausible explanation, never proven causality
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
- Date-range keyword endpoints such as `keyword-trend` and `product-traffic-terms-timeline` accept ranges up to 93 days. Do not probe longer ranges just to learn the limit from HTTP 422.
- For `keyword-trend`, the canonical CLI pattern is:
  `python {skill_base_dir}/scripts/zoodata.py keyword-trend --keyword "small baskets for organizing" --date-from 2026-04-01 --date-to 2026-07-02 --marketplace US`

### Data Notes Rule

- When the current evidence set does not include Amazon backend ABA-SQP search conversion data, do not place the seller-side SQP enrichment request inside each traffic-related conclusion, traffic-source bucket, likely-cause group, or recommendation group.
- Full-mode reports must also include a standalone `Data Notes` section immediately after the opening disclaimer. This section must use natural prose and must be translated to the user's language; do not leave the title in English when the report body is Chinese. For Chinese output, render the opening title exactly as the Unicode escape `\u6570\u636e\u8bf4\u660e`; decode the escape into visible Chinese characters in the final report. Avoid SQP-specific status titles.
- Full-mode reports must repeat the same data-basis message near the end in a `Data Notes Reminder` section immediately before `API Usage`. Translate the title and body to the user's language. For Chinese output, render the end title exactly as the Unicode escape `\u6570\u636e\u8bf4\u660e\uff08\u518d\u6b21\u63d0\u9192\uff09`; decode the escape into visible Chinese characters in the final report. This reminder is for users who may have skipped the opening note.
- Do not output status labels or similar form-like wording.
- When the current evidence set is ZooData plus Amazon Brand Analytics market-wide signals only, keep the section short and direct. Follow this order: first describe the evidence used (`ZooData` plus `Amazon Brand Analytics market-wide signals`), then say that if the user can provide seller-side ABA-SQP conversion funnel data, the analysis can tailor for the user a more exclusive operating strategy that better fits the product's actual conversion performance, then include the Seller Central path `Brand Analytics → Search Analytics → Search Query Performance → Brand View`, the recommended sorting instruction `Search Funnel - Impressions → Brand Count`, and the requested input format `screenshot or CSV`.
- Avoid deficit-framed wording in user-facing `Data Notes`; frame seller-side ABA-SQP as an optional enrichment that unlocks a more bespoke strategy.
- Do not use per-conclusion SQP caveats in full-mode reports; use only the opening `Data Notes` and the end `Data Notes Reminder`.
- The end reminder body should repeat the opening `Data Notes` body, including the Seller Central path when the opening note included it. Do not replace it with a shorter alternate wording unless the user explicitly asks for a shortened report.
- Traffic-related conclusions include traffic-source structure, exposure movement, traffic share, ranking visibility, "worth bidding/worth targeting" verdicts, and budget/spend priority recommendations.
- If the user provided ABA-SQP data, do not add the seller-side SQP enrichment request; use the provided SQP impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate as first-party conversion evidence.
- Do not use ZooData estimated exposure/search/visibility signals as a substitute for user-provided ABA-SQP conversion evidence.
- For ABA-SQP backend paths and recommended data provision method, see reference.md § Keyword Value Boundary.

### Date Handling

- Keyword endpoints are keyword-query workflows: inputs named `keyword` or `query` should be Amazon search queries / keyword phrases, not category paths or product-search substitutes
- When a keyword endpoint requires `date` or `dateTo`, prefer T-1 or earlier; avoid using the current date unless explicitly requested. Keep this as an internal date-selection rule and do not proactively explain the rationale unless the user asks why.
- Use the current date only when the user explicitly requests today's lookup, and label it as potentially incomplete if the returned data is missing or sparse
- `keywords/detail` and `keywords/extends` are weekly snapshots
- `keywords/trend` is weekly time series
- `keywords/search-results` and ASIN keyword endpoints are recent daily observations
- `keywords/product-traffic-terms-overview` is the preferred core evidence for two-week / previous-period ASIN all-keyword impression traffic changes; compare current placement-level impression-point fields to matching `*Prev` fields for previous-period movement
- For `keywords/product-traffic-terms-overview`, display the period from response `periodStartDate` / `periodEndDate` exactly; never substitute the request date or an inferred range as the overview period
- In `keywords/product-traffic-terms-overview`, `first3PagesNewOrganicKeywords` lists keywords newly entering ORG first three pages, and `first3PagesLostOrganicKeywords` lists keywords that dropped out of ORG first three pages
- `keywords/product-traffic-terms-timeline` is the preferred ASIN + keyword timeline input; requested ranges cannot exceed 93 days
- In `keywords/product-traffic-terms-timeline`, `keyword*` fields use the keyword metric period shown by `keywordPeriodStartDate` / `keywordPeriodEndDate`, `latest*` fields are the ASIN's latest snapshot on the specified date, and impression/`avg*`/ad-activity fields are rolling metrics for the most recent 7 days ending at that date
- For timeline diagnosis, inspect price, BSR, sales, rating, and traffic-estimate curves separately; use keyword-level fields only as supporting context for traffic-estimate changes
- Treat `latestTitle` and `latestMainImageLink` changes as listing events, not continuous curves
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
4. Price, BSR, sales, rating, or traffic-estimate curves moved
5. Title or main image changed near the anomaly
6. New head competitors entered
7. The keyword's top-ASIN traffic concentration changed (check `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`, or head-ASIN dominance visible in SERP)
8. The ASIN's all-keyword impression traffic changed versus the previous period
9. Keywords entered or dropped out of ORG first three pages

If multiple causes are plausible, rank them rather than presenting one as certain.

For ASIN + keyword movement, prefer `keywords/product-traffic-terms-timeline` as the ASIN-side movement source before stitching together isolated observations. For all-keyword ASIN traffic changes and ORG first-3-page entry/exit, use `keywords/product-traffic-terms-overview`; do not infer first-3-page organic gains/losses from SERP snapshots alone.

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
