<!-- prompt-source: skill/datas/market-seller-concentrations/definition.md 915cc0482d857ce761901b16b80e95eac2fb4c68661d634d502af05714e6e03a -->

> 英文原文：[原文](../../../../skill/datas/market-seller-concentrations/definition.md)

# 卖家集中度

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_seller_concentrations` (`markets/seller-concentrations`).

## `markets/seller-concentrations`

### 查询参数

| 参数 | 用法 |
|---|---|
| `categoryIds` | 必填。已确认的类目 ID 数组。 |
| `sampleType` | 选择按销量或营收取头部样本的方式。 |
| `includeDescendantCategoryProducts` | 是否计入下级类目的商品。 |
| `date` | 观察日期，格式 YYYY-MM-DD。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"categoryIds": ["679399011"]}
```

### 返回处理

1. 读取 `topnMetrics` 和 `topSellerList`，保留各 Top N 标识、`concentrationRate`、样本排序依据及各返回对象的销量和收入指标。

## 交付结果

卖家集中度，按指定类目及样本展示。
