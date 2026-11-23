<!-- prompt-source: skill/datas/market-launch-composition/definition.md c0ae5f2d279ed74d1a650301417c0d5b8259696983170254f68c8f1ba1036e0a -->

> 英文原文：[原文](../../../../skill/datas/market-launch-composition/definition.md)

# 新品上架构成

## 任务输入

按首次上架时间查看类目头部商品构成。

## 接口与调用顺序

`openapi_v2_markets_listing_launch_trend` (`markets/listing-launch-trend`).

## `markets/listing-launch-trend`

### 查询参数

指定 categoryIds、sampleType、includeDescendantCategoryProducts 和 granularity（month 或 year）。dateFrom、dateTo 可限定首次上架日期。

```json
{"categoryIds": ["679399011"], "granularity": "month"}
```

### 返回处理

读取所选头部样本的 points[].date 和 productCount。判断新品成功率还需完整同期上架商品作分母。

## 交付结果

新品上架构成.
