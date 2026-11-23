<!-- prompt-source: skill/datas/market-rating-distributions/definition.md 75a9520acafc0ed57fa3f93e7c69a429c1f0177cbd81007d98036d67af310dc0 -->

> 英文原文：[原文](../../../../skill/datas/market-rating-distributions/definition.md)

# 星级分布

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_rating_distributions` (`markets/rating-distributions`).

## `markets/rating-distributions`

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

1. 读取 `ratingDistribution` 及其星级上下界，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。
2. 星级区间左开右闭，最高一档包含 5 星。

## 交付结果

星级分布，按指定类目及样本展示。
