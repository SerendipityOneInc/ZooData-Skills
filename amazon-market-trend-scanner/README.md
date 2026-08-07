# Amazon Market Trend Scanner — ZooData Agent Skill

> Find rising categories before everyone else.

## What This Skill Does

Scans Amazon category landscapes to discover trending subcategories, emerging niches, and market shifts. Give it a parent category and it analyzes all subcategories for demand surges, brand consolidation, new entrant waves, price band migration, and margin changes. Complements Daily Market Radar (defensive monitoring) with offensive trend discovery for product selection and market entry timing.

### What Makes This Different

- **Category-level trends**: Analyzes across ALL subcategories under a parent, not just individual products
- **7 key metrics per subcategory**: Sales, new SKU rate, brand concentration, avg price, gross margin, total SKUs, FBA rate
- **Trend signals**: Demand surge 🔴, red ocean warning 🔴, new entrant wave 🟡, brand loosening 🟡, price/margin shifts 🟡
- **Dual mode**: Full Scan for discovery, Quick Check for scheduled monitoring with auto-alerts
- **Emerging product detection**: Scans hot subcategories for emerging and new-release products

## Install

```bash
npx skills add SerendipityOneInc/ZooData-Skills
```

Select **Amazon Market Trend Scanner** when prompted.

## API Key Setup

1. Get a free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys) — 1,000 free credits, no credit card
2. Set the environment variable:
   ```bash
   export ZOODATA_API_KEY='hms_live_xxxxxx'
   ```

## Data & Privacy

- Each scan sends your category names, keywords, and marketplace/date/numeric filters to the ZooData API (`api.zoodata.ai`). With scheduled Quick Check monitoring enabled, this happens on a recurring, unattended basis.
- Nothing else is transmitted: no budget, seller-account, or free-text profile data leaves your machine.
- Local state: `baseline.json`, `watchlist.json`, `alerts.json`, and `history/` snapshots under the skill's `scan-data/` folder persist between runs solely for trend comparison. Delete the folder (or prune old `history/` files) anytime to reset and remove the retained data.
- Scheduled monitoring is opt-in — the skill asks for explicit confirmation before enabling recurring runs. Every API call consumes account credits.

## Example Prompts

- *"Scan Pet Supplies for trending subcategories"*
- *"Which categories are growing? Scan Home & Kitchen"*
- *"Which subcategories under Sports & Outdoors are growing fastest?"*
- *"Run a category trend scan and show me which niches are gaining momentum"*
- *"Find emerging niches in Beauty & Personal Care"*

## What You Get

| Section | Description |
|---------|-------------|
| 📊 Trend Dashboard | All subcategories with 7 key metrics |
| 🔥 Hot Categories TOP 5 | Fastest-growing subcategories ranked |
| 🆕 New Entrants Scan | Emerging and new-release products in hot categories |
| ⚠️ Risk Alerts | Red ocean warnings, demand surges, margin compression |
| 📋 Subcategory Detail | Deep dive per hot category |
| 🎯 Next Steps | Market entry timing and strategy |

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `categories` | Category tree resolution |
| `markets/search` | Subcategory-level market metrics (paginated) |
| `products/search` | Emerging and new-release product scanning |

## Credit Cost

Full Scan: ~40-60 credits (~2-3 per subcategory × 20). Quick Check: ~20-30 credits.

## Powered By

[ZooData](https://zoodata.ai) — The data infrastructure built for agents. 200M+ Amazon products, 1B+ reviews, real-time signals.
