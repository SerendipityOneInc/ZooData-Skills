<!-- prompt-source: skill/datas/traffic-terms/definition.md ec1d9e33dacf1d860378cd80bd3b5aa219ebc2dc06d613254285e263295e80d3 -->

> 英文原文：[原文](../../../../skill/datas/traffic-terms/definition.md)

# 商品引流词

查询指定期间为商品带来曝光的搜索词及其贡献。

## 任务输入

一个商品 ASIN、观察周及所需的引流词排序方式。

## 接口与调用顺序

1. 调用 `openapi_v2_product_traffic_terms`（`keywords/product-traffic-terms`）。首次调用前核对接口计费。

## `keywords/product-traffic-terms`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 必填。单个商品 ASIN。 |
| `date` | 必填。观察日期，格式 YYYY-MM-DD。 |
| `sortBy` | 接口支持的排序字段。 |
| `sortOrder` | 升序 asc 或降序 desc。 |
| `exploreTypes` | 需要限定自然或广告位置时传入位置类型。 |
| `page` | 需要分页时传页码。 |
| `pageSize` | 每页返回条数。 |
| `marketplace` | 美国站使用 `US`。 |

| 取数目的 | 排序方式 |
|---|---|
| 曝光贡献较高 | `trafficShare desc` 或 `estimateImpressionPoint desc` |
| 同一位置类型内观测位置更靠前 | `avgPosition asc` 或 `absolutePosition asc` |
| 搜索词需求量较高 | `keywordEstimateSearchCount desc` |

```json
{"asin":"B0C7P89D14","date":"2026-11-07","sortBy":"trafficShare","sortOrder":"desc"}
```

### 返回处理

1. 逐行读取搜索词、`trafficShare`、`estimateImpressionPoint`、位置、位置类型、搜索量和 ABA 排名及观测覆盖，按所需范围继续分页。


2. 占比的分母是该 ASIN 同期观测到的总曝光。位置缺失时保留未知，最近一次位置与平均位置分别呈现。

## 交付结果

引流词及其曝光贡献和展示位置。
