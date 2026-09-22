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

- For a named parent category, the comparison population is every direct child that remains eligible under the user's explicit hard filters. Category-tree order and an arbitrary preselected subset cannot support a parent-wide ranking. Acquire and validate that population through `reference.md` and `evidence-protocols.md` before selecting the requested number of candidates.
- A parent-wide top K requires complete compatible coverage of that eligible child population. When the call boundary prevents complete coverage, return a bounded shortlist from the observed set and identify the uncovered children; do not label it the parent's overall top K.
- Without a named parent, define a bounded catalog discovery set and keep the conclusion within the validated rows. Preserve distinct category identities and avoid combining overlapping parent and child market totals according to the evidence protocol.
- Rank observed categories by the user's declared priorities. Without priorities, present full-category demand, selected Top 100 product and brand concentration, new-product activity for an identified window, and price distribution as separate axes; use `market-metric-semantics.md` for their metric identity. Do not collapse them into an unexplained 1–100 score or apply undocumented new-product thresholds.
- A high market size and low selected-sample concentration may support a category for closer evaluation. It does not establish capital fit, differentiated demand, or product profitability.

## Product candidate application

- Require a resolved category identity before candidate ranking. If it was inferred from a product, expose that inference before making a seller-specific priority claim.
- Honor the user's price, sales, review-count, and seller-fit constraints through the documented category-locked product capabilities. Choose a bounded granular screen or an explicitly requested composite scan through the Interface and Cost Gate.
- Validate and deduplicate the observed candidate set through `evidence-protocols.md`. Keep each product observation and its compatible category-market context as separate evidence families.
- State which user criteria each candidate meets or fails. If economics or compliance inputs are missing, label the candidate a validation priority, never a profitable winner.

## Section content requirements

Inside the shared report template, show the observed category or product rows with exact identity, requested filters, coverage, and principal metrics in `Evidence`; explain tradeoffs and sample bias in `Analysis`; give a bounded shortlist and its material evidence gaps in `Conclusion`. A chosen category can support an evaluation continuation only when the remaining question is relevant to the user; render any selectable question through the guide-owned final list.
