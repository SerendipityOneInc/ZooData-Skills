<!-- prompt-source: skill/workflows/competitor-comparison/monthly-purchases.md 708b64a949c9b974e040bab9b55f4bed74dda11553c609b23c63099911da7798 -->

> 英文原文：[原文](../../../../skill/workflows/competitor-comparison/monthly-purchases.md)

# 比较最近三个完整月的购买量

1. 确认美国站和选定的商品 ASIN，自家商品参与比较时也计入。用户指定具体月份时，直接按第 3 步所链接的月度销量数据方法传入指定起止月，按这些月份对齐。用户问“最近三个完整月”时，将各 ASIN 作为独立参数传给[查询计划脚本](../../../../skill/workflows/competitor-comparison/plan_monthly_purchases.py)，按下列步骤处理脚本结果。脚本按月度数据的产出时间（UTC）确定查询月份。
2. 脚本返回 `confirm_asins` 时，请用户提供或选定一至三个不同的有效 ASIN。有候选清单时完整列出，等待选择。返回 `outside_coverage` 时，说明所问月份尚无数据。这两种情况都不发起查询。
3. 返回 `ready` 时，按 ASIN 和月份复用已有数据。预算不足以补齐全部商品时，先请用户选定要查的商品。其余每个缺数据的 ASIN，按脚本给出的参数调用一次 **zoodata-product-sales-trend**。独立流程会话通过[随包的数据技能说明](../../datas/product-sales-trend/definition.md)执行同一操作。
4. 按自然月对齐商品ASIN 与父体的购买量下限，保留各月返回的父 ASIN，保留全部三个月。单个商品查询失败时，保留其余结果并标明缺失的单元格。仅在两个月均有完整数据（pointKind=monthEnd）时比较购买量；返回 monthToDate 的月份标为“数据仍在更新”。
5. 在报告的统计期间写明实际三个月。若刚结束的月份仍在更新，注明该月尚未计入。例如 11 月 2 日的报告写“7 至 9 月，10 月数据尚在更新”。
