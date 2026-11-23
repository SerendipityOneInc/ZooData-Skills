<!-- prompt-source: skill/datas/product-competitors/definition.md faa3154e5ae0e8ef0d700ef1aa49f83f32643f746f4c9d03fe91c1784e861bdb -->

> 英文原文：[原文](../../../../skill/datas/product-competitors/definition.md)

# 竞品查找

## 任务输入

已明确的 ASIN、品牌、卖家、商品关键词或类目路径。

## 接口与调用顺序

1. 首次查询前检查额度，使用接口 `openapi_v2_competitors` (`products/competitors`).

## `products/competitors`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin`、`brandName`、`sellerName`、`keyword`、`categoryPath` | 传入用于界定对比商品的条件。 |
| `marketplace`、`page`、`pageSize` | 站点和分页范围。 |
| `sortBy`、`sortOrder` | 已确认且接口支持的排序指标和方向。 |

```json
{"asin": "B0C7P89D14", "marketplace": "US"}
```

### 返回处理

1. 按本工具的输入定义传入指定 ASIN、品牌、卖家或商品和类目范围。
2. 分页读取匹配行，保留ASIN、商品信息及返回的表现指标，使用用户所需且工具支持的排序，并保留查询范围。保留实际返回的ASIN；只返回输入ASIN的查询，不证明已取得其他竞品或执行了自动相似商品搜索。

## 交付结果

匹配到的商品 ASIN、属性和取得的对比指标。
