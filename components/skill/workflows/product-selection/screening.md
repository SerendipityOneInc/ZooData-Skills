# Screen candidates

1. Identify the product scope, filters and ranking measure in the seller’s words. “Best-selling” calls for descending purchase volume. For newly listed products without a stated age window, use 180 days. Apply price, sales and fulfillment limits only when requested.
2. Reuse the specified category, keyword and order. Clarify only missing choices that affect the result. Confirm one category or all categories if the scope is unclear. Resolve ambiguous names through [category lookup](../../datas/category-lookup/definition.md). If the ranking measure is unclear, ask which measure matters.
3. Map the seller’s conditions to fields supported by [product search](../../datas/product-discovery/definition.md). Supply the scope, one sort field and direction, and effective filters to the [request planner](plan_screening.py). Resolve conflicting or unsupported conditions before querying.
4. For one overall ranking, keep one query scope and ordering across pages. Retain distinct ASINs in that order up to the requested count and identify ties in the observed results. Use the response total for match count. For a separate ranking per category, query each confirmed category under the same filters and sort within budget. A category subset of a partial overall list describes that sample only.

Run `python3 <planner> <selection.json>`, for example

```json
{"scope":"all","sortBy":"monthlySalesFloor","sortOrder":"desc","filters":{"priceMax":30},"pageSize":10}
```
