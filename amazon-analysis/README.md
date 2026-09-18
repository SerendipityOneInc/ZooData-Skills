# Amazon Analysis — Full-Spectrum Research & Seller Intelligence

> 13 product selection strategies. One skill to rule them all.

## What This Skill Does

The Swiss Army knife of Amazon product research. Supports 13 built-in selection modes — from fast-movers and emerging products to long-tail niches and FBM-friendly picks. Combines market research, product selection, competitor analysis, ASIN evaluation, pricing reference, and category research into a single unified workflow.

### What Makes This Different

- **13 selection modes**: fast-movers, emerging, single-variant, high-demand-low-barrier, long-tail, underserved, new-release, fbm-friendly, low-price, broad-catalog, selective-catalog, speculative, top-bsr
- **Composite commands**: `report` and `opportunity` run multi-endpoint pipelines in one shot
- **Flexible filtering**: Modes stack with explicit filters (`--price-max`, `--sales-min`, etc.)
- **Confidence tagging**: Every data point tagged as 📊 Data-backed, 🔍 Inferred, or 💡 Directional

## Install

```bash
npx skills add SerendipityOneInc/ZooData-Skills
```

Select **Amazon Analysis** when prompted.

## API Key Setup

1. Get a free key at [zoodata.ai/api-keys](https://zoodata.ai/en/api-keys) — 1,000 free credits, no credit card
2. Set the environment variable:
   ```bash
   export ZOODATA_API_KEY='hms_live_xxxxxx'
   ```

## Example Prompts

- *"Analyze the yoga mat market on Amazon"*
- *"Use the emerging mode to find products in the $15-30 range"*
- *"Find beginner-friendly products in kitchen gadgets under $25"*
- *"Run a full report on keyword 'silicone spatula'"*
- *"Use the underserved mode to find improvable products rated below 3.7"*

## What You Get

| Section | Description |
|---------|-------------|
| 📊 Analysis Findings | Market overview, selection results, key insights |
| 🏆 Top Products | Ranked candidates with scores and mode tags |
| 🔍 ASIN Deep Dive | Real-time data for top candidates |
| 📋 Data Source & Conditions | Endpoints used, category, date range, filters |
| ⚠️ Data Notes | Estimated values, T+1 delay, sampling basis |

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `categories` | Lock category path before analysis |
| `markets/search` | Market-level metrics and context |
| `products/search` | Product scanning with 20+ filter fields (13 CLI presets) |
| `products/competitors` | Competitive landscape |
| `realtime/product` | Live ASIN validation |
| `reviews/analysis` | Consumer pain points and sentiment |
| `products/price-band-overview` | Price band opportunity |
| `products/price-band-detail` | Detailed price distribution |
| `products/brand-overview` | Brand concentration (CR10) |
| `products/brand-detail` | Per-brand breakdown |
| `products/history` | 30-day trend analysis |

## Credit Cost

Varies by workflow. `report` composite: ~15-20 credits. `opportunity` composite: ~20-30 credits.

## Powered By

[ZooData](https://zoodata.ai) — The data infrastructure built for agents. 200M+ Amazon products, 1B+ reviews, real-time signals.
