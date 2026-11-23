# Product Selection & Market Research

## Step 1: Identify what the seller is selecting first

1. **Market first.** When the seller asks which subcategories are growing, admit more new listings or merit entry, follow the [category market method](market-research.md). Compare peers in batches and use market evidence to select the scope before reading products from it.
2. **Product first.** When the seller asks which products to find or assess, treat categories, price, launch date and other filters as one product population. Screen or assess within that scope. A named category alone does not call for a market comparison.
3. Use the route established by the question and context. Ask which decision comes first only when both interpretations remain plausible and change the unit of analysis.

| Seller request | Route | Result |
|---|---|---|
| The seller’s goal is unclear | Ask what selection decision the seller wants to make | Ask one focused question. If the seller asks how to phrase a request, illustrate it with a relevant example. |
| Research or compare category demand, prices, competition, buyer needs or entry | [Research a category market](market-research.md) | Answer the requested market question, adding examples where needed. |
| Compare the number of new listings among category sales leaders | [Research a category market](market-research.md) | Use `market-research` for counts and category ranking. |
| Compare new-listing counts and examine how the leading new products developed | [New listings and product trends](market-research.md) | Use `new-launches` for market counts and trends for the three highest-selling identified new listings in the selected market. |
| Find categories with growing sales | [Compare growing markets](market-research.md) | Rank peer categories by whole-market sales growth. Include representative products when requested. |
| Find products under the seller’s conditions, including bestsellers ranked by purchase volume | [Screen candidates](screening.md) | One ranked candidate sample under the confirmed conditions. |
| Assess named candidates: how did each product grow and how does it compare with the stated thresholds? | [Assess candidates](methods.md) | One assessment of the product’s development, covering the full picture or just the requested measures. |

## Choose the data source

1. Start with the seller’s figures or files when they cover the question. Analyze those locally, label their source, and skip connector setup. If the seller limits the task to those figures, report only what they support.
2. Fresh Amazon US data comes from ZooData. The configured connector uses a ZooData API Key and charges account credits for paid reads. Keep private costs and supplier quotes in the session.

## Call the selected data tool

For a named category whose children are needed, start with `openapi_v2_categories`. For other requests, use the business tool named in the selected data method (server `{{mcp_server}}`). If tools are deferred, pass that exact business tool name in `ToolSearch.tool_names`, then invoke the match with the method’s parameters. A connector missing from the introductory status list does not establish a connection failure. Apply the [shared query rules](../../../contract/query.md) to the actual lookup or call result.

For latest ranked-new-listing counts use `openapi_v2_markets_listing_launch_trend`; for requested examples use `openapi_v2_markets_top_product_concentrations` within the selected markets.

Reuse matching evidence and apply the [query](../../../contract/query.md), [evidence](../../../contract/evidence.md) and, for private operating figures, [seller-data rules](../../../contract/seller-evidence.md). For research tasks, assemble the [task outline](report-outline.md). Independently, generate the HTML with the [report guide](../../../tools/report/definition.md). In an expert session give the findings to the expert for one render. Follow the [file handoff](../../../contract/report.md) or the format the seller explicitly requests.
