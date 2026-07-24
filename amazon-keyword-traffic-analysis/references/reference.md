# ZooData Keyword API Reference

> Read before choosing tools or interpreting fields. Production status was verified by direct calls on 2026-07-13; `market-profile` was inspected on localhost on 2026-07-14 and is not yet published. Re-check the target surface when behavior matters; the response is authoritative over this file and over the design document.

## Contents

- [Layer model](#layer-model)
- [Production availability](#production-availability)
- [Common contract](#common-contract)
- [Live endpoints by layer](#live-endpoints-by-layer)
- [Planned metric endpoints](#planned-metric-endpoints)
- [Evidence boundaries](#evidence-boundaries)
- [CLI and callable mapping](#cli-and-callable-mapping)

## Layer model

Keep the three layers distinct:

1. **Data endpoints** return traceable snapshots and details in `items[]`, `rows[]`, or `series[]`.
2. **Metric endpoints** return deterministic aggregate objects, context, coverage, and evidence—not full detail rows.
3. **Agent + skill workflows** combine evidence, explain it, add confidence and limitations, and recommend actions.

Do not move Agent outputs such as `recommendedAction`, `conclusion`, `reasoning`, root cause, or Mermaid diagrams into the API layer. Do not describe an Agent calculation as an API field.

### Access priority: metric first, data on demand

Terminology:

| Concept | Meaning | Access implication |
|---|---|---|
| Calculation coverage | Source inputs available to calculate a metric dimension | Limits that metric conclusion; does not authorize down-drill |
| Metric contract scope | Indicators, summaries, reasons, and grain intentionally exposed by the metric | Compare this scope with the requested inference |
| Inference sufficiency | Whether returned metric information supports the Agent's required judgment | Descend only if data is known to provide the missing information |

- Start from the judgment, not from a fixed endpoint chain.
- Prefer a matching metric endpoint because it provides the stable server-calculated object intended for that judgment.
- Treat a successful, sufficiently covered metric response as complete for its contract. Do not call the source data endpoint by default.
- Do not equate a dimension's calculation status with data-access permission. When both layers share the same source, missing metric inputs usually remain missing below.
- Descend only when the Agent's required inference needs information the metric contract does not expose but the data contract explicitly does: rows, series points, placements, raw fields, or another traceable evidence grain.
- A non-deployed/metric-specific failure may also justify data fallback when transparent Agent calculation is valid; a same-source `empty`/unsupported dimension normally does not.
- Make fallback surgical: retrieve only the missing subject, period, placement, rows, or fields.

| Judgment / deliverable | Metric-first source | Data fallback or direct-data exception |
|---|---|---|
| Weekly keyword market structure | `keywords/market-profile` | `keywords/detail` only when a required inference needs raw snapshot fields omitted by the metric, or the metric endpoint itself is unavailable; not merely because a profile dimension is unsupported/unavailable |
| Trend shape and volatility | `keywords/trend-profile` | `keywords/trend` only when the Agent needs weekly points or fields omitted from the profile for a specific inference |
| SERP structure/concentration | `keywords/search-results-metrics` when live | `keywords/search-results` for unavailable metric or requested product/placement rows |
| Root-universe demand | `keywords/root-aggregate` when live | No equivalent fallback; `extends` is candidate recall, not root-demand proof |
| ASIN aggregate traffic change | `keywords/product-traffic-terms-overview` | Use its verified live contract; do not infer missing keyword contribution from traffic-list rows |
| Keyword change contribution | `keywords/product-traffic-term-changes` when live | No equivalent fallback if contribution is absent |
| ASIN × keyword timeline evidence summary | `keywords/product-traffic-terms-timeline-review` when live | `keywords/product-traffic-terms-timeline` for unavailable metric, unsupported evidence, or requested raw series |
| Candidate recall / current traffic-term list | No metric endpoint | Call `extends` or one ASIN traffic-list data endpoint directly because rows are the deliverable |

## Production availability

| Endpoint | Layer | Live status | Verified live body |
|---|---|---|---|
| `keywords/detail` | data | available | `data.context + data.items[]` |
| `keywords/market-profile` | metric | localhost pre-release; not published | `data.context + data.items[].marketProfile` |
| `keywords/trend-profile` | metric | localhost pre-release; not published | `data.context + data.items[].rows[]` |
| `keywords/trend` | data | available | `data.context + data.items[].series[]` |
| `keywords/extends` | data | available | `data.context + data.query + data.queryType + data.rows[]` |
| `keywords/search-results` | data | available | `data.context + data.identity + data.rows[]` |
| `keywords/product-traffic-terms` | data | available | `data.context + data.identity + data.rows[]` |
| `keywords/competitor-product-keywords` | data | available | same shape as `product-traffic-terms` |
| `keywords/product-traffic-terms-timeline` | data | available | `data.context + data.items[].series[]` |
| `keywords/product-traffic-terms-overview` | aggregate | available, legacy shape | flat `data` object with current and `*Prev` fields |
| `keywords/search-results-metrics` | metric | unavailable | HTTP 404 |
| `keywords/root-aggregate` | metric | unavailable | HTTP 404 |
| `keywords/product-traffic-term-changes` | metric | unavailable | HTTP 404 |
| `keywords/product-traffic-terms-timeline-review` | metric | unavailable | HTTP 404 |

Treat unavailable metric endpoints as planned capability. Before first use in a later session, inspect/probe the live surface. On 404, use only the available data endpoints and transparent Agent-side aggregation; do not invent the planned response objects.

## Common contract

### Identity and context

- Keyword identity: `{ keyword, site }`.
- ASIN identity: `{ asin, site }`.
- ASIN + keyword identity: `{ asin, keyword, site }`.
- Single query objects use `data.identity`; batch endpoints use `data.items[].identity`.
- `requestedDate*` records the request. `resolvedDate*` records the actual available observation. Report resolved dates and returned period boundaries.
- Snapshot/current-window endpoints may contain `dataWindow.currentPeriod`; range endpoints use `resolvedDateFrom`, `resolvedDateTo`, and series dates instead.
- `latestObservedAt` is row collection time. Never use it to manufacture a snapshot period.

### Batch behavior

The following live endpoints support batch subjects:

| Endpoint | Single subject | Batch subject | Limit |
|---|---|---|---:|
| `keywords/detail` | `keyword` | `keywords[]` | 20 |
| `keywords/market-profile` | `keyword` | `keywords[]` | 20 |
| `keywords/trend-profile` | `keyword` | `keywords[]` | 20 |
| `keywords/trend` | `keyword` | `keywords[]` | 20 |
| `keywords/product-traffic-terms-timeline` | `asin + keyword` | `asin + keywords[]` | 20 keywords for one ASIN |

Rules:

- Prefer batch over repeated single-subject calls whenever subjects share all non-subject request parameters.
- Plan the full compatible subject set before the first call; do not discoverably loop one keyword at a time and batch only later.
- Send exactly one of the single or batch fields.
- Batch only subjects with the same marketplace, snapshot/range, granularity, window, filters, and sort context; timeline batches must share one ASIN.
- Deduplicate case-insensitively before calling; duplicate subjects return 422.
- Preserve input order in `data.items[]` and when merging multiple chunks.
- Inspect every item independently: `status=ok|empty|error`, `emptyReason`, `errorCode`, and `errorMessage`.
- Outer `success` is service execution status, not proof that every item has data.
- Do not discard empty/error items from the report; name their reason.
- Billing is per `status=ok` item. Empty and error items are not billed. Always report the returned `meta.creditsConsumed` rather than calculating credits yourself.

CLI examples:

```bash
python {skill_base_dir}/scripts/zoodata.py keyword-detail \
  --keywords "yoga mat,pilates mat" --date 2026-07-12 --marketplace US

python {skill_base_dir}/scripts/zoodata.py keyword-market-profile \
  --keywords "yoga mat,pilates mat" --date 2026-07-12 --marketplace US

python {skill_base_dir}/scripts/zoodata.py keyword-trend-profile \
  --keywords "yoga mat,pilates mat" --date 2026-07-12 \
  --window-periods 4,12 --marketplace US

python {skill_base_dir}/scripts/zoodata.py keyword-trend \
  --keywords "yoga mat,pilates mat" \
  --date-from 2026-06-01 --date-to 2026-07-12 --marketplace US

python {skill_base_dir}/scripts/zoodata.py product-traffic-terms-timeline \
  --asin B01CGLCGRA --keywords "yoga mat,pilates mat" \
  --date-from 2026-07-06 --date-to 2026-07-12 --marketplace US
```

For more than 20 compatible subjects, issue sequential chunks of 20 or fewer and restore global input order when merging. Keep one usage record per response. Use a single-subject request only for one subject, incompatible request contexts, or an endpoint without batch support.

### Empty results and errors

- `status=empty` means no matching observation in the resolved snapshot/window. It does not prove low demand.
- `keywords/extends` may return an empty `rows[]`; try `phrase` and `fuzzy` before concluding low expandability.
- HTTP 422 is request validation failure. Read the detail, fix parameters, and do not retry unchanged.
- HTTP 404 on a planned metric endpoint means it is not deployed on that surface; do not relabel it as a data-empty success.

### Credits

Track `_query.endpoint`, `_query.params`, `meta.creditsConsumed`, and `meta.creditsRemaining` for every response. Aggregate usage by endpoint in the final `API Usage` table. Use `not returned` when metadata is absent.

## Live endpoints by layer

### Data layer: `keywords/detail`

Request:

- exactly one of `keyword` or `keywords[]` (1–20)
- required `date` (`YYYY-MM-DD`)
- `marketplace=US|UK`, default `US`
- `granularity=week` only

Response:

- `data.context`: marketplace, site, requested/resolved date, weekly granularity, current period
- `data.items[]`: identity, status, `snapshotData`, empty/error fields
- `snapshotData`: `estimateSearchCount`, `abaRank`, Top3 click/conversion shares, market characteristics, SKU/brand/title coverage, organic/ad counts, and Top48 organic-product benchmarks

Do not expect legacy `estimateSearchCountWeekly`, `totalSkuCnt`, or top-level `data:null` in the current response. Read `snapshotData.estimateSearchCount`, `totalSkuCount`, and item status.

### Metric layer: `keywords/market-profile`

Availability:

- Pre-release on `http://localhost:8080` as of 2026-07-14; do not assume the production API exposes it.
- Localhost tool name: `openapi_v2_keyword_market_profile`.
- Before calling, inspect the target surface. On 404 or missing tool, continue with `keywords/detail` and transparent Agent-side interpretation; do not fabricate profile objects.
- Local CLI localhost pattern: `ZOODATA_BASE_URL=http://localhost:8080/openapi/v2 python {skill_base_dir}/scripts/zoodata.py keyword-market-profile ...`. Do not switch hosts unless that target surface is in scope and available.

Request:

- exactly one of `keyword` or `keywords[]` (1–20)
- required `date` (`YYYY-MM-DD`)
- `marketplace=US|UK`, default `US`
- `granularity=week` only

Response:

- `data.context`: marketplace, site, requested/resolved date, weekly period, and `scoringSpec` (`id`, `version`, `scoreType`, `scoreRange`, `referenceScope`)
- `data.items[]`: input-order identity, `status=available|not_found`, `marketProfile`, and `unavailableReason`
- `marketProfile`: `marketCharacteristics`, `demandScale`, `top3Concentration`, `adActivity`, `top20OrganicEntryDifficulty`, `supplySaturation`, `brandStructure`, and `organicProductBenchmark`
- current profile objects use camelCase fields. Each scored dimension returns `supported`, `level`, `interpretation`, `calculationStatus`, `unsupportedReason`, and `levelEvidence.score.{value,direction}`
- internal objects are versioned by `context.scoringSpec`; interpret scores with its returned model id/version, normalized range, and reference scope rather than as timeless universal thresholds
- inspect every dimension independently. Treat `supported=false`, `calculationStatus!=complete`, `level=unknown`, null `levelEvidence.score.value`, or non-null `unsupportedReason` as unavailable; the current contract has no aggregate `calculationCoverage` object
- `marketCharacteristics.volatility` exposes its own support/status boundary, `type`, source value, and mapping-confidence evidence
- `marketCharacteristics.annualSeasonality` independently exposes support/status, `classification`, year-over-year correlation, eligible pair count, peak-pattern detection, and `peakPeriods`. Do not let either seasonality object overwrite the other. `seasonalPeakPatternDetected=true` alone does not override `classification`, and an empty `peakPeriods` array cannot support named peak periods.

This endpoint returns deterministic weekly snapshot evidence. It does not return history, strategy advice, root cause, recommended actions, or seller-private ABA-SQP conversion data. An unmatched keyword returns `status=not_found`, `marketProfile=null`, and `unavailableReason=keyword_not_observed`; context fields such as `resolvedDate`, `dataWindow`, and `scoringSpec` may then be null. Not-found items are not billed. Use returned `meta.creditsConsumed` / `meta.creditsConsumedExact` rather than estimating.

Current localhost failure boundary: a subject-specific calculation error can return HTTP 500 for the entire batch instead of an item-level error. Treat that as a service failure, not `not_found`. Do not fan out the entire batch automatically; allow at most one diagnostic split only when isolating the failing subject is required for the task.

Layer boundary: obtain stable server-calculated multidimensional profile objects from metric-layer `keywords/market-profile` first. An unsupported/unavailable dimension limits the conclusion but does not itself justify calling data-layer `keywords/detail`, because both are snapshot-source related. Access `detail` only when a required Agent inference needs raw fields omitted by the metric contract, the metric endpoint is unavailable for a metric-specific reason, or the user requests traceable source fields. Combine evidence, explain limitations, assign confidence, and recommend actions only in the Agent + skill layer.

### Data layer: `keywords/trend`

Request:

- exactly one of `keyword` or `keywords[]` (1–20)
- `dateFrom`, `dateTo`; maximum 93-day range
- `marketplace=US|UK`; `granularity=week` only

Response:

- `data.context`: requested/resolved range and weekly granularity
- `data.items[].series[]`: `periodStartDate`, `periodEndDate`, `estimateSearchCount`, `abaRank`, `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`

This is raw weekly history. Use it only when weekly points or fields omitted by `trend-profile` are required.

### Metric layer: `keywords/trend-profile`

Request:

- exactly one of `keyword` or `keywords[]` (1–20)
- required as-of `date` (`YYYY-MM-DD`)
- required `windowPeriods[]`: 1–4 unique values selected from `4`, `8`, `12`, `26`
- `marketplace=US|UK`, default `US`; `granularity=week` only

Response:

- `data.context`: marketplace/site, requested/resolved date, weekly granularity, and requested windows
- `data.items[]`: input-ordered keyword identity and one `rows[]` entry per requested window
- each row contains `rowContext`, `status=available|unavailable|not_found`, `unavailableReason`, and `trendProfile`
- available profiles contain `searchDemand` and `abaRank`; inspect `supported`, `calculationStatus`, and `unsupportedReason` independently
- `trendEvidence` fields are `{ value, direction }` pairs covering first/last/change evidence, normalized slope, direction consistency, and eligible/aligned period counts

Use this endpoint first for server-calculated trend shape and volatility. Do not reduce `trend` to a first-to-last comparison: normalized slope and direction-consistency evidence may support a different window-level label. Preserve null `unavailableReason` / `observedPeriodCount` values without inventing a reason. Billing is per keyword with at least one available row; use returned credit metadata.

### Data layer: `keywords/extends`

Request:

- required `query`; do not rename it to `keyword`
- `queryType=phrase|fuzzy`
- optional marketplace, page, pageSize (1–100), sortBy, sortOrder
- no date is required; the service uses the latest available weekly snapshot. A legacy `date` may be sent but is ignored.
- `sortBy=relevanceScore|estimateSearchCount|abaRank|keyword`

Response:

- `data.context.coverageType` and `coverageReason`
- `data.query`, `data.queryType`
- `data.rows[].matchData`: query, keyword, site, relevanceScore
- `data.rows[].keywordSnapshot`: `dataWindow.currentPeriod` plus the same core snapshot families as detail

Do not flatten the response back to legacy `term`, `seedKeyword`, or `estimateSearchCountWeekly` fields.

### Data layer: `keywords/search-results`

Request:

- required `keyword`, `date`
- `granularity=lately_day`, `lookbackDays=7`
- optional `exploreTypes=ORG|SP|SB|SBV|SPR`, page/pageSize
- `sortBy=absolutePosition|estimateImpressionPoint|latestObservedAt|price|rating|ratingCount|recentSales|asin|title`

Response:

- `data.context`: requested/resolved date and 7-day current period
- `data.identity`
- `data.rows[]`: `latestObservedAt`, placement/position, listing fields, `estimateImpressionPoint`, `keywordTotalEstimateImpressionPoint`

Use this as the primary observed SERP source. Split ORG from sponsored placements. Do not substitute `products/search` for SERP ordering.

### Data layer: `keywords/product-traffic-terms` and `keywords/competitor-product-keywords`

Request:

- required `asin`, `date`
- `granularity=lately_day`, `lookbackDays=7`
- optional `keywordContains`, `exploreTypes`, page/pageSize
- `sortBy=trafficShare|estimateImpressionPoint|absolutePosition|avgPosition|keywordEstimateSearchCount|keywordAbaRank|latestObservedAt|keyword`

Response:

- `data.context`, `data.identity`, `data.rows[]`
- rows include placement/position, keyword, impression points, `trafficShare`, `avgPosition`, coverage/observation counts, keyword search/change fields, and ABA rank/change

The two endpoints currently return the same row shape. Prefer `product-traffic-terms` for the user's target ASIN; use the competitor-named route for competitor/overlap framing or fallback. One call is enough unless explicitly checking parity.

`trafficShare` is the row's sampled 7-day share within the ASIN traffic observation, not exact Amazon share of voice.

### Data layer: `keywords/product-traffic-terms-timeline`

Request:

- one ASIN and exactly one of `keyword` or `keywords[]` (1–20)
- `dateFrom`, `dateTo`; maximum 61-day range
- `granularity=lately_day`, `lookbackDays=7`
- no page/pageSize pagination for series

Response:

- `data.context`: requested/resolved range, granularity, lookbackDays
- `data.items[].identity`, status, `series[]`, empty/error fields
- each series point contains:
  - `date`
  - `asinSnapshot`: title, price, link/image, brand, badges, sales, rating, BSR, video
  - `traffic`: ORG/SP/SB/SBV/SPR impression points
  - `placement`: organic/ad positions, pages, observation timestamps, average observations
  - `keywordMetrics`: `metricWindow` plus search count, ABA rank, Top3 shares
  - `adActivity`: observation count, day coverage, campaign count, ad count

Keep time grains separate: `asinSnapshot` is tied to the series date; traffic/placement/ad activity cover the 7-day rolling window ending on that date; `keywordMetrics` belongs to its own weekly `metricWindow`.

### Metric layer (legacy response): `keywords/product-traffic-terms-overview`

The endpoint is conceptually aggregate, but production still returns the legacy flat shape:

- `periodStartDate`, `periodEndDate`, `asin`, `site`
- current ORG/SP/SB/SBV/SPR impression points
- matching `*Prev` values
- `first3PagesNewOrganicKeywords[]`
- `first3PagesLostOrganicKeywords[]`

Use returned period boundaries exactly. Do not claim that live production returned the planned `trafficPoints`, `trafficStructure`, `aggregateChanges`, `keywordConcentration`, or `channelBreakdown` objects. You may calculate simple current-minus-previous channel changes and shares transparently in the Agent layer.

## Planned metric endpoints

Use these only after live verification succeeds.

| Endpoint | Planned deterministic objects | Never substitute with |
|---|---|---|
| `keywords/search-results-metrics` | `serpStructure`, organic stats, top ASINs/brands, target-ASIN evidence, competition evidence | strategy conclusion or raw rows |
| `keywords/root-aggregate` | root-universe series and `rootDemand` | summing `extends` candidates |
| `keywords/product-traffic-term-changes` | top losers/gainers, change rows and contribution within filter scope | overview aggregate or timeline inference |
| `keywords/product-traffic-terms-timeline-review` | drill-down evidence signals for specified ASIN + keywords | final root cause or top loser discovery |

Important boundaries:

- Do not calculate root-universe demand by summing expansion rows.
- Do not infer keyword losers/gainers from the flat ASIN overview; it has no keyword contribution rows.
- Do not claim a timeline review proved causality; it is planned to return evidence signals only.
- `market-profile` occupies the stable snapshot-profile metric role. If a dimension is unsupported/unavailable, mark that metric judgment unavailable; do not assume `detail` can reconstruct the missing metric. Use `detail` only when it exposes additional raw evidence needed for a different, explicitly named Agent inference or when the metric endpoint itself is unavailable.

## Evidence boundaries

- Keyword opportunity workflow: use `extends` directly for candidate recall, `market-profile` first for weekly market judgment, and trend/SERP metrics when live; descend to targeted raw detail/trend/SERP only for unavailable metrics or contract-omitted evidence required by a named inference. Without seller ABA-SQP, value/spend recommendations remain directional.
- ASIN keyword health: live production can describe current traffic terms and legacy aggregate current-vs-previous movement. Full keyword change contribution requires the planned `product-traffic-term-changes` endpoint.
- ASIN anomaly diagnosis: use overview, current traffic terms, raw timeline, keyword trend, and SERP only as required to resolve the named uncertainty. Rank explanations only when the retrieved evidence distinguishes them; otherwise stop at the unresolved question and required next evidence. Do not claim a server-returned root cause.
- `products/search` is broader ZooData catalog data, not observed keyword SERP evidence.
- ZooData WebTools is the only page/web-retrieval channel authorized by this skill. Use `/webtools/scrape` for known URLs, `/webtools/scrape-interactive` only when rendering/actions are required, and `/webtools/search` only for URL discovery. These are crawler/retrieval sources, not ZooData keyword intelligence, observed Amazon keyword SERP, traffic, or seller-private evidence. Do not fall back to an external browser or public web search.
- Do not compare CTR, CVR, rank, or traffic quality against competitors without same-metric, same-keyword, same-marketplace, comparable-period and comparable-placement evidence.
- ZooData does not supply the seller's private ABA Search Query Performance funnel. Use user-provided impressions, clicks, cart adds, purchases, shares, and conversion rates as first-party enrichment when available.

## CLI and callable mapping

Use `python {skill_base_dir}/scripts/zoodata.py` after reading subcommand help.

| HTTP endpoint | CLI subcommand |
|---|---|
| `keywords/detail` | `keyword-detail` |
| `keywords/market-profile` | `keyword-market-profile` |
| `keywords/trend-profile` | `keyword-trend-profile` |
| `keywords/trend` | `keyword-trend` |
| `keywords/extends` | `keyword-extends` |
| `keywords/search-results` | `keyword-search-results` |
| `keywords/product-traffic-terms` | `keyword-product-traffic-terms` |
| `keywords/competitor-product-keywords` | `keyword-competitor-product-keywords` |
| `keywords/product-traffic-terms-overview` | `product-traffic-terms-overview` |
| `keywords/product-traffic-terms-timeline` | `product-traffic-terms-timeline` |

If using MCP/session tools, inspect the live tool surface and exact schema first. Never infer a callable name from an HTTP path or draft name.
