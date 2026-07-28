---
name: zoodata
description: >
  API endpoint reference for the ZooData data platform. Provides the 12
  commerce endpoints plus 10 keyword intelligence endpoints (categories,
  markets, products, competitors, realtime ASIN, AI review analysis, raw
  reviews, price band, brand, history, keyword detail/trend/extends/search
  results/market profile/product traffic/competitor keywords, traffic overview/timeline),
  their inputs/outputs,
  parameter quirks, Quick Start (auth, base URL), how credits are tracked
  (meta.creditsConsumed field), and the Local Review Toolkit (Map/Reduce
  for raw reviews).
  Use when the user asks about the API itself — which endpoints exist,
  how to call them, field schemas, parameter quirks, how to authenticate,
  how credit consumption is reported, or how the Local Review Toolkit works.
  Use when user asks: what endpoints does ZooData have, how do I call
  /products/search, fields returned by reviews/analysis, how to check
  credit usage, how the Local Review Toolkit works, how to get started.
  Requires ZOODATA_API_KEY.
metadata:
  version: "1.1.6"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

> **📋 Live API Reference**: Field names and parameters may change. If you encounter field errors,
> check the latest OpenAPI spec at https://zoodata.ai/api/v1/openapi-spec for current field definitions.

# ZooData — Commerce Data Infrastructure for AI Agents

200M+ Amazon products. 22 endpoints. One API key.

## Quick Start
1. Get key: [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys) (1,000 free credits)
2. `export ZOODATA_API_KEY='hms_live_xxx'`
3. Base URL: `https://api.zoodata.ai/openapi/v2` — all POST with JSON body
4. Auth: `Authorization: Bearer YOUR_API_KEY`
5. New keys need 3-5s to activate. If 403, wait and retry.

## Capabilities & Data Flow

- **Network**: only `https://api.zoodata.ai` (Bearer `ZOODATA_API_KEY`). Setting `ZOODATA_BASE_URL` to an untrusted host (anything other than `api.zoodata.ai` / `*.zoodata.ai` / localhost) makes the CLI **refuse the request and withhold the key** — the Bearer token is never sent to an untrusted host.
- **Execution**: bundled shared ZooData CLI `{skill_base_dir}/scripts/zoodata.py` (Python 3, stdlib-only). The shared CLI exposes ALL ZooData endpoints as subcommands; this skill's workflows use: all subcommands — this is the data-layer reference skill, so the full CLI surface is the declared surface. Do not invoke unrelated subcommands for this skill's tasks.
- **Local files**: none by default; reads the optional credential store `~/.zoodata/config.json`; the Local Review Toolkit uses a temporary `/tmp/review_<ASIN>_<timestamp>/` working dir during the review fallback.
- **Sent to the API**: keywords, category paths, ASINs, marketplace/date and numeric filter values only. **Never sent**: budget, experience level, risk tolerance, or any other user-profile text — profile inputs map client-side to numeric filters.
- **Credits**: every API call consumes account credits. For broad or ambiguous requests, state the estimated credit cost and confirm with the user before running multi-call scans.

## ⚠️ Critical API Pitfalls (ALL skills must follow)
1. **Keyword search is broad** → MUST lock `categoryPath` first via `categories` endpoint
2. **Brand/price-band queries MUST include --category** to avoid cross-category contamination
3. **Revenue** = `sampleAvgMonthlyRevenue` directly. **NEVER** calculate avgPrice × totalSales (overestimates 30-70%)
4. **Sales** = `monthlySalesFloor` (lower bound). Fallback: 300,000 / BSR^0.65, tag as 🔍
5. **Use API fields directly**: `sampleOpportunityIndex`, `sampleTop10BrandSalesRate` — never reinvent
6. **reviews/analysis** needs 50+ reviews. Fallback chain when sample is insufficient:
   1. Lightweight: `realtime/product` → `ratingBreakdown` (star distribution only, no themes)
   2. Full 11-dim insights: `realtime/reviews` (raw text, up to 100) + local Map/Reduce via the
      Local Review Toolkit below — see "Local Review Toolkit" section
7. **Aggregation endpoints** (price-band, brand) without categoryPath produce severely distorted data
8. **Price-band and brand endpoints only accept `keyword`** (not categoryPath) — cross-validate returned products
9. **`mode` is CLI-local, NOT an API parameter** → `zoodata.py` expands `--mode` client-side into the filter sets in `PRODUCT_MODES` (`{skill_base_dir}/scripts/zoodata.py`, 13 presets) before the request; sending `mode` raw → 422
10. **CLI filter flags ≠ API field names** → `--sales-min` → `monthlySalesMin`; `--ratings-max` (review count) → `ratingCountMax`, **not** `ratingMax` (a different valid field — max star rating — that returns wrong results silently, no 422). Pass `categoryPath` as a JSON array (`["Electronics"]`), never a string. Unknown fields (`salesMin`, `ratingsMax`, …) → 422

## On Missing Key (no credentials configured)

**BEFORE calling any endpoint**, verify credentials are configured. The reliable check is `python {skill_base_dir}/scripts/zoodata.py check` — credentials-only by default, no endpoint calls and no credit usage; exits non-zero if no key is found in env vars OR config files. A `[ -z "$ZOODATA_API_KEY" ]` test alone is NOT sufficient — a user may have only `~/.zoodata/config.json` set.

When no key is found through any mechanism:

1. **STOP.** Do not run the workflow. Do not call `zoodata.py` (you'll just get the same credential error and burn tokens).
2. **Do NOT fall back to a "partial analysis from training data" / "industry common-sense headlines" / "for reference only" preview.** Your training data is stale, has no per-ASIN granularity, and presenting it as analysis — even disclaimed — misrepresents what this skill produces. The deliverable is data-backed; without data, there is no deliverable.
3. **Tell the user, in their language**, all three of:
   - "`ZOODATA_API_KEY` is not set — I need this to run the analysis."
   - **Get a free key** (1,000 credits, no credit card): https://zoodata.ai/en/api-keys
   - **Configure** via one of:
     - `export ZOODATA_API_KEY='hms_live_xxx'` (session only)
     - `mkdir -p ~/.zoodata && echo '{"api_key":"hms_live_xxx"}' > ~/.zoodata/config.json` (persistent)
4. **Optionally** state in **one sentence** what the workflow will produce once the key is configured (deliverable shape only — no numbers, no market color, no "common sense" preview).

## On 401 Invalid Key

When `zoodata.py` returns `{"code": 401, "message": "API Key invalid or expired"}`:

1. **STOP further endpoint calls immediately.** Do not retry — a rejected key won't be accepted on a second try; every subsequent call will return 401 too.
2. **Report to the user**:
   - The `ZOODATA_API_KEY` in use was rejected (likely invalid, revoked, or expired)
   - If any partial findings were collected before the failure, show them and mark as partial
   - Fix at https://zoodata.ai/en/api-keys (verify the key, regenerate if needed)
3. **Do not fabricate or guess** the data the failed calls would have returned. This includes "training-data fallback" / "industry common-sense" headlines disguised as preview — those are fabrications.

## On 402 Credit Exhausted

When `zoodata.py` returns `{"code": 402, "message": "API quota exhausted or subscription expired"}`:

1. **STOP further endpoint calls immediately.** Do not retry. Do not switch endpoints as a workaround — 402 is account-level (key/subscription), not endpoint-level.
2. **Report to the user** with all four of:
   - Which step in the workflow was reached (e.g. "Completed step 3/5: brand analysis")
   - Partial findings already collected (show the actual data, not just a list of completed steps)
   - Rough credits needed to resume (sum remaining-step costs from this skill's API Budget table)
   - Top-up link: https://zoodata.ai/en/pricing
3. **Do not fabricate or guess** the missing data to "complete" the report. Mark partial findings explicitly as partial. **No "training-data fallback" / "industry common-sense" filler** — substituting public-knowledge prose for missing endpoint data is still fabrication.

## 22 Endpoints

| # | Endpoint | Purpose | Key Output |
|---|----------|---------|------------|
| 1 | `categories` | Browse/search category tree | categoryPath, productCount |
| 2 | `markets/search` | Market-level metrics | sampleAvgMonthlySales, sampleAvgPrice, topSalesRate, sampleNewSkuRate |
| 3 | `products/search` | Product search (20+ filter fields) | asin, price, monthlySalesFloor, rating, ratingCount, fbaFee |
| 4 | `products/competitors` | Competitor discovery | same fields as products/search |
| 5 | `realtime/product` | Live ASIN detail | rating, features, bestsellersRank[], buyboxWinner.price, variants |
| 6 | `reviews/analysis` | AI review insights (11 dims) | sentimentDistribution, consumerInsights, topKeywords |
| 7 | `realtime/reviews` | Live raw review text (cursor paginated, max 100) | reviews[], nextCursor — feeds Local Review Toolkit |
| 8 | `products/price-band-overview` | Price band summary | hottestBand, bestOpportunityBand, sampleOpportunityIndex |
| 9 | `products/price-band-detail` | Full 5-band distribution | priceBands[] with sales, brands, ratings per band |
| 10 | `products/brand-overview` | Brand concentration | sampleTop10BrandSalesRate (CR10), sampleBrandCount |
| 11 | `products/brand-detail` | Per-brand breakdown | brands[] with sales, revenue, sampleProducts |
| 12 | `products/history` | Time series (single ASIN per call) | timestamps[], price[], bsr[], monthlySalesFloor[], rating[], ratingCount[], sellerCount[], title/imageUrl/bestSeller/newRelease/aPlus/inventoryStatus changelogs |
| 13 | `/openapi/v2/keywords/detail` | Keyword summary from the nearest available weekly snapshot | `estimateSearchCountWeekly`, `abaRank`, `marketCharacteristics`, `adCount`; may return `data: null` |
| 14 | `/openapi/v2/keywords/market-profile` | Pre-release multidimensional weekly keyword profile | demand scale, Top3 concentration, ad activity, organic-entry difficulty, saturation, brand structure, organic benchmark, coverage |
| 15 | `/openapi/v2/keywords/trend` | Weekly keyword time series | `estimateSearchCount`, `abaRank`, `rankChangeCount`, `periodStartDate`, `periodEndDate` |
| 15b | `/openapi/v2/keywords/trend-profile` | Server-calculated trend profile over fixed weekly windows | trend shape, volatility, normalized slope, direction consistency, ABA-rank evidence |
| 16 | `/openapi/v2/keywords/extends` | Keyword expansion / long-tail discovery | related keywords ranked by `relevanceScore` / `estimateSearchCount`; may return empty array |
| 17 | `/openapi/v2/keywords/search-results` | Daily keyword SERP snapshot | `asin`, `exploreType`, `absolutePosition`, `estimateImpressionPoint`, listing fields |
| 18 | `/openapi/v2/keywords/competitor-product-keywords` | Keyword set where an ASIN appears as a competitor | `keyword`, `avgPosition`, `keywordEstimateSearchCount`, `trafficShare` |
| 19 | `/openapi/v2/keywords/product-traffic-terms` | Traffic-driving keywords for an ASIN | same live response shape as competitor-product-keywords |
| 20 | `/openapi/v2/keywords/product-traffic-terms-overview` | Weekly ASIN all-keyword traffic-change overview | current vs previous-period placement-level impression points, ORG first-3-page keyword entries/exits |
| 21 | `/openapi/v2/keywords/product-traffic-terms-timeline` | ASIN + keyword daily timeline | position/impression points, listing snapshot, keyword weekly metrics, ad activity |

## Known Quirks
- `topN`, `listingAge`, `newProductPeriod` are **strings** (`"10"` not `10`)
- Many search/list endpoints return `.data` as an **array** — use `.data[0]` for the first record. But some commands may return non-array payloads inside `data`, so inspect the actual response shape before indexing.
- `ratingCount` not `reviewCount` everywhere
- `bsr` (int) in products vs `bestsellersRank` (array) in realtime
- `buyboxWinner.price` — NOT top-level `price` in realtime
- `realtime/product` does NOT return: monthlySalesFloor, fbaFee, sellerCount
- `realtime/product` cold-start: first call for an uncached ASIN may return `success: true` with an EMPTY `data` (`asin: ""`) while the live fetch warms up — retry once after a few seconds before concluding "no data" (still billed 1 credit per call)
- `reviewCountMin/Max` filters currently broken (API-56)
- `reviews/analysis` may 500 for certain ASINs (API-58) — retry different ASIN
- Rate limit: 100 req/min, 10 req/sec burst
- `categories` uses `categoryKeyword` (not `keyword`) and `parentCategoryPath` (not `parentCategoryName`)
- `reviews/analysis`: `mode` required ("asin"/"category"), use `asins` (plural array) not `asin`
- `realtime/reviews`: returns 10 reviews/page fixed (no `pageSize` param); 1 credit/page; cursor-paginated; hard cap = 100 reviews (10 pages); supports `marketplace` US/UK only
- `keywords/detail` resolves the input `date` to the nearest available weekly snapshot at or before that date, and may legitimately return `data: null` even with `success: true`
- `keywords/market-profile` is pre-release on localhost as of 2026-07-14 and is not yet published; it accepts one of `keyword` / `keywords[]` (max 20), requires `date`, supports weekly granularity only, and returns input-ordered `data.items[]`
- `keywords/trend-profile` is available on localhost and not yet published; it accepts one of `keyword` / `keywords[]` (max 20), requires `date` and 1–4 unique `windowPeriods` selected from 4/8/12/26, and supports weekly granularity only
- `keywords/extends` also resolves the input `date` to the nearest available weekly snapshot, requires `query` (not `keyword`), supports `queryType` = `phrase` or `fuzzy`, and may legitimately return `data: []`
- `keywords/search-results`, `keywords/competitor-product-keywords`, and `keywords/product-traffic-terms` use daily observations over a sliding ~7-day window, not a long-retention historical store
- Keyword endpoints are keyword-query workflows; for inputs named `keyword` or `query`, use the Amazon search query / keyword phrase being analyzed
- For keyword endpoints that require `date` or `dateTo`, prefer T-1 or earlier and avoid the current date unless the user explicitly asks for today's lookup
- `keywords/search-results` requires `date` + `keyword`; `exploreTypes` values are `ORG`, `SP`, `SB`, `SBV`, `SPR`
- `keywords/competitor-product-keywords` and `keywords/product-traffic-terms` require `date` + `asin`; both currently return the same live item shape, including `trafficShare`
- `keywords/product-traffic-terms-overview` requires `date` + `asin`; it returns the latest weekly overview of all keyword impression traffic changes under that ASIN at or before the date, compared with the previous period
- `keywords/product-traffic-terms-timeline` requires `asin` + exact `keyword` + `dateFrom` + `dateTo`; the date range cannot exceed 60 days
- `keywords/search-results` is the default source for explaining what products currently appear on a keyword SERP because it already returns listing-level product fields
- `products/search` is a broader ZooData product-database query and must not be presented as Amazon live keyword SERP ordering

## Keyword Intelligence Endpoints

These nine endpoints fill the gap between raw
catalog data and search-demand/search-visibility intelligence.

Keyword value boundary:
- Keyword endpoints provide estimated search, visibility, rank, traffic-share, and impression-point signals
- They do not provide a seller's first-party ABA Search Query Performance funnel by themselves
- Treat keyword value, profitability, and conversion potential as directional unless the user supplies ABA-SQP impressions, clicks, cart adds, purchases, click share, purchase share, and conversion rate
- ABA-SQP backend location: Chinese Seller Central path `品牌分析 -> 搜索分析 -> 搜索查询绩效 -> 品牌视图`; English Seller Central path `Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View`
- Recommended ABA-SQP data provision method: in Brand View, sort descending by `[Search Funnel - Impressions](https://sellercentral.amazon.com/brand-analytics/metric-glossary?linkedFrom=query-performance-brand-report-table-qp-impressions-group) -> Brand Count` / `搜索漏斗-展示次数 -> 品牌数量`, then provide a screenshot; alternatively, download the CSV and provide it for model analysis
- If the user has not provided Amazon backend ABA-SQP search conversion data, every traffic-related conclusion or recommendation group should include: "建议结合 Amazon 后台 ABA-SQP 的搜索转化数据做更精确分析（中文路径：品牌分析 -> 搜索分析 -> 搜索查询绩效 -> 品牌视图；英文路径：Brand Analytics -> Search Analytics -> Search Query Performance -> Brand View）."
- If the user provided ABA-SQP data, use it as first-party conversion evidence and do not add that caveat

### `/openapi/v2/keywords/detail`
- Input: `keyword`, `date`, optional `marketplace`
- Data window: resolves the requested `date` to the nearest available weekly snapshot at or before that date
- Date rule: prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- Response shape: top-level `data` is an object or `null` (not an array)
- Key fields from schema: `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`,
  `abaTop3ConversionShareRate`, `marketCharacteristics`, `totalSkuCnt`, `brandCount`,
  `organicSkuCount`, `adCampaignCount`, `adCount`
- Live validation note: for `keyword="yoga mat"` and several June 2026 dates, the endpoint returned
  `success: true` with `data: null`

### `/openapi/v2/keywords/market-profile` (metric layer, localhost pre-release)
- Availability: exposed on `http://localhost:8080` as of 2026-07-14; not yet published to production
- Input: exactly one of `keyword` or `keywords[]` (1–20), required `date`, optional `marketplace`, `granularity=week`
- Response shape: `data.context + data.items[]`, preserving request order
- Context fields: `requestedDate`, `resolvedDate`, `dataWindow.currentPeriod`, `scoringSpec`, marketplace/site/granularity
- Item fields: `identity`, `status=available|not_found`, `marketProfile`, `unavailableReason`
- `marketProfile` dimensions: `marketCharacteristics`, `demandScale`, `top3Concentration`, `adActivity`, `top20OrganicEntryDifficulty`, `supplySaturation`, `brandStructure`, `organicProductBenchmark`
- Interpret scores only with `context.scoringSpec` (`id`, `version`, `scoreType`, `scoreRange`, `referenceScope`). Scored dimensions expose `supported`, `calculationStatus`, `unsupportedReason`, `level`, `interpretation`, and `levelEvidence.score.{value,direction}`. There is no aggregate coverage object.
- `marketCharacteristics.volatility` and `marketCharacteristics.annualSeasonality` are independent evidence objects. Do not collapse their classifications, let one override the other, or invent peak periods from an empty list.
- Unmatched keywords return `status=not_found`, `marketProfile=null`, `unavailableReason=keyword_not_observed`, and zero consumed credits; resolved context and `scoringSpec` may be null
- A subject-specific calculation failure can currently produce HTTP 500 for the whole batch. Treat it as a service failure, not `not_found`; do not automatically fan out all subjects into single calls.
- Three-layer boundary: use data-layer `keywords/detail` for source snapshot fields, metric-layer `keywords/market-profile` for stable deterministic profile objects, and the Agent + skill layer for evidence composition, confidence, explanations, limitations, and actions
- Metric-first access: call the matching metric before its source data endpoint. Descend only when the Agent needs an indicator or evidence grain omitted by the metric contract, the metric endpoint is unavailable and transparent data-based calculation is valid, no metric exists, or raw evidence is explicitly requested. Incomplete metric calculation coverage is a conclusion limit—not by itself a reason to call same-source data.
- Batch-first execution: after selecting the endpoint, collect all subjects with identical non-subject context and prefer its batch contract over repeated single calls. Deduplicate case-insensitively, preserve order, chunk compatible sets at the endpoint limit (20 for current keyword batches), and merge results back into global input order. Batch support never justifies an extra cross-layer call.

### `/openapi/v2/keywords/trend`
- Input: `keyword`, `dateFrom`, `dateTo`, optional `marketplace`
- Data window: weekly-granularity points across the requested date range
- Date rule: prefer T-1 or earlier for `dateTo`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an array
- Key fields from live response/schema: `observedAt`, `periodStartDate`, `periodEndDate`,
  `estimateSearchCount`, `estimateSearchChangeCount`, `estimateSearchChangeRate`, `abaRank`,
  `prevAbaRank`, `prevEstimateSearchCount`, `rankChangeCount`

### `/openapi/v2/keywords/trend-profile` (metric layer, localhost pre-release)
- Input: exactly one of `keyword` / `keywords[]` (1–20), required `date`, required unique `windowPeriods[]` selected from 4/8/12/26, optional `marketplace`, `granularity=week`
- Response: `data.context + data.items[].rows[]`; every requested window returns one row with `rowContext`, `status=available|unavailable|not_found`, `unavailableReason`, and `trendProfile`
- Available profiles contain independently guarded `searchDemand` and `abaRank` dimensions with `trend`, `trendPattern`, and `{value,direction}` entries under `trendEvidence`
- Evidence includes first/last/change values, normalized slope, direction consistency, aligned/eligible period counts, plus demand volatility/window position or ABA best/worst rank
- Use this metric endpoint before raw `keywords/trend` for trend-shape and volatility judgments. Descend only for required weekly points or fields omitted from the profile.
- Preserve null unavailable reasons rather than inventing one. Billing is per keyword with at least one available window; use returned credit metadata.

### `/openapi/v2/keywords/extends`
- Input: `query`, `date`, optional `marketplace`, `page`, `pageSize`, `queryType`, `sortBy`, `sortOrder`
- Important quirk: seed field is `query`, not `keyword`; `queryType` supports `phrase` and `fuzzy`
- Data window: resolves the requested `date` to the nearest available weekly snapshot at or before that date
- Date rule: prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an array
- Key fields from schema: `term`, `seedKeyword`, `relevanceScore`, `estimateSearchCountWeekly`,
  `abaRank`, `marketCharacteristics`, `brandCount`, `organicSkuCount`, `adCount`,
  `periodStartDate`, `periodEndDate`, `observedAt`
- Live validation note: empty arrays are normal; `query="yoga mat"` returned `data: []` for both
  `queryType="phrase"` and `queryType="fuzzy"`

### `/openapi/v2/keywords/search-results`
- Input: `keyword`, `date`, optional `marketplace`, `page`, `pageSize`, `exploreTypes`, `sortBy`, `sortOrder`
- Data window: daily observations surfaced through a sliding ~7-day window
- Date rule: prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an array
- Key fields from live response/schema: `exploreType`, `absolutePosition`, `pageIndex`,
  `pagePosition`, `asin`, `title`, `brand`, `price`, `currency`, `link`, `imageLink`, `rating`,
  `ratingCount`, `recentSales`, `hasVideo`, `estimateImpressionPoint`,
  `keywordTotalEstimateImpressionPoint`
- Interpretation rule: use this endpoint first for "what is on page 1 / what products dominate this keyword / what does the SERP look like"
- Do not substitute `products/search` when the question is about observed keyword SERP composition or ordering

### `/openapi/v2/keywords/competitor-product-keywords`
- Input: `asin`, `date`, optional `marketplace`, `page`, `pageSize`, `exploreTypes`,
  `keywordContains`, `sortBy`, `sortOrder`
- Data window: daily observations surfaced through a sliding ~7-day window
- Date rule: prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an array
- Key fields from live response/schema: `exploreType`, `absolutePosition`, `pageIndex`,
  `pagePosition`, `asin`, `keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`,
  `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`,
  `keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`,
  `keywordAbaRankChangeCount`, `trafficShare`

### `/openapi/v2/keywords/product-traffic-terms`
- Input: same request shape as `keywords/competitor-product-keywords`
- Data window: daily observations surfaced through a sliding ~7-day window
- Date rule: prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an array
- Key fields from live response/schema: `exploreType`, `absolutePosition`, `pageIndex`,
  `pagePosition`, `asin`, `keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`,
  `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`,
  `keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`,
  `keywordAbaRankChangeCount`, `trafficShare`
- Live validation note: current live response item shape matches `keywords/competitor-product-keywords`
  field-for-field; keep the semantic distinction in output wording rather than assuming a unique schema

### `/openapi/v2/keywords/product-traffic-terms-overview`
- Input: `asin`, `date`, optional `marketplace`
- Data window: latest weekly overview snapshot at or before the requested date; compares all keyword impression traffic under the ASIN with the previous period
- Date rule: prefer T-1 or earlier for `date`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an object or `null`
- Key fields from live localhost MCP response: `periodStartDate`, `periodEndDate`, `asin`, `site`,
  `organicImpressionPoint`, `sponsoredProductImpressionPoint`, `sponsoredBrandImpressionPoint`,
  `sponsoredBrandVideoImpressionPoint`, `sponsoredRecommendImpressionPoint`,
  `organicImpressionPointPrev`, `sponsoredProductImpressionPointPrev`,
  `sponsoredBrandImpressionPointPrev`, `sponsoredBrandVideoImpressionPointPrev`,
  `sponsoredRecommendImpressionPointPrev`, `first3PagesNewOrganicKeywords`,
  `first3PagesLostOrganicKeywords`
- `*Prev` fields are previous-period baselines for the matching current impression-point fields
- `first3PagesNewOrganicKeywords` and `first3PagesLostOrganicKeywords` are arrays of objects with
  `keyword`, `pageIndex`, and `pagePosition`
- `first3PagesNewOrganicKeywords` lists keywords newly entering ORG first three pages; `first3PagesLostOrganicKeywords`
  lists keywords that dropped out of ORG first three pages
- Live validation request: MCP tool `openapi_v2_product_traffic_terms_overview` on
  `http://localhost:8080/mcp`, `asin="B01CGLCGRA"`, `date="2026-06-29"`, `marketplace="US"`

### `/openapi/v2/keywords/product-traffic-terms-timeline`
- Input: `asin`, exact `keyword`, `dateFrom`, `dateTo`, optional `marketplace`, `page`, `pageSize`,
  `sortBy`, `sortOrder`
- Data window: ASIN + keyword timeline across the requested date range; date range cannot exceed 60 days
- Date rule: prefer T-1 or earlier for `dateTo`; avoid current-date lookup unless explicitly requested
- Response shape: `data` is an array
- Metric groups:
  - `keyword*` fields are keyword traffic-forecast dependency data for the provided keyword's corresponding metric period, indicated by `keywordPeriodStartDate` / `keywordPeriodEndDate`
  - `latest*` fields are the ASIN's latest product/listing/rank snapshot on the specified `date`
  - impression-point fields, `avg*` fields, ad-activity fields, and placement observations are rolling metrics for the most recent 7 days ending at the given `date`
- Diagnosis curves/events: price (`latestPrice`), BSR (`latestSmallCategoryBsr`, `latestBigCategoryBsr`),
  sales (`latestMonthlySaleCnt`), rating (`latestRatingAmt`, `latestRatingCnt`), traffic estimate
  (impression-point fields plus `avgOrganicObservation` / `avgAdObservation`), and listing events
  (`latestTitle`, `latestMainImageLink`)
- Key fields from live localhost MCP response: `date`, `site`, `asin`, `keyword`, listing snapshot fields
  such as `latestTitle`, `latestPrice`, `latestCurrency`, `latestLink`, `latestMainImageLink`,
  `latestBrandName`, `latestMonthlySaleCnt`, `latestRatingAmt`, `latestRatingCnt`,
  `latestSmallCategoryName`, `latestSmallCategoryBsr`, `latestBigCategoryName`,
  `latestBigCategoryBsr`, `latestProductHasVideo`; placement fields such as `exploreTypes`,
  `exploreRecommendTypes`, `organicImpressionPoint`, `sponsoredProductImpressionPoint`,
  `sponsoredBrandImpressionPoint`, `sponsoredBrandVideoImpressionPoint`,
  `sponsoredRecommendImpressionPoint`, `latestOrganicPosition`, `latestOrganicPageIndex`,
  `latestOrganicPagePosition`, `latestOrganicObservedAt`, `latestAdPosition`,
  `latestAdPageIndex`, `latestAdPagePosition`, `latestAdObservedAt`, `avgOrganicObservation`,
  `avgAdObservation`; keyword snapshot fields such as `keywordPeriodStartDate`,
  `keywordPeriodEndDate`, `keywordEstimateSearchCnt`, `keywordEstimateSearchGrowthCnt`,
  `keywordAbaRank`, `keywordAbaRankGrowthCnt`, `keywordAbaTopClickShareRate`,
  `keywordAbaTopConversionShareRate`, `keywordTitleDensity`, `keywordTotalSkuCnt`,
  `keywordObservedSkuCnt`, `keywordOrganicSkuCnt`, `keywordSponsoredProductSkuCnt`,
  `keywordSponsoredBrandSkuCnt`, `keywordSponsoredBrandVideoSkuCnt`,
  `keywordSponsoredRecommendSkuCnt`; ad activity fields `adActiveObservationCount`,
  `adActiveDayCoverageRate`, `adCampaignCnt`, `adCnt`
- Live validation request: MCP tool `openapi_v2_product_traffic_terms_timeline` on
  `http://localhost:8080/mcp`, `asin="B01CGLCGRA"`, `keyword="yoga mat"`,
  `dateFrom="2026-06-23"`, `dateTo="2026-06-29"`, `marketplace="US"`

## Local Review Toolkit

When `/reviews/analysis` lacks aggregation (ASIN has <50 reviews or no daily snapshot),
fall back to live raw reviews + your own LLM. The toolkit does NOT call any external
LLM — you (the calling skill's LLM) perform the Map/Reduce steps.

**Workflow:**

```bash
# 1. Fetch raw reviews (up to 100, cursor-paginated, ~60s, 10 credits at full)
zoodata.py reviews-raw --asin B0XXXXXXXX [--marketplace US] [--max-pages 10]

# 2. For EACH review, render the per-review Map prompt
zoodata.py review-tag-prompt --review '<single review JSON>' \
    [--product-title "..."] [--product-category "..."]
# → Your LLM produces a JSON object with sentiment + 11 dimension arrays
#   (mentioned_scenarios, mentioned_issues, mentioned_positives, mentioned_improvements,
#    mentioned_buying_factors, mentioned_pain_points, user_profiles, mentioned_usage_times,
#    mentioned_usage_locations, mentioned_behaviors, keywords)
# Suggested map parallelism: ~20 concurrent if your LLM supports it

# 3. Collect candidate phrases per dimension. For EACH dimension render the Reduce prompt
zoodata.py review-reduce-prompt --label-type positives \
    --candidates '["comfortable","comfy","very comfortable",...]'
# → Your LLM produces {clusters: [{canonical, members}, ...]}
# Suggested chunk size for `keywords` dim when >150 candidates: 150 per call

# 4. Aggregate into reviews/analysis-compatible consumerInsights
zoodata.py review-aggregate --reviews raw.json --tagged tags.json --clusters clusters.json
# → Output shape matches /reviews/analysis: reviewCount, avgRating,
#   sentimentDistribution, consumerInsights[], topKeywords[]
```

**When to use the toolkit instead of `reviews/analysis`:**
- ASIN has fewer than 50 reviews
- `reviews/analysis` returns sparse `consumerInsights` (missing dimensions)
- Need the freshest possible data (Spider scrape vs. T+1 BigQuery snapshot)
- Need to analyze a brand-new product that has no daily snapshot yet

## Field Differences Across Endpoints

| Data | markets | products/competitors | realtime/product | reviews/analysis | realtime/reviews | price-band | brand | history |
|------|---------|---------------------|----------|---------|---------|------------|-------|---------|
| Sales | sampleAvgMonthlySales | monthlySalesFloor | ❌ | ❌ | ❌ | sampleSalesRate | sampleGroupMonthlySales | monthlySalesFloor[] |
| Price | sampleAvgPrice | price | buyboxWinner.price | ❌ | ❌ | bandMin/MaxPrice | sampleAvgPrice | price[] |
| BSR | sampleAvgBsr | bsr (int) | bestsellersRank[] | ❌ | ❌ | ❌ | ❌ | bsr[] |
| Rating | sampleAvgRating | rating | rating | avgRating | rating (per review) | sampleAvgRating | sampleAvgRating | rating[] |
| Reviews | sampleAvgReviewCount | ratingCount | ratingCount | reviewCount | reviews[] (raw text, max 100) | ❌ | sampleAvgRatingCount | ratingCount[] |
| Insights | ❌ | ❌ | ❌ | ✅ consumerInsights | ❌ (raw only — feeds Local Review Toolkit) | ❌ | ❌ | ❌ |
| Concentration | topSalesRate | ❌ | ❌ | ❌ | ❌ | sampleTop3BrandSalesRate | CR10 | ❌ |
| Opportunity | ❌ | ❌ | ❌ | ❌ | ❌ | sampleOpportunityIndex | ❌ | ❌ |

## Confidence Labels (all skills)
- 📊 **Data-backed** — direct API data
- 🔍 **Inferred** — logical reasoning from data
- 💡 **Directional** — suggestions, predictions

Strategy recommendations and subjective conclusions are NEVER 📊. Extreme growth (>200%) = 💡 only.

## Data Notes
- Sales (`monthlySalesFloor`) = lower-bound estimate
- Realtime = live; products/competitors = ~T+1 delay
- Amazon US only (amazon.com) — more marketplaces planned
- Each call consumes credits; check `meta.creditsConsumed`

## Links
- [zoodata.ai](https://zoodata.ai) · [API Docs](https://api.zoodata.ai/api-docs) · [GitHub](https://github.com/SerendipityOneInc/ZooData-Skills) · support@zoodata.ai
