<!-- prompt-source: skill/datas/market-content-distributions/definition.md 2348c90cc82a60aaee7ce501f2e2a2c9096c94b40208b48a4f73c71c47ea8177 -->

> 英文原文：[原文](../../../../skill/datas/market-content-distributions/definition.md)

# 内容配置分布

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_content_distributions` (`markets/content-distributions`).

## `markets/content-distributions`

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

1. 读取 `contentDistribution` 及其返回的内容类型标识，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。
2. 同一商品可能包含多种内容。

## 交付结果

内容配置分布，按指定类目及样本展示。
