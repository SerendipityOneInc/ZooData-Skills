<!-- prompt-source: skill/datas/keyword-statistics/definition.md 775dd1c2bd89241983582819b1ab265ae4a61248f199cfd1a6771b5a58ae726c -->

> 英文原文：[原文](../../../../skill/datas/keyword-statistics/definition.md)

# 关键词基础统计

## 任务输入

指定词及用户关心的基础指标。

## 接口与调用顺序

1. 调用 `openapi_v2_keyword_detail`（`keywords/detail`）。 首次查询前核对计费。

## `keywords/detail`

### 查询参数

| 参数 | 用法 |
|---|---|
| `keyword` / `keywords` | 传单个词或 1–20 个已去首尾空格、转小写并去重的词。条件和期间相同的词合并查询。 |
| `date` | 必填，查询日期 YYYY-MM-DD。查看最新完整数据时取昨天，以返回的实际统计周为准。 |
| `marketplace` / `granularity` | 美国站 US，周粒度 week。 |

```json
{"keywords":["small storage baskets","woven baskets"],"date":"2026-11-07"}
```

### 返回处理

1. 从 `data.context` 取实际统计周，在 `data.items[]` 中按 `identity`、`status` 读取每个词的 `snapshotData`。
2. 按需取 `estimateSearchCount`、`abaRank`、前三商品点击或购买份额、商品数量、标题含词比例或自然位靠前商品的均值。无数据的记录保留对应词。

## 交付结果

各词实际统计周及用户要求的基础指标。
