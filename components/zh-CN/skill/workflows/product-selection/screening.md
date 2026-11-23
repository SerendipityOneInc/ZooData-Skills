<!-- prompt-source: skill/workflows/product-selection/screening.md 0d8840b0107efe976c4a93b432a3f2f384abbef42038e00a8f39e7e9b08cd12e -->

> 英文原文：[原文](../../../../skill/workflows/product-selection/screening.md)

# 筛选候选商品

1. 从用户原话确定商品范围、筛选条件和排名依据。“卖得最多”表示按购买量降序。筛选“近半年上架”或未指定时长的新品时，直接使用 180 天，并在报告范围中注明；价格、销量门槛和配送方式只采用用户提出的条件。
2. 复用已明确的类目、关键词和排序。只澄清会改变结果的缺项：范围不清时确认指定类目或全部类目；类目名称有歧义时用[类目查询](../../datas/category-lookup/definition.md)列出匹配路径；排名依据不清时询问用户想比较哪项指标。
3. 按[商品搜索](../../datas/product-discovery/definition.md)的接口定义，将用户条件映射为有效字段。将范围、一个排序字段及方向、有效筛选条件传给[查询参数脚本](../../../../skill/workflows/product-selection/plan_screening.py)。条件冲突或无法支持时，在查询前确认如何处理。
4. 筛选整个范围的前 N 款时，翻页沿用相同的范围和排序，按原顺序保留不同 ASIN，取足所需数量，标明已观察到的并列。匹配总数取自接口。用户要求各类目分别排名时，在额度内按同一组条件和排序分别查各类目。从总榜部分商品得到的类目统计仅代表样本。

执行 `python3 <planner> <selection.json>`，例如

```json
{"scope":"all","sortBy":"monthlySalesFloor","sortOrder":"desc","filters":{"priceMax":30},"pageSize":10}
```
