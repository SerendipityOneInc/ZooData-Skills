# Competitor discovery

## Task input

A named ASIN, brand, seller, keyword or confirmed category path.

## Endpoints and call order

1. Before the first read check billing, then call `openapi_v2_competitors` (`products/competitors`).

## `products/competitors`

### Request parameters

| Parameter | Use |
|---|---|
| `asin`, `brandName`, `sellerName`, `keyword`, `categoryPath` | Supply the filters that identify the comparison set. |
| `marketplace`, `page`, `pageSize` | Requested marketplace and coverage. |
| `sortBy`, `sortOrder` | Supported comparison measure and order. |

```json
{"asin": "B0C7P89D14", "marketplace": "US"}
```

### Response handling

1. Pass the named ASIN, brand, seller or product/category scope using this tool's own input schema.
2. Read the paginated matching rows with ASINs, product facts and returned performance measures. Apply the requested supported sorting and preserve the query scope. Retain which ASINs were actually returned; a lookup returning only the input ASIN is not evidence of additional competitors or an automatic similarity search.

## Deliverable

Matching ASINs, their attributes and the observed comparison measures.
