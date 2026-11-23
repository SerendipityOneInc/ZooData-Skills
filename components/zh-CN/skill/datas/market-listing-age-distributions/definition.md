<!-- prompt-source: skill/datas/market-listing-age-distributions/definition.md deb401ee378fab78255a67746dd01446f522324ab9cf53b4f1a3e0df665fbc11 -->

> 英文原文：[原文](../../../../skill/datas/market-listing-age-distributions/definition.md)

# 上架时长分布

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_listing_age_distributions` (`markets/listing-age-distributions`).

## `markets/listing-age-distributions`

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

1. 读取 `listingAgeDistribution` 及其上架时长区间，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。
2. 上架时长按自然月计算，区间左闭右开。

## 交付结果

上架时长分布，按指定类目及样本展示。
