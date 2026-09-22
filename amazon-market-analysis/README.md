# Amazon Market Analysis

This package provides one ZooData skill for three connected market questions: which categories or products merit investigation, whether a named market fits a seller's conditions, and what changed in that market over time. A user can start at any question. Runtime instructions are owned by [SKILL.md](SKILL.md) and its routed modules.

## Package map

- [SKILL.md](SKILL.md) — trigger router, module responsibility map, and global boundaries
- [API reference](references/reference.md) — live market and supporting endpoint/CLI contracts
- [Execution guide](references/execution-guide.md) — common stage structure, evidence authority, Gate order, and handoff
- [Evidence protocols](references/evidence-protocols.md) — acquisition, identity, coverage, comparison, and reuse procedures
- [Market metric semantics](references/market-metric-semantics.md) — full-category versus Top 100 field meaning and inference limits
- [Seller input semantics](references/seller-input-semantics.md) — seller capital, costs, and compliance-input boundaries
- [Output rules](references/output-rules.md) — language, report shape, provenance, and API usage
- [Discover scenario](references/scenarios-discover.md) — category discovery and product candidate validation
- [Evaluate scenario](references/scenarios-evaluate.md) — market screen and conditional entry assessment
- [Track scenario](references/scenarios-track.md) — observed historical movement and opted-in watch comparisons
- [Bundled CLI](scripts/zoodata.py), [shared CLI contract](references/cli-contract.md), and [command manifest](scripts/allowed-commands.json) — independently publishable runtime

## Data and privacy

The CLI sends category, product, and date/filter requests to `api.zoodata.ai` using a locally configured key. Seller profile, economics, and compliance notes remain local. No watchlist or baseline is written unless the user explicitly requests monitoring; any opted-in baseline is stored outside the skill package under `~/.zoodata/market-analysis/`.
