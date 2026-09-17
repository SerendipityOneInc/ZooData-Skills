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
  version: "1.0.8"
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
| `{skill_base_dir}/references/scan-workflow.md` | Load for scan modes, baseline handling, signals, and ranking |
| `{skill_base_dir}/scan-data/` | Runtime: watchlist.json, baseline.json, alerts.json, history/ (auto-created) |

For market scanning, this file routes the request and sets runtime boundaries; `references/reference.md` owns endpoint parameters and fields, `references/scan-workflow.md` owns scan modes, baseline handling, and signals, `references/cli-contract.md` owns shared invocation/result handling, and `scripts/zoodata.py` owns request construction.

## Credential

Required: `ZOODATA_API_KEY`. Get free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys).

## Capabilities & Data Flow

- **Network**: only `https://api.zoodata.ai` (Bearer `ZOODATA_API_KEY`). Setting `ZOODATA_BASE_URL` to an untrusted host (anything other than `api.zoodata.ai` / `*.zoodata.ai` / localhost) makes the CLI **refuse the request and withhold the key** — the Bearer token is never sent to an untrusted host.
- **Execution**: bundled shared ZooData CLI `{skill_base_dir}/scripts/zoodata.py` (Python 3, stdlib-only). This skill allows `categories`, `market`, `market-overview`, `market-structure-profile`, `market-history`, `products`, and `check`. Do not invoke unrelated subcommands for this skill's tasks — the bundled manifest `{skill_base_dir}/scripts/allowed-commands.json` enforces this: the CLI refuses out-of-scope subcommands with a structured `COMMAND_NOT_ALLOWED` error before any API request.
- **Local files**: scan state under `{skill_base_dir}/scan-data/` (`baseline.json`, `watchlist.json`, `alerts.json`, `history/*.json`); reads the optional credential store `~/.zoodata/config.json`. This state persists between runs solely for baseline comparison and alerting — it may be deleted at any time to reset monitoring, and old `history/` snapshots should be pruned when no longer needed.
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
3. **Market metrics**: read `references/reference.md § 2` for the current field identity and denominator; apply `references/scan-workflow.md` for scan metrics and signals.
4. **`--mode` presets are CLI-local, NOT API params** — `zoodata.py` expands them via `PRODUCT_MODES` before the call; a raw `products/search` request must send the expanded filter fields and must not send `mode` (`mode` raw → 422)

## On Missing Key

When `ZOODATA_API_KEY` is not set (verify via `python {skill_base_dir}/scripts/zoodata.py check` — exits 2 if no key in env or `~/.zoodata/config.json`), stop before any evidence call. Tell the user that a ZooData API key is required, link to https://zoodata.ai/en/api-keys, and explain that the key may be set in the environment or local config. Do not substitute public knowledge or a "for reference only" analysis.
## On 401 Invalid Key

When `_transport.status=401`, stop further calls, tell the user that the configured key was rejected, direct them to https://zoodata.ai/en/api-keys, and do not fabricate missing data.

## On 402 Credit Exhausted

When `_transport.status=402`, stop further calls. Report where the workflow stopped, any compatible partial findings already gathered, and returned credit metadata when present; direct the user to https://zoodata.ai/en/pricing and do not fabricate missing data.

## Full scan, quick check, trend signals, and subcategory ranking

Load `references/scan-workflow.md` for this workflow. That module owns the detailed steps and interpretation rules.

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
| (e.g. Market Overview) | `markets/overview` | Copy actual `_query.params` | 📊 Full category and selected Top 100 metrics |
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
