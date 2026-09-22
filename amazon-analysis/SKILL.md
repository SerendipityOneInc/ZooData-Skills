---
name: amazon-analysis
description: >
  Amazon-domain general analysis and multi-endpoint research engine.
  Handles broad or composite Amazon research requests that span multiple data
  dimensions or have no single specialized angle. For focused category-market
  discovery, market-entry evaluation, or category trends, use
  amazon-market-analysis.
  Use when:
  - user asks for multi-endpoint Amazon research or composite reports
  - user asks "what kind of Amazon analysis can I run" or wants an overview
    of available Amazon insights
  - user wants broad Amazon data exploration with no single specific
    deliverable in mind
  Uses {skill_base_dir}/scripts/zoodata.py. Requires ZOODATA_API_KEY.
metadata:
  version: "1.1.13"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Amazon Seller Data Analysis

Respond in the user's language. Use this skill for broad or composite Amazon research without a single specialized deliverable. Route a focused market-entry, market-discovery, or category-trend request to `amazon-market-analysis`; route a focused keyword, listing, pricing, review, or competitor request to its dedicated skill.

## Start here

1. Classify the user's question. For a single data point, use the quick path in `references/execution-guide.md`; for multi-endpoint research, load its full workflow.
2. Read `references/cli-contract.md` before selecting or invoking a command. Inspect the bundled CLI's top-level and selected subcommand help.
3. Read `references/reference.md` for endpoint fields and local CLI options. Load the applicable scenario module: `scenarios-composite.md` for broad cross-validation, `scenarios-eval.md` for product evaluation, `scenarios-expand.md` for expansion, `scenarios-listing.md` for listing context, `scenarios-ops.md` for operations, or `scenarios-pricing.md` for pricing context.
4. Apply the shared interpretation and reporting rules in `references/execution-guide.md`; use the selected scenario for its specific evidence and conclusion scope.

## Source-of-truth boundaries

- This `SKILL.md` owns trigger routing, module loading, the responsibility map, and non-negotiable runtime boundaries. It does not define product presets, thresholds, endpoint fields, procedures, or report templates.
- `references/cli-contract.md` owns shared CLI invocation, command identity, result classification, retries, and terminal or partial-result handling.
- `references/reference.md` owns endpoint availability, request and response fields, CLI parameter mapping, data shapes, and field identity. It does not set analytical thresholds.
- `references/execution-guide.md` owns shared workflow steps, product-preset selection, market-health interpretation, cross-endpoint analysis, and user-facing output rules. It does not redefine endpoint fields.
- Scenario modules own the evidence selection, conclusions, and scenario-specific report sections for their named task. They may narrow shared workflow rules but cannot redefine endpoint contracts or shared output rules.
- `{skill_base_dir}/scripts/zoodata.py` owns local preset expansion, request construction, transport metadata, and credential handling; it does not issue business conclusions.

## Shared CLI Contract

Before selecting or invoking the first command, read and apply the local `references/cli-contract.md`. Reapply it after every granular or composite result and before any fallback, additional call, state write, interpretation, or report. The local `references/execution-guide.md` owns user-facing failure rendering.

### Local Interface Failure Output

Use the failure rendering in `references/execution-guide.md`; direct a user with exhausted credits to https://zoodata.ai/en/pricing.

## Non-negotiable boundaries

- Require `ZOODATA_API_KEY`; use the bundled CLI and the local command manifest. The credential-only `check` path precedes evidence calls. Stop and follow the shared CLI contract on credential, credit, validation, or terminal interface failures; do not invent missing evidence.
- Resolve and preserve a category path or ID before category-scoped comparisons. Distinguish inferred category paths from direct matches. Preserve marketplace, date, category scope, sample type, and the difference between full-category `marketTotal` and selected Top 100 `marketSample` metrics.
- Treat seller budget, experience, risk tolerance, and other profile text as local interpretation inputs. Send only the documented category/product identifiers and numeric filters to the API.
- State estimated credit cost before a broad multi-call scan. Require the user's explicit monitoring request before creating recurring work or saved baselines.

## Capabilities and data flow

- **Network**: the bundled CLI sends authenticated requests to `https://api.zoodata.ai` and refuses an untrusted `ZOODATA_BASE_URL`.
- **Execution**: Python 3 standard-library shared CLI at `{skill_base_dir}/scripts/zoodata.py`.
- **Local files**: reads optional `~/.zoodata/config.json`; review fallback may use a private temporary directory.
- **Sent to the API**: keywords, category paths/IDs, ASINs, marketplace, dates, and numeric filters. Seller profile text remains local.
- **Credits**: evidence calls consume account credits; the credential-only `check` path does not.

## Execution entry

```bash
python {skill_base_dir}/scripts/zoodata.py <documented-subcommand> ...
```

This skill allows `categories`, `market`, `market-structure-profile`, `market-history`, `products`, `competitors`, `product`, `analyze`, `report`, `opportunity`, `history`, `brand-overview`, `brand-detail`, `price-band-overview`, `price-band-detail`, `check`, `reviews-raw`, `review-tag-prompt`, `review-reduce-prompt`, and `review-aggregate`.
