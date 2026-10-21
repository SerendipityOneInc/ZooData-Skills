# 市场接口 Request / Response 审计

核对日期：2026-10-21。直接向配置中的 `http://localhost:8080/mcp` 执行 initialize、tools/list，获取 14 个市场工具的 inputSchema 和 outputSchema，并用更新后的 CLI 构造参数执行实际 tools/call。没有使用公开文档、会话缓存工具定义或旧本地模型代替本次契约。

## 当前契约与技能适配

- 计数、销量、销售额统一为 Count、Sales、Revenue；常用均值统一为 avgPrice、avgRating、avgRatingCount、avgMonthlySales、avgMonthlyRevenue。筛选 Min/Max、192 个排序值和 CLI 标志同步使用新名称，例如 --avg-price 和 --avg-monthly-sales。旧标志/旧排序值在发请求前拒绝。
- search 使用 date 截止日、resolvedDate 实际日期，28 对平铺 Min/Max 及 sellerCountryCodes；不发送 dateRange 或嵌套指标对象。省略/null 商品范围均包含下级商品。
- profile、七种分布、三种集中度使用精确 date。profile 样本统计在 sampleProfile；分布和集中度根层保留 sampleProductCount、sampleMonthlySales/Revenue 及 sampleAvgPrice、sampleAvgMonthlySales/Revenue、sampleAvgRating/Count。
- 三种集中度根层统一为 topnMetrics，实体数组为 topProductList、topBrandList、topSellerList。实体 rank 为按样本指标排序的名次；国家分布 distributionRank 是展示顺序。profile.concentrationProfile 内的 topnBrandMetrics 保持原名，不能全局机械替换。
- history 是月末快照系列，读取 data[].points[].date、marketSize/sampleProfile，包含样本单品均值。每个月按当期指标独立选样，不能解释为固定商品群增长；不补齐缺失月份。
- launch 的 dateFrom/dateTo 筛选首次上架日期，样本始终取最新；返回 points[].date/productCount，无快照日期。
- 价格桶下界包含、上界排除，最后一档无上限；band_1 等编码不能跨市场或日期直接对比。其他数值维度遵循各自编码的边界定义。
- 国家商品成员可重叠，但销量/销售额按相应国家卖家记录归属，不是整款销量重复计入各国，也不是平均分摊。价格和评分均值逐指标排除 null、包含零，无有效值时为 null。月销量和销售额表示快照时近 30 天，不是新品窗口内累计销量。
- search 按次收费，空结果也收费；其他接口按实际返回去重市场数收费，空结果免费，余额准入不预扣。

API 事实、指标语义、证据读取与输出分别保留在既有责任模块；共享 CLI 仅修改 canonical 源并同步至 8 个活跃技能，未改变白名单或所有权映射。

## 实际 MCP 响应

全部 14 个接口取得 success=true 且有数据的响应，每次单市场计费 1 credit，累计 14 credits。查询类目为 679399011、样本 unitSalesTop100；search 使用截止日 2026-09-15、价格 10–50 和 avgMonthlyRevenue 排序，返回 2026-08-31；其他单快照详情使用 date=2026-10-19；history 与 launch 使用 2026-07-01 至 09-30。

| 接口 | 根响应模型 | 实际根字段数 | requestId |
|---|---|---:|---|
| search | MarketSearchFact | 202 | req_a6e25680f68146e5 |
| history | MarketHistorySeries | 6 | req_fb3fe47e5b914e67 |
| profile | MarketProfile | 11 | req_bccc968f27774803 |
| price-distributions | PriceDistribution | 18 | req_57f111e19c554ab5 |
| rating-distributions | RatingDistribution | 18 | req_2eacb3d553d146b3 |
| rating-count-distributions | RatingCountDistribution | 18 | req_e48209841ba5478e |
| listing-age-distributions | ListingAgeDistribution | 18 | req_0d4cada927ea4bab |
| fulfillment-distributions | FulfillmentDistribution | 18 | req_37e47af3cc414bd7 |
| seller-country-distributions | SellerCountryDistribution | 18 | req_e7c65d57df324f34 |
| content-distributions | ContentDistribution | 18 | req_c71e379659bf4526 |
| top-product-concentrations | TopProductConcentration | 19 | req_2046d226a4a24219 |
| brand-concentrations | BrandConcentration | 20 | req_50d1e83e71564459 |
| seller-concentrations | SellerConcentration | 19 | req_d9a77e3311d64ac1 |
| listing-launch-trend | ListingLaunchTrend | 8 | req_96ff74ddd8bc4a78 |

history 返回 2026-07-31、08-31、09-30 三个月末；launch 返回 07/08/09 三个上架批次。每份实际响应均通过其公开 outputSchema（含格式与元数据）校验，并对业务嵌套对象额外关闭未知字段，以检查旧字段残留。

## 本地检查与限制

- 332 组 CLI 请求通过当前 MCP inputSchema：14 接口 × 2 样本 × 2 商品范围，以及 28 个筛选各三种边界、192 个排序值。
- 28 组完整嵌套/全 null 模拟响应通过公开 outputSchema。冻结清单直接提取 4 种请求结构和 39 种业务根/嵌套响应模型，不含通用错误、元数据及 token usage 模型，见 [contract fixture](../tests/fixtures/market-spu-contract.json)。
- 全量仓库测试为 311 passed、2 skipped（可选 live 测试）。共享文件检查为 8 个技能、0 差异；9 个相关技能 quick_validate 和 git diff --check 通过。
- 回归检查包含新筛选/排序构造、旧参数拒绝、日期边界、0/null、完整市场系列身份、元数据保留，以及集中度根字段与 profile 内字段的上下文差别。

以上是单类目和有限组合的实际验收，不是全部业务数据、BigQuery 计算或多市场计费的穷举验证。上游 history 描述中的迁移表仍有旧字段名，本技能按当前 outputSchema 与实际响应使用新名称。未独立验收 dev 或已安装副本，未部署服务、发布技能或创建 Release。
