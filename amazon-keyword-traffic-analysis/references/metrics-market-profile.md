# Market Profile Metric Semantics

Load this file **after** `keywords/market-profile` returns and **before** interpreting any market-profile dimension. It defines conclusion boundaries; it does not replace the live response.

## Interpretation order

For each keyword, inspect in this order:

1. item `status`; interpret only `status=ok`
2. resolved period and `context.scoringSpec`
3. dimension `supported`, `calculationStatus`, `unsupportedReason`
4. returned `level` and `interpretation`
5. `levelEvidence.score.value` together with its returned `direction`

If a dimension is unsupported, incomplete, unknown, or null, mark only that conclusion unavailable. Scores are versioned normalized indices relative to the returned `referenceScope`; they are not universal percentages or timeless thresholds.

## Scored dimension matrix

The final column lists **related audit fields**, not published formulas. Do not claim that a field is an exact calculation input unless the live schema says so.

| Metric | Meaning | Direction | Directly supports | Prohibited inference | Related raw snapshot fields |
|---|---|---|---|---|---|
| `demandScale` | Relative strength of keyword demand in the returned scoring context | Higher score = stronger demand | Relative demand level for this keyword and snapshot | Profitability, conversion, sales potential for an ASIN, or exact market size | `detail.snapshotData.estimateSearchCount`, `abaRank` |
| `top3Concentration` | Concentration of ABA Top-3 click and conversion shares | Higher score = greater Top-3 concentration | Whether ABA click/conversion attention is more concentrated among the Top 3 | Brand concentration, one brand's dominance, seller concentration, or SERP-ASIN concentration | `abaTop3ClickShareRate`, `abaTop3ConversionShareRate` |
| `adActivity` | Relative advertising activity around the keyword | Higher score = greater advertising activity | Whether observed advertising participation/activity is relatively high or low | Ad traffic share, CPC, bid price, auction pressure, Ads conversion, profitability, or “ads take most traffic” | `sponsoredProductSkuCount`, `sponsoredBrandSkuCount`, `sponsoredBrandVideoSkuCount`, `sponsoredRecommendSkuCount`, `adCampaignCount`, `adCount` |
| `top20OrganicEntryDifficulty` | Relative difficulty of entering the Top-20 organic result set | Higher score = greater entry difficulty | Relative organic-entry difficulty and whether the modeled entry barrier is higher/lower | That a matched listing can enter, exact rank probability/time, per-position stability, or Amazon ranking causes | `organicRolloverRate`, `organicSkuCount`, Top-48 organic benchmark fields |
| `supplySaturation` | Relative saturation of observed supply for the keyword | Higher score = greater saturation | Whether observed supply is relatively more/less saturated | Demand-supply profitability, inventory excess, category-wide seller count, or exact number of viable substitutes | `totalSkuCount`, `observedSkuCount`, `organicSkuCount`, sponsored SKU counts, `titleDensity` |
| `brandStructure` | Concentration of the keyword's observed brand structure | Higher score = greater brand concentration | Whether brand structure is relatively concentrated or fragmented | ABA Top-3 click/conversion concentration, ASIN concentration, monopoly, or a causal entry barrier | `brandCount`, `observedSkuCount`; use `search-results.rows[].brand` only for a separately disclosed returned-row analysis |
| `organicProductBenchmark` | Barrier represented by leading organic products | Higher score = higher leading organic-product barrier | Relative strength of the leading-organic-product benchmark | A required review/sales threshold, exact entry probability, ranking-algorithm requirements, or proof that reviews/sales caused rank | `top48OrganicSkuAvgPrice`, `top48OrganicSkuAvgRating`, `top48OrganicSkuAvgRatingsTotal`, `top48OrganicSkuAvgRecentSaleCount` |

## Market characteristics matrix

| Metric | Meaning | Directly supports | Prohibited inference | Evidence fields |
|---|---|---|---|---|
| `marketCharacteristics.volatility` | Returned mapping of market volatility | The returned volatility `type`, subject to support/status and mapping confidence | A trend direction, lifecycle stage, cause of volatility, or future volatility | `type`, `evidence.sourceValue`, `evidence.mappingConfidence.{value,direction}` |
| `marketCharacteristics.annualSeasonality` | Returned annual-seasonality classification | The returned `classification` and any explicitly returned historical peak evidence | Invented peak months, future forecast, trend direction, or seasonality from `seasonalPeakPatternDetected` alone | `classification`, year-over-year correlation, eligible-pair count, peak-pattern flag, `peakPeriods` |

## Claim rules

- Prefer the endpoint's returned `interpretation` when it is consistent with the status and score direction; do not rewrite a dimension into a different business concept.
- Keep `top3Concentration` and `brandStructure` separate. One is ABA Top-3 click/conversion concentration; the other is brand-structure concentration.
- Describe `adActivity` as activity, never as traffic contribution or bid economics.
- Describe low `top20OrganicEntryDifficulty` as **relatively lower modeled entry difficulty**, never as “easy to rank.”
- Describe `organicProductBenchmark` as a market-relative barrier, not an Amazon ranking formula.
- Raw detail fields may provide traceability or a different named inference. They do not override the metric result and must not be used to reverse-engineer an undocumented formula.
- When `annualSeasonality` is unsupported or has no returned peak evidence, omit seasonal timing and seasonal-cause narratives entirely. Hedging with `may`, `might`, `possibly`, or `可能` does not authorize an invented season, peak, or explanation.

## Cross-metric reconciliation framework

Apply this framework to any current or future dimensions that inform the same operator question. Do not maintain a fixed list of metric pairs.

### Normalize each signal

| Attribute | Question |
|---|---|
| Subject | What entity or phenomenon is measured? |
| Measure | What quantity, classification, or profile is returned? |
| Population / grain | Which result set, aggregation level, or observation grain does it cover? |
| Period | Snapshot, fixed trend window, or returned observation period? |
| Reference scope | Absolute value, same-marketplace normalized index, returned-row sample, or another comparison basis? |
| Direction | What does higher/lower/positive/negative mean according to the returned contract? |
| Conclusion authority | What is the strongest direct conclusion, and which stronger inference is forbidden? |

### Classify the relationship

| Relationship | Test | Handling |
|---|---|---|
| `aligned` | Same relevant scope and mutually reinforcing direction | Synthesize only the intersection of supported conclusions |
| `complementary` | Same operator question but different subjects, grains, periods, or axes | Preserve each signal and explain their bounded joint meaning |
| `incomparable` | No valid common scope or denominator | Report separately; do not rank, average, or reconcile numerically |
| `genuinely inconsistent` | Same subject, definition, grain, period, and reference scope but incompatible results | Recheck status/context/fields; report unresolved unless additional evidence discriminates |

### Synthesis rules

- Use `signal A scope + signal B scope → common supported implication → remaining unknown`.
- The joint conclusion cannot exceed the authority of any evidence used to support it.
- Do not infer causality merely because two signals move together or differ.
- Do not explain a composite score with related raw fields unless those fields were retrieved and the contract documents the relationship; related audit fields are not formulas.
- Put any material aligned, complementary, incomparable, or inconsistent relationship needed for the decision in the first report. Do not wait for a follow-up question.
