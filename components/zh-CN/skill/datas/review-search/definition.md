<!-- prompt-source: skill/datas/review-search/definition.md fe8cb67af651305a53d46ce45ccd47cb62c050fb12f99c85d140516b505feb24 -->

> 英文原文：[原文](../../../../skill/datas/review-search/definition.md)

# 指定商品的买家评论原文

用户想看买家原话，或需要评论举例说明某个问题时，查询单条评论。已有原文覆盖所需范围时直接复用。

## 任务输入

一个商品 ASIN，以及需要查看的评论范围。

## 接口与调用顺序

选择已连接的 `openapi_v2_reviews_search`，对应 `reviews/search`。首次调用时查看当前接口定义。每次请求一页消耗 1 积分。

## `reviews/search`

### 查询参数

| 输入 | 填写规则 |
|---|---|
| `asin` | 必填。一个 ASIN，查询它所属父体的评论。 |
| `dateStart`、`dateEnd`、`ratingMin`、`ratingMax` | 评论日期格式为 YYYY-MM-DD，日期和星级均包含上下界。 |
| `verifiedOnly`、`vineOnly`、`helpfulVoteCountMin`、`mediaTypes` | 返回同时满足所选条件的评论。查带图评论传 ["image"]。主题标签随结果返回，仅供读取。 |
| `sortBy`、`sortOrder` | 默认按 `recent` 从新到旧。需要按星级或有用票数排列时，分别传 `rating` 或 `helpfulVoteCount`。方向为 `asc`（升序）或 `desc`（降序）。 |
| `page`、`pageSize` | 从第 1 页开始，每页默认 10 条、最多 20 条。按用户需要的范围和预算翻页。 |

查询最新五条低星评论的示例

```json
{"asin":"B000000001","ratingMax":2,"pageSize":5}
```

### 返回处理

1. 摘录相关原文，保留评论编号、日期、星级和已知变体。评论归属该 ASIN 所在的父体。只有记录明确指出具体变体时，才把反馈归到该变体。
2. 统计提及次数时说明查看了哪些评论。每个父体最多读取 5,000 条评论后再筛选，解释可能达到上限的总量时注明范围。
3. 零条表示所选条件下无匹配评论。保留本次筛选条件，避免重复读取已计费页面。连接器不可用时，说明缺少哪部分评论。

## 交付结果

所选商品的评论原文及已获得的日期、星级和变体信息。
