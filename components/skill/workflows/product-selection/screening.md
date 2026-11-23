# Screen candidates

1. Identify the product scope, filters and ranking measure in the seller’s words. “Best-selling” calls for descending purchase volume. For products launched in the past half year, or new products without a stated age window, apply 180 days and label the window in the report scope. Apply price, sales and fulfillment limits only when requested.
2. Reuse the specified category, keyword and order. Clarify only missing choices that affect the result. Treat a category path or an explicit set of categories as the full scope. The product search accepts one hierarchical path. If the requested set cannot be expressed exactly, explain that a combined ranking is unavailable and ask whether to research a selected market. Resolve ambiguous names through [category lookup](../../datas/category-lookup/definition.md). If the ranking measure is unclear, ask which measure matters.
3. Map the seller’s conditions to fields supported by [product search](../../datas/product-discovery/definition.md). Supply the scope, one sort field and direction, and effective filters to the [request planner](plan_screening.py). Resolve conflicting or unsupported conditions before querying.
4. For one overall ranking, keep one query scope and ordering across pages. Retain distinct ASINs in that order up to the requested count and identify ties in the observed results. Use the response total for match count. Do not build the ranking from separate searches for each category or broaden it to a common parent that includes other products. A category subset of a partial overall list describes that sample only.

Run `python3 <planner> <selection.json>`, for example

```json
{"scope":"all","sortBy":"monthlySalesFloor","sortOrder":"desc","filters":{"priceMax":30},"pageSize":10}
```
