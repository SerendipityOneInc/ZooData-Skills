<!-- prompt-source: skill/datas/market-discovery/definition.md c71b35727e58ac778bc1a8ba075514972b9843a5a404fd06639bf0b14c76b8a5 -->

> 英文原文：[原文](../../../../skill/datas/market-discovery/definition.md)

# 类目市场筛选

## 任务输入

按已确认的条件筛选美国站类目。

## 接口与调用顺序

`openapi_v2_markets_search` (`markets/search`).

## `markets/search`

### 查询参数

已确定的类目合并传入 `categoryIds`，每次最多 100 个不同 ID；将 `pageSize` 设为能覆盖本批类目的数量。按目标设置 filters、sortBy 和 sortOrder。用 date、sampleType、includeDescendantCategoryProducts、page 和 pageSize 控制日期、样本、是否含下级商品及分页。查销量榜中的新品时，使用 `sampleType="unitSalesTop100"`，通过 `newProductPeriod`（"1"、"3"、"6"、"12"）选择预先统计的新品数。该统计纳入的最早上架日为实际榜单数据日向前推相应日历月数，再加一天。只有这个日期与任务要求的起始日相同时，才能用该数量回答按天筛选的问题。按符合口径的新品数量排名时使用 `sortBy="sampleNewProductCount"` 和 `sortOrder="desc"`。保留该新品数和实际样本数 `sampleProductCount`，计数缺失时标为未获取。

```json
{"categoryIds": ["679399011"], "sortBy": "totalMonthlySales", "sortOrder": "desc"}
```

### 返回处理

保留类目标识、完整路径、实际数据日期和覆盖范围。类目销量和营收取 totalMonthlySales 和 totalMonthlyRevenue，另标明头部样本指标。

## 交付结果

类目市场筛选.
