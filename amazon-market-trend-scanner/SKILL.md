---
name: amazon-market-trend-scanner
description: >
  Amazon category trend scanner. Scans Amazon category landscapes to discover
  trending subcategories, emerging niches, and market shifts. Tracks demand
  surges, brand consolidation, new entrant waves, price band migration, and
  margin changes across all subcategories under a parent category.
  Use when user asks about: market trends, category trends, trending
  categories, what's hot, emerging categories, trend scanner,
  which categories are growing, where the market is heading.
  Pick this to track how categories shift OVER TIME (trends, momentum, emerging niches). To
  evaluate one specific niche right now, use amazon-market-entry-analyzer; to discover products
  to sell, use amazon-opportunity-discoverer.
  Requires ZOODATA_API_KEY.
metadata:
  version: "1.0.7"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Market Trend Scanner

> Find rising categories before everyone else. Respond in user's language.

## Files

| File | Purpose |
|------|---------|
| `{skill_base_dir}/scripts/zoodata.py` | **Execute** for all API calls (run `--help` for params) |
| `{skill_base_dir}/references/reference.md` | Load for exact field names or response structure |
| `{skill_base_dir}/scan-data/` | Runtime: watchlist.json, baseline.json, alerts.json, history/ (auto-created) |

## Credential

Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys).

## Capabilities & Data Flow

- **Network**: only `https://api.zoodata.ai` (Bearer `ZOODATA_API_KEY`). Setting `ZOODATA_BASE_URL` to an untrusted host (anything other than `api.zoodata.ai` / `*.zoodata.ai` / localhost) makes the CLI **refuse the request and withhold the key** — the Bearer token is never sent to an untrusted host.
- **Execution**: bundled shared ZooData CLI `{skill_base_dir}/scripts/zoodata.py` (Python 3, stdlib-only). This skill allows `categories`, `market`, `products`, and `check`. Do not invoke unrelated subcommands for this skill's tasks.
- **Local files**: scan state under `{skill_base_dir}/scan-data/` (`baseline.json`, `watchlist.json`, `history/*.json`); reads the optional credential store `~/.zoodata/config.json`.
- **Sent to the API**: keywords, category paths, ASINs, marketplace/date and numeric filter values only. **Never sent**: budget, experience level, risk tolerance, or any other user-profile text — profile inputs map client-side to numeric filters.
- **Credits**: every API call consumes account credits. For broad or ambiguous requests, state the estimated credit cost and confirm with the user before running multi-call scans.

## Shared CLI Contract

Before selecting or invoking the first command, read and apply the local `references/cli-contract.md`. Reapply it after every granular or composite result and before any fallback, additional call, state write, interpretation, or user-facing report. Use this skill's fallback logic only when the shared contract classifies the result as non-terminal.

### Local Interface Failure Output

For a terminal interface failure, respond in the user's language that the trend scan could not be completed, then list succeeded and failed endpoint identifiers and state that existing scan state remains unchanged. Do not emit trend signals, hot-category rankings, alerts, or write watchlists, history, or baselines. Keep control tokens, parameters, and retry logs internal unless diagnostics are requested.

## Input

Tell the user: "Give me one or more categories to monitor (e.g. 'Pet Supplies > Dogs'). I'll scan all subcategories and find trending directions. Single or batch supported."

Required: 1+ category paths or keywords. Optional: scan depth, metric preferences.

## API Pitfalls (CRITICAL)

1. **Category first**: resolve categoryPath via `categories --keyword` before anything
2. **All keyword endpoints MUST include `--category`**; omitting it distorts aggregation
3. **Use API fields directly**: revenue=`sampleAvgMonthlyRevenue`, sales=`monthlySalesFloor`
4. **Key metrics per subcategory**: sampleAvgMonthlySales, sampleNewSkuRate, topBrandSalesRate, sampleAvgPrice, sampleAPlusRate, totalSkuCount, sampleFbaRate
5. **`--mode` presets are CLI-local, NOT API params** — `zoodata.py` expands them via `PRODUCT_MODES` before the call; a raw `products/search` request must send the expanded filter fields and must not send `mode` (`mode` raw → 422)

## On Missing Key

When `ZOODATA_API_KEY` is not set (verify via `python {skill_base_dir}/scripts/zoodata.py check` — exits 2 if no key in env or `~/.zoodata/config.json`), stop before any evidence call. Tell the user that a ZooData API key is required, link to https://zoodata.ai/en/api-keys, and explain that the key may be set in the environment or local config. Do not substitute public knowledge or a "for reference only" analysis.
## On 401 Invalid Key

When `_transport.status=401`, stop further calls, tell the user that the configured key was rejected, direct them to https://zoodata.ai/en/api-keys, and do not fabricate missing data.

## On 402 Credit Exhausted

When `_transport.status=402`, stop further calls. Report where the workflow stopped, any compatible partial findings already gathered, and returned credit metadata when present; direct the user to https://zoodata.ai/en/pricing and do not fabricate missing data.

## Mode 1: Full Scan

1. `categories --keyword "{keyword}"` → resolve category path
2. `market --category "{path}" --page-size 20` → collect all subcategory market data (paginate)
3. Record 7 key metrics per subcategory (see Pitfalls #4)
4. `products --keyword "{sub}" --category "{path}" --mode emerging --page-size 20` per hot subcategory
5. `products --keyword "{sub}" --category "{path}" --mode new-release --page-size 20` per hot subcategory
6. Save baseline → `{skill_base_dir}/scan-data/baseline.json`, config → `{skill_base_dir}/scan-data/watchlist.json`
7. Output full trend report (see Output Spec)
8. Offer Auto-Monitor setup

## Mode 2: Quick Check (scheduled)

1. Read `{skill_base_dir}/scan-data/watchlist.json` + `{skill_base_dir}/scan-data/baseline.json`
2. `market --category "{path}"` per watched category
3. Compare vs baseline using signal rules below
4. 🔴 alerts → notify user; else silent log
5. Save snapshot to `{skill_base_dir}/scan-data/history/{timestamp}.json`, update baseline

## Trend Signals

| Signal | Condition | Level |
|--------|-----------|-------|
| Demand surge | sampleAvgMonthlySales >20% vs baseline | 🔴 |
| Red ocean warning | topBrandSalesRate >70% AND rising | 🔴 |
| New entrant wave | sampleNewSkuRate up >5 percentage points | 🟡 |
| Brand loosening | topBrandSalesRate down >3 percentage points | 🟡 |
| Price band shift | sampleAvgPrice change >10% | 🟡 |
| Margin change | sampleAPlusRate change >5 percentage points | 🟡 |
| Minor movement | None of the above triggered | 🟢 Silent log |

### Trend Interpretation & Action Guide
| Signal Combination | Market Phase | Recommended Action |
|--------------------|-------------|-------------------|
| Demand surge + New entrant wave | 🚀 Growth phase | Enter quickly, first-mover advantage matters 💡 |
| Demand surge + Brand loosening | 🎯 Opportunity window | Best timing — demand up, incumbents losing grip 💡 |
| Demand surge + Red ocean warning | ⚠️ Late stage growth | High demand but leaders consolidating — need strong differentiation 💡 |
| Red ocean warning + No demand surge | 🔒 Mature/locked | Avoid — established players dominate with flat demand 💡 |
| Brand loosening + Price band shift down | 💰 Price war | Wait — margins compressing, enter after shakeout 💡 |
| New entrant wave + Margin change | 🔄 Disruption | Category being redefined — study new entrants' strategies 🔍 |

### Subcategory Ranking Criteria
Rank subcategories by composite attractiveness (apply market-entry scoring logic):
- **Demand**: sampleAvgMonthlySales — higher = more attractive 📊
- **Competition**: topBrandSalesRate — lower = more open 📊
- **Entry barrier**: sampleAvgRatingCount — lower = easier entry 📊
- **Activity**: sampleNewSkuRate — higher = more dynamic 📊
- **Margin signal**: sampleAvgPrice — higher generally = better margins 🔍

## Auto-Monitor

After each Full Scan, ask user to enable scheduled monitoring. If yes, generate cron config with: category list, alert thresholds, schedule. Supports OpenClaw /cron, ChatGPT Scheduled Tasks, Claude Projects. Quick Check only notifies on 🔴 alerts.

## Output Spec

Full Scan: Trend Dashboard (all subcategories) → 🔥 Hot Categories TOP 5 → 🆕 New Entrants Scan → ⚠️ Risk Alerts → Subcategory Detail (per hot category) → Next Steps → Data Provenance → API Usage.

### Language (required)

Output language MUST match the user's input language. If the user asks in Chinese, the entire report is in Chinese. If in English, output in English. Exception: API field names (e.g. `monthlySalesFloor`, `categoryPath`), endpoint names, technical terms (e.g. ASIN, BSR, CR10, FBA, credits) remain in English.

### Disclaimer (required, at the top of every report)

> Data is based on ZooData API sampling as of [date]. Monthly sales (`monthlySalesFloor`) are lower-bound estimates. This analysis is for reference only and should not be the sole basis for business decisions. Validate with additional sources before acting.

### Confidence Labels (required, tag EVERY conclusion)

- 📊 **Data-backed** — direct API data (e.g. "CR10 = 54.8% 📊")
- 🔍 **Inferred** — logical reasoning from data (e.g. "brand concentration is moderate 🔍")
- 💡 **Directional** — suggestions, predictions, strategy (e.g. "consider entering $10-15 band 💡")

Rules: Strategy recommendations are NEVER 📊. Anomalies (>200% growth) are always 💡. Sample bias note required. User criteria override AI judgment.

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

## API Budget

Full Scan: ~40-60 credits (~2-3 per subcategory × 20). Quick Check: ~20-30 credits (market only).
