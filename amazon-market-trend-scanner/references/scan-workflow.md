# Full scan, quick check, trend signals, and subcategory ranking

Use full-category `totalMonthlySales` and `totalMonthlyRevenue` for market size. Keep selected Top 100 measures separate: `top100ConservativeNewProductRate6m`, `top100Top10BrandSalesRate`, `top100MedianPrice`, `top100FbmRate`, and `top100AvgRatingCount`. For their API definitions, read `reference.md § 2`.

## Mode 1: Full Scan

1. `categories --keyword "{keyword}"` → resolve category path
2. `categories --parent "{path}"` → child IDs; `market --category-id "{id}" --scope subtree --page-size 1` for each child. Use each matching `data[0]` row for the snapshot and an unscoped `market` query for size-filtered discovery.
3. Record the full-category size and selected Top 100 metrics listed above for each subcategory.
4. `products --keyword "{sub}" --category "{path}" --mode emerging --page-size 20` per hot subcategory
5. `products --keyword "{sub}" --category "{path}" --mode new-release --page-size 20` per hot subcategory
6. Save baseline → `{skill_base_dir}/scan-data/baseline.json`, config → `{skill_base_dir}/scan-data/watchlist.json`
7. Output full trend report (see Output Spec)
8. Offer Auto-Monitor setup

## Mode 2: Quick Check (scheduled)

1. Read `{skill_base_dir}/scan-data/watchlist.json` + `{skill_base_dir}/scan-data/baseline.json`
2. Resolve each watched category path through `categories --category "{path}"` if its watchlist entry lacks `categoryId`; then run `market --category-id "{id}" --scope subtree --page-size 1` and use its matching `data[0]` row. Use `market-history --category-id "{id}" --start-date YYYY-MM-DD --end-date YYYY-MM-DD` when a server month-end trend is needed.
3. If the saved baseline contains legacy `sample*` market fields instead of the new `total*` / `top100*` fields, initialize a new baseline from the successful current snapshot and suppress change alerts for that first migrated check. Preserve the old snapshot in history for audit, but do not compare incompatible fields.
4. Compare vs baseline using signal rules below
5. 🔴 alerts → notify user; else silent log
6. Save snapshot to `{skill_base_dir}/scan-data/history/{timestamp}.json`, update baseline and watchlist ID

## Trend Signals

| Signal | Condition | Level |
|--------|-----------|-------|
| Demand surge | `totalMonthlySales` >20% vs comparable baseline | 🔴 |
| Red ocean warning | `top100Top10BrandSalesRate` >70% AND rising | 🔴 |
| New entrant wave | `top100ConservativeNewProductRate6m` up >5 percentage points | 🟡 |
| Brand loosening | `top100Top10BrandSalesRate` down >3 percentage points | 🟡 |
| Price shift | `top100MedianPrice` change >10%; inspect `market-structure-profile --dimension price` | 🟡 |
| Minor movement | None of the above triggered | 🟢 Silent log |

### Trend Interpretation & Action Guide
| Signal Combination | Market Phase | Recommended Action |
|--------------------|-------------|-------------------|
| Demand surge + New entrant wave | 🚀 Growth phase | Enter quickly, first-mover advantage matters 💡 |
| Demand surge + Brand loosening | 🎯 Opportunity window | Best timing — demand up, incumbents losing grip 💡 |
| Demand surge + Red ocean warning | ⚠️ Late stage growth | High demand but leaders consolidating — need strong differentiation 💡 |
| Red ocean warning + No demand surge | 🔒 Mature/locked | Avoid — established players dominate with flat demand 💡 |
| Brand loosening + Price band shift down | 💰 Price war | Wait — margins compressing, enter after shakeout 💡 |
| New entrant wave + Price shift | 🔄 Disruption | Study the new products and price distribution 🔍 |

### Subcategory Ranking Criteria
Rank subcategories by composite attractiveness (apply market-entry scoring logic):
- **Demand**: `totalMonthlySales` — higher observed demand 📊
- **Competition**: `top100Top10BrandSalesRate` — lower selected-sample concentration 📊
- **Entry barrier**: `top100AvgRatingCount` — lower review burden 📊
- **Activity**: `top100ConservativeNewProductRate6m` — higher recent listing share 📊
- **Price positioning**: `top100MedianPrice`; price alone does not establish margin 🔍
