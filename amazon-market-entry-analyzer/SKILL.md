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
  Pick this to EVALUATE a specific niche/category the user already named (one GO/CAUTION/AVOID
  verdict). To discover what to sell with no target in mind, use amazon-opportunity-discoverer;
  to track how categories shift over time, use amazon-market-trend-scanner.
  Requires ZOODATA_API_KEY.
metadata:
  version: "1.0.9"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# Amazon Market Entry Analyzer — GO / CAUTION / AVOID

One input (keyword/category). Full market viability assessment with sub-market discovery.

## Files
- **Script**: `{skill_base_dir}/scripts/zoodata.py` — run `--help` for params
- **Reference**: `{skill_base_dir}/references/reference.md` (field names & response structure)
- **Market workflow**: `{skill_base_dir}/references/market-workflow.md` (sub-market selection, scoring, and risk gates)

For market analysis, this file routes the request and sets runtime boundaries; `references/reference.md` owns endpoint parameters and fields, `references/market-workflow.md` owns selection and scoring, `references/cli-contract.md` owns shared invocation/result handling, and `scripts/zoodata.py` owns request construction.

## Credential
Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys)

## Capabilities & Data Flow

- **Network**: only `https://api.zoodata.ai` (Bearer `ZOODATA_API_KEY`). Setting `ZOODATA_BASE_URL` to an untrusted host (anything other than `api.zoodata.ai` / `*.zoodata.ai` / localhost) makes the CLI **refuse the request and withhold the key** — the Bearer token is never sent to an untrusted host.
- **Execution**: bundled shared ZooData CLI `{skill_base_dir}/scripts/zoodata.py` (Python 3, stdlib-only). This skill allows `market-entry`, `categories`, `market`, `market-overview`, `market-structure-profile`, `market-history`, `products`, `competitors`, `product`, `analyze`, `price-band-overview`, `price-band-detail`, `brand-overview`, `brand-detail`, `history`, `check`, plus the review fallback toolkit (`reviews-raw` / `review-tag-prompt` / `review-reduce-prompt` / `review-aggregate`) — each only as explicitly routed below. The bundled manifest `{skill_base_dir}/scripts/allowed-commands.json` enforces this set: the CLI refuses out-of-scope subcommands with a structured `COMMAND_NOT_ALLOWED` error before any API request.
- **Local files**: a private temporary working dir (created with `mktemp -d`, removed when the fallback completes) during the review fallback; reads the optional credential store `~/.zoodata/config.json`.
- **Sent to the API**: keywords, category paths, ASINs, marketplace/date and numeric filter values only. **Never sent**: budget, experience level, risk tolerance, or any other user-profile text — profile inputs map client-side to numeric filters.
- **Credits**: every API call consumes account credits. For broad or ambiguous requests, state the estimated credit cost and confirm with the user before running multi-call scans. The composite `market-entry` command executes ~17+ API calls (~15-25 credits) in ONE invocation and has NO skip/trim flags — under a credit cap, use the granular commands instead.

### CLI Route Selection

- Use `market-entry` for the full assessment.
- Use granular commands only when the workflow selected a granular route before the composite call, or when an explicit non-terminal fallback in this skill requires evidence not already returned.
- Map granular evidence requests only through this table:

| API endpoint | CLI subcommand |
|---|---|
| `categories` | `categories` |
| `markets/search` | `market` |
| `markets/overview` | `market-overview` |
| `markets/structure-profile` | `market-structure-profile` |
| `markets/history` | `market-history` |
| `products/search` | `products` |
| `products/competitors` | `competitors` |
| `realtime/product` | `product` |
| `reviews/analysis` | `analyze` |
| `products/price-band-overview` | `price-band-overview` |
| `products/price-band-detail` | `price-band-detail` |
| `products/brand-overview` | `brand-overview` |
| `products/brand-detail` | `brand-detail` |
| `products/history` | `history` |

Use `check` only for credential diagnostics. Use `reviews-raw`, `review-tag-prompt`, `review-reduce-prompt`, and `review-aggregate` only for the documented review fallback.

## Shared CLI Contract

Before selecting or invoking the first command, read and apply the local `references/cli-contract.md`. Reapply it after every granular or composite result and before any fallback, additional call, state write, interpretation, or user-facing report. Use this skill's fallback logic only when the shared contract classifies the result as non-terminal.

### Local Interface Failure Output

For a terminal interface failure, respond in the user's language that the market-entry assessment could not be completed, followed by the succeeded and failed endpoint identifiers. Do not issue GO/CAUTION/AVOID, a viability score, risk-gate result, or entry strategy. Keep control tokens, parameters, and retry logs internal unless diagnostics are requested.

## Input
- **Required**: keyword or categoryPath
- **Optional**: marketplace (default US)
- **Optional (seller-side — drives the Small-Seller Entry Risk Gates section below)**:
  - `budget` — first-6-month capital available (e.g. "$10K", "$50K", "$200K+")
  - `risk_tolerance` — low / medium / high
  - `ip_concern` — known compliance, patent, trademark, or restricted-category concerns; or "none"

  If the user hasn't supplied these, **ask once at the start of the workflow** (a single batched question is fine). If the user declines or skips, **omit the Risk Gates section from the final verdict** and add a line under Data Provenance: "Risk Gates: skipped — seller-side inputs not provided." **Do not guess thresholds** — silent gate evaluation with invented inputs produces inconsistent verdicts across runs.

## API Pitfalls (CRITICAL)
- Keyword search is broad → categoryPath is auto-resolved via `categories` endpoint, with fallback to top search result. If `category_source` is `inferred_from_search`, confirm with user
- Brand/price-band queries **MUST include --category** to avoid cross-category contamination
- For full-category and selected Top 100 revenue fields, read `references/reference.md § 2`; apply the revenue interpretation in `references/market-workflow.md`.
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
     - **Working dir**: `WORK=$(mktemp -d)` (private, 0700 — not a predictable path); remove it with `rm -rf "$WORK"` after `review-aggregate` succeeds or the fallback aborts
     - **Step b CLI behavior**: `review-tag-prompt` RENDERS the prompt only; YOUR LLM produces the JSON. Render once to learn the schema, then produce tags for all N reviews in one in-context pass (don't call the CLI N times).
     - **Step c candidate extraction** (Python one-liner):
       `candidates = {d: sorted({el.strip().lower() for t in tagged for el in (t.get(d) or [])}) for d in DIMS}`
     - **Small-sample rule (reviewCount<50)**: demote single-mention items 📊→🔍; NEVER attach table-level or section-header 📊 when any row inside is 🔍; suppress "🔴 Critical" verdicts on count=1
     - **Scope**: fallback replaces ONLY the `/reviews/analysis` aggregation. This skill's primary workflow outputs (GO/CAUTION/AVOID verdict, market size, brand/price analysis) remain valid — do not re-run them.
- Aggregation endpoints without categoryPath produce severely distorted data

## On Missing Key

When `ZOODATA_API_KEY` is not set (verify via `python {skill_base_dir}/scripts/zoodata.py check` — exits 2 if no key in env or `~/.zoodata/config.json`), stop before any evidence call. Tell the user that a ZooData API key is required, link to https://zoodata.ai/en/api-keys, and explain that the key may be set in the environment or local config. Do not substitute public knowledge or a "for reference only" analysis.
## On 401 Invalid Key

When `_transport.status=401`, stop further calls, tell the user that the configured key was rejected, direct them to https://zoodata.ai/en/api-keys, and do not fabricate missing data.

## On 402 Credit Exhausted

When `_transport.status=402`, stop further calls. Report where the workflow stopped, any compatible partial findings already gathered, and returned credit metadata when present; direct the user to https://zoodata.ai/en/pricing and do not fabricate missing data.

## Market-entry scoring, sub-market selection, and seller risk gates

Load `references/market-workflow.md` for this workflow. That module owns the detailed steps and interpretation rules.

## Composite Command
```bash
python3 {skill_base_dir}/scripts/zoodata.py market-entry --keyword "{kw}" --category "{path}"
```
Runs all 11 endpoints (~20 calls). Apply `references/cli-contract.md` to its invocation and returned composite bundle.

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
| (e.g. Market Overview) | `markets/overview` | Copy actual `_query.params` | 📊 Full category and selected Top 100 metrics |
| ... | ... | ... | ... |

Extract endpoint and params from `_query` in JSON output. Add notes: sampling method, T+1 delay, realtime vs DB, minimum review threshold, etc.

### API Usage (required)

| Endpoint | Calls | Credits |
|----------|-------|---------|
| (each endpoint used) | N | N |
| **Total** | **N** | **N** |

Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N`.

## API Budget: ~20 calls
