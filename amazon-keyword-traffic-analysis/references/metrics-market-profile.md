# Market Profile Metric Semantics

Load this file **after** `keywords/market-profile` returns and **before** interpreting any market-profile dimension. It defines conclusion boundaries; it does not replace the live response.

## Interpretation order

For each keyword, inspect in this order:

1. returned profile availability under the active shape described by `reference.md`; respect an explicit item `status=empty`, but do not require a status field in a compact profile
2. resolved snapshot period and each evidence object's historical or population scope
3. dimension presence and any explicitly returned `supported`, `calculationStatus`, or `unsupportedReason`
4. returned `level` and `interpretation`
5. returned raw business evidence in `levelEvidence`, preserving each value's field identity, unit, denominator, and direction

If a dimension is unsupported, incomplete, unknown, null, or omitted under the active contract, mark only that conclusion unavailable. Missing legacy flags do not mean an available compact dimension is unsupported. A raw count or rate is business evidence, not a normalized score or a disclosed calculation formula.

For a legacy score-bearing response, read `levelEvidence.score.value` with its returned `direction` and `context.scoringSpec`. Those scores are versioned normalized indices relative to `referenceScope`; they are not universal percentages or timeless thresholds. Do not synthesize a score or require scoring metadata when the compact response returns raw evidence instead.

## Dimension meanings

The evidence column identifies returned compact business evidence, not a disclosed grading formula. Follow each field's returned direction; `higher_means_more` does not mean a higher grade or a better opportunity. Legacy normalized-score directions apply only to legacy scores.

| Metric | Meaning and compact evidence | Directly supports | Prohibited inference |
|---|---|---|---|
| `demandScale` | Keyword demand strength, with `estimatedSearchVolume` and `abaSearchFrequencyRank`; a lower ABA rank is better ranked, not lower demand | Returned demand level and its concrete volume/rank evidence | Profitability, conversion, sales potential for an ASIN, or exact market size |
| `top3Concentration` | ABA Top-3 click/conversion concentration, with `abaTop3ClickShare` and `abaTop3ConversionShare` | Returned concentration level and the Top-3 shares | Brand concentration, one brand's dominance, seller concentration, or SERP-ASIN concentration |
| `top20OrganicEntryDifficulty` | Relative modeled difficulty of entering Top-20 organic results, with `organicTop20RolloverMultiplier` | Returned entry-difficulty level and rollover evidence | Exact rank probability/time, position-level stability, Amazon ranking causes, or an undocumented multiplier formula/cadence |
| `supplySaturation` | Supply saturation, with `searchResultSkuCount`, `observedSkuCount`, and `titleKeywordDensity`; search-result counts and observed counts have different populations | Returned supply level and its count/density evidence | Demand-supply profitability, inventory excess, category-wide seller count, or exact number of viable substitutes |
| `brandStructure` | Observed brand concentration, with `top20RankWeightedBrandHhi`, `top1BrandShare`, and `top3BrandShare` | Returned concentrated/fragmented interpretation and Top-20 rank-weighted HHI/brand-share evidence | ABA Top-3 click/conversion concentration, monopoly, a causal entry barrier, or an invented HHI weighting/share denominator formula |
| `organicProductBenchmark` | Leading organic-product benchmark, with `top48OrganicAverageRating`, `top48OrganicAverageReviewCount`, and `top48OrganicAverageRecentSaleCount` | Returned barrier level and Top-48 rating/review/recent-sales averages | A required review/sales threshold, exact entry probability, ranking-algorithm requirements, or proof that reviews/sales caused rank |

`organicTop20RolloverMultiplier` is not interchangeable with the raw snapshot's `organicRolloverRate`; preserve the returned field identity without assuming an undocumented conversion. Brand-share fields are not ABA click/conversion shares; do not infer their exact weighting or denominator from nearby field names.

Compact `adCoverage` describes the fraction of distinct observed products seen in sponsored placements, not advertising activity scores, spend, impression share, or ad traffic contribution. `adCoverageRate` is the returned coverage rate, `observedAdSkuCount` the distinct observed advertising-product count, and `observedSkuCount` the observed-product denominator. Preserve the returned numerator and denominator; overlapping placement types must not be added as though they were distinct products.

`adActivity` applies only when that legacy dimension is actually returned. Its score supports relative advertising activity, not compact coverage, CPC, bid price, auction pressure, Ads conversion, or profitability. Legacy score evidence supports only the returned versioned grade; related raw snapshot fields are not proof of a disclosed calculation formula.

## Market characteristics matrix

| Metric | Meaning | Directly supports | Prohibited inference | Evidence fields |
|---|---|---|---|---|
| `marketCharacteristics.volatility` | Returned mapping of market volatility | The returned volatility `type`, subject to support/status and mapping confidence | A trend direction, lifecycle stage, cause of volatility, or future volatility | `type`, `evidence.sourceValue`, `evidence.mappingConfidence.{value,direction}` |
| `marketCharacteristics.annualSeasonality` | Returned annual-seasonality classification | The returned `classification` and any explicitly returned historical peak evidence | Invented peak months, future forecast, trend direction, or seasonality from `seasonalPeakPatternDetected` alone | `classification`, year-over-year correlation, eligible-pair count, peak-pattern flag, `peakPeriods` |

Compact annual seasonality is returned directly at `marketProfile.annualSeasonality`; the legacy nested path applies only to the legacy shape. A returned classification remains usable without peak evidence; an omitted peak field is not an empty peak array and supplies no seasonal timing. Its historical estimation scope is independent of the selected snapshot and any trend-profile window. Historical peaks do not prove yearly recurrence, and `non_seasonal` may still have historical `peakPeriods`. An empty returned peak array means no peak was identified in available evidence. Window-specific volatility belongs to the returned trend-profile window; do not derive it from annual seasonality or require the legacy market-volatility object.

## Claim rules

- Prefer the endpoint's returned `interpretation` when it is consistent with returned availability and evidence directions; do not rewrite a dimension into a different business concept.
- Keep `top3Concentration` and `brandStructure` separate. One is ABA Top-3 click/conversion concentration; the other is brand-structure concentration.
- Describe `adActivity` as activity, never as traffic contribution or bid economics.
- Describe low `top20OrganicEntryDifficulty` as **relatively lower modeled entry difficulty**, never as “easy to rank.”
- Describe `organicProductBenchmark` as a market-relative barrier, not an Amazon ranking formula.
- Raw detail fields may provide traceability or a different named inference. They do not override the metric result and must not be used to reverse-engineer an undocumented formula.
- When `annualSeasonality` is unsupported or has no returned peak evidence, omit seasonal timing and seasonal-cause narratives entirely. Hedging with `may`, `might`, `possibly`, or an equivalent in any language does not authorize an invented season, peak, or explanation.

For relationships among multiple returned dimensions, apply the cross-metric reconciliation protocol in `evidence-protocols.md`. The field-specific distinctions and inference limits above remain authoritative for each market-profile dimension.
