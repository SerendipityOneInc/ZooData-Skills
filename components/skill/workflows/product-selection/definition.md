# Product Selection & Market Research

## Choose the data source

1. Start with the seller’s figures or files when they cover the question. Analyze those locally, label their source, and skip connector setup. If the seller limits the task to those figures, report only what they support.
2. Fresh Amazon US data comes from ZooData. The configured connector uses a ZooData API Key and charges account credits for paid reads. Keep private costs and supplier quotes in the session.

## Call the selected data tool

For a named category whose children are needed, start with `openapi_v2_categories`. For other requests, use the business tool named in the selected data method (server `{{mcp_server}}`). If tools are deferred, pass that exact business tool name in `ToolSearch.tool_names`, then invoke the match with the method’s parameters. A connector missing from the introductory status list does not establish a connection failure. Apply the [shared query rules](../../../contract/query.md) to the actual lookup or call result.

## Select the task

Choose the route by what the seller wants to rank. For products, keep all category and business filters in one screening scope. For categories, read the [category market method](market-research.md) and compare the requested markets with batched market data. For new-listing counts use `openapi_v2_markets_listing_launch_trend`; for requested product examples use `openapi_v2_markets_top_product_concentrations`. Follow the method’s ranking date and launch window. If the seller wants individual market studies, shortlist the markets first and examine one selected category at a time.

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
