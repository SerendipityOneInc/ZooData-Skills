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

- When a parent category is named, resolve its path and use one `categories --parent '["Root", "Parent, With Comma"]'` call to enumerate **all direct child IDs**. `--parent` requires a nonempty JSON string array; never construct it by joining names with commas or pass a free-form path string. An ambiguous value must fail locally before the API call and be rebuilt from the resolved path, without user involvement or credit use. Preserve the complete returned `data[]` locally, then query all child IDs together with one `market --category-ids ID1,ID2,... --page-size 100` call when there are at most 100 IDs. The ID list selects market rows; the default product inclusion setting also counts each row's descendant-category products. Category-tree order, name, and `productCount` are not market rankings. Never preselect an arbitrary K children before reading their market measures.
- For a parent-wide demand and concentration shortlist, obtain a compatible market row for **every** enumerated child eligible under any explicit hard filters before ranking, then return at most the user's requested K candidates. Read all pages and, when there are more than 100 child IDs, batch them within the call limit and merge by exact `categoryId`. For at most 100 direct children, the normal acquisition cost is exactly one `categories` call plus one `markets/search` call; transcript folding or local projection never justifies repeating either call. Hard filters apply before pagination; `meta.total` then counts eligible markets **within that ID batch**, not all children. Treat preferred ranking axes such as demand and concentration as comparison measures, not implicit filters that hide tradeoffs. If the call limit prevents complete coverage, report only the observed set and its missing IDs, not a parent-wide top K.
- When no parent is named, a bounded `market` filter/page search can discover category rows across the catalog. Preserve `meta.total`, page range, sort direction, and exact observed category set. For parent-scoped discovery, report enumerated child count, returned rows, and unreturned child IDs; when filters were applied, do not assume an unreturned ID lacks a snapshot. Use returned `categoryId` to avoid merging same-name categories from different paths; compare only matching dates, product inclusion settings, and sample selectors. Do not sum overlapping parent and child market totals.
- Rank observed categories by the user's declared priorities. Without priorities, present demand (`totalMonthlySales` or `totalMonthlyRevenue`), selected Top 100 concentration, `sampleNewProductRate6m`, and price distribution as separate axes; do not collapse them into an unexplained 1–100 score or apply former conservative-new-product thresholds.
- A high market size and low selected-sample concentration may support a category for closer evaluation. It does not establish capital fit, differentiated demand, or product profitability.

## Product candidate application

- Lock the category path before keyword-based `products` or `competitors` calls. When the path was inferred from a top product, expose that inference and require confirmation before a seller-specific priority claim.
- Translate an explicit price, sales, or review-count constraint to CLI filters. A `--mode` preset supplies local filters and can stack with user filters; inspect actual `_query.params` and do not call a mode name an API field.
- For an explicitly requested full multi-mode scan, `opportunity-scan` may gather product, real-time, brand, price, history, and review evidence in one call. State that its fan-out is materially larger than a two-mode granular screen; use the granular `products` route for a bounded quick scan.
- Deduplicate ASINs across modes/pages. Keep product lower-bound sales, observed price, rating count, listing age, and category-market context separate. Use `product` for current listing detail, not database sales.
- State which user criteria each candidate meets or fails. If economics or compliance inputs are missing, label the candidate a validation priority, never a profitable winner.

## Section content requirements

Inside the shared report template, show the observed category or product rows with exact identity, requested filters, coverage, and principal metrics in `Evidence`; explain tradeoffs and sample bias in `Analysis`; give a bounded shortlist and its material evidence gaps in `Conclusion`. A chosen category can support an evaluation continuation only when the remaining question is relevant to the user; render any selectable question through the guide-owned final list.
