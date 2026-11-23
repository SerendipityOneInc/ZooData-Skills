# Category lookup

Resolve a category name or path to the appropriate category ID.

## Task input

A category name, path or ID; for children, identify the parent.

## Endpoints and call order

1. Call `openapi_v2_categories` (`categories`). Check billing before the first read.

## `categories`

### Request parameters

| Parameter | Use |
|---|---|
| `categoryKeyword` | Keyword for matching category names. |
| `categoryPath` | Path from the root to the target category. |
| `parentCategoryPath` | Parent path for listing direct children. |
| `marketplace` | Use `US` for Amazon US. |

```json
{"categoryKeyword":"Storage Baskets"}
```

### Response handling

1. Read `categoryId`, `categoryName` and `categoryPath` for each match.
2. For a direct-child comparison, use the returned child IDs as the market scope. Ask the user to select a category when matches lead to different intended markets.

## Deliverable

Names, IDs and full paths of matching categories.
