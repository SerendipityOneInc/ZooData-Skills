# Competitor Insight Research

Analyze the seller’s own ASIN, a competitor ASIN or a specified set of products. Select one task based on the seller's question. Use the marketplace, selected products, dates and budget already given.

| What the seller wants to know | Task and result |
|---|---|
| How is this product positioned, and how is it performing? | Profile the one named ASIN. Explain its selling points and price, recent sales trend, traffic sources and buyer feedback. |
| How did purchases change in the last three complete months for these US products? | Show each selected product’s monthly purchase lower bound for the same three months. |
| What changed recently for this product? | Check the named ASIN over the requested period and report dated changes to its title, main image and price. |
| Which products compete with mine? | Use the target ASIN or product brief and confirmed search scope. Deliver comparable ASINs and why each belongs. |
| How do these competitors compare overall? | Compare their specifications, commercial performance, traffic and changes over time. Include buyer feedback for an expressly deep comparison. |
| How do these products differ on one measure? | Compare only the named measure over the requested period, such as monthly revenue or price history. |
| What could distinguish my product? | Compare the target and competitors on the relevant product features, page information and buyer experience. |

1. For supplied observations, use the seller’s product labels, units and dates. A focused comparison of two identified offers can use those labels without an ASIN lookup. For fresh Amazon US data, use the selected ASINs and the ZooData connection. If a required read is unavailable, explain which observations the seller can supply to complete that comparison.
2. When the question is limited to purchases over the last three complete months on Amazon US, read and follow [Compare monthly purchases](monthly-purchases.md). For dated changes to the title, main image or price of a named ASIN, go directly to [product history](../../datas/product-history/definition.md). For other tasks with missing measures use the [comparison methods](methods.md) to select the data Skill for each missing measure. Follow its bundled instructions and reuse the result.
3. Apply the [evidence rules](../../../contract/evidence.md). Before acquiring data, follow the [MCP rules](../../../contract/query.md).
4. Assemble the findings in the [task outline](report-outline.md) and apply the [presentation rules](../../../contract/report.md). In a standalone session, use the [HTML report guide](../../../tools/report/definition.md) to generate one report. In an expert session, pass the same findings and outline to the expert for a single final render. Honor an explicit request for another format.
