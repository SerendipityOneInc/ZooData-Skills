# Execution Guide — Complete Protocols

This document contains detailed execution standards for Full-mode analysis.
Load when performing comprehensive product selection, market analysis, or competitor comparison.

---

## Execution Mode

| Task Type | Mode | Behavior |
|-----------|------|----------|
| Single ASIN lookup, simple data query | **Quick** | Execute command, return key data. Skip evaluation criteria and output standard block. |
| Market analysis, product selection, competitor comparison, risk assessment | **Full** | Complete flow: command → analysis → evaluation criteria → output standard block. |

**Quick mode trigger:** User asks for a single specific data point ("B09XXX monthly sales?", "how many brands in cat litter?") — no decision analysis needed.

**Credit-conscious scanning:** For opportunity discovery with limited credits, use 2 modes × 1 page (instead of 5 modes × 5 pages) + brand-overview + price-band-overview ≈ ~10 credits. Label output: "Quick Scan — reduced sample, directional only."

---

## Product Selection Mode Mapping

> **Modes are CLI-local presets, NOT API parameters.** `zoodata.py` expands `--mode` into real filter fields before the call — copy them from `PRODUCT_MODES` in `{skill_base_dir}/scripts/zoodata.py` if you bypass the CLI. For a raw `products/search` request, never send `mode`, `salesMin`, or `ratingsMax`; use the expanded API filters, distinguish `ratingMax` from `ratingCountMax`, and send `categoryPath` as a JSON array.

| Mode | One-line Description |
|------|---------------------|
| `fast-movers` | Monthly sales≥300, growth≥10% — quick turnover |
| `emerging` | Monthly sales≤600, growth≥10%, ≤6 months old |
| `single-variant` | Growth≥20%, 1 variant, ≤6 months — small & rising |
| `high-demand-low-barrier` | Monthly sales≥300, reviews≤50 — easy entry |
| `long-tail` | BSR 10K-50K, ≤$30, exclusive sellers — niche |
| `underserved` | Monthly sales≥300, rating≤3.7 — improvable products |
| `new-release` | Monthly sales≤500, New Release tag |
| `fbm-friendly` | Monthly sales≥300, self-fulfilled |
| `low-price` | ≤$10 products |
| `broad-catalog` | BSR growth≥99%, reviews≤10, ≤90 days |
| `selective-catalog` | BSR growth≥99%, ≤90 days |
| `speculative` | Monthly sales≥600, ≥3 sellers |
| `top-bsr` | BSR≤1000 best sellers |

Modes can combine with explicit filters (`--price-max`, `--sales-min`, etc). Overrides win.

## Pre-Execution Checklist (MANDATORY for Full Mode)

Before running any Full-mode product selection or market analysis, **complete this checklist**:

- [ ] **Step 1 — Mode Selection:** Check the Product Selection Mode Mapping in this guide. If ANY of the 13 preset modes matches the user's intent, **USE IT** (`--mode xxx`). Do NOT manually piece together filters when a preset mode exists.
- [ ] **Step 2 — Realtime Supplement:** Plan to call `product --asin` for the top 3-5 ASINs from results.
- [ ] **Step 3 — Review Analysis:** Plan to call `analyze --asins` for top ASINs to get consumer insights (especially painPoints, improvements, buyingFactors).
- [ ] **Step 4 — Output Blocks:** Prepare to include Disclaimer, Confidence Labels, Data Provenance, and API Usage.

---

## parentAsin Handling

If `realtime/product` returns null fields (common for variant/child ASINs), use `products/search --keyword "{asin}"` to find the parentAsin, then re-fetch with the parent ASIN. Do not report null data — always attempt parent resolution first.

---

## Leader/Benchmark Deduplication

When selecting Top 5 products for benchmarking or comparison, deduplicate by parentAsin — if multiple results share the same parent (color/size variants), keep only the highest-selling variant. The goal is 5 distinct products, not 5 variants of the same listing.

---

## Competitors Fallback

If competitors endpoint returns empty results (common with broad keywords), rely on `products/search` sorted by sales as the competitor discovery source. Tell the user the primary competitors endpoint returned no data and that the competitor set comes from a sales-ranked products fallback.

---

## Review Analysis Protocols

### Independent Brand Analysis
When comparing multiple brands, analyze each brand's ASIN separately — do NOT combine ASINs from different brands in a single `analyze` call. Mixed-ASIN analysis produces averaged insights that hide competitive differences and cannot be attributed to specific brands.

### Fallback for Insufficient Reviews
If `analyze` returns insufficient data (requires 50+ reviews), fall back to `realtime/product` ratingBreakdown data. Extract sentiment distribution from star ratings. Disclose that direct review analysis was unavailable and that sentiment is derived from the star-rating breakdown — a lower-confidence proxy, not full review analysis.

When the user specifically needs the full review dimensions and the shared CLI contract classifies the result as non-terminal, use `reviews-raw --asin` for a bounded sample, render per-review Map prompts with `review-tag-prompt`, cluster candidate phrases with `review-reduce-prompt`, and combine tagged reviews with `review-aggregate`. State that these are sample-derived insights, not a replacement for unavailable full-corpus review analysis. Filter `consumerInsights` by returned `labelType` locally; it is not an API request filter.

### Review Fallback Chain
`realtime/product` provides ratingBreakdown (star distribution). When reviews/analysis is unavailable (insufficient reviews), use this as the consumer insight source. Cross-validate: compare positive_sentiment% from analyze against (4+5 star)% from ratingBreakdown — if gap > 15%, flag potential discrepancy.

---

## Realtime Data Supplementation

When `products` or `competitors` returns ASINs in Full-mode analysis, call `product --asin` for the top 3-5 most relevant ASINs to get current real-time data. For bulk lookups (>3 ASINs), confirm with the user before proceeding.

**When to supplement**: Product selection / competitor analysis → top 3 by sales. Risk assessment → target + top 2 competitors. Multi-product comparison → all compared ASINs (max 5). Skip for: single ASIN lookup, market overview, listing analysis.

**Data conflict rule**: `products`/`competitors` = ~T+1 delay; `realtime/product` = live. Use realtime for price/BSR/rating; use products/competitors for sales/margin/fees. Note significant differences: "⚡ Price updated: $29.99 → $24.99 (likely promotion)"

---

## Category Resolution — Detailed Flow

1. Query categories endpoint with the user's keyword
2. If empty or too broad, split/broaden keyword and retry (up to 3 variations)
3. If still no match, use realtime/product on a known ASIN to extract categoryPath
4. Validate categoryPath matches the user's intended product type

**Data-driven category selection:** When the user provides a broad interest (e.g. "home products") instead of a specific niche, resolve its category ID with `categories`, browse children with `categories --parent`, and call `market --category-id` for candidates. Compare returned `sampleNewProductRate6m`, `sampleTop10BrandSalesRate`, `sampleFbmRate`, and `sampleMedianPrice` as separate selected Top 100 observations; keep them separate from full-category totals and avoid an uncalibrated composite score. Select Top 3-5 for deeper analysis.

---

## Growth Signal Validation

- A single product's high growth rate (e.g. +900%) may be seasonal rebound, restock recovery, or promotion spike — NOT necessarily a market trend
- To validate: check if the MAJORITY of products in the category show positive growth, not just 1-2 outliers
- Flag seasonal patterns explicitly: "This growth coincides with [season], which may be temporary"
- Mark single-product growth signals as 💡 **Directional**, not 📊 **Data-backed**

---

## Alert Signal Tiers (for monitoring scenarios)

- 📊 **Sustained trend** — multiple data points over 7+ days showing consistent direction
- 🔍 **Possible signal** — 2-3 days of change, needs more observation
- 💡 **Single-day spike** — could be promotion, restock, or data lag; do not treat as confirmed trend

---

## Sales Estimation Fallback

When `monthlySalesFloor` is null: **Monthly sales ≈ 300,000 / BSR^0.65**

---

## Output Standards — Full Specification

**Data consistency rule:** The same metric must use the same precision throughout the report. Do NOT use "10K+" in one table and "47,000" in another for the same product. Pick one level of precision and apply it consistently across all sections.

Respond in the user's language, retaining API field names and established technical terms in English. Show findings, the actual query conditions (`_query.params`, category identity, date, scope, sample type), and data notes about estimation, freshness, and sampling.

**Sample bias disclosure:** Clearly state in the report body (not just Data Provenance): "This analysis is based on Top [N] products by sales volume, which skews toward established products. New or niche products may be underrepresented."

**Scope acknowledgment:** End every strategy/recommendation section with: "This analysis covers [list dimensions covered]. Dimensions not covered by this data include: advertising costs (CPC/ACoS), search keyword competition, supply chain logistics, and regulatory compliance. Consider supplementing with additional tools before final decisions."

**Anomaly handling:** Products with extreme growth rates (>200%) or sudden BSR changes must be tagged 💡 Directional, never 📊 Data-backed. Do NOT claim "proves innovation works" or "confirms market opportunity" based on a single product's spike. State: "Product X showed [metric], which MAY indicate [hypothesis]. Further validation needed."

### Disclaimer (every Full-mode report)

> ⚠️ **Important**: This analysis is based on ZooData API data as of [date]. Sales figures are lower-bound estimates. Market conclusions are directional indicators based on available data, not definitive business recommendations. Always validate key findings with additional sources before making business decisions.

### Confidence Labels (every conclusion must be tagged)

**Confidence labels — tag every conclusion with one of:**
- 📊 **Data-backed** — Supported by API data with cross-validation
- 🔍 **Inferred** — Reasonable inference, not directly measured
- 💡 **Directional** — Hypothesis only, verify before acting

Do not label a section heading, summary, or table grouping 📊 when any content under it is inferred or directional. Omit a grouping label or use its least certain contained tier. Reserve 📊, 🔍, and 💡 for confidence labels, not decorative prefixes. Strategy suggestions never receive 📊; user-supplied decision criteria take precedence over default thresholds.

### Data Provenance Block (Full Mode Only)

Use this rendered template at the end of every Full-mode report:

---

📋 **Data Provenance**

| Item | Value |
|------|-------|
| Query Keyword | [keyword used] |
| Locked CategoryPath | [resolved category] |
| Category Resolution | [how many attempts, final path] |
| Marketplace | [US/etc] |
| Timestamp | [date] |
| Sample Size | [total returned / post-filter valid / analyzed] |
| Data Freshness | DB data ~T+1, realtime = live |
| Endpoints Used | [list with call count] |
| Credits Consumed | [total] |
| Known Limitations | [list any gaps] |

**Rules**:
1. Every Full-mode analysis MUST end with this block
2. Filter conditions MUST list specific parameter values
3. If multiple interfaces used, list each one
4. If data has limitations, proactively explain
5. ⚠️ **Self-check:** scan your response — if you don't see `📋 **Data Provenance**`, ADD IT before replying

### API Usage Summary (All Modes — MANDATORY)

Use this rendered template at the end of every report:

**API Usage**

| Interface | Calls counted by CLI |
|-----------|-------|
| (each observed endpoint) | (actual call count) |
| Unattributed internal calls, if any | (count) |
| **Calls with credit metadata** | **(returned `meta.apiCalls` or unavailable)** |
| Failed calls without credit metadata | (visible count or unavailable) |
| **Credits consumed** | **(returned total or unavailable)** |
| **Credits remaining** | **(returned value or unavailable)** |

**Tracking rules:**
1. Count endpoint calls, not CLI executions. A composite invocation can make several calls. The CLI's top-level `meta.apiCalls` counts calls that returned credit metadata. Inspect nested `_query.endpoint` values to attribute visible calls, and show any difference as unattributed internal calls. List visible failed calls without credit metadata separately; they may be absent from `meta.apiCalls`. Do not invent endpoint identities for calls omitted from the composite payload.
2. For each CLI invocation, take the top-level `meta.creditsConsumed` as its accumulated credit total. Sum those top-level totals across separate invocations; do not add a composite's nested credit values to its top-level total again.
3. Use the latest returned top-level `meta.creditsRemaining` across invocations. If `meta.apiCalls` or a credit field is absent, report the unavailable value instead of deriving credits from call counts.
4. Check that the final report contains an `API Usage` block with actual call and credit evidence.

---

## Shared analysis framework

Every analysis should address these dimensions where data is available:

### Market Health Assessment

Use the thresholds in `Market Health Assessment` below only with matching returned fields and denominator.

### Competitive Position Assessment
- **Price vs category avg**: >20% above = premium positioning, >20% below = value play 🔍
- **Rating vs category avg**: ≥0.3 above = quality advantage, ≥0.3 below = quality risk 🔍
- **Review count vs Top 10 avg**: <10% of leaders = high barrier, >50% = competitive 🔍
- **BSR trend (30d)**: Improving = momentum, stable = holding, declining = losing share 🔍

### Opportunity Viability
When user asks "should I sell X" or "is this a good niche":
- Compare selected-sample demand, review burden, and `sampleTop10BrandSalesRate` separately against markets with compatible category scope, sample selector, and date. A selected Top 100 rate alone does not establish entry viability.
- Treat seller costs, product differentiation, and compliance evidence as separate inputs before an entry verdict.
- Mixed signals → Present data, let user decide with their domain knowledge 💡

### Sales Estimation Notes
- `monthlySalesFloor` is a **lower-bound** estimate 📊
- Null sales fallback: Monthly sales ≈ 300,000 / BSR^0.65 🔍
- For market revenue interpretation, use `Market Health Assessment` below.

## Market Health Assessment

Use `totalMonthlyRevenue` from `markets/search` for full-category revenue and `sampleMonthlyRevenue` for its selected sample. Do not calculate revenue from price × sales; the field definitions are in `reference.md § 2`.

| Indicator | Good | Caution | Warning |
|-----------|------|---------|---------|
| Monthly demand (`sampleMonthlySales`) | >1,500 units 🔍 | 500-1,500 🔍 | <500 🔍 |
| Avg review count (`sampleAvgRatingCount`) | <500 🔍 | 500-5,000 🔍 | >5,000 🔍 |
| FBM rate (`sampleFbmRate`) | <40% 🔍 | 40-60% 🔍 | >60% 🔍 |

These remaining bands are exploratory heuristics, not calibrated entry verdicts. Read `sampleTop10ProductSalesRate` and `sampleTop10BrandSalesRate` as separate selected Top 100 monthly-sales concentration measures. Read `sampleNewProductRate6m` as a six-month new-product share within that sample. Do not classify these three rates from former fixed cutoffs; compare compatible peers or prior snapshots and state the observed denominator.

## Cross-endpoint evidence use

Read `reference.md § Cross-endpoint field identity` before matching fields across endpoints.

**Usage rule:**
- `products`/`competitors` → sales, pricing, competition
- `realtime/product` → review details, listing content, seller info
- `market` → category-level aggregates
- `reviews/analysis` → AI-powered review insights
- `price-band-*` → price segment analysis and opportunity
- `brand-*` → brand landscape and concentration
- `history` → historical trends
- For reports: combine quantitative + qualitative + consumer insights + market structure

## Error Handling

Errors are handled by the script with structured JSON output. **Never expose error details to users.**
Self-check: `python3 scripts/zoodata.py check`

For a terminal interface failure, give one concise notice that analysis could not be completed and list succeeded and failed endpoint identifiers. Do not render findings, recommendations, an API-usage table, or another workflow choice. Keep parameters and retry logs internal unless diagnostics are requested. For a missing key, explain where to configure `ZOODATA_API_KEY`; for `_transport.status=401`, explain the key was rejected; for 402, report where the workflow stopped and returned credit metadata without fabricating missing data.

| Error | Fix |
|-------|-----|
| `Cannot index array with string` | If the response `data` is an array, use `.data[0].fieldName`; otherwise inspect the actual payload shape first |
| Empty `data: []` | Use `categories` to confirm category exists |
| `monthlySalesFloor: null` | BSR estimate: 300,000 / BSR^0.65 |

**FORBIDDEN in Data Provenance**: HTTP status codes (422, 500, 403), endpoint failure details, "fallback", "degraded", "retry", internal implementation details. The user should see clean data sourcing, not debugging logs.

---

## API Coverage Boundaries

| Scenario | Coverage | Suggestion |
|----------|----------|------------|
| Market data: Popular keywords | ✅ Has data | Use `--keyword` directly |
| Market data: Niche/long-tail keywords | ⚠️ May be empty | Use `--category` instead |
| Product data: Active ASIN | ✅ Has data | — |
| Product data: Delisted/variant ASIN | ❌ No data | Try parent ASIN or realtime |
| Real-time data: US site | ✅ Full support | — |
| Real-time data: Non-US sites | ⚠️ Partial | Core fields OK, sales may be null |
