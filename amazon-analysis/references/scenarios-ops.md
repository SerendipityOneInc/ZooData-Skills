# Amazon Seller Daily Operations & Monitoring

> Monitor Amazon market trends, track competitor pricing and BSR changes, detect anomalies, and automate daily seller operations.
> Load when handling market monitoring, competitor tracking, or anomaly detection.
> For API parameters, see `reference.md`.
>
> ⚠️ **Resolve categoryPath for product endpoints and categoryId for market endpoints before running these queries.** Tag conclusions with 📊/🔍/💡 confidence labels.
>
> **History coverage**: Use `history` for product-level ASIN history and `market-history` for category-market history. For a requested dimension without a corresponding history endpoint, compare only compatible saved snapshots or a clearly labeled same-scope peer baseline.

---

## 6.1 Market Dynamics Monitoring

```bash
# Step 1: Market overview
python3 scripts/zoodata.py categories --category "Pet Supplies > Dogs"
python3 scripts/zoodata.py market --category-id "<categoryId from categories>"

# Step 2: New products in last 90 days
python3 scripts/zoodata.py products --keyword "dog toys" --listing-age 90d --page-size 20
```

---

## 6.2 Competitor Dynamics

```bash
python3 scripts/zoodata.py competitors --brand "CompetitorBrand" --sort listingDate
```

---

## 6.3 Top Products Changes

```bash
python3 scripts/zoodata.py products --category "Pet Supplies > Dogs > Toys" --page-size 20
```

---

## 6.4 Anomaly Alerts

```bash
# Step 1: Market indicators
python3 scripts/zoodata.py categories --category "Pet Supplies > Dogs > Toys"
python3 scripts/zoodata.py market --category-id "<categoryId from categories>"

# Step 2: Current top products
python3 scripts/zoodata.py products --category "Pet Supplies > Dogs > Toys" --page-size 20

# Step 3: High-growth new products (potential threats)
python3 scripts/zoodata.py products --category "Pet Supplies > Dogs > Toys" --listing-age 90d --growth-min 0.2 --page-size 10
```

**Alert Signal Detection**:

Choose comparison evidence by subject: use `market-history` for category-market movement and `history` for ASIN price/BSR/sales movement. A current snapshot can be compared with a compatible saved snapshot or same-scope peer baseline only when the requested dimension has no corresponding history data. Do not infer a change from one current snapshot.

| Alert Type | Detection Method | Trigger Condition |
|------------|-----------------|-------------------|
| New blockbuster invasion | Step 3 results | New product (<90 days) already in Top 20 by sales |
| Price war risk | Step 2 price distribution | Multiple top products clustered at same low price point |
| Concentration shift | Step 1 Top 10 product sales concentration | Investigate only against a comparable prior snapshot or peer baseline with the same category scope and Top 100 selector; no fixed 60% alert. |
| New-product share shift | Step 1 sample new-product share for a matching launch window | Investigate only against a comparable prior snapshot or peer baseline; the former conservative-classification cutoffs do not apply. |

Both rates describe the selected Top 100, not the entire category. Without a compatible baseline, report the current values as context rather than triggering an alert.

**For continuous monitoring:** Use `market-history` for available category month-end comparisons and `history` for product-level daily comparisons. Persist compatible snapshots only for dimensions those history routes do not provide.

## 6.5 Historical Trend Analysis (New Endpoints)

```bash
# Track ASIN price/BSR/sales history
python3 scripts/zoodata.py history --asins B09XXXXX --start-date "<YYYY-MM-DD>" --end-date "<YYYY-MM-DD>"

# Track category-market month-end history
python3 scripts/zoodata.py market-history --category-id "<categoryId>" --date-from "<YYYY-MM-DD>" --date-to "<YYYY-MM-DD>"

# Inspect brand ranking, then select CompetitorBrand from the returned rows
python3 scripts/zoodata.py brand-detail --keyword "dog toys" --page-size 20
```

**Output Template**

```markdown
# Anomaly Alert Report - [Category]

## Alert Signals
| Signal | Level | Description |
|--------|-------|-------------|

## Detailed Analysis
[Each alert signal with specific data]

## Recommended Actions
[Response strategy for each alert]
```
