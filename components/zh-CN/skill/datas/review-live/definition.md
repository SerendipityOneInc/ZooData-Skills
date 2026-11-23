<!-- prompt-source: skill/datas/review-live/definition.md 701cd2e59cf9fe94888d9863b36a08bd3ed6d52c5ed00ab41d0545aa9415ff6a -->

> 英文原文：[原文](../../../../skill/datas/review-live/definition.md)

# 当前页面评论

读取指定商品页面当前展示的评论。

## 任务输入

一个商品 ASIN 和需要查看的页面评论范围。

## 接口与调用顺序

1. 调用 `openapi_v2_realtime_reviews`（`realtime/reviews`）。首次调用前核对接口计费。

## `realtime/reviews`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 必填。单个商品 ASIN。 |
| `cursor` | 首页省略，后续页传上一页的 nextCursor。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14"}
```

### 返回处理

1. 从 `data.reviews` 读取评论原文和日期；用 `nextCursor` 判断是否还有下一页。
2. 保留该页面样本的实际评论日期和商品范围，不以它替代指定历史期间的评论。

## 交付结果

实际读到的买家评论原文及日期。
