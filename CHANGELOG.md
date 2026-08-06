# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed — Composite category resolution is no longer misread as missing data

Keyword-driven composites (`report`, `market-entry`, `competitor-analysis`, `pricing-analysis`, `daily-radar`, `listing-audit`, `opportunity-scan`, `review-deepdive`) resolve the working category through a fallback chain. For a multi-word product phrase (e.g. `"yoga mat"`) the first step — `categories`/search, which matches category *names* — returns empty, and the category is instead resolved from the top product's `categoryPath`. The bundle then carried an empty top-level `categories` section that read like missing data, even though `meta.category_source` recorded the fallback. The composite `meta` now also carries `resolved_category_path` (the path actually used, or `null` when genuinely unresolved), so an empty `categories` section paired with a non-null path is unambiguously successful fallback resolution. `cli-contract.md` § *Command identity and composite reuse* documents the signal; hermetic tests cover the fallback and unresolved cases. Live-verified: `report --keyword "yoga mat"` reports `category_source: inferred_from_search` and `resolved_category_path: ["Sports & Outdoors","Exercise & Fitness","Yoga","Mats"]`.

### Fixed — Keyword ABA out-of-window dates now distinguishable and retriable

ABA weekly keyword endpoints (`keywords/detail`, `market-profile`, `trend-profile`, `search-results`, …) publish with a lag and retain a bounded recent window; a `date` outside it returns `status=empty` with `resolvedDate=null`, previously indistinguishable from a resolved snapshot that simply lacks the keyword — so a stale or guessed date silently returned an empty result. The keyword skill's owner modules now separate the two cases: `reference.md` (date/availability facts) documents that a null `resolvedDate` means an out-of-window date distinct from a genuine no-observation snapshot, and that weekly date endpoints should target a recent completed week; `evidence-protocols.md` (in-stage date handling) directs the agent to reselect a recent in-window week and re-request once on a null-`resolvedDate` empty, while a non-null-`resolvedDate` empty stays valid no-observation evidence. Docs only — no CLI behavior change (date selection stays the agent's responsibility per the module ownership map).

### Fixed — Accurate credit reporting for composite commands

Composite commands (`report`, `market-entry`, `competitor-analysis`, `pricing-analysis`, `daily-radar`, `listing-audit`, `opportunity-scan`, …) fan out to many endpoints, but their output surfaced only one internal call's `meta.creditsConsumed` (or none) — a live audit found e.g. `market-entry` reporting `1` while actually consuming `23`. A run-scoped credit tracker now hooks the single HTTP call site and accumulates every internal call's real consumption; `output()` stamps the total onto the top-level `meta` (`creditsConsumed`, `creditsConsumedExact`, `creditsRemaining`, `apiCalls`). Single-endpoint responses are unchanged in meaning (the total equals that one call). Account billing was always correct — this fixes the *reported* total so agents can tell users the true cost.

The same tracker was ported to `web-extract`'s standalone `webtools.py`: the multi-call `crawl-wait` (submit + poll) previously reported no credit info at all (`meta: {"polled": true}`); it now surfaces the true total (live-verified: 2 credits for a 1-page crawl). Single-call webtools commands (`search`/`scrape`/`map`) are unchanged.

### Security — Removed bundled API key + credential-source hardening

A live, full-scope ZooData API key had been hand-placed into `zoodata/config.json` and shipped inside the published `zoodata` bundle (v1.1.4–v1.1.5), because `clawhub sync` bundles the skill folder from disk and does **not** honor `.gitignore`. The key has been revoked. Hardening:

- **Removed the `{skill_dir}/config.json` credential fallback** from the shared CLI (present since v1.0.0). The skill directory ships inside the published bundle, so it must never be a credential source — a key placed there leaks publicly.
- **Added `.clawhubignore`** (excluding `config.json`) to every skill directory so a stray config can never be bundled again; `.gitignore` does not apply to `clawhub sync`.
- **Removed the legacy `APICLAW_API_KEY` env var and `~/.apiclaw/config.json` credential fallbacks** (briefly soft-deprecated with a warning during this release cycle, removed before shipping in response to a ClawHub scan finding: every extra readable secret source widens the CLI's credential surface beyond what the skills declare). Both CLIs (`zoodata.py` and `web-extract`'s separate `webtools.py`) now read exactly the two declared sources: `ZOODATA_API_KEY` env, then `~/.zoodata/config.json`. Regression tests assert the legacy sources no longer resolve and the legacy config file is never opened.
- **Per-skill command allowlists are now CLI-enforced.** Every `amazon-*` skill bundles a `scripts/allowed-commands.json` manifest listing exactly the subcommands its SKILL.md declares; the shared CLI refuses anything else with a structured `COMMAND_NOT_ALLOWED` error before any API request (no credits consumed). `<cmd> --help` stays available for the full surface (documentation, not execution); a malformed manifest fails closed; the canonical copy and the `zoodata` data-layer reference skill ship no manifest and keep the full surface. This converts the previous prose-only "do not invoke unrelated subcommands" rule into a mechanical guarantee.
- **Credential-file hardening:** the CLI setup hint and skill docs now create `~/.zoodata` with `chmod 700` and write `config.json` under `umask 077` (0600) — the key is a bearer credential.
- **Review-fallback temp dirs are no longer predictable:** the documented working directory changed from `/tmp/review_<ASIN>_<timestamp>` to `mktemp -d` (private, 0700) with an explicit cleanup step after aggregation.
- **`ZOODATA_BASE_URL` pointing at an untrusted host now withholds the key entirely.** Previously the CLI warned but still sent the Bearer token; now requests to any host other than `zoodata.ai` / `*.zoodata.ai` / localhost are refused before the key is transmitted, so credentials can never reach an arbitrary host. The 11 SKILL.md "Capabilities & Data Flow" declarations that carry a base-url note were updated to state this refusal (they previously said "triggers a CLI warning"); `web-extract` has no such declaration because its `webtools.py` hardcodes the base URL with no `ZOODATA_BASE_URL` override.
- Hardened `_read_config_api_key` against a `{"api_key": null}` config (previously crashed on `None.strip()`); added tests for the untrusted-host refusal path and the null-key case.

**Migration / impact on existing installs (only after `openclaw skills update`):**
- `ZOODATA_API_KEY` env or `~/.zoodata/config.json` users — no change.
- `APICLAW_API_KEY` env or `~/.apiclaw/config.json` users — **no longer resolve** (breaking): the CLI reports "API Key not found" with setup guidance. Migrate the key to `ZOODATA_API_KEY` or `~/.zoodata/config.json` (same key value, new name/location).
- Anyone who placed a key in the **skill directory's** `config.json` — that path no longer resolves; move the key to `ZOODATA_API_KEY` or `~/.zoodata/config.json`.

### Changed — LLM security-review content fixes (needs-review clearance)

ClawHub's LLM review flagged 7 skills. Content corrections:
- **amazon-analysis** — the "Chinese Seller Case Study" scenario reframed to seller-origin analysis driven **only** by the `buyBoxSellerCountryCode` data field; removed the name/pinyin/suffix/category stereotyping heuristics and now discloses origin coverage instead of guessing. Two execution-guide fallbacks that told the agent to hide data limitations from users now require transparent disclosure. The over-broad "can I do this" risk-assessment trigger tightened to qualified phrases requiring a product/ASIN/niche.
- **amazon-listing-audit-pro** and **amazon-market-trend-scanner** — `references/reference.md` was a verbatim copy of the Market Entry Analyzer reference (wrong title, "uses all 11 endpoints" claim). Retitled to each skill and reframed as a shared field reference, with a note that the skill's workflows use only the subcommands listed in SKILL.md.
- **amazon-competitor-intelligence-monitor** — excluded the `monitor-data/` runtime-state directory (leftover test baseline/config) from the published bundle via `.clawhubignore`.

### Added — Security-audit response: Capabilities & Data Flow declarations (all 12 skills)

ClawHub's SkillSpector audit flagged an under-declared capability surface (env-only metadata vs actual network/execution/file behavior) and missing data-flow transparency. Every SKILL.md now carries a standardized "Capabilities & Data Flow" section declaring: exact network host, the bundled shared CLI and which subcommands the skill's workflows use, local files written, what is/isn't sent to the API (user profile text never leaves the machine — it maps client-side to numeric filters), and a credit-cost confirmation rule for broad requests.

### Changed — CLI hardening
- `ZOODATA_BASE_URL` pointing at a non-zoodata.ai / non-localhost host now prints a Bearer-token warning before any request.
- Missing-key hint now recommends the environment variable first; the `~/.zoodata/config.json` home config is listed as the persistent alternative.
- Patch version bump on all 12 skills for ClawHub republish.


### Changed — amazon-keyword-traffic-analysis marketing copy

`description` rewritten to lead with value hooks — ABA-backed data, Priority/Selective/Observe/Exclude test tiers, bid-worthiness verdicts, reverse-ASIN traffic terms — while preserving every trigger phrase for agent routing. Skill README restructured to lead with outcomes and example prompts; agent implementation details (draft MCP tool names, tool-selection rules) moved to a trailing "Agent Implementation Notes" section; data-boundary disclaimers consolidated under "Data Source & Boundaries". No workflow or endpoint content changed.

### Changed — Patch version bumps for ClawHub republish

All 12 skills' `metadata.version` bumped one patch level. All SKILL.md files changed since the last publish (frontmatter spec compliance, APIClaw → ZooData rebrand, On Missing Key protocol, etc.), so installed copies will hit `openclaw skills update` fingerprint mismatch; republishing with a version bump gives clients a clean upgrade path instead of requiring `--force` (same approach as #56).

### Changed — SKILL.md Frontmatter Spec Compliance

Frontmatter of all 10 SKILL.md files restructured to comply with the [Agent Skills open standard](https://agentskills.io/specification). The spec recognizes only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools` as top-level fields; previously the files used `version`, `author`, `homepage` at the top level. These are now nested under the spec-recognized `metadata` field (the spec's official example shows `version` and `author` as `metadata` sub-keys). The `openclaw` runtime contract (`requires.env`, `primaryEnv`) is preserved as inline JSON at `metadata.openclaw` — relocated, not rewritten.

**Impact per install path:**
- **ClawHub (`openclaw skills install`)**: URL, slug, install directory, page display all unchanged. `openclaw skills update` will refuse on fingerprint mismatch (SKILL.md bytes changed even though semantics didn't) — pass `--force` to overwrite.
- **Claude Code**: No user-visible change. Frontmatter is parsed by a standard YAML parser; inline JSON and YAML block style are equivalent.
- **Codex / Cursor / Gemini CLI**: Improved spec compliance for strict skill loaders.

### Fixed — Description content quality

- **amazon-pricing-command-center**: rewrote description from first-person ("Give me your ASIN(s) — I auto-detect...") to third-person, per spec guidance. Removed duplicate `pricing strategy` trigger keyword.
- **amazon-competitor-intelligence-monitor**: removed duplicate trigger keywords (`competitor analysis`, `competitor monitoring`, `competitor tracking` each appeared twice).
- **amazon-analysis**: added explicit `Use when user asks about...` trigger keyword list (previously missing) and added a routing hint pointing strict/specialized intents to the corresponding specialized skill.

## [1.2.2] — 2026-06-05

### Added — Realtime Reviews Fallback Toolkit (#57)
- **`/openapi/v2/realtime/reviews` endpoint integration** — cursor-paginated raw review fetch (10 reviews/page, max 100 reviews / 10 pages, 1 credit/page, US+UK only). Spider-live, no AI tags.
- **Local Review Toolkit in `zoodata.py`** — prompt-as-data fallback path when `/reviews/analysis` lacks aggregation (ASIN <50 reviews or no daily snapshot). New CLI commands:
  - `reviews-raw` — fetch raw reviews with auto-pagination + early exit
  - `review-tag-prompt` — render per-review Map prompt for the caller's own LLM
  - `review-reduce-prompt` — render per-dimension Reduce prompt for the caller's own LLM
  - `review-aggregate` — combine raw reviews + Map tags + Reduce clusters into `consumerInsights` output compatible with `/reviews/analysis`
- **Three-layer sync enforcement docs** in `zoodata/scripts/zoodata.py` file header (pre-commit hook + `sync-scripts.sh` + CI workflow).
- **CONTRIBUTING.md** sections on local branch hygiene and shared CLI script sync mechanism.

### Changed — Realtime Reviews Fallback Documentation (#57)
- All 8 review-using SKILL.md files now document the realtime/reviews fallback chain (each self-contained, no cross-skill references):
  - Tier A (deep update): `zoodata`, `amazon-review-intelligence-extractor`, `amazon-analysis`
  - Tier B (pitfall expansion): `amazon-competitor-intelligence-monitor`, `amazon-daily-market-radar`, `amazon-listing-audit-pro`, `amazon-market-entry-analyzer`, `amazon-opportunity-discoverer`
- Reference docs updated with `realtime/reviews` and `reviews/search` schemas (`zoodata/references/{openapi-reference,reference}.md`, `amazon-review-intelligence-extractor/references/reference.md`).
- All 9 `amazon-*/scripts/zoodata.py` copies force-resynced to canonical (one-time cleanup of pre-existing drift; future syncs now safe via AUTO-SYNCED marker in file header).

### Fixed — SKILL.md `name` Field Spec Compliance (#65)

All 10 SKILL.md `name:` fields rewritten to kebab-case matching the parent directory name, per the [Agent Skills open standard](https://agentskills.io/specification). Previous values were human-readable titles (e.g., `Amazon Daily Market Radar — Automated Monitoring & Alerts`) which violated the spec rules: lowercase alphanumeric + hyphens only, max 64 characters, must match parent directory. This caused strict loaders (Codex) to skip these skills at startup.

**Impact per install path:**
- **ClawHub (`openclaw skills install`)**: URL, slug, install directory, page display all unchanged. `openclaw skills update` will refuse on fingerprint mismatch — pass `--force` to overwrite.
- **Claude Code**: No user-visible change. Claude Code uses the directory name for slash commands; the `name:` field is just a display name.
- **Codex**: Skills now load successfully. `npx skills add` users with pre-existing installs from the old long-name version will have orphaned directories.

**Cleanup for `npx skills add` users with old installs:**

```bash
npx skills list
npx skills remove "amazon-daily-market-radar-automated-monitoring-alerts"
npx skills remove "amazon-review-intelligence-extractor-consumer-insights-from-1b-reviews"
# (and any other long-name orphans shown by `list`)
npx skills add SerendipityOneInc/ZooData-Skills
```

### Other (#51–#56, #62, #63)
- Sync infrastructure: `scripts/sync-scripts.sh` repointed at canonical-source banner (#63); SKILL.md PR CI checks for path prefix (#53)
- Bug fixes: market-entry keyword-only fallback when `categoryPath` empty (#62); API v2 field renames + rate limiting + category auto-detection (#52)
- ClawHub: security scan warnings resolved (#55); patch version bumps for republish (#56)
- Docs: README skill tables updated with input/output format (#51); README updates (#54)

### CI
- Removed `check-skill-name-unchanged` job. Its premise (that `name:` determines installed directory) was incorrect — ClawHub uses its own slug fixed at publish time, and other install paths are independent.

## [1.2.0] — 2026-04-03

### Breaking Changes — API V2 Field Renames
- `atLeastMonthlySales` → `monthlySalesFloor`, `atLeastMonthlyRevenue` → `monthlyRevenueFloor`
- `bsrRank` → `bsr`, `subBsrRank` → `subBsr`
- `ratingConversionRate` → `ratingToSalesRate`, `ratingMonthlyNew` → `monthlyRatingCount`
- `buyboxSeller` → `buyBoxSellerName`, `sellerLocation` → `buyBoxSellerCountryCode`
- `sampleEbcSkuRate` → `sampleAPlusRate`, `sampleAvgPackageDimensions` → `sampleAvgPackageVolume`
- `totalReviews` → `reviewCount`, `reviewPercentage` → `reviewRate`, `verifiedRatio` → `verifiedRate`
- Endpoint: `products/competitor-lookup` → `products/competitors`
- Endpoint: `reviews/analyze` → `reviews/analysis`
- Endpoint: `products/product-history` → `products/history`
- Removed: `profitMargin`, `sampleAvgGrossMargin`
- `pageSize` max: 20 → 100

### Bug Fixes
- Fixed argparse prefix matching: `--page` silently overriding `--page-size`. Added `allow_abbrev=False`.

### Skill Updates
- **Renamed**: Dynamic Pricing Intelligence Agent → Amazon Pricing Command Center — RAISE/HOLD/LOWER Signals
- **Renamed**: Market Radar → Amazon Market Trend Scanner — Daily Category Radar
- **Removed**: amazon-blue-ocean-finder
- **Disabled**: beginner mode (excludeKeywords not working)
- Removed cost/COGS/profit from pricing skill
- Added OpenAPI spec reference to all SKILL.md
- Unified all reference.md to complete 11-endpoint version
- 13 selection modes (was 14)

## [1.1.4] — 2026-04-01

### amazon-analysis v1.1.4
- Major SKILL.md rewrite: improved intent routing, workflow structure, and agent instructions
- Added `references/execution-guide.md` — step-by-step execution playbook for agents
- Updated `references/reference.md` with 11 endpoints (was 6), new field descriptions
- Enhanced scenarios files with additional guidance
- Rewrote `scripts/zoodata.py` with improved error handling

### zoodata v1.1.0
- Expanded from 6 to 11 API endpoints: added price-band overview/detail, brand overview/detail, product history
- Rewrote SKILL.md with complete endpoint documentation
- Updated `references/openapi-reference.md` with full field reference for all 11 endpoints

### 7 New Hero Skills v1.0.0
- **amazon-competitor-war-room** — Real-time competitive monitoring and response strategy
- **amazon-daily-market-radar** — Daily market pulse check and anomaly detection
- **amazon-listing-audit-pro** — Comprehensive listing quality audit and optimization
- **amazon-market-entry-analyzer** — Market viability assessment for new category entry
- **amazon-opportunity-discoverer** — Underserved niche and opportunity identification
- **amazon-pricing-command-center** — Dynamic pricing strategy and margin optimization
- **amazon-review-intelligence-engine** — Deep review sentiment analysis and insight extraction

### Repo
- Added `scoring-methodology.md` — unified quality scoring framework for all skills

## [1.1.3] — 2026-03-20

### amazon-analysis
- Fixed potential API key exposure risk in example configurations
- Removed hardcoded endpoint URLs from skill documentation
- Rewrote all reference files with improved field descriptions and usage examples
- Improved SKILL.md descriptions for better agent intent matching
- Enforced mandatory API usage tracking in output
- Enforced mandatory Data Source block in Full Mode output
- Added mandatory pre-execution checklist for Full Mode
- Optimized name and description for search discoverability

## [1.1.2] — 2026-03-18

### amazon-analysis
- **Credits Tracking**: API responses now include `creditsConsumed` and `creditsRemaining`
- **Realtime Data Supplementation**: automatically calls `realtime/product` for top 3-5 ASINs in Full mode
- **Reviews/Analyze Endpoint**: new `analyze` command for AI-powered review analysis (11 dimensions)
- **New Scenario 4.6**: Category Consumer Insights
- **Breaking**: `review` → `rating` rename across fields, filters, and CLI args
- **Breaking**: `topReviews` removed from `realtime/product` (use `reviews/analysis`)
- 6 new market response fields for new product metrics
- Slimmed SKILL.md from 448 → 417 lines

### zoodata v1.0.0
- Initial release of general skill — platform overview, 6 API endpoints

## [1.1.1] — 2026-03-16

### amazon-analysis
- Improved credential handling security: require user confirmation before writing to config.json
- Use ClawHub standard metadata format for credential declaration
- Emphasize environment variable as preferred credential method

## [1.1.0] — 2026-03-16

### amazon-analysis
- **Security**: removed API key logging, added SECURITY.md
- **8 Documentation Fixes**: interface data differences, API call ordering, null fallbacks
- **New**: Listing Optimization Module (8.1 Analysis, 8.2 Copy Generation, 8.3 Diagnosis)
- **6 Mode Corrections**: beginner, long-tail, new-release, fbm-friendly, speculative, top-bsr
- **New CLI Parameters**: `--keyword-match-type`, `--bsr-min/max`, `--seller-count-min/max`, etc.

## [1.0.0] — 2026-03-13

### amazon-analysis
- Initial release with full Amazon seller analytics skill
- CLI tool (`zoodata.py`) with 8 subcommands and 14 preset search modes
- Full API reference documentation
- 7 scenario reference files

---

### Repo Maintenance (not versioned)

**2026-03-25**
- Fixed CI markdown link check failure
- Added `README.zh-CN.md` with language switcher
- Updated repo description to match official website positioning

**2026-03-23**
- Restructured repo: added general `zoodata/` skill, moved amazon-analysis to subdirectory
- Added LICENSE (MIT), CONTRIBUTING.md, CODE_OF_CONDUCT.md, Issue Templates, PR template
- Added CI workflow (CLI smoke test + markdown link check)
- Rewrote README.md with badges, Quick Start, API examples
