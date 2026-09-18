# Seller Input and Economics Semantics

This module owns the identity and interpretation limits of seller-provided capital, cost, operating, and compliance inputs. The evaluation scenario chooses whether those inputs are needed; this module does not issue the entry verdict.

## Input identity

For each supplied number, preserve currency, marketplace, unit, time horizon, and whether it is a quote, estimate, or actual result. Keep seller inputs distinct from ZooData observations. Budget is deployable capital only if the seller says so; experience and risk tolerance are qualitative constraints, not numeric API filters.

| Input | Meaning to preserve | Missing-input boundary |
|---|---|---|
| Capital and cash runway | Cash available for first order, freight, launch ads, storage, returns, and replenishment cycle | A listed budget without committed costs does not establish capital fit |
| COGS and landed cost | Per-unit manufacturing plus freight, duty, packaging, and other seller-confirmed landed components | Product price or category median is not COGS |
| Selling price and fees | Intended net selling price, referral fee, fulfillment fee, storage, and other known marketplace charges | An API price observation alone is not the seller's realizable net price |
| Acquisition and return cost | Expected ads, promotions, returns, and allowances per unit or a justified scenario range | Missing cost cannot silently be set to zero |
| Compliance and IP status | Seller-provided documents, known restrictions, certifications, claims, trademark/patent/design review status | API data and a seller's unverified assertion do not constitute legal clearance |

## Calculation boundaries

When enough compatible per-unit inputs exist, show `contribution per unit = net realized price − landed cost − marketplace/fulfillment fees − acquisition and expected return costs`. Show every included component and mark omitted material costs. `contribution margin = contribution per unit ÷ net realized price` only when that denominator is positive and all included costs use the same unit/currency. A scenario range is preferable to a point estimate when ads or returns are uncertain. Do not compute or claim profit from market `totalMonthlyRevenue`, `sampleMedianPrice`, or A+ content rate.

## Risk evidence

Seller capital and risk tolerance can bound a conditional entry verdict. A known unresolved compliance/IP hard block can prevent a GO claim; neither this skill nor ZooData API can certify legality. A weak review position or uncertain differentiation is an observed validation burden, not proof of failure. Document assumptions and unresolved items instead of filling them with benchmark guesses.
