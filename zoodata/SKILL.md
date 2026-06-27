---
name: zoodata
description: >
  API endpoint reference for the ZooData data platform. Provides the 12
  commerce endpoints plus 6 keyword intelligence endpoints (categories,
  markets, products, competitors, realtime ASIN, AI review analysis, raw
  reviews, price band, brand, history, keyword detail/trend/extends/search
  results/product traffic/competitor keywords), their inputs/outputs,
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
  version: "1.1.3"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

> **📋 Live API Reference**: Field names and parameters may change. If you encounter field errors,
> check the latest OpenAPI spec at https://zoodata.ai/api/v1/openapi-spec for current field definitions.

# ZooData — Commerce Data Infrastructure for AI Agents

200M+ Amazon products. 18 endpoints. One API key.

## Quick Start
1. Get key: [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys) (1,000 free credits)
2. `export ZOODATA_API_KEY='hms_live_xxx'`
3. Base URL: `https://api.zoodata.ai/openapi/v2` — all POST with JSON body
4. Auth: `Authorization: Bearer YOUR_API_KEY`
5. New keys need 3-5s to activate. If 403, wait and retry.

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

## On Missing Key (no credentials configured)

**BEFORE calling any endpoint**, verify credentials are configured. The reliable check is `python {skill_base_dir}/scripts/zoodata.py check` — exits 2 if no key is found in env vars OR config files. A `[ -z "$ZOODATA_API_KEY" ]` test alone is NOT sufficient — a user may have only `~/.zoodata/config.json` set.

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

## 18 Endpoints

| # | Endpoint | Purpose | Key Output |
|---|----------|---------|------------|
| 1 | `categories` | Browse/search category tree | categoryPath, productCount |
| 2 | `markets/search` | Market-level metrics | sampleAvgMonthlySales, sampleAvgPrice, topSalesRate, sampleNewSkuRate |
| 3 | `products/search` | Product search (14 modes) | asin, price, monthlySalesFloor, rating, ratingCount, fbaFee |
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
| 14 | `/openapi/v2/keywords/trend` | Weekly keyword time series | `estimateSearchCount`, `abaRank`, `rankChangeCount`, `periodStartDate`, `periodEndDate` |
| 15 | `/openapi/v2/keywords/extends` | Keyword expansion / long-tail discovery | related keywords ranked by `relevanceScore` / `estimateSearchCount`; may return empty array |
| 16 | `/openapi/v2/keywords/search-results` | Daily keyword SERP snapshot | `asin`, `exploreType`, `absolutePosition`, `estimateImpressionPoint`, listing fields |
| 17 | `/openapi/v2/keywords/competitor-product-keywords` | Keyword set where an ASIN appears as a competitor | `keyword`, `avgPosition`, `keywordEstimateSearchCount`, `trafficShare` |
| 18 | `/openapi/v2/keywords/product-traffic-terms` | Traffic-driving keywords for an ASIN | same live response shape as competitor-product-keywords |

## Known Quirks
- `topN`, `listingAge`, `newProductPeriod` are **strings** (`"10"` not `10`)
- Many search/list endpoints return `.data` as an **array** — use `.data[0]` for the first record. But some commands may return non-array payloads inside `data`, so inspect the actual response shape before indexing.
- `ratingCount` not `reviewCount` everywhere
- `bsr` (int) in products vs `bestsellersRank` (array) in realtime
- `buyboxWinner.price` — NOT top-level `price` in realtime
- `realtime/product` does NOT return: monthlySalesFloor, fbaFee, sellerCount
- `reviewCountMin/Max` filters currently broken (API-56)
- `reviews/analysis` may 500 for certain ASINs (API-58) — retry different ASIN
- Rate limit: 100 req/min, 10 req/sec burst
- `categories` uses `categoryKeyword` (not `keyword`) and `parentCategoryPath` (not `parentCategoryName`)
- `reviews/analysis`: `mode` required ("asin"/"category"), use `asins` (plural array) not `asin`
- `realtime/reviews`: returns 10 reviews/page fixed (no `pageSize` param); 1 credit/page; cursor-paginated; hard cap = 100 reviews (10 pages); supports `marketplace` US/UK only
- `keywords/detail` resolves the input `date` to the nearest available weekly snapshot at or before that date, and may legitimately return `data: null` even with `success: true`
- `keywords/extends` also resolves the input `date` to the nearest available weekly snapshot, requires `query` (not `keyword`), supports `queryType` = `phrase` or `fuzzy`, and may legitimately return `data: []`
- `keywords/search-results`, `keywords/competitor-product-keywords`, and `keywords/product-traffic-terms` use daily observations over a sliding ~7-day window, not a long-retention historical store
- `keywords/search-results` requires `date` + `keyword`; `exploreTypes` values are `ORG`, `SP`, `SB`, `SBV`, `SPR`
- `keywords/competitor-product-keywords` and `keywords/product-traffic-terms` require `date` + `asin`; both currently return the same live item shape, including `trafficShare`
- `keywords/search-results` is the default source for explaining what products currently appear on a keyword SERP because it already returns listing-level product fields
- `products/search` is a broader ZooData product-database query and must not be presented as Amazon live keyword SERP ordering

## Keyword Intelligence Endpoints

These six endpoints were verified against the live API surface and fill the gap between raw
catalog data and search-demand/search-visibility intelligence.

### `/openapi/v2/keywords/detail`
- Input: `keyword`, `date`, optional `marketplace`
- Data window: resolves the requested `date` to the nearest available weekly snapshot at or before that date
- Response shape: top-level `data` is an object or `null` (not an array)
- Key fields from schema: `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`,
  `abaTop3ConversionShareRate`, `marketCharacteristics`, `totalSkuCnt`, `brandCount`,
  `organicSkuCount`, `adCampaignCount`, `adCount`
- Live validation note: for `keyword="yoga mat"` and several June 2026 dates, the endpoint returned
  `success: true` with `data: null`

### `/openapi/v2/keywords/trend`
- Input: `keyword`, `dateFrom`, `dateTo`, optional `marketplace`
- Data window: weekly-granularity points across the requested date range
- Response shape: `data` is an array
- Key fields from live response/schema: `observedAt`, `periodStartDate`, `periodEndDate`,
  `estimateSearchCount`, `estimateSearchChangeCount`, `estimateSearchChangeRate`, `abaRank`,
  `prevAbaRank`, `prevEstimateSearchCount`, `rankChangeCount`

### `/openapi/v2/keywords/extends`
- Input: `query`, `date`, optional `marketplace`, `page`, `pageSize`, `queryType`, `sortBy`, `sortOrder`
- Important quirk: seed field is `query`, not `keyword`; `queryType` supports `phrase` and `fuzzy`
- Data window: resolves the requested `date` to the nearest available weekly snapshot at or before that date
- Response shape: `data` is an array
- Key fields from schema: `term`, `seedKeyword`, `relevanceScore`, `estimateSearchCountWeekly`,
  `abaRank`, `marketCharacteristics`, `brandCount`, `organicSkuCount`, `adCount`,
  `periodStartDate`, `periodEndDate`, `observedAt`
- Live validation note: empty arrays are normal; `query="yoga mat"` returned `data: []` for both
  `queryType="phrase"` and `queryType="fuzzy"`

### `/openapi/v2/keywords/search-results`
- Input: `keyword`, `date`, optional `marketplace`, `page`, `pageSize`, `exploreTypes`, `sortBy`, `sortOrder`
- Data window: daily observations surfaced through a sliding ~7-day window
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
- Response shape: `data` is an array
- Key fields from live response/schema: `exploreType`, `absolutePosition`, `pageIndex`,
  `pagePosition`, `asin`, `keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`,
  `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`,
  `keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`,
  `keywordAbaRankChangeCount`, `trafficShare`

### `/openapi/v2/keywords/product-traffic-terms`
- Input: same request shape as `keywords/competitor-product-keywords`
- Data window: daily observations surfaced through a sliding ~7-day window
- Response shape: `data` is an array
- Key fields from live response/schema: `exploreType`, `absolutePosition`, `pageIndex`,
  `pagePosition`, `asin`, `keyword`, `estimateImpressionPoint`, `asinTotalEstimateImpressionPoint`,
  `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`,
  `keywordEstimateSearchGrowthCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`,
  `keywordAbaRankChangeCount`, `trafficShare`
- Live validation note: current live response item shape matches `keywords/competitor-product-keywords`
  field-for-field; keep the semantic distinction in output wording rather than assuming a unique schema

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
