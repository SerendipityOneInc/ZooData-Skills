# Market-entry scoring, sub-market selection, and seller risk gates

Use `totalMonthlyRevenue` for full-category revenue and `top100MonthlyRevenue` only for the selected Top 100. Never calculate revenue from price × sales; see `reference.md § 2` for field definitions.

## Unique Logic

### Sub-Market Discovery
Resolve child nodes with `categories --parent "{path}"`, then call `market --category-id "{id}" --scope subtree --page-size 1` for each candidate. Read the matching `data[0]` row and score each sub-market (1-100) from its fields:

| Dimension | Weight | Field | Good→100 | Bad→0 |
|-----------|--------|-------|----------|-------|
| Demand | 30% | top100MonthlySales | ≥1500 | <200 |
| New Entrant | 25% | top100ConservativeNewProductRate6m | ≥0.20 | <0.05 |
| Brand Openness | 25% | top100Top10BrandSalesRate | ≤0.50 | ≥0.90 (inverted) |
| Capacity | 20% | totalSkuCount | 300-8000 | extreme |

No margin field exists in these market endpoints. Evaluate profit potential only when the seller supplies cost inputs; do not treat A+ content rate as margin.

Present TOP 10 sub-markets. Ask user which to deep-dive (default: top 3). If ≤3 sub-markets, deep-dive all.

### Market Viability Score (1-100)

| Dimension | Weight | Good | Medium | Warning |
|-----------|--------|------|--------|---------|
| Market Size | 15% | >$10M/mo | $5-10M | <$5M |
| Market Trend | 10% | Rising | Stable | Declining |
| Competition | 25% | CR10<40% | 40-60% | >60% |
| Price Opportunity | 15% | oppIndex>1.0 | 0.5-1.0 | <0.5 |
| New Entrant Space | 10% | >15% | 5-15% | <5% |
| Consumer Pain Points | 15% | Clear gaps | Some | None |
| Profit Potential | 10% | >30% | 15-30% | <15% |

### Go/No-Go Decision
| Score | Signal | Action |
|-------|--------|--------|
| 70-100 | ✅ GO | Proceed with product development |
| 40-69 | ⚠️ CAUTION | Possible but needs differentiation |
| 0-39 | 🔴 AVOID | Too competitive or too small |

**CR10 dual-level check**: Category CR10 PASS + sub-market CR10 FAIL → ⚠️ CAUTION. Both FAIL → AVOID.
**User criteria override**: If user sets thresholds, ANY fail → CAUTION/AVOID. Never override.

### Small-Seller Entry Risk Gates
Before upgrading a market to GO, run these gates against the user's budget, operating constraints, and risk tolerance:

| Gate | Pass Signal | Hard-Block Signal |
|------|-------------|-------------------|
| Capital fit | First order, launch PPC, storage, and cash cycle fit available runway | MOQ, inventory, or ad spend requires more cash than the seller can safely hold |
| Review barrier | Top competitors' review counts, ratings, and review velocity are reachable with a realistic launch plan | Conversion depends on matching an entrenched review moat |
| Compliance/IP risk | Certifications, restricted claims, safety rules, and trademark/design risks are known and manageable | Unresolved compliance, patent, trademark, or restricted-product exposure |
| Differentiation evidence | Clear pain point, feature, bundle, content, or price-band wedge | Only commodity resale, copycat design, or no defendable reason to buy |
| Validation speed | Demand and positioning can be tested in 7-30 days with samples or lightweight listings | Proof requires tooling, a full PO, or a large irreversible launch |

Decision adjustment (precedence is pinned — apply in order):

1. **Final verdict formula**: `final = MIN(score_tier, lowest_gate_tier)` where the tier ordering is `GO > CAUTION > AVOID`. A score-90 GO with one gate at AVOID → final AVOID; a score-90 GO with one gate at CAUTION → final CAUTION.
2. **GO** requires BOTH a passing viability score AND every gate in PASS (or with a documented mitigation plan in the same workflow turn).
3. **CAUTION** fits markets with 1–2 uncertain gates that can plausibly be validated inside the **Validation Speed** window (7–30 days, sampled or lightweight listing).
4. **AVOID is mandatory** when any of {Compliance/IP, Capital fit, Review barrier} is a hard-block — regardless of viability score. These three categories are non-negotiable for small sellers.
5. **Relationship to "User criteria override" above**: that rule remains authoritative — if the user sets explicit thresholds (e.g. "min monthly sales 500", "max CR10 50%"), those override even gates. The Gates fire as the default backstop when no user-set thresholds cover the same dimension.
6. Tag each gate conclusion with the required confidence label (`📊`, `🔍`, or `💡`) — never treat the gate table itself as data-backed.
