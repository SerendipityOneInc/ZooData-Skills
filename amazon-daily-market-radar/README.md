# Amazon Daily Market Radar — ZooData Agent Skill

> Set it. Forget it. Get alerted when it matters.

## What This Skill Does

Automated daily monitoring and alert system for Amazon sellers. Tracks your ASINs and competitors, detects price changes, BSR movements, new entrants, review spikes, and stock-out signals. First run establishes a baseline; subsequent runs compare against it and fire tiered alerts. Designed for unattended agent automation.

### What Makes This Different

- **Set-and-forget**: First run = baseline, every run after = smart change detection
- **Three-tier alerts**: 🔴 RED (price crash, BSR collapse, 1-star spike), 🟡 YELLOW (new competitors, moderate shifts), 🟢 GREEN (opportunities like competitor stock-outs)
- **Signal validation**: Distinguishes sustained trends (📊 7+ days) from single-day spikes (💡)
- **Cron-ready**: Built for scheduled execution with auto-monitor setup

## Install

```bash
npx skills add SerendipityOneInc/ZooData-Skills
```

Select **Amazon Daily Market Radar** when prompted.

## API Key Setup

1. Get a free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys) — 1,000 free credits, no credit card
2. Set the environment variable:
   ```bash
   export ZOODATA_API_KEY='hms_live_xxxxxx'
   ```

## Data & Privacy

- Each run sends your tracked ASINs, competitor ASINs, keywords, category paths, and marketplace/date/numeric filters to the ZooData API (`api.zoodata.ai`). Because this skill is designed for scheduled, unattended execution, that transmission recurs on every scheduled run.
- Nothing else is transmitted: no budget, seller-account, or free-text profile data leaves your machine.
- Local state: `watchlist.json` and the `last-run.json` baseline under the skill's `data/` folder persist between runs for day-over-day comparison. Delete the folder anytime to reset monitoring and remove the retained data.
- Baselines and scheduled runs are only established on your explicit request — never from a vague or merely related question — and recurring monitoring always requires your explicit opt-in. Every API call consumes account credits.

## Example Prompts

The skill activates on explicit monitoring requests like these — it does not
self-trigger on vague update questions, and recurring monitoring always
requires your explicit opt-in:

- *"Set up daily market monitoring for my ASINs: B0XXXXXXXX, B0YYYYYYYY"*
- *"Set up daily market monitoring for keyword 'yoga mat', track these 3 ASINs"*
- *"Run my daily market radar — what changed since yesterday?"*
- *"Run a daily radar check on my tracked products"*
- *"Run the daily radar and report competitor changes"*

## What You Get

| Section | Description |
|---------|-------------|
| 🚨 Alert Summary | RED / YELLOW / GREEN alert counts |
| 🔴 RED Alerts | Critical changes requiring immediate action |
| 🟡 YELLOW Alerts | Watch-worthy shifts in competitors or market |
| 🟢 GREEN Opportunities | Favorable changes to capitalize on |
| 📊 KPI Dashboard | Today vs yesterday comparison |
| 🏃 Competitor Movement | Price, BSR, listing changes per competitor |
| 🌊 Market Shifts | Brand share, new entrants, price band migration |
| ✅ Action Items | Prioritized next steps |

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `categories` | Category resolution |
| `markets/search` | Market-level metrics |
| `products/search` | Product landscape |
| `products/competitors` | Competitor discovery |
| `realtime/product` | Live ASIN polling |
| `reviews/analysis` | Review spike detection |
| `products/price-band-overview` | Price band shifts |
| `products/price-band-detail` | Detailed price analysis |
| `products/brand-overview` | Brand share changes |
| `products/brand-detail` | Per-brand tracking |
| `products/history` | Trend validation |

## Credit Cost

~15-30 credits per run (depends on number of tracked ASINs).

## Powered By

[ZooData](https://zoodata.ai) — The data infrastructure built for agents. 200M+ Amazon products, 1B+ reviews, real-time signals.
