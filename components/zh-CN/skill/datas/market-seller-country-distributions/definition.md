<!-- prompt-source: skill/datas/market-seller-country-distributions/definition.md 160bbb2cf4b5684710df9c0d98b30211915f223f38346b1e356c1c9827073406 -->

> 英文原文：[原文](../../../../skill/datas/market-seller-country-distributions/definition.md)

# 卖家国家分布

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_seller_country_distributions` (`markets/seller-country-distributions`).

## `markets/seller-country-distributions`

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

1. 读取 `sellerCountryDistribution` 及其卖家国家标识，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。
2. 同一商品可能涉及多个国家的卖家。

## 交付结果

卖家国家分布，按指定类目及样本展示。
