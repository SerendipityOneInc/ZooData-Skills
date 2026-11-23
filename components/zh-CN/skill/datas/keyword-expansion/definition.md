<!-- prompt-source: skill/datas/keyword-expansion/definition.md 83c307de3318f6846b2130f32f77f3aa603f46533b15aeb14e0e32c51ed81e2b -->

> 英文原文：[原文](../../../../skill/datas/keyword-expansion/definition.md)

# 相关关键词

## 任务输入

美国站核心词和所需候选范围。

## 接口与调用顺序

1. 调用 `openapi_v2_keyword_extends`（`keywords/extends`）。 首次查询前核对计费。

## `keywords/extends`

### 查询参数

| 参数 | 用法 |
|---|---|
| `query` | 必填。按核心词本身判断语言。中文核心词在首次查询前译为一个自然的英文搜索词，保留原有的品类、属性、品牌和型号。其他语言的核心词按原文查询，即使用户用中文提问。 |
| `queryType` | 常规拓词使用 fuzzy。用户明确要求短语匹配时使用 phrase。 |
| `sortBy` / `sortOrder` | 常规拓词按 relevanceScore 降序。用户明确要求时可按 estimateSearchCount 降序、abaRank 升序或 keyword 升序。 |
| `page` / `pageSize` | 从第 1 页开始。默认每页 20 个，最多 100 个。按用户所需数量和预算翻页。 |
| `marketplace` / `granularity` | 美国站 US，周粒度 week。 |

```json
{"query":"small storage baskets","marketplace":"US","queryType":"fuzzy","sortBy":"relevanceScore","sortOrder":"desc","page":1,"pageSize":20}
```

### 返回处理

1. 从 `data.rows[]` 的 `matchData` 读取 `keyword`、`site` 和 `relevanceScore`。从 `keywordSnapshot` 读取 `estimateSearchCount`、`abaRank` 和 `dataWindow.currentPeriod`。
2. 接口使用最新可用周。返回空列表时交付零个候选，区分实际读取条数与匹配总数。

## 交付结果

候选词及其相关度、周预估搜索量、ABA 排名、统计周和覆盖范围。
