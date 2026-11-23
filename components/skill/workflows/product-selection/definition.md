# Product Selection & Market Research

## Choose the data source

1. Start with the seller’s figures or files when they cover the question. Analyze those locally, label their source, and skip connector setup. If the seller limits the task to those figures, report only what they support.
2. Fresh Amazon US data comes from ZooData. Before the first fresh read, make sure the seller knows a ZooData API Key is entered in the connector and queries use account credits. Keep private costs and supplier quotes in the session.

## Call the selected data tool

1. Use the full WorkBuddy tool name printed in the selected data method. If deferred, load it with `ToolSearch.tool_names` and invoke only an exact match. Skip keyword searches and plugin inventories.
2. If the exact name is missing, request the `{{mcp_server}}` MCP connection once. After connection succeeds, look up the same name once more. If it remains unavailable, stop that read. Keep this process internal unless the user needs to connect or authorize ZooData.

3. For blocked or empty reads follow the [shared query rules](../../../contract/query.md).

## Select the task

For new listings among category bestsellers, read the [category market method](market-research.md) before querying. Use the market tools with the confirmed category IDs in a batch. Establish each category’s sales-ranked sample before evaluating launch dates.

| Seller request | Route | Result |
|---|---|---|
| The seller’s goal is unclear | Ask what selection decision the seller wants to make | Ask one focused question. If the seller asks how to phrase a request, illustrate it with a relevant example. |
| Research or compare category demand, prices, competition, buyer needs or entry | [Research a category market](market-research.md) | Answer the requested market question, adding examples where needed. |
| Compare the number of new listings among category sales leaders | [Research a category market](market-research.md) | Use `market-research` for counts and category ranking. |
| Compare new-listing counts and examine how the leading new products developed | [New listings and product trends](market-research.md) | Use `new-launches` for counts and trends for the three highest-selling identified new listings. |
| Find categories with growing sales | [Compare growing markets](market-research.md) | Rank peer categories by whole-market sales growth. Include representative products when requested. |
| Find products under the seller’s conditions, including bestsellers ranked by purchase volume | [Screen candidates](screening.md) | One ranked candidate sample under the confirmed conditions. |
| Assess named candidates: how did each product grow and how does it compare with the stated thresholds? | [Assess candidates](methods.md) | One assessment of the product’s development, covering the full picture or just the requested measures. |

Reuse matching evidence and apply the [query](../../../contract/query.md), [evidence](../../../contract/evidence.md) and, for private operating figures, [seller-data rules](../../../contract/seller-evidence.md). For research tasks, assemble the [task outline](report-outline.md). Independently, generate the HTML with the [report guide](../../../tools/report/definition.md). In an expert session give the findings to the expert for one render. Follow the [file handoff](../../../contract/report.md) or the format the seller explicitly requests.
