# 市场接口技能迁移

本次以 2026-10-21 从 `http://localhost:8080/mcp` 直接取得的 tools/list、inputSchema、outputSchema 和实际 tools/call 响应为准。旧源码提交或会话缓存的工具定义不能代替当前服务契约。接口仍为 14 个，统计粒度为合并同父商品变体的 Listing/SPU，仅美国站。

## 字段命名迁移

| 旧名称 | 当前名称 |
|---|---|
| productCnt、sampleProductCnt | productCount、sampleProductCount |
| monthlySaleCnt、monthlySaleAmt | monthlySales、monthlyRevenue |
| avgProductPrice30d、avgProductRatingAmt | avgPrice、avgRating |
| avgProductMonthlySaleCnt、avgProductMonthlySaleAmt | avgMonthlySales、avgMonthlyRevenue |
| topProducts、topnBrandList、sellerList | topProductList、topBrandList、topSellerList |

筛选 Min/Max 和排序值都使用新名称，CLI 标志同步为 `--avg-price`、`--avg-monthly-sales` 等，不提供旧字段标志别名。响应的 39 个模型直接以 MCP outputSchema 冻结。

## 请求迁移

| 原调用或构造 | 当前调用或构造 |
|---|---|
| `market --date-range 30d` | `market`，省略日期取最新 |
| `market --date-range YYYY-MM` | `market --date YYYY-MM-DD`，取不晚于截止日的最近共同快照 |
| `filters.avgProductPrice30d={min:10,max:30}` | `filters.avgPriceMin=10`、`avgPriceMax=30` |
| 192 个响应指标均可筛选 | 仅公开的 28 对 Min/Max 可筛选；192 个排序字段独立维护 |
| `market-listing-launch-trend --date ...` | 可选 `--date-from ... --date-to ...`，过滤首次上架日期 |
| detail/history 的 `--category-scope direct` | `--no-include-descendant-category-products` |
| `market-structure-profile` | 对应的独立分布或集中度命令 |

CLI 保留 `--avg-price 10:30` 这样的范围写法，构造请求时展开为平铺 Min/Max。`MIN:MAX`、`MIN:`、`:MAX` 分别为双边、仅下限、仅上限，有限值且下限不得超过上限。金额为 USD，比例为小数；不支持的筛选标志在发请求前拒绝，不能因为字段可以排序就把它用作筛选。

所有市场命令使用顶层 includeDescendantCategoryProducts 布尔值。详情、历史与上架组成支持 `--category-ids ID1,ID2`。商品范围与市场行选择独立；父类目和子类目统计可能重叠。

## 日期与响应读取

- `resolvedDate` 是返回数据的实际业务日期，不是生产时间。请求的 `date` 用于选择数据，可能与实际返回的业务日期不同；分析和比较使用实际业务日期。
- search 的 `--date` 是截止日，历史数据从 2026-02 的月末业务观测起，截止日无需月末；实际采用日期看 `resolvedDate`。最新结果是近 30 天画像。
- profile、七种分布和三种集中度的 `--date` 是精确业务日期，未发布该日则为空；省略取最新，响应使用 resolvedDate。
- history 必须传 `--date-from/--date-to`。边界无需月末，但只返回范围内已发布的月末快照，按日期升序。读取 `data[].points[].date`，不是 `data.points[]` 或 `history[]`。当前不完整月份不用于已完成月份趋势，也不补齐缺失月份。
- history 每点的 marketSize 是全市场总量，sampleProfile 是样本总量及 avgPrice、avgMonthlySales、avgMonthlyRevenue、avgRating、avgRatingCount。没有新品、分布历史或 min/max 价格评分字段。
- launch 的范围筛选首次上架日期，使用最新样本，先过滤再按 month/year 分组。读取 `data[].points[]` 中的 date/productCount；其时间身份是首次上架月份或年份，有效回答不要求额外的数据日期，不补造 resolvedDate 或 snapshotDate，也不把上架月份当作样本的数据日期。上架组成不是历史需求曲线。
- profile 的样本统计位于 sampleProfile；分布和集中度在根层返回 sampleProductCount、sampleMonthlySales、sampleMonthlyRevenue 和 sampleAvgPrice、sampleAvgMonthlySales、sampleAvgMonthlyRevenue、sampleAvgRating、sampleAvgRatingCount，桶或排名组使用自己的均值。
- 分布桶使用 bucketProductCount、bucketProductRate、monthlySalesRate/monthlyRevenueRate；实体明细的份额字段现统一为 monthlySalesRate/monthlyRevenueRate。三个集中度接口均用 topnMetrics，实体数组分别为 topProductList/topBrandList/topSellerList。profile 内 concentrationProfile 的 topnBrandMetrics 保持原名。Top N 新品份额的分母是排名组对应的销量或销售额。分布桶不提供新品或品牌集中度子画像。

保留 null、真实 0、空数组和缺失字段的区别；公开小数保持两位，不能从四舍五入后的零份额推断精确零。旧 SKU 基线不能与新口径混用。

`avgRatingCount` 表示样本平均评分数，不等于文字评论数。市场搜索返回 `avgBigBsr30d`，并支持对应筛选和排序；它是样本平均 BSR，与单品 `bsr` 区分。

通用分析的快速回答及完整报告按来源展示业务日期或期间；组合报告不再套用统一 Timestamp 或固定数据新鲜度。上架组成展示首次上架期间，查询时间不能替代数据业务时间。市场参考只保留接口事实，上架组成和历史比较的推断边界统一引用语义模块。

## 计费与发布

search 按次收费，空结果也收费。其余市场接口按实际返回的去重市场数收费，空结果免费；查询前按请求去重市场数及单价检查余额，不预扣。批量不再按固定一次 1 credit 估算，实际账单读取 meta。

共享 CLI 仅修改 canonical 源，经同步脚本分发至 8 个活跃技能；市场分析和通用分析更新白名单，其余技能保持原范围。API 事实留在参考模块，语义、证据投影、输出分别留在其责任模块。

本 PR 更新仓库源文件和测试，未部署服务、未发布 ClawHub 或创建 GitHub Release。既有安装需要单独更新，维护者按仓库发布流程手动执行 clawhub sync。回滚需匹配服务与技能契约，并处理不兼容基线。

逐接口结果和验证限制见[市场接口审计](market-api-contract-audit.md)。
