<!-- prompt-source: skill/datas/category-lookup/definition.md c06e714d293e78cc64b485371e08a2e6949c31dbf302ab232a0b2333f2086e49 -->

> 英文原文：[原文](../../../../skill/datas/category-lookup/definition.md)

# 类目匹配

按类目名称或路径查找对应类目编号。

## 任务输入

类目名称、路径或编号；查看子类目时提供父类目。

## 接口与调用顺序

1. 调用 `openapi_v2_categories`（`categories`）。首次调用前核对接口计费。

## `categories`

### 查询参数

| 参数 | 用法 |
|---|---|
| `categoryKeyword` | 用来匹配类目名称的关键词。 |
| `categoryPath` | 从根类目到目标类目的路径。 |
| `parentCategoryPath` | 列出直接子类目时传父类目路径。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"categoryKeyword":"Storage Baskets"}
```

### 返回处理

1. 逐项读取 `categoryId`、`categoryName` 和 `categoryPath`。
2. 比较直接子类时，以返回的子类 ID 作为市场范围；匹配结果对应不同目标市场时，请用户明确要研究的类目。

## 交付结果

匹配类目的名称、编号和完整路径。
