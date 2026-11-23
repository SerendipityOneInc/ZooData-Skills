<!-- prompt-source: tools/report/layouts.md f416bd5be3b47cfde0a7292f7f4c99fd73b60fc957cae4a730cc44abcef8f6e5 -->

> 英文原文：[tools/report/layouts.md](../../../tools/report/layouts.md)

# 报告组件

[生成工具](../../../tools/report/scripts/render_report.py)读取结构化 JSON 并填充公共[模板](../../../tools/report/assets/template.html)。使用这些组件，不另写页面样式。章节标题、顺序和发现由当前问题及所选报告提纲确定。

## 固定结构与内容位置

| 位置 | 内容 |
|---|---|
| 页首 | `title`、`expert` 和 `scope`，由模板统一渲染一次 |
| 关键数量卡片 | `metrics`，有内容时在页首下方渲染一次 |
| 分析章节 | `sections`，按传入顺序展示，每节包含标题和支持的内容块 |
| 可选详情 | 相关分析章节内部的 `profiles` 内容块 |

1. 按本次任务的提纲及公共呈现规则，将内容安排到上述位置。不另设介绍或结尾总结位置，解释放在对应章节内。
2. 生成工具统一提供一个页首。生成器校验完全相同的数量卡片，以及同一商品、同一章节内重复的内容块。商品清单自带标识和销量期间，跨章节也只展示一次。措辞不同但含义重复的内容，由公共规则中的呈现检查处理。

## 报告数据

| 字段 | 结构 |
|---|---|
| `title` | 报告标题 |
| `expert` | 专家或分析能力的展示名称 |
| `lang` | 读者语言代码，例如 `zh-CN` 或 `en` |
| `scope` | `{ "label": "…", "value": "…" }` 条目列表，每条信息渲染为一行 |
| `metrics` | 可选的数量卡片：`{ "label": "…", "value": 120, "unit": "…", "note": "…" }` |
| `task` | 所选报告提纲要求时，填写本次选定的工作流任务标识 |
| `sections` | 有序章节列表：`{ "title": "…", "blocks": […] }` |
| `footer` | 可选的简短来源或结束说明 |

## 内容块

| `type` | 必要字段 | 展示形式 |
|---|---|---|
| `text` | `paragraphs`：字符串列表 | 紧邻相关结果的简短解释 |
| `callout` | `heading` 和 `evidence`，均为非空文本 | 正文结论卡，紧贴相关图表或事实。标题点明判断，正文用一两句话写清决定这一判断的证据。 |
| `list` | `items`：非空字符串列表 | 编号发现列表，每项一条发现 |
| `table` | `columns`：一至六个列名；`rows`：等宽数值列表；分组表改用下述 `groups` | 指标对齐的比较表 |
| `chart` | `kind`、`title`、`unit`、`labels`、`series` | 柱状图、折线图或饼图 |
| `daily-history` | `title`、`name`、`field`、`asin`、`startDate`、`endDate`、`source` | 从原始 JSON 响应文件读取日序列，路径相对于报告 JSON。起止日使用 YYYY-MM-DD。价格币种来自原始响应；取数不可用时填 `source: null` 和简短的 `unavailable` 原因。 |
| `products` | `currency`、`items`，可选 `period`；月销量使用 `monthly: true` | 每行一个商品，按每项的 `scope` 选父体或子体模板 |
| `profiles` | `items`，每项包含 `name`、`id`、`facts` | 当前问题需要时使用的可选对象详情卡片 |

1. 表格单元格和卡片数值使用字符串或数字。未取得的值用 JSON `null`，工具显示对应语言的缺失提示。业务名称和已翻译的分级以文字传入。
2. 每组图表序列包含 `name` 和 `values`；每个标签对应一个数值或 `null`。同图序列使用相同单位和可比较的量级。单位不同或量级差异明显时，拆成时间对齐的独立图表。
3. `bar` 接收非负数；`line` 接收正负数，缺少记录的期间用断线表示。整组数据都缺失时只标注一次。仅当用户要求时列出具体缺失日期。`pie` 接收一组完整、非负且互斥的组成项，最多六项，`total` 必须等于各项合计。 折线图可传 `yScale="observed"` 将纵轴缩放到有效数据附近，刻度仍显示实际数值；默认包含零点。
4. 详情卡片的 `facts` 使用 `label`/`value` 对。可选的 `finding` 补充分析已有依据支持的简短解读；可选的 `image` 是本地 PNG/JPEG 路径，相对于 JSON 文件定位，大小不超过 10 MB。
5. 图表 `note` 和顶层 `missing_label` 可提供读者语言的说明。数字、名称和发现均来自输入；工具不筛选候选、不计算业务指标，也不获取数据。

6. 分组表用 `groups` 替代 `rows`。每组的 `headers` 提供左侧跨行表头，`rows` 只填写右侧各行的值。每组表头数量相同。例如“商品、ASIN、范围、件数”四列中的一组写作 `{"headers":["收纳篮","B000000001"],"rows":[["本商品",50],["父体合计",200]]}`。

最小报告见[版式示例](../../../tools/report/example.json)。工具在写文件前拒绝未知内容块类型、序列长度不一致的图表及超过六列的表格。

## 父体与子体商品模板

商品展示使用 `type: "products"`。两种模板均传 `scope`、完整标题 `title`、品牌 `brand`、图片 `image`、父体 ASIN `parentAsin`、父体销量 `parentSales`、价格 `price`、星级 `rating` 和评分数 `ratingCount`。子体（`scope: "product"`）另传商品 ASIN `asin` 和商品销量 `sales`。父体（`scope: "parent"`）省去这两项，保留父体 ASIN。父体条目将取自代表款的字段以 `representativeFields` 传入，可选 `image`、`title`、`brand`。模板在标识旁自动注明实际展示了哪些代表款信息。缺项填 null，实测零值填 0。下限保留“800+”等标记。每组标明币种。在页首说明销量期间的条目上设置 `"kind": "period"`，显示名称按问题选用，值写明实际月份、日期区间或滚动窗口。商品列表与页首期间相同时省略 `period`；期间不同或页首没有共同期间时填写该列表的 `period`。`group` 可放类目，`facts` 可放本次比较另需的指标。将接口返回的商品图保存为本地 PNG/JPEG 供离线嵌入，未取得时传 null。窄屏自动换行，标题、品牌和指标放在同一个商品条目内。
