<!-- prompt-source: skill/workflows/product-selection/market-research.md 33d2d8d80deea1f0889175d261438311ead1df2674cd2698852d7a1cd8958b90 -->

> 英文原文：[原文](../../../../skill/workflows/product-selection/market-research.md)

# 类目市场研究

1. 用[类目检索](../../datas/category-lookup/definition.md)确定类目。名称匹配到多个不同市场时，列出完整路径请用户选择。用户已要求在指定大类中找机会时，比较该范围内同层级的市场。
2. 筛选类目用[类目市场筛选](../../datas/market-discovery/definition.md)；研究已知市场从[类目画像](../../datas/market-profile/definition.md)开始。分开解读全类目需求与头部样本指标。跨市场比较时对齐日期、类目层级和下级商品范围。
3. 单项问题直接查看相应证据。价格看[价格带](../../datas/market-price-distribution/definition.md)，竞争集中度按问题选择[商品](../../datas/market-top-product-concentrations/definition.md)、[品牌](../../datas/market-brand-concentrations/definition.md)或[卖家](../../datas/market-seller-concentrations/definition.md)。其他类目分布按问题选取：[星级分布](../../datas/market-rating-distributions/definition.md)、[评分数分布](../../datas/market-rating-count-distributions/definition.md)、[上架时长分布](../../datas/market-listing-age-distributions/definition.md)、[配送方式分布](../../datas/market-fulfillment-distributions/definition.md)、[卖家国家分布](../../datas/market-seller-country-distributions/definition.md)、[内容配置分布](../../datas/market-content-distributions/definition.md)。趋势看[市场历史](../../datas/market-history/definition.md)。
4. 找未满足需求时，用[类目评价画像](../../datas/market-review-profile/definition.md)识别买家诉求，按需用已确定代表商品的评论原文佐证。评估进入条件时，列出市场需求、竞争情况及卖家给定的条件。用户询问特定售价的上榜新品时，按相同日期、类目范围和销量样本读取[榜单商品](../../datas/market-top-product-concentrations/definition.md)。按父体首次上架日期和代表售价筛选，列出匹配的父体和所在类目。只取得部分榜单时，未找到可比商品的类目保留为尚无法判断。

## 统计销量榜中的新品

1. 以月销量前 100 个父体为样本。“近半年上架”按榜单日 D 往前 180 天至 D 当天计算，含起止日。
2. 查最新榜单时，先按本次范围调用[类目市场筛选](../../datas/market-discovery/definition.md)，不传日期，取实际榜单日 D。按该上架期间批量查[新品上架构成](../../datas/market-launch-composition/definition.md)。计数结果未附榜单日期，批量查询结束后再核对一次最新榜单日。日期有变时丢弃此次计数，在预算内按新日期重查一次；仍无法对齐时，将计数标为未获取。
3. 用户指定历史榜单，或要求沿用此前报告日期时，按指定日查询市场统计，返回的榜单日不符时，注明指定日期的榜单未获取。日期一致且上架期间吻合时采用汇总数；否则仅在取得完整当期榜单及上架日期时逐款计数。只有部分明细时，注明已确认的数量及覆盖范围。
4. 按同一榜单日、同一范围比较各类目新品数，同值并列。用户需要商品示例或走势时，再取榜单商品明细。

## 上榜新品的成长表现

1. 开头说明类目、上架期间、统计日期和销量前 100 名的范围。各类目均取得相同范围的完整榜单计数时，按上榜新品数比较同级类目；默认各类目包含下级商品，复核已有报告时沿用原报告的范围。
2. 对已确认有新品或新品总数未知的入选类目，用同一日期和统计范围批量取[销量领先商品](../../datas/market-top-product-concentrations/definition.md)。在各类目返回的最多 20 款中，用父体首次上架日期筛出符合本次上架期间的新品。跨类目按父体 ASIN 去重，按父体月销量降序选三款。销量缺失的商品不参与排序，同销量标为并列，取舍时以父体 ASIN 排序。写明“已识别上榜新品中月销量前三”，只有完整覆盖时才称全榜前三。可确认商品不足三款时展示实际数量，说明覆盖缺口。
3. 按榜单中的父体 ASIN 查[该父体的变体](../../datas/listing-members/definition.md)，取已确认属于该父体的代表商品 ASIN。直接对这些已选商品使用[商品走势取数方法](methods.md#trace-how-each-product-grew)，取得月销量、每日价格、周曝光和每日大类与小类排名，按[商品趋势模板](../../../tools/report/product-trends.md)出图。图上区分父体销量与代表变体的表现。以榜单数据日为截止日，最多回看六个月；新品从首次上架起观察。月销量只比较完整月，当月有数据时标明“截至当日”。

## 比较增长市场

1. 确认类目范围。用[类目检索](../../datas/category-lookup/definition.md)列出指定大类的直接子类目；用户明确选择全类目时比较一级类目。同一次比较使用同层级类目，统一包含下级商品。用户只指定一个末级类目时分析它自身的历史，需要加入同级市场时先询问。预算不足以覆盖所选范围时，先与用户缩小范围。
2. 用[市场历史](../../datas/market-history/definition.md)比较全类目月销量（`marketSize.monthlySales`）。用户指定某月或说“上个月”时，先确定目标月及其上一个月。未指定月份时，选有可比数据的最近两个连续完整月，并用最近六个完整月观察走势。所有类目使用同一对月份。缺少任一月份或基期销量小于等于零的类目单独注明，其他类目仍按原月份比较。列出两个月的销量、增加件数和增幅，按增幅对正增长类目降序排列，同值并列。
3. 结合此前月份区分单月跳升、回升和连续增长。基数小时结合增加件数解读增幅。市场判断以类目数据为依据。如果没有可比较的正增长市场，到此交付结果。
4. 用户要求展示增长市场的代表商品时，用[头部商品集中度](../../datas/market-top-product-concentrations/definition.md)取同一月末、同一下级类目范围、按销量选取的样本（`unitSalesTop100`）。父体条目保留榜单返回的父体 ASIN、父体月销量、代表价格、星级和评分数。对增速前三市场，默认每个市场展示销量排名最高的一款，数量以用户要求为准。优先复用已确认的父体标题、品牌和图像；需要补充主图、标题或品牌时，按同一月份读取[父体成员](../../datas/listing-members/definition.md)第一页第一条，使用月购买量下限最高的代表款。用该款补足可用字段，将这些字段名传入 `representativeFields`。条目仍按父体展示，未取得的字段标为未获取。样本占比只说明头部样本内的份额。没有该期数据或商品清单时保留市场结论，注明代表商品未获取。商品举例说明市场里卖什么；仅凭入选商品或同期降价无法解释类目增长的原因。
