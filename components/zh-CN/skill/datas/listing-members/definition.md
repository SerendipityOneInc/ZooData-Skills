<!-- prompt-source: skill/datas/listing-members/definition.md bd79054cef2925c96f8a79dd75fc1dd2ba0a7b77113beff5bd74daf0db76478a -->

> 英文原文：[原文](../../../../skill/datas/listing-members/definition.md)

# 父体成员

## 任务输入

一个已知的父体 ASIN、美国站及所需观测月份。

## 接口与调用顺序

使用 `openapi_v2_products_detail` 的父体成员查询。调用前按连接工具说明核对计费。

## 父体成员 · `products/detail`

### 查询参数

传入 `parentAsin`；查询历史月份时以 YYYY-MM 传入 `dateRange`。取代表款时只需第一页第一条，使用 page=1、pageSize=1，省略 `asins`。

```json
{"parentAsin":"B000000001","dateRange":"2026-10","marketplace":"US","page":1,"pageSize":1}
```

### 返回处理

读取 `data.items` 和 `context.resolvedDate`。成员按月购买量下限降序排列，并列按 ASIN 排列。返回的 title、brandName 和 imageUrl 属于该变体；空结果表示未取得代表款。历史查询保留指定月份和返回的数据日期，不用当前记录替换。

## 交付结果

指定父体下已确认的代表款及其可用的商品标识信息。
