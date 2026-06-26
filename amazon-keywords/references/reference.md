# Amazon Keyword Intelligence — Reference

> Load this file when you need exact endpoint choices, field priorities, or scenario-to-endpoint mapping.

## Endpoints

| Endpoint | Use in this skill | Key fields |
|----------|-------------------|------------|
| `/openapi/v2/keywords/detail` | Weekly keyword snapshot | `estimateSearchCountWeekly`, `abaRank`, `abaTop3ClickShareRate`, `abaTop3ConversionShareRate`, `marketCharacteristics`, `totalSkuCnt`, `brandCount`, `organicSkuCount`, `adCampaignCount`, `adCount` |
| `/openapi/v2/keywords/trend` | Weekly trend validation | `estimateSearchCount`, `estimateSearchChangeRate`, `abaRank`, `rankChangeCount`, `periodStartDate`, `periodEndDate` |
| `/openapi/v2/keywords/extends` | Expansion / long-tail discovery | `term`, `seedKeyword`, `relevanceScore`, `estimateSearchCountWeekly`, `abaRank`, `marketCharacteristics`, `brandCount`, `organicSkuCount`, `adCount` |
| `/openapi/v2/keywords/search-results` | SERP structure, page-1 product mix, and ad density | `exploreType`, `absolutePosition`, `pageIndex`, `pagePosition`, `asin`, `title`, `brand`, `price`, `rating`, `ratingCount`, `recentSales`, `estimateImpressionPoint`, `keywordTotalEstimateImpressionPoint` |
| `/openapi/v2/keywords/competitor-product-keywords` | Keywords where ASIN appears as competitor | `keyword`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`, `trafficShare` |
| `/openapi/v2/keywords/product-traffic-terms` | Traffic-driving keywords for ASIN | `keyword`, `avgPosition`, `daysCoverageRate`, `observationCount`, `keywordEstimateSearchCount`, `keywordEstimateSearchCountChangeRate`, `keywordAbaRank`, `trafficShare` |

## Draft Callable Tool Mapping

Use these as draft full names only. Final authority is the tool surface actually
exposed in the current session.

| HTTP endpoint path | Draft callable tool name |
|----------|--------------------------|
| `/openapi/v2/keywords/detail` | `mcp__apiclaw.openapi_v2_keyword_detail` |
| `/openapi/v2/keywords/trend` | `mcp__apiclaw.openapi_v2_keyword_trend` |
| `/openapi/v2/keywords/extends` | `mcp__apiclaw.openapi_v2_keyword_extends` |
| `/openapi/v2/keywords/search-results` | `mcp__apiclaw.openapi_v2_keyword_search_results` |
| `/openapi/v2/keywords/competitor-product-keywords` | `mcp__apiclaw.openapi_v2_keyword_competitor_product_keywords` |
| `/openapi/v2/keywords/product-traffic-terms` | `mcp__apiclaw.openapi_v2_keyword_product_traffic_terms` |

Tool selection rules:
- Use the full callable tool name, not a shortened alias
- Do not infer a callable name from another tool such as `openapi_v2_categories`
- If the live session exposes a different full name, follow the live session
- If the live session does not expose keyword tools, report that explicitly

## Endpoint Quirks

- `keywords/detail`: top-level `data` is an object or `null`
- `keywords/trend`: `data` is an array of weekly points
- `keywords/extends`: input seed is `query`; try `queryType=phrase` first, then `fuzzy`
- `keywords/search-results`: daily-ish observation in a ~7-day sliding window
- `keywords/competitor-product-keywords` and `keywords/product-traffic-terms`: same live item shape today, different business meaning

## SERP Product Interpretation Rule

- If the user asks "首页卖的都是什么产品", "这个词搜出来都是什么款", or similar, answer that primarily from `/openapi/v2/keywords/search-results`
- This endpoint already returns product-level fields such as `asin`, `title`, `brand`, `price`, `rating`, `ratingCount`, and `recentSales`, so it is not just an ad-density endpoint
- Treat `/openapi/v2/keywords/search-results` as the default source for page-1 product mix, intent shape, brand mix, and ad vs organic composition
- Do not add `products/search` by default just to explain what appears on the keyword SERP
- Add `products/search` only as an optional supplement when the user explicitly asks for broader market winners,销量分布, price-band structure, or best-selling variants beyond the observed keyword SERP

## `products/search` Boundary Rule

- `products/search` is a query against our own product database snapshot, not a direct Amazon live search-result page
- Its result set can help describe broader catalog winners,销量分布, price-band structure, and variant concentration
- Do not present `products/search` output as "Amazon search results", "Amazon首页结果", or evidence of current keyword SERP ordering
- Do not classify `products/search` as a front-end keyword SERP interface
- When both endpoints are used, describe them separately:
  `keywords/search-results` = observed keyword SERP
  `products/search` = broader product-database supplement

## `webtools_search` Boundary Rule

- `webtools_search` is a crawler / web retrieval utility, not a keyword-intelligence endpoint
- Do not use `webtools_search` as a substitute for `/openapi/v2/keywords/detail`, `/trend`, `/extends`, or `/search-results`
- Use it only when the task is genuinely about web collection or when you need an explicitly labeled supplementary source outside the APIClaw keyword endpoints

## Capability Verification Order

Before judging whether a question can be answered:

1. Read the live tool schema and field descriptions for the exposed callable tool
2. Map those fields to the business question
3. Use these docs only as confirmation or fallback
4. Treat endpoint naming alone as weak evidence, not proof

If step 1 is not possible from the current surface, report that boundary explicitly instead of inventing capability.

## Scenario Mapping

| Scenario | Must-have endpoints | Optional endpoints | Main decision output |
|----------|---------------------|--------------------|----------------------|
| Keyword expansion | `keywords/extends`, `keywords/detail` | `keywords/trend`, `keywords/search-results`, `products/search` | Candidate tiers and coarse filtering |
| Single keyword analysis | `keywords/detail`, `keywords/search-results` | `keywords/trend`, `products/search` | Worth targeting or not |
| Reverse ASIN keyword analysis | `keywords/product-traffic-terms`, `keywords/competitor-product-keywords` | `keywords/detail`, `keywords/search-results`, `products/search` | Traffic-source map and bid focus |
| Keyword traffic monitoring | `keywords/search-results`, `keywords/detail` | `keywords/trend`, ASIN keyword endpoints, `products/search` | Cause analysis for changes |

Availability interpretation:
- `Must-have endpoints` means the scenario should not be presented as fully executable without them
- `Optional endpoints` may enrich confidence or context, but they must not be silently substituted for missing must-have endpoints
- For reverse ASIN, `keywords/detail` and `keywords/search-results` are enrichers only; they do not replace the two ASIN keyword endpoints
- For traffic monitoring, if ASIN keyword endpoints are missing, omit ASIN-side traffic-share conclusions instead of inferring them
- For single keyword analysis, if `keywords/trend` is missing, keep the conclusion snapshot-led and avoid strong claims about demand direction

## Scoring Inputs

### Demand

- Primary: `estimateSearchCountWeekly`, `keywordEstimateSearchCount`
- Secondary: `estimateSearchChangeRate`, `keywordEstimateSearchCountChangeRate`, `abaRank`

### Competition

- Primary: `adCount`, `adCampaignCount`, SERP ad-slot share
- Secondary: top ASIN repetition, `avgPosition`, `trafficShare`

### Relevance

- Primary: `relevanceScore`
- Secondary: semantic closeness to seed term, alignment between keyword intent and SERP results

### Stability

- Primary: trend consistency across 4-8 weekly points
- Secondary: `daysCoverageRate`, `observationCount`

## Recommended Reporting Dimensions

### For keyword expansion

- Search demand bucket
- Competition bucket
- Relevance bucket
- Suggested usage scene: auto, broad, phrase, exact, product targeting support, or SEO observation

### For single keyword analysis

- Traffic size
- Traffic direction
- Ad crowding
- Organic room
- Head-listing strength
- Bid recommendation tier

### For reverse ASIN

- Top traffic-source keywords
- Ranking quality by keyword
- Defensive keywords vs expansion keywords
- Missing but strategically relevant competitor keywords
- Bucket labels: `Defend` / `Expand` / `Observe` / `Avoid`

### For monitoring

- Position change
- Exposure change
- Search demand change
- Ad density change
- Head competitor change
- Likely cause and urgency
