<!-- prompt-source: skill/datas/market-rating-count-distributions/definition.md e38ea4211ef8a106388ed31cebe0e7ecbae8d6a8f6404ed1fecbc50d8c337210 -->

> 英文原文：[原文](../../../../skill/datas/market-rating-count-distributions/definition.md)

# 评分数分布

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_rating_count_distributions` (`markets/rating-count-distributions`).

## `markets/rating-count-distributions`

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

1. 读取 `ratingCountDistribution` 及其评分数上下界，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。
2. 评分数是连续整数分段，两端均包含；单列的零值组保留。

## 交付结果

评分数分布，按指定类目及样本展示。
