# Product-traffic metric meanings

## Exposure and placement

| Metric | Meaning |
|---|---|
| Estimated exposure score (`estimateImpressionPoint`) | An estimated exposure score for the specified ASIN/query/placement and returned period. |
| `trafficShare` | Contributor rows measure the row's exposure share within the ASIN period. In named-term weekly data, `trafficByExploreType.<type>.trafficShare` measures that placement type's share within the ASIN-query period. |
| `asinTrafficShare` | In named-term weekly data, the ASIN-query exposure divided by that ASIN's exposure across all queries for the same period. |
| `exploreType` | Placement type: `ORG` for organic results; sponsored types use their returned labels. |
| Absolute / average position | The specified ASIN's position under one search query and placement type. `absolutePosition` is the latest valid position observation in the period; `avgPosition` is the mean of valid position observations in that period. Lower values are ahead. These observations measure the ASIN-query placement, not a word or fragment in the product's title. |
| Observation count / covered days | The number of observations and covered days supporting a measurement. |
| Null position | No numeric position has been returned for that field. Interpret its supporting coverage using [position availability](#position-availability). |
| Query-total exposure points | The keyword-period total repeated on result rows; a keyword-level value. |

## Position availability

Read `absolutePosition` and `avgPosition` separately for the same ASIN, query, period and placement type. Apply only fields supplied by that interface; a null field does not invalidate another field's numeric value.

| Returned condition | Supported interpretation |
|---|---|
| Position is null and contributor-row `observationCount=0` | No valid position observations were returned for that row; the position is unknown. |
| Position is null and contributor-row `observationCount>0` | The row has valid position observations, but this position field is unavailable; retain the count and leave this position unknown. |
| Position is null, `observationCount` is unavailable and `daysCoverageRate=0` | No observation days are recorded for that placement type in the period; the position is unknown. |
| Position is null, `observationCount` is unavailable and `daysCoverageRate>0` | Observation days are recorded, but this position field is unavailable; the position is unknown. |
| A weekly period is returned but its `trafficByExploreType` key is absent | No record was returned for that placement type; its position and exposure are unknown. |
| Item `status=empty` with `emptyReason=asin_keyword_not_found`, or a requested period is absent from `series` | No matching ASIN-query records were returned for that range or period; the position is unknown. |
| Position is null and the relevant coverage fields are null, absent or insufficient to explain it | The response does not establish why the position is unavailable; keep the position and reason unknown. |

Do not infer ranking loss or zero exposure from missing positions or coverage alone; retain any returned exposure value. Null `resolvedDateFrom`, `resolvedDateTo` or `resolvedDate` also does not by itself establish that the source period was unobserved.

## Structure and weekly measures

| Metric | Meaning |
|---|---|
| Structure profile | The returned ASIN's current-versus-previous-week aggregate and channel composition. |
| Prior-period null / zero | A prior count/share/exposure null means unavailable prior-week data; numeric zero is a measured field with no corresponding signal in an available week. |
| Term count / new and lost terms | Observed query coverage, with new/lost coverage defined relative to an available comparison period. |
| Change drivers | The terms contributing to observed exposure increases or decreases. |
| Absolute share change / relative change | A share difference of 0.05 is five percentage points; a relative change of 0.05 is five percent. |

## Trend and context

| Metric | Meaning |
|---|---|
| Trend classification | The service's direction for the specified object, component and resolved window. |
| Volatility / last-period position | Fluctuation within the window and the latest observation's place in that window's range. |
| Normalized slope | The service's dimensionless trend-support measure for one object within its window. |
| Query measures | Search count and ABA rank describe the keyword's own measurement window. |
| Product snapshot / ad activity | The product facts for the snapshot date and observed sponsored participation for the corresponding traffic period. |
