---
name: amazon-market-analysis
description: >
  Analyze Amazon category markets through one connected workflow: discover
  candidate niches and products, evaluate a named market's entry conditions,
  and inspect market changes over time. Use for market opportunity discovery,
  niche selection, category viability, GO/CAUTION/AVOID questions, market
  structure, subcategory comparison, trend scans, and explicitly requested
  market monitoring. Requires ZOODATA_API_KEY.
metadata:
  version: "0.1.0"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Amazon Market Analysis

Respond in the user's language.

## Start here

1. Read and apply `references/analysis-contract.md` before classifying the request, making an evidence call, or sending user-facing text.
2. Classify the current question. Route an open-ended "what market/product should I explore?" request to **discover**; a named category or niche and entry/competition question to **evaluate**; a change, trend, or watch question to **track**. A single field or one dated snapshot is a quick lookup. A product/ASIN may support a market question, but a listing audit, competitor war room, or price-setting request belongs to its dedicated skill.
3. Read `references/cli-contract.md` and `references/reference.md`; inspect the selected bundled CLI subcommand's `--help`. The reference owns production endpoint availability, parameters, response shapes, dates, and credit facts.
4. Load `references/output-rules.md`. For a quick lookup, load only `references/execution-guide.md` sections `Authority and routing`, `Execution mode`, `Field Identity Gate`, `Interface Failure Stop Gate`, `Final Output Gate`, and `Credential and Credit Failures`.
5. For a full analysis, load the complete `references/execution-guide.md`, `references/evidence-protocols.md`, and exactly the applicable scenario: `references/scenarios-discover.md`, `references/scenarios-evaluate.md`, or `references/scenarios-track.md`. The guide owns market stage selection and domain Gate decisions; the scenario owns its evidence and conclusion scope. Reclassify a follow-up from the user's actual question rather than forcing the next story step.
6. Before interpreting returned market measures, load `references/market-metric-semantics.md`. Before interpreting seller capital, cost, margin, risk tolerance, or compliance claims, also load `references/seller-input-semantics.md`.

## Source-of-truth boundaries

- This `SKILL.md` owns trigger classification, module loading, the responsibility map, and non-negotiable runtime boundaries. It does not define endpoint contracts, workflow procedures, market metric meanings, scenario thresholds, or report templates.
- `references/analysis-contract.md` owns the repository-wide rule hierarchy, universal analysis principles and Gates, and user-facing implementation boundary. Every market module may add or narrow domain rules but must not duplicate, weaken, or override it.
- `references/cli-contract.md` owns shared CLI invocation, command identity, composite reuse, transport and retry classification, terminal failures, and partial results. It does not select a market scenario or define market fields, interpretation, or output.
- `references/reference.md` owns only production API facts: endpoint availability, request and response contracts, category identity, date and sample options, CLI mapping, and credit metadata. It does not decide whether a market is attractive or when to advance a stage.
- `references/execution-guide.md` owns the market scenario/stage schema, market-specific Gate decisions, evidence-level conclusion ceilings, and follow-up handoff. It does not redefine the shared analysis contract, API fields, detailed evidence procedures, or scenario-specific capability maps.
- `references/evidence-protocols.md` owns shared acquisition, identity matching, comparison, coverage, reconciliation, and evidence reuse inside an active stage. It does not select a stage or render the report.
- `references/market-metric-semantics.md` owns the meaning, denominator, time grain, and inference limits of returned market fields. It does not define request parameters, stage transitions, or business verdicts.
- `references/seller-input-semantics.md` owns seller-provided inputs, unit-economics calculations, and the limits of capital and compliance evidence. It does not redefine API contracts or independently issue a verdict.
- `references/output-rules.md` owns market-specific localized rendering, the report skeleton, confidence labels, provenance, and usage accounting within the shared user-facing boundary. It does not redefine that boundary, select stages, or raise conclusion authority.
- Scenario files own only their specific entry inputs, capability selection, stage evidence, conclusion authority, and section content. They may narrow an owner rule but cannot restate or override it. `scenarios-discover.md` owns market and product candidate discovery; `scenarios-evaluate.md` owns entry assessment; `scenarios-track.md` owns trend and explicitly opted-in monitoring.
- `{skill_base_dir}/scripts/zoodata.py` owns CLI request construction and transport metadata, not analysis policy. `README.md` is a human-facing package index only and does not set runtime rules.

## Non-negotiable boundaries

- Require `ZOODATA_API_KEY`; use the credential-only `check` path before evidence calls. Do not substitute guessed numbers or unrelated public data when the API cannot be used.
- Use the bundled `{skill_base_dir}/scripts/zoodata.py` and its local `scripts/allowed-commands.json`. Query market snapshots through `markets/search`; the experimental `markets/overview` path and `market-overview` command were never published and are outside the supported interface.
- Resolve and preserve a category ID for a named market. A broad product keyword is not itself a category. If category resolution relies on a top product, label it inferred and confirm before making an entry verdict.
- Preserve each market row's product inclusion scope, `sampleType`, marketplace, returned date, and the distinction between all-category `total*` and selected Top 100 `sample*` measures. Do not infer margin from market revenue, price, or content rate.
- A market ranking is limited to the categories and pages actually observed. A daily snapshot and available month-end history are different grains; compare only compatible observations.
- Do not create a watchlist, baseline, schedule, notification, or recurring run without the user's explicit monitoring request. A one-time trend question does not activate monitoring.
- State credit cost before a broad multi-call scan; use the smallest evidence set needed for the active stage. Seller budget, experience, costs, and risk tolerance remain local interpretation inputs and are not sent as free text to ZooData.

## Capabilities and data flow

- **Network**: the bundled CLI sends authenticated requests only to `https://api.zoodata.ai`; it refuses an untrusted `ZOODATA_BASE_URL` and withholds the bearer key.
- **Execution**: Python 3 standard-library shared CLI at `{skill_base_dir}/scripts/zoodata.py`, restricted by the local command manifest.
- **Local files**: reads optional `~/.zoodata/config.json` for credentials. No query state is written by default; an explicitly opted-in watch may save non-secret baseline data under `~/.zoodata/market-analysis/` as described by `scenarios-track.md`.
- **Sent to the API**: category paths/IDs, product keywords, ASINs, dates, marketplace, and numeric filters. Seller budget, costs, experience, risk tolerance, and compliance notes remain local.
- **Credits**: live endpoint calls consume account credits; the shared CLI's diagnostic `check` without probe flags does not.

## Execution entry

```bash
python {skill_base_dir}/scripts/zoodata.py <documented-subcommand> ...
```

The bundled manifest allows exactly: `categories`, `market`, `market-structure-profile`, `market-history`, `products`, `competitors`, `product`, `analyze`, `price-band-overview`, `price-band-detail`, `brand-overview`, `brand-detail`, `history`, `market-entry`, `opportunity-scan`, and the diagnostic `check`.
