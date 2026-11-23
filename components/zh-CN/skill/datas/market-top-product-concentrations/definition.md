<!-- prompt-source: skill/datas/market-top-product-concentrations/definition.md 0dfb6f024d4364d15dd5e8085eac09e29d17fa65fcc1d5aed2dc5723bf648d2c -->

> 英文原文：[原文](../../../../skill/datas/market-top-product-concentrations/definition.md)

# 商品集中度

## 任务输入

已确认的类目 ID、是否包含子类目、样本范围和数据日期。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_top_product_concentrations` (`markets/top-product-concentrations`).

## `markets/top-product-concentrations`

### 查询参数

| 参数 | 用法 |
|---|---|
| `categoryIds` | 必填。日期和范围相同的类目合并查询，一次最多 100 个不同 ID；当前按实际返回的每个市场 1 积分计费。 |
| `sampleType` | 选择按销量或营收取头部样本的方式。 |
| `includeDescendantCategoryProducts` | 是否计入下级类目的商品。 |
| `date` | 观察日期，格式 YYYY-MM-DD。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"categoryIds": ["679399011"]}
```

### 返回处理

1. 读取 `topnMetrics` 和 `topProductList`，保留各 Top N 标识、`concentrationRate`、样本排序依据及各返回对象的销量和收入指标。

## 交付结果

商品集中度，按指定类目及样本展示。
