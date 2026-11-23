<!-- prompt-source: skill/datas/market-price-distribution/definition.md 38d08e2c1914161654b811adb25183262d6fb65cbf77fbd86350cc843c3d96c9 -->

> 英文原文：[原文](../../../../skill/datas/market-price-distribution/definition.md)

# 类目价格分布

比较同一类目样本在各价格区间的商品与销量分布。

## 任务输入

已确认的类目及要分析的价格分布范围。

## 接口与调用顺序

1. 调用 `openapi_v2_markets_price_distributions`（`markets/price-distributions`）。首次调用前核对接口计费。

## `markets/price-distributions`

### 查询参数

| 参数 | 用法 |
|---|---|
| `categoryIds` | 必填。已确认的类目 ID 数组。 |
| `sampleType` | 选择按销量或营收取头部样本的方式。 |
| `includeDescendantCategoryProducts` | 是否计入下级类目的商品。 |
| `date` | 观察日期，格式 YYYY-MM-DD。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"categoryIds":["679399011"]}
```

### 返回处理

1. 读取 `priceDistribution` 及其价格上下界，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。
2. 使用指定类目、样本和实际数据日。按返回的左闭右开价格区间解释分组，占比保留样本分母。

## 交付结果

各价格区间的商品数量、销量与占比。
