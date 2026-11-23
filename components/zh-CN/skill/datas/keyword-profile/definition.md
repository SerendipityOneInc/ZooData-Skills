<!-- prompt-source: skill/datas/keyword-profile/definition.md dfef3852e578819fc87b99f9963f965d934d6e0917b37bf346b9062b9b604227 -->

> 英文原文：[原文](../../../../skill/datas/keyword-profile/definition.md)

# 关键词市场画像

## 任务输入

指定词、比较期间及关心的搜索需求或竞争维度。

## 接口与调用顺序

1. 调用 `openapi_v2_keyword_market_profile`（`keywords/market-profile`）。 首次查询前核对计费。

## `keywords/market-profile`

### 查询参数

| 参数 | 用法 |
|---|---|
| `keyword` / `keywords` | 传单个词或 1–20 个已去首尾空格、转小写并去重的词。条件和期间相同的词合并查询。 |
| `date` | 必填，查询日期 YYYY-MM-DD。查看最新完整数据时取昨天，以返回的实际统计周为准。 |
| `marketplace` / `granularity` | 美国站 US，周粒度 week。 |

```json
{"keyword":"small storage baskets","date":"2026-11-07"}
```

### 返回处理

1. 从 `data.context` 读取实际统计周，从 `data.items[]` 读取各词的 `marketProfile`。只有词标识的记录表示该词无可用画像。
2. 按需读取各维度的 `level`、`interpretation` 和 `levelEvidence` 数值。`demandScale` 提供预估搜索量和 ABA 排名；`top20OrganicEntryDifficulty` 描述进入前 20 个自然位的难度。`supplySaturation` 给出供给饱和等级，搜索结果商品数、实际观察商品数和标题含词比例分别标注。
3. `organicProductBenchmark` 描述领先自然位商品的平均星级、评价数量及销量。`top3Concentration` 分别给出前三商品的点击份额和购买份额。`brandStructure` 描述品牌集中程度。`adCoverage` 表示观察到的商品中出现在广告位的比例。
4. 年度季节性读取 `annualSeasonality`，只在返回历史高峰期时列出对应期间。

## 交付结果

同期各词画像及每个已展示维度的支撑指标。
