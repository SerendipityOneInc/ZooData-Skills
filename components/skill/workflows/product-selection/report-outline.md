# Selection report outline

| Task | Reading order |
|---|---|
| `screening` | Give the effective filters, scope, selected ordering and result coverage once. For an overall Top N, present one ordered product list using the shared product template. Show category as an attribute when useful. For leaders requested per category, present a separate ordered group for each category. Show a shared value once and keep ties visible. |
| `market-research` | Identify the category and answer the requested market question. Show the relevant distribution for a focused question, or market indicators and the seller’s stated thresholds for an entry question. |
| `new-launches` | Show the category comparison first, then a section per selected listing, identified by parent and representative ASIN. Apply the [product trend panels](../../../tools/report/product-trends.md) for monthly sales, daily price, weekly exposure and both daily ranks. |
| `market-growth` | Lead with which markets grew, their monthly unit sales for the two months compared, absolute and percentage change. Use the longer history to describe persistence. When examples are requested, group the leading markets’ representative listings in a single compact product list. Use the parent template for parent-ranked listings and the child template for identified variants. |
| `assessment` | Identify products by name and available ASIN, with the observed period. Lead with how the product developed, then use the [product trend panels](../../../tools/report/product-trends.md) for the supporting changes. Mark meaningful turning points and how long the new level held. For a focused question show only its measures. For multiple candidates compare like measures in one report and show which stated thresholds each meets. In an expert session, place the expert’s decision and decisive constraint together in this report. |

For `new-launches` report JSON, set `parentAsin` on each product section and include it in its title. Tag each trend block with its `measure`: `sales`, `price`, `exposure`, `bsr`, or `subBsr`. Use charts for a series and a tagged text block for a single observation or unavailable measure. With fewer than three products, set `productCoverageNote` to one reader-facing sentence explaining the shortfall; the renderer displays it.

When a candidate table includes cumulative rating count, place the signed change in rating count for the comparison period beside it. In screening, use the returned 30-day change. Retain negative changes as decreases. Explain a cause only when observations directly connect it to that product’s change. Keep individual products and values in the table.

For zero matches, report the confirmed scope and zero results; omit empty sections. Present one HTML file. The shared report rules govern its handoff.
