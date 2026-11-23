<!-- prompt-source: skill/datas/query-weeks/definition.md ae36ba5426621d50344034fdb6347726f4fffa8d07a2b9eacc6d5dfe4cb67542 -->

> 英文原文：[原文](../../../../skill/datas/query-weeks/definition.md)

# 每周搜索需求

查询前按[趋势查询期间](../../../contract/query.md#select-the-trend-period)确定要传入的窗口。

查看指定搜索词每周的搜索量或 ABA 排名。

## 任务输入

指定搜索词和观察期间。

## 接口与调用顺序

1. 调用 `openapi_v2_keyword_trend`（`keywords/trend`）。首次调用前核对接口计费。

## `keywords/trend`

### 查询参数

| 参数 | 用法 |
|---|---|
| `keyword` | 本次查询的搜索词。 |
| `dateFrom` | 必填。周度数据的起始日期。 |
| `dateTo` | 必填。周度数据的截止日期。 |
| `keywords` | 与 `keyword` 二选一，每批传 1–20 个已去首尾空格并转小写的不同词。每次日期范围最多 93 天。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"keyword":"small storage baskets","dateFrom":"2026-08-16","dateTo":"2026-11-07"}
```

### 返回处理

1. 从各词的 `series` 读取每周起止日期、`estimateSearchCount`、`abaRank`，并按需提取 `abaTop3ClickShareRate` 或 `abaTop3ConversionShareRate`。结合 ASIN 曝光与位置时，按同一周对齐。

## 交付结果

每个词所需指标的周度数据及实际统计周。
