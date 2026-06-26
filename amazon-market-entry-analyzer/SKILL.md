---
name: amazon-market-entry-analyzer
description: >
  One-click market viability assessment for Amazon sellers.
  Analyzes market size, competition intensity, brand landscape, pricing structure,
  and consumer pain points to deliver a GO/CAUTION/AVOID recommendation.
  Uses all 11 ZooData API endpoints with cross-validation for data-backed decisions.
  Use when user asks about: market entry, can I sell, should I enter, market viability,
  is this niche worth it, category analysis, market opportunity, market assessment,
  niche evaluation, product category research.
  Requires ZOODATA_API_KEY.
metadata:
  version: "1.0.3"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# Amazon Market Entry Analyzer — GO / CAUTION / AVOID

One input (keyword/category). Full market viability assessment with sub-market discovery.

## Files
- **Script**: `{skill_base_dir}/scripts/zoodata.py` — run `--help` for params
- **Reference**: `{skill_base_dir}/references/reference.md` (field names & response structure)

## Credential
Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys)

## Input
- **Required**: keyword or categoryPath
- **Optional**: marketplace (default US)
- **Optional (seller-side — drives the Small-Seller Entry Risk Gates section below)**:
  - `budget` — first-6-month capital available (e.g. "$10K", "$50K", "$200K+")
  - `risk_tolerance` — low / medium / high
  - `ip_concern` — known compliance, patent, trademark, or restricted-category concerns; or "none"

  If the user hasn't supplied these, **ask once at the start of the workflow** (a single batched question is fine). If the user declines or skips, **omit the Risk Gates section from the final verdict** and add a line under Data Provenance: "Risk Gates: skipped — seller-side inputs not provided." **Do not guess thresholds** — silent gate evaluation with invented inputs produces inconsistent verdicts across runs.

## API Pitfalls (shared with zoodata skill — critical!)
- Keyword search is broad → categoryPath is auto-resolved via `categories` endpoint, with fallback to top search result. If `category_source` is `inferred_from_search`, confirm with user
- Brand/price-band queries **MUST include --category** to avoid cross-category contamination
- Revenue = `sampleAvgMonthlyRevenue` (NEVER calculate avgPrice × totalSales — overestimates 30-70%)
- Sales = `monthlySalesFloor` (lower bound). Fallback: 300,000 / BSR^0.65, tag 🔍
- Use `sampleOpportunityIndex`, `sampleTop10BrandSalesRate` directly — never reinvent
- `reviews/analysis` needs 50+ reviews. Fallback chain when sample is insufficient:
  1. **Lightweight**: `realtime/product` ratingBreakdown — only star distribution, no themes
  2. **Full 11-dim insights** — bypass `/reviews/analysis` entirely:
     a. `zoodata.py reviews-raw --asin X` → fetch up to 100 raw reviews (10 credits, ~60s)
     b. For each review: render Map prompt via `zoodata.py review-tag-prompt --review '<json>'`
        and have your own LLM produce JSON tags (sentiment + 11 dimensions)
     c. Collect candidate phrases per dimension; for each dimension render
        Reduce prompt via `zoodata.py review-reduce-prompt --label-type X --candidates '[...]'`
        and have your LLM produce semantic clusters
     d. `zoodata.py review-aggregate --reviews R --tagged T --clusters C`
        → consumerInsights output compatible with `/reviews/analysis`
  3. **Fallback caveats** (apply to the 4-step chain above — lessons from end-to-end validation):
     - **Working dir**: `WORK=/tmp/review_<ASIN>_$(date +%s) && mkdir -p $WORK`
     - **Step b CLI behavior**: `review-tag-prompt` RENDERS the prompt only; YOUR LLM produces the JSON. Render once to learn the schema, then produce tags for all N reviews in one in-context pass (don't call the CLI N times).
     - **Step c candidate extraction** (Python one-liner):
       `candidates = {d: sorted({el.strip().lower() for t in tagged for el in (t.get(d) or [])}) for d in DIMS}`
     - **Small-sample rule (reviewCount<50)**: demote single-mention items 📊→🔍; NEVER attach table-level or section-header 📊 when any row inside is 🔍; suppress "🔴 Critical" verdicts on count=1
     - **Scope**: fallback replaces ONLY the `/reviews/analysis` aggregation. This skill's primary workflow outputs (GO/CAUTION/AVOID verdict, market size, brand/price analysis) remain valid — do not re-run them.
- Aggregation endpoints without categoryPath produce severely distorted data

## On 401 Invalid Key

When `zoodata.py` returns code 401: follow the **"On 401 Invalid Key"** protocol in `zoodata/SKILL.md` — STOP further calls, tell the user the key was rejected and direct them to api-keys, do not fabricate missing data.

## On 402 Credit Exhausted

When `zoodata.py` returns code 402: follow the **"On 402 Credit Exhausted"** protocol in `zoodata/SKILL.md` — STOP further calls, report partial findings already gathered, do not fabricate missing data.

## Unique Logic

### Sub-Market Discovery
Run `market --category "{path}" --topn 10 --page-size 20`, paginate all pages. Score each sub-market (1-100):

| Dimension | Weight | Field | Good→100 | Bad→0 |
|-----------|--------|-------|----------|-------|
| Demand | 25% | sampleAvgMonthlySales | ≥1500 | <200 |
| Profit | 25% | sampleAPlusRate | ≥0.35 | <0.15 |
| New Entrant | 20% | sampleNewSkuRate | ≥0.20 | <0.05 |
| Brand Openness | 20% | topBrandSalesRate | ≤0.50 | ≥0.90 (inverted) |
| Capacity | 10% | totalSkuCount | 300-8000 | extreme |

**Fallback** (grossMargin=0 for all): redistribute to Demand 30%, New Entrant 25%, Brand 25%, Capacity 20%.

Present TOP 10 sub-markets. Ask user which to deep-dive (default: top 3). If ≤3 sub-markets, deep-dive all.

### Market Viability Score (1-100)

| Dimension | Weight | Good | Medium | Warning |
|-----------|--------|------|--------|---------|
| Market Size | 15% | >$10M/mo | $5-10M | <$5M |
| Market Trend | 10% | Rising | Stable | Declining |
| Competition | 25% | CR10<40% | 40-60% | >60% |
| Price Opportunity | 15% | oppIndex>1.0 | 0.5-1.0 | <0.5 |
| New Entrant Space | 10% | >15% | 5-15% | <5% |
| Consumer Pain Points | 15% | Clear gaps | Some | None |
| Profit Potential | 10% | >30% | 15-30% | <15% |

### Go/No-Go Decision
| Score | Signal | Action |
|-------|--------|--------|
| 70-100 | ✅ GO | Proceed with product development |
| 40-69 | ⚠️ CAUTION | Possible but needs differentiation |
| 0-39 | 🔴 AVOID | Too competitive or too small |

**CR10 dual-level check**: Category CR10 PASS + sub-market CR10 FAIL → ⚠️ CAUTION. Both FAIL → AVOID.
**User criteria override**: If user sets thresholds, ANY fail → CAUTION/AVOID. Never override.

### Small-Seller Entry Risk Gates
Before upgrading a market to GO, run these gates against the user's budget, operating constraints, and risk tolerance:

| Gate | Pass Signal | Hard-Block Signal |
|------|-------------|-------------------|
| Capital fit | First order, launch PPC, storage, and cash cycle fit available runway | MOQ, inventory, or ad spend requires more cash than the seller can safely hold |
| Review barrier | Top competitors' review counts, ratings, and review velocity are reachable with a realistic launch plan | Conversion depends on matching an entrenched review moat |
| Compliance/IP risk | Certifications, restricted claims, safety rules, and trademark/design risks are known and manageable | Unresolved compliance, patent, trademark, or restricted-product exposure |
| Differentiation evidence | Clear pain point, feature, bundle, content, or price-band wedge | Only commodity resale, copycat design, or no defendable reason to buy |
| Validation speed | Demand and positioning can be tested in 7-30 days with samples or lightweight listings | Proof requires tooling, a full PO, or a large irreversible launch |

Decision adjustment (precedence is pinned — apply in order):

1. **Final verdict formula**: `final = MIN(score_tier, lowest_gate_tier)` where the tier ordering is `GO > CAUTION > AVOID`. A score-90 GO with one gate at AVOID → final AVOID; a score-90 GO with one gate at CAUTION → final CAUTION.
2. **GO** requires BOTH a passing viability score AND every gate in PASS (or with a documented mitigation plan in the same workflow turn).
3. **CAUTION** fits markets with 1–2 uncertain gates that can plausibly be validated inside the **Validation Speed** window (7–30 days, sampled or lightweight listing).
4. **AVOID is mandatory** when any of {Compliance/IP, Capital fit, Review barrier} is a hard-block — regardless of viability score. These three categories are non-negotiable for small sellers.
5. **Relationship to "User criteria override" above**: that rule remains authoritative — if the user sets explicit thresholds (e.g. "min monthly sales 500", "max CR10 50%"), those override even gates. The Gates fire as the default backstop when no user-set thresholds cover the same dimension.
6. Tag each gate conclusion with the required confidence label (`📊`, `🔍`, or `💡`) — never treat the gate table itself as data-backed.
## Composite Command
```bash
python3 {skill_base_dir}/scripts/zoodata.py market-entry --keyword "{kw}" --category "{path}"
```
Runs all 11 endpoints (~20 calls). Output JSON is large — use targeted extraction, not full read.

## Output
Respond in user's language.

Sections: Sub-Market Landscape → Executive Summary → Market Overview → Trend → Brand Landscape → Price Structure → Top 5 Competitors → Consumer Insights → Scoring Breakdown (with "Basis" column) → Entry Strategy → Data Provenance → API Usage → Cross-Market Comparison

If user provides COGS, calculate break-even and profit. If not, prompt for it.

### Language (required)

Output language MUST match the user's input language. If the user asks in Chinese, the entire report is in Chinese. If in English, output in English. Exception: API field names (e.g. `monthlySalesFloor`, `categoryPath`), endpoint names, technical terms (e.g. ASIN, BSR, CR10, FBA, credits) remain in English.

### Disclaimer (required, at the top of every report)

> Data is based on ZooData API sampling as of [date]. Monthly sales (`monthlySalesFloor`) are lower-bound estimates. This analysis is for reference only and should not be the sole basis for business decisions. Validate with additional sources before acting.

### Confidence Labels (required, tag EVERY conclusion)

- 📊 **Data-backed** — direct API data (e.g. "CR10 = 54.8% 📊")
- 🔍 **Inferred** — logical reasoning from data (e.g. "brand concentration is moderate 🔍")
- 💡 **Directional** — suggestions, predictions, strategy (e.g. "consider entering $10-15 band 💡")

Rules: Strategy recommendations are NEVER 📊. Anomalies (>200% growth) are always 💡. User criteria override AI judgment.

**Aggregate-label rule (applies to ALL report output, not just fallback)**: NEVER attach 📊 to ANY element that aggregates or groups underlying content when ANY piece of that content is 🔍 or 💡. "Aggregate/grouping elements" include:
- Section headers at EVERY level (`#`, `##`, `###`, `####`) — including top-level summary sections like "Overall Score", "Verdict", "Executive Summary"
- Summary/score lines anywhere in the report (e.g. `## Overall Score — 27/100 · Grade F 📊` is WRONG if any Basis row inside is 🔍)
- Table **column** headers in comparison tables (e.g. `**Target ASIN** 📊` as a column label is WRONG if any cell in that column contains 🔍)
- Table row headers or row-aggregation labels (when the row aggregates multiple cells of mixed confidence)
- Any other visual grouping label — bullet-list group titles, callout box titles, etc.

A group-level 📊 implies the whole block/column/row is data-backed, which smuggles inferred/directional content into the 📊 tier via visual grouping. Either (a) **omit the group-level label entirely** (preferred when content mixes tiers), or (b) use the LOWEST confidence present inside (🔍 if any underlying content is 🔍; 💡 if any is 💡). This is a universal output-quality rule — it applies regardless of which fallback path (if any) was triggered.

**Emoji reservation rule (closely related)**: The three confidence symbols `📊 🔍 💡` are RESERVED for confidence labeling. NEVER use them as decorative prefixes on section headers, table headers, or any aggregate element — even when you also include a correct confidence suffix on the same line. Example:
- ❌ WRONG: `## 📊 Overall Score — 27/100 · Grade F 🔍` (the leading 📊 reads as a data-backed claim even though the trailing 🔍 is correct)
- ✅ RIGHT: `## Overall Score — 27/100 · Grade F 🔍` (no decorative emoji, just the proper confidence suffix)
- ✅ RIGHT: `## 🎯 Overall Score — 27/100 · Grade F 🔍` (use non-reserved decorative icons like 🎯 🧭 📋 📝 📂 🏁 🚨 🏆 🔔 when a visual prefix is desired)

Decorative emoji ≠ confidence label — but from a reader's perspective, a leading `📊/🔍/💡` is indistinguishable from a confidence claim. Reserve these three symbols EXCLUSIVELY for confidence annotation to avoid ambiguity.

### Data Provenance (required)

Include a table at the end of every report:

| Data | Endpoint | Key Params | Notes |
|------|----------|------------|-------|
| (e.g. Market Overview) | `markets/search` | categoryPath, topN=10 | 📊 Top N sampling, sales are lower-bound |
| ... | ... | ... | ... |

Extract endpoint and params from `_query` in JSON output. Add notes: sampling method, T+1 delay, realtime vs DB, minimum review threshold, etc.

### API Usage (required)

| Endpoint | Calls | Credits |
|----------|-------|---------|
| (each endpoint used) | N | N |
| **Total** | **N** | **N** |

Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N`.

## API Budget: ~20 calls
