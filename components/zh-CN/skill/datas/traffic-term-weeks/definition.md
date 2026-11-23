<!-- prompt-source: skill/datas/traffic-term-weeks/definition.md bedf7c9c14e358d40664976d54ccc06a432c737a6561ca2e027cfb5d62f6325a -->

> 英文原文：[原文](../../../../skill/datas/traffic-term-weeks/definition.md)

# 指定词下的商品曝光变化

查询前按[趋势查询期间](../../../contract/query.md#select-the-trend-period)确定要传入的窗口。

比较商品在指定搜索词下每周的曝光、位置和搜索需求。

## 任务输入

一个商品 ASIN、指定搜索词和观察期间。

## 接口与调用顺序

1. 调用 `openapi_v2_product_traffic_terms_trend`（`keywords/product-traffic-terms-trend`）。首次调用前核对接口计费。

## `keywords/product-traffic-terms-trend`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 必填。单个商品 ASIN。 |
| `keyword` | 本次查询的搜索词。 |
| `dateFrom` | 必填。周度数据的起始日期。 |
| `dateTo` | 必填。周度数据的截止日期。 |
| `keywords` | 批量查询时传入搜索词数组。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14","keyword":"small storage baskets","dateFrom":"2026-08-16","dateTo":"2026-11-07"}
```

### 返回处理

1. 按搜索词读取各自的周度 `series`。
2. 逐期读取 `totalEstimateImpressionPoint`、`trafficByExploreType`、`keywordEstimateSearchCount` 和 `keywordAbaRank`。各位置类型只比较自身的曝光和位置，`absolutePosition` 与 `avgPosition` 分别比较。仅在问题需要时读取 `asinSnapshot` 和对应位置类型的 `adActivity`。
3. 按返回的期间边界，对齐曝光、位置，以及搜索量或 ABA 排名。已有关键词序列直接复用，搜索量和 ABA 排名具备一项即可。

## 交付结果

指定词下逐周的商品曝光、位置及同期搜索需求。
