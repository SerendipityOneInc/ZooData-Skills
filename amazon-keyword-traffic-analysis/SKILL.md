---
name: amazon-keyword-traffic-analysis
description: >
  Analyze Amazon keyword demand, market structure, weekly trends, observed SERP
  signals, and ASIN keyword visibility or traffic observations. Use for keyword
  expansion, keyword deep dives, reverse-ASIN keyword analysis, and diagnosing
  observed ASIN × keyword changes. Produces evidence-bounded validation priorities;
  does not make direct bid, budget, pause, or negative-keyword decisions without
  seller ABA-SQP and Amazon Ads data. Requires ZOODATA_API_KEY.
metadata:
  version: "0.1.4"
  author: SerendipityOneInc
  homepage: https://github.com/SerendipityOneInc/ZooData-Skills
  openclaw: {"requires": {"env": ["ZOODATA_API_KEY"]}, "primaryEnv": "ZOODATA_API_KEY"}
---

# ZooData — Amazon Keyword Intelligence

Respond in the user's language.

## Start here

1. Classify the request: seed-keyword expansion, target-keyword analysis, reverse ASIN, ASIN × keyword diagnosis, or a single lookup.
   - Route ASIN requests about current traffic terms, traffic-source structure, candidate discovery, or which keywords merit examination to reverse ASIN.
   - Route ASIN or ASIN × keyword requests containing change, drop, rise, volatility, anomaly, `why`, cause, or time-based explanation to keyword traffic diagnosis. This diagnosis route takes precedence even when the request also mentions reverse ASIN or traffic terms. A keyword-only demand/trend question remains target-keyword analysis.
   - Route an ASIN-wide anomaly without a named keyword to diagnosis for aggregate triage; do not use reverse ASIN to explain the cause.
   - If a reverse-ASIN follow-up selects a term and asks why it moved, start the diagnosis scenario in that next turn and reuse compatible prior evidence.
2. Read `references/reference.md` and the relevant `zoodata.py --help` before selecting a tool. It is the sole source for production endpoint availability, parameters, response fields, dates, batching, credits, and API capability boundaries.
3. Load `references/execution-guide.md` for every non-trivial task. It is the sole source for the shared workflow: question → evidence plan → retrieval → analysis → conclusion, evidence authority, diagnostic/action gates, and output rules. After every retrieval or tool result, apply its `Interface Failure Stop Gate` before selecting any next capability or command.
4. Route the request to the applicable scenario guide, or to multiple non-exclusive guides, for capability selection and output shape. Follow `execution-guide.md` for scenario ownership and permitted combinations:
   - `references/scenarios-expand.md`
   - `references/scenarios-keyword-analysis.md`
   - `references/scenarios-reverse-asin.md`
   - `references/scenarios-keyword-traffic-diagnosis.md`
5. After API retrieval, load only the field-semantic reference needed for the returned data:
   - `references/metrics-market-profile.md` for `market-profile`
   - `references/metrics-trend-profile.md` for `trend-profile`
   - `references/serp-and-rollover.md` for SERP or `organicRolloverRate`
6. Before requesting or interpreting a seller artifact, load `references/sqp-field-semantics.md`. Treat it as the sole acquisition and field-semantics source for user-provided ABA-SQP or Amazon Ads data.

## Source-of-truth boundaries

- This file owns only trigger classification, reference loading, scenario routing, and non-negotiable global acquisition/safety boundaries. It may point to an owner module but must not define endpoint contracts, shared workflow procedures, field semantics, or scenario-specific stage logic.
- `reference.md` owns only production API and acquisition-surface facts: availability, request parameters, response schema, status meaning, batching, dates, and billing. It may name fields and capabilities to describe their contract, but must not define Agent workflow, action/output policy, business interpretation, or scenario transitions.
- `execution-guide.md` owns only cross-scenario Agent workflow, evidence authority, action gates, and output rules. It may reference endpoint or field identifiers to route the reader to their owner, but must not redefine API contracts, field meanings, or scenario-specific capability/stage maps.
- The metric/observation semantic references (`metrics-*.md` and `serp-and-rollover.md`) own only documented field meaning, direction, scope, and permitted/prohibited inference. They may identify source fields/endpoints, but must not define production availability or request parameters, shared workflow policy, or scenario routing/stages.
- `sqp-field-semantics.md` owns seller-artifact acquisition order, schema identity, denominator rules, field meaning, and seller-artifact output labels. It must not define ZooData API contracts or scenario-specific stage triggers and conclusions.
- Scenario files own only scenario-specific capability selection, stage transitions, and report shape. They may reference owner-defined capabilities, fields, and gates, but must not restate, relax, replace, or create exceptions to their contracts or semantics.
- Cross-module references are allowed; cross-module redefinition and duplicated policy are not. When statements span modules, split API fact, shared workflow consequence, field interpretation, and scenario application into their respective owners.
- Preserve this file's global boundaries. For an ownership conflict, follow the responsible owner above and narrow downstream behavior. If a cross-cutting conflict cannot be separated without changing a top-level owner contract, surface it for discussion instead of choosing a competing rule, combining scoring systems, or inventing a fallback.

## Non-negotiable boundaries

- Require `ZOODATA_API_KEY`. If it is missing or rejected, follow the credential procedure in `execution-guide.md`; do not substitute public web data.
- Use the bundled `{skill_base_dir}/scripts/zoodata.py` for documented keyword endpoints and `realtime/product`. Use ZooData WebTools `/search`, `/scrape`, and `/scrape-interactive` only through an exposed, documented ZooData WebTools surface after inspecting its live schema.
- Use only the acquisition routes whitelisted in `reference.md`. WebTools `/search` is permitted URL discovery; it is not `products/search`. Never use `products/search`, external browser automation, direct Amazon navigation, or non-ZooData public web search as evidence or fallback.
- Treat keyword inputs as Amazon search queries. Default an omitted marketplace to `US`; choose T-1 or earlier before the first request for endpoints requiring `date` or `dateTo` unless the user requests today's data.
- ZooData keyword data is estimated search, visibility, rank, placement, and impression evidence. It is not the seller's ABA-SQP conversion funnel. Keep product-specific value, profitability, bids, spend, budgets, pauses, negatives, and unconditional go/no-go decisions within the evidence authority defined in `execution-guide.md`.
- Preserve returned status, period, subject, field scope, and uncertainty. `status=empty` is an observation-coverage boundary, not proof of low demand.
- Do not report an API root cause, strategy recommendation, or undocumented metric as though the API returned it.

## Execution entry

Use:

```bash
python {skill_base_dir}/scripts/zoodata.py <documented-subcommand> ...
```

Run bare `python {skill_base_dir}/scripts/zoodata.py check` for credential diagnostics only. Without `--endpoints` or `--keyword-endpoints`, it makes no evidence calls; those opt-in probe flags consume credits and are outside this skill's evidence workflow.

WebTools has no bundled subcommand in this skill. Use only an exposed ZooData WebTools session/callable surface as documented in `reference.md`.
