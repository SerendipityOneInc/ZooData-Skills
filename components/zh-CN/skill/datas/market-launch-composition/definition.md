<!-- prompt-source: skill/datas/market-launch-composition/definition.md 21a8116ca0fe6f339cb340bb184626bcdd2e9572e5106487026300c505c9f896 -->

> 英文原文：[原文](../../../../skill/datas/market-launch-composition/definition.md)

# 新品上架构成

## 任务输入

按首次上架时间查看类目头部商品构成。

## 接口与调用顺序

`openapi_v2_markets_listing_launch_trend` (`markets/listing-launch-trend`).

## `markets/listing-launch-trend`

### 查询参数

将同一范围的类目批量传入 `categoryIds`。销量榜用 `sampleType="unitSalesTop100"`，保持下级类目范围一致。用 `dateFrom` 和 `dateTo` 限定首次上架日期，含两端，再按 `granularity="month"` 分组。接口始终使用最新榜单。

```json
{"categoryIds":["679399011"],"sampleType":"unitSalesTop100","includeDescendantCategoryProducts":true,"dateFrom":"2026-05-04","dateTo":"2026-10-31","granularity":"month"}
```

### 返回处理

返回的日期表示首次上架期间，响应中没有榜单日期。逐类目累加各月的 `points[].productCount`。保留明确的零值；缺失的类目或计数标为未获取。

## 交付结果

新品上架构成.
