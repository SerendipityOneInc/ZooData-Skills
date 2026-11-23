<!-- prompt-source: skill/datas/market-history/definition.md 025021d0b4b7683fe7925ecfcba6a9c524b099cfd8ff56efe16c611f68a2e632 -->

> 英文原文：[原文](../../../../skill/datas/market-history/definition.md)

# 市场历史

## 任务输入

已确认的类目 ID、统一的样本范围和观察期间。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_markets_history` (`markets/history`).

## `markets/history`

### 查询参数

| 参数 | 用法 |
|---|---|
| `categoryIds` | 必填。已确认的类目 ID 数组。 |
| `sampleType` | 选择按销量或营收取头部样本的方式。 |
| `includeDescendantCategoryProducts` | 是否计入下级类目的商品。 |
| `dateFrom`、`dateTo` | 必填。起止日期，格式 YYYY-MM-DD。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"categoryIds": ["679399011"], "dateFrom": "2026-05-01", "dateTo": "2026-10-31"}
```

### 返回处理

1. 传入类目 ID、`dateFrom`、`dateTo` 及一致的商品包含和样本规则，读取各序列的类目身份和 `points`。
2. 按返回的月末日期对齐，比较 `marketSize` 或 `sampleProfile` 中的同一指标；按问题要求计算观测变化，保留各期样本选择。
3. 用户未指定期间时使用[共享趋势周期](../../../contract/query.md)。

## 交付结果

类目趋势图的横轴标月份，纵轴标“月销量（件）”，图例使用类目名称。
