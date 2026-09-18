# Discover Markets and Product Candidates

This scenario owns open-ended market exploration and category-scoped product opportunity discovery. Apply the guide's stage and Gate contract, shared evidence procedures, metric semantics, and canonical output rules; this file does not define independent API or report contracts.

## Scenario boundary

Use this route when the user has not chosen a market, asks which niches are worth investigating, or asks for products to examine within an identified category. The result is an observed validation shortlist, not a seller-specific entry verdict, profit projection, or claim that the entire catalog was scanned.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| Market landscape | User's scope or broad product interest, marketplace, and any stated filters | Bounded `market` discovery pages; `categories` when a parent/child structure is named | Rank only observed category markets for further evaluation; no product winner or GO/AVOID verdict. |
| Product candidate validation | Resolved category ID/path plus explicit request for products, seller profile or numeric constraints when supplied | Category-locked `products` modes/filters; compatible `market` snapshot; `product`, `brand-*`, `price-band-*`, or `history` only for a named candidate question | Rank observed ASINs by documented demand/barrier/fit signals as validation priorities; no measured margin or guaranteed opportunity. |

The second row can be entered directly when the user already names a category. An earlier market shortlist does not automatically authorize product calls.

## Market landscape application

- Choose a bounded search from the user's stated parent category, marketplace, filters, and credit limit. `categories --parent` enumerates children when a parent is known; `market --scope subtree` with explicit filters/pages discovers market rows. Do not paginate the global catalog by default.
- Preserve `meta.total`, page range, sort direction, and exact observed category set. Use returned `categoryId` to avoid merging same-name categories from different paths.
- Rank observed categories by the user's declared priorities. Without priorities, present demand (`totalMonthlySales` or `totalMonthlyRevenue`), selected Top 100 concentration, conservative new-product share, and price distribution as separate axes; do not collapse them into an unexplained 1–100 score.
- A high market size and low selected-sample concentration may support a category for closer evaluation. It does not establish capital fit, differentiated demand, or product profitability.

## Product candidate application

- Lock the category path before keyword-based `products` or `competitors` calls. When the path was inferred from a top product, expose that inference and require confirmation before a seller-specific priority claim.
- Translate an explicit price, sales, or review-count constraint to CLI filters. A `--mode` preset supplies local filters and can stack with user filters; inspect actual `_query.params` and do not call a mode name an API field.
- For an explicitly requested full multi-mode scan, `opportunity-scan` may gather product, real-time, brand, price, history, and review evidence in one call. State that its fan-out is materially larger than a two-mode granular screen; use the granular `products` route for a bounded quick scan.
- Deduplicate ASINs across modes/pages. Keep product lower-bound sales, observed price, rating count, listing age, and category-market context separate. Use `product` for current listing detail, not database sales.
- State which user criteria each candidate meets or fails. If economics or compliance inputs are missing, label the candidate a validation priority, never a profitable winner.

## Section content requirements

Inside the shared report template, show the observed category or product rows with exact identity, requested filters, coverage, and principal metrics in `Evidence`; explain tradeoffs and sample bias in `Analysis`; give a bounded shortlist and the specific next validation question in `Conclusion`. A chosen category may be offered as an evaluation continuation only when that question remains relevant to the user.
