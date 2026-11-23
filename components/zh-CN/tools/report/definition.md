<!-- prompt-source: tools/report/definition.md 17f187ff6c4564baea269fab9b22afcba75698ce6ef0ea5479151e7d3b5538af -->

> 英文原文：[tools/report/definition.md](../../../tools/report/definition.md)

# 研究报告生成 · ZooData

将已有分析结果制作成 HTML 研究报告。完成分析后，或用户要求将已有结果展示为 HTML 时使用。使用用户或专家提供的分析发现。本 Skill 负责组织展示，不查询数据，不增加业务结论。

## 资源职责

| 资源 | 职责 |
|---|---|
| [呈现规则](../../contract/report.md) | 业务用语、阅读顺序、指标标识和输出检查 |
| [报告组件](layouts.md) | 支持的内容块及其输入结构 |
| [生成工具](../../../tools/report/scripts/render_report.py) | 校验组件数据、嵌入本地图片、绘制图表并填充模板 |
| [商品历史观测](../../../skill/datas/product-history/summarize_changes.py) | 从已保存的商品历史中提取有效观测并统计变更次数 |
| [页面模板](../../../tools/report/assets/template.html) | 公共页面框架、样式、自适应布局和打印样式 |

## 生成和交付报告

1. 使用已确认的问题和已有发现；专家会话还使用该专家当前适用的报告提纲。呈现规则尚未加载时再读取。准备报告时读取组件说明，通过链接定位生成器和模板。仅在诊断渲染错误时读取其源码。
2. 用已定义的组件安排相关内容，将输入 JSON 和本次下载的图片放入临时工作目录，仅将生成的 HTML 写入交付目录。仅在演示版式或组件输入还不明确时读取使用虚构数据的[示例](../../../tools/report/example.json)。
3. 对组装完成的稿件执行[整稿审阅](../../contract/report.md#review-the-complete-report)，修正 JSON 内容后再运行生成工具。
4. 运行 `python3 <generator-path> <data.json> <report.html>`，相对于当前文档定位链接中的生成工具。图片只使用已取得或用户提供、且已保存到本地的文件。
5. 用可用的预览打开生成文件，检查标题、表格宽度、图表标识和图片尺寸，修正显示问题。没有预览能力时，直接检查生成的 HTML 及其内嵌资源。不为完成展示而查询额外数据。
6. 根据文件展示结果，按[HTML 文件交付](../../contract/report.md#hand-off-the-html-report)结束本轮。生成失败时，修正报错指出的输入或文件问题；无法解决时，说明 HTML 文件未生成，并在对话中交付已有结果。
