<!-- prompt-source: skill/datas/product-detail/definition.md ce9998f26e97ff0543fcef7494e6427d1b06e7615bfb86b320ae75fcc7706dfc -->

> 英文原文：[原文](../../../../skill/datas/product-detail/definition.md)

# 美国站商品详情

按 ASIN 查询亚马逊美国站商品详情，包括标题、品牌、所属类目、上架日期、价格、类目畅销排名（BSR）、月购买量下限和评分等信息。

## 任务输入

一个或多个美国站商品 ASIN。

## 接口与调用顺序

1. 先使用接口 `openapi_v2_products_detail`（`products/detail`）读取指定商品的最新快照。
2. 对快照未命中的商品，直接使用接口 `openapi_v3_realtime_product`（`realtime/product`）补查。

## 商品详情接口 `products/detail`

### 查询参数

| 参数 | 必填 | 取值 |
|---|---|---|
| `asins` | 是 | 1–50 个互不重复的商品 ASIN，每个由 10 位大写字母或数字组成。 |
| `marketplace` | 否 | 默认 `US`，仅支持美国站。 |
| `dateRange` | 否 | 本 Skill 省略此参数，读取最新快照。 |

```json
{"asins":["B000000001","B000000002"],"marketplace":"US"}
```

### 返回处理

1. `data.items` 按请求顺序返回，每条记录的 `identity.asin` 对应一个商品。数据日期取返回的 `data.context.resolvedDate`。
2. `status=ok` 表示已查到商品。读取该条记录的 `product` 并结束该 ASIN 的查询。个别字段为空也按查询成功处理。每条成功记录消耗 1 积分。
3. `status=empty` 且 `emptyReason=asin_not_found` 表示快照未命中，转实时接口查询该 ASIN。快照服务出错时，仅补查尚未取得的商品。
4. 参数错误（422）时先修正参数。鉴权、连接或额度不足以继续查询时，停止并说明受影响的 ASIN。

## 实时商品详情接口 `realtime/product`

### 查询参数

| 参数 | 必填 | 取值 |
|---|---|---|
| `asin` | 是 | 每次传入一个待补查的商品 ASIN。 |
| `marketplace` | 否 | 沿用原查询的站点 `US`。 |

```json
{"asin":"B000000002","marketplace":"US"}
```

### 返回处理

1. 从 `data` 读取该商品的当前详情，按问题提取实际返回的字段，例如标题、规格或当前报价 `buyboxWinner.price`。
2. 如果实时查询失败或所需字段仍然为空，将对应信息标为未获取，保留已取得的其他记录。

## 交付结果

1. 保留数值 0。价格标明美元，月购买量和月营收标明下限，排名注明所属类目。变体数据与父体合计分别呈现。
2. 区分商品规格和卖点。引用五点原文时，保留原顺序和页面区域。
