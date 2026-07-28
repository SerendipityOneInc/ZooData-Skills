# Amazon Seller Comprehensive Analysis & Case Studies

> Amazon product recommendation workflows and real-world FBA/FBM seller case studies.
> Load when handling comprehensive product recommendations or seller origin case studies.
> For API parameters, see `reference.md`.
>
> ⚠️ **Always resolve categoryPath before running these queries.** Tag conclusions with 📊/🔍/💡 confidence labels.

---

## 2.10 Composite Product Recommendation (Comprehensive Decision Recommendations)

> Trigger: "help me choose" / "comprehensive recommendations" / "what should I sell" / "most suitable for me"

**First collect user information (if not provided, proactively ask):**

| Element | Example |
|------|------|
| Target category | "Pet supplies" |
| Budget range | < $10K / $10-50K / > $50K |
| Experience level | Beginner / Experienced / Expert |
| Preferences | Small & light items / High-ticket items / Fast turnover |

**Workflow**

```bash
# Step 1: Confirm category
python3 scripts/zoodata.py categories --keyword "pet toys"

# Step 2: Market conditions
python3 scripts/zoodata.py market --category "Pet Supplies > Dogs > Toys" --topn 10

# Step 3: Run 2-3 modes based on user profile
# Beginner → beginner + high-demand-low-barrier
python3 scripts/zoodata.py products --keyword "pet toys" --mode beginner --page-size 20
python3 scripts/zoodata.py products --keyword "pet toys" --mode high-demand-low-barrier --page-size 20

# Step 4: Brand landscape check
python3 scripts/zoodata.py brand-overview --keyword "pet toys"

# Step 5: Price band opportunity scan
python3 scripts/zoodata.py price-band-overview --keyword "pet toys"

# Step 6: AI weighted scoring → Top 5 recommendation
```

**AI Weighted Scoring Dimensions**:

| Dimension | Weight | Field | Source Interface |
|------|------|---------|---------|
| Demand Strength | 25% | `monthlySalesFloor` | `products` / `competitors` |
| Competition Difficulty | 25% | `ratingCount` + `sellerCount` | `products` / `competitors` |
| Differentiation Opportunity | 15% | `rating` < 4.3 or `ratingCount` < 200 | `products` / `competitors` |
| User Match | 15% | Budget/Experience/Preferences | User input |

**⚠️ All scoring fields come from `products`/`competitors` interface. Do NOT use `realtime/product` for scoring — it lacks sales and sellerCount.**

**Output Template**

```markdown
# 🎯 [Category] Comprehensive Product Selection Recommendations

## User Profile
| Item | Value |
|----|-----|
| Budget | ... |
| Experience | ... |
| Preferences | ... |

## Top 5 Recommended Products
| # | ASIN | Product | Price | Monthly Sales | Reviews | Comprehensive Score | Recommendation Reason |
|---|------|------|------|-------|-------|---------|---------|

## Action Recommendations
[Specific recommendations based on user profile]
```

---

## 3.4 Seller Origin Case Study (by country code)

> Trigger: "Are there Chinese sellers who succeeded" / "sellers from a specific country" / "seller origin analysis"

```bash
python3 scripts/zoodata.py competitors --keyword "wireless earbuds" --page-size 50
# → Filter results by the buyBoxSellerCountryCode field
```

**Origin filtering — use the `buyBoxSellerCountryCode` field only**:
- Filter by the reported `buyBoxSellerCountryCode` (e.g. `CN` for China-based sellers). This is the only reliable origin signal.
- Sort qualifying sellers by `monthlySalesFloor` to find the top performers by sales volume.

**⚠️ When `buyBoxSellerCountryCode` is null** (common — many ASINs lack it):
- Do NOT infer a seller's country from names, brand text, spelling/pinyin, name suffixes, or product category — those are unreliable and biased proxies.
- Report only the sellers whose country code is present, and state the coverage explicitly (e.g. "origin known for 12/50 results; the rest are unclassified"). Never present an inferred origin as fact.

**Analysis Dimensions** (over sellers with a known country code):
- Count and ratio of sellers from the target country vs. the classified total
- Common traits of the top performers (price range, review count, listing age)
- Listing strategies of the top performers (use `product --asin XXX` for details)
- Replicable strategy points

**Output Template**

```markdown
# [Category] Seller Origin Case Analysis

## Origin Coverage
| Metric | Value |
|-----|------|
| Country code known | X / Total Y (Z% coverage) |
| Sellers from [country] | X |
| Top [country] seller average monthly sales | X units |
| Top [country] seller average price | $X |

## Top 5 [country] Seller Products
| # | ASIN | Brand | Price | Monthly Sales | Rating | Reviews | Listing Date |
|---|------|------|------|-------|------|------|---------|

## Success Strategy Analysis
[Common traits + replicable strategies, over sellers with a known country code]

## Action Recommendations
[Recommendations grounded in observed data; note origin-coverage limits]
```

---

## 3.5 Full Market Cross-Validation (All Endpoints)

> Trigger: "full picture" / "cross-validate" / "comprehensive market analysis"

```bash
# Step 1: Category resolution
python3 scripts/zoodata.py categories --keyword "yoga mat"

# Step 2: Market aggregate
python3 scripts/zoodata.py market --category "Sports & Outdoors > Exercise & Fitness > Yoga > Yoga Mats" --topn 10

# Step 3: Product landscape
python3 scripts/zoodata.py products --keyword "yoga mat" --category "Sports & Outdoors > Exercise & Fitness > Yoga > Yoga Mats" --page-size 30

# Step 4: Price band analysis
python3 scripts/zoodata.py price-band-overview --keyword "yoga mat"
python3 scripts/zoodata.py price-band-detail --keyword "yoga mat" --price-min 20 --price-max 40

# Step 5: Brand landscape
python3 scripts/zoodata.py brand-overview --keyword "yoga mat"
python3 scripts/zoodata.py brand-detail --keyword "yoga mat" --brand "TopBrand"

# Step 6: Realtime deep dive on top ASINs
python3 scripts/zoodata.py product --asin B09XXXXX

# Step 7: Historical validation
python3 scripts/zoodata.py history --asin B09XXXXX --period 90d

# Step 8: Consumer insights
python3 scripts/zoodata.py analyze --category "Sports & Outdoors > Exercise & Fitness > Yoga > Yoga Mats" --period 90d
```

**Cross-validation checks:**
- Market avg price vs price-band distribution (consistency check)
- Brand concentration from `market` vs `brand-overview` (should align)
- Top products from `products` should appear in best price band from `price-band-detail`
- Historical trend from `history` should support growth claims from `products`
