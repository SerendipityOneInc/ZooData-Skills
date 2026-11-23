<!-- prompt-source: skill/datas/product-live/definition.md 83f558e0ef723e00581c1a219331063830f293ed19e8ccf14fa06791f9d11d3b -->

> 英文原文：[原文](../../../../skill/datas/product-live/definition.md)

# 实时商品详情

获取指定 ASIN 当前页面的报价、规格或五点原文。

## 任务输入

一个商品 ASIN 和想了解的当前页面信息。

## 接口与调用顺序

1. 调用 `openapi_v3_realtime_product`（`realtime/product`）。首次调用前核对接口计费。

## `realtime/product`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 必填。单个商品 ASIN。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14"}
```

### 返回处理

1. 从 `data` 提取实际返回的商品信息。当前报价取 `buyboxWinner.price`；规格和五点原文保留所属变体和页面区域。
2. 未取得的部分标为未获取。仅在连接器明确允许重试且额度足够时重试。

## 交付结果

当前商品报价、规格或页面原文。
