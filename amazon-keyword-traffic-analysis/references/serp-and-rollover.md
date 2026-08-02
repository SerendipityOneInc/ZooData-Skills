# SERP, Exposure, and Organic Rollover Semantics

Load this file after retrieving `keywords/search-results` or when interpreting `detail.snapshotData.organicRolloverRate`. It prevents placement-record counts, estimated exposure, and organic turnover from being conflated.

## Question-to-field routing

| Question | Primary evidence | What it can answer |
|---|---|---|
| How many returned records are organic vs sponsored? | `search-results.rows[].exploreType` | Placement-record mix within the returned rows |
| Which returned placements have more estimated exposure? | `rows[].estimateImpressionPoint` | Row-level estimated-impression-point comparison |
| What is the estimated ORG vs sponsored contribution within the retrieved sample? | Transparent sums of `estimateImpressionPoint` grouped by `exploreType` | Derived contribution mix within the disclosed returned-row scope |
| What is ZooData's snapshot organic rollover metric? | `detail.snapshotData.organicRolloverRate` | The returned official snapshot metric value only |
| How much did the Top-N organic ASIN set change between weekly snapshots? | Multiple complete `search-results` ORG snapshots | Agent-derived Top-N set retention/turnover |
| Did a specific position rotate during one week? | Observation-level chronological position history | Not supported by weekly aggregate search-result rows alone |

## Placement records are not traffic contribution

- Record count by `exploreType` answers how many placement records were returned. It does not answer how traffic or exposure is distributed.
- Compare exposure with `estimateImpressionPoint`, not row count. Keep `ORG`, `SP`, `SB`, `SBV`, and `SPR` separate before optionally combining sponsored types.
- A high number of sponsored rows supports “advertising formats/participation are present in the returned sample.” It does not support “ads take most traffic,” high CPC, or high bid competition.
- A few ORG rows with much larger `estimateImpressionPoint` values can coexist with many lower-point sponsored rows. Report both facts without collapsing them.

### Transparent contribution calculation

When rows share the same keyword, resolved weekly period, filters, and compatible observation scope:

`returned-row contribution share(type) = Σ estimateImpressionPoint(type) / Σ estimateImpressionPoint(all returned rows)`

This is an Agent-derived mix within the returned rows. State page/filter/pagination coverage and missing-value handling. Do not call it exact Amazon traffic share or Ads share of voice.

`keywordTotalEstimateImpressionPoint` is a keyword-level denominator repeated on rows. Verify that its non-null value is consistent and **never sum it across rows**. If using it as a denominator, label the result as a sampled keyword-total-referenced estimate and disclose row coverage.

## Brand and concentration boundaries

- A unique-brand count or brand frequency from `rows[].brand` is a returned-SERP-sample calculation.
- `marketProfile.brandStructure` is the server-calculated brand-structure metric.
- `marketProfile.top3Concentration` is ABA Top-3 click/conversion concentration. It is not brand concentration.
- Unique ASIN count is ASIN diversity, not brand diversity and not proof of low market control.

## Organic rollover boundaries

`detail.snapshotData.organicRolloverRate` is the direct ZooData snapshot metric. The published contract names it but does not document its formula, Top-N scope, observation cadence, or whether it is position-specific. Therefore:

- report the returned value as `organicRolloverRate` and preserve the resolved weekly period;
- do not rename it Top-10/Top-20 turnover, weekly retention, or position churn;
- do not derive exact entry probability, ranking time, or “easy to enter” from it;
- do not state that relevance, clicks, conversion, sales, reviews, or any other factor caused the observed rollover unless separate discriminating evidence supports that causal claim.

### Agent-derived Top-N set turnover

When the user explicitly needs multiweek Top-N stability and complete comparable ORG snapshots are available, define:

- `S(t,N)`: unique ASINs with `exploreType=ORG` and `absolutePosition <= N` in resolved week `t`
- `retention(t,N) = |S(t-1,N) ∩ S(t,N)| / |S(t-1,N)|`
- `set turnover(t,N) = 1 - retention(t,N)`

Report each week pair, `N`, set sizes, deduplication, missing rows, pagination, and resolved periods. Call this **Agent-derived Top-N set turnover**, not ZooData `organicRolloverRate` and not per-position rotation.

Weekly aggregate rows do not provide a chronological event stream. Multiple ASINs associated with the same `absolutePosition` in one resolved week may reflect aggregation or observation coverage; without ordered observation-level evidence, they do not prove that the position rotated that many times.

## Conclusion authority

- SERP and rollover evidence can describe observed structure, estimated exposure distribution, and stability.
- It cannot by itself prove an ASIN's relevance, conversion, profitability, future rank, Amazon ranking mechanism, bid requirement, or budget priority.
