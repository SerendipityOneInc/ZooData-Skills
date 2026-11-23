<!-- prompt-source: skill/datas/search-placements/definition.md 1d2c459df8896e3fee62555012d797c76f7452b4a4755c626271303ef85a2a03 -->

> 英文原文：[原文](../../../../skill/datas/search-placements/definition.md)

# 搜索展示位置

查看指定商品在某个搜索词下的展示位置。

## 任务输入

一个搜索词、观察周及需要查看的展示位置。

## 接口与调用顺序

1. 调用 `openapi_v2_keyword_search_results`（`keywords/search-results`）。首次调用前核对接口计费。

## `keywords/search-results`

### 查询参数

| 参数 | 用法 |
|---|---|
| `keyword` | 必填。本次查询的搜索词。 |
| `date` | 必填。观察日期，格式 YYYY-MM-DD。 |
| `exploreTypes` | 需要限定自然或广告位置时传入位置类型。 |
| `sortBy` | 接口支持的排序字段。 |
| `sortOrder` | 升序 asc 或降序 desc。 |
| `page` | 需要分页时传页码。 |
| `pageSize` | 每页返回条数。 |
| `marketplace` | 美国站使用 `US`。 |

查看位置时用 `absolutePosition asc`，按曝光排序时用 `estimateImpressionPoint desc`。

```json
{"keyword":"small storage baskets","date":"2026-11-07"}
```

### 返回处理

1. 保留 ASIN、可读商品名称、`exploreType`、`absolutePosition` 和 `estimateImpressionPoint`，在相同搜索词、期间及位置类型内比较选定商品，明确取得的记录范围。
2. 每个搜索词及期间的 `keywordTotalEstimateImpressionPoint` 读取一次。用户要求样本内曝光份额时，将指定分组的记录曝光点求和，再除以同一样本全部记录的曝光点之和。

## 交付结果

该词下实际观察到的商品、位置和曝光。
