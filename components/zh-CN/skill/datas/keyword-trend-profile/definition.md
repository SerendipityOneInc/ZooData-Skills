<!-- prompt-source: skill/datas/keyword-trend-profile/definition.md e83b4d973dd53ea0bddb21e81ed3bc6af6de084a28d010e8424d6b30f6c796a3 -->

> 英文原文：[原文](../../../../skill/datas/keyword-trend-profile/definition.md)

# 关键词需求趋势画像

## 任务输入

指定词、截止日期和趋势观察窗口。

## 接口与调用顺序

1. 调用 `openapi_v2_keyword_trend_profile`（`keywords/trend-profile`）。 首次查询前核对计费。

## `keywords/trend-profile`

### 查询参数

| 参数 | 用法 |
|---|---|
| `keyword` / `keywords` | 传单个词或 1–20 个已去首尾空格、转小写并去重的词。条件和期间相同的词合并查询。 |
| `date` | 必填，查询日期 YYYY-MM-DD。查看最新完整数据时取昨天，以返回的实际统计周为准。 |
| `marketplace` / `granularity` | 美国站 US，周粒度 week。 |
| `windowPeriods` | 必填，从 4、8、12、26 周中选择 1–4 个不同窗口。未指定周度期间时使用 12 周。 |

```json
{"keyword":"small storage baskets","date":"2026-11-07","windowPeriods":[12]}
```

### 返回处理

1. 在 `data.items[].rows[]` 中逐窗口读取 `rowContext`、`status` 和 `trendProfile`。区分整个窗口无数据与个别指标缺失。
2. 分别从 `searchDemand` 和 `abaRank` 的 `trend` 取方向，从 `trendEvidence` 取变化依据。需要时列出搜索需求的波动程度 `volatilityLevel` 和最新周所处水平 `lastPeriodWindowPosition`。首尾变化只比较两期，趋势分类取决于整个窗口。

## 交付结果

各窗口的搜索需求与排名走势、变化幅度及波动程度。
