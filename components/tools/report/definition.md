# Research Report Generator · ZooData

Generate an HTML research report from supplied analysis results. Use this Skill after the analysis is available or when the user asks to present existing results as HTML. Use the findings supplied by the user or the expert. This Skill organizes their presentation without querying data or adding business conclusions.

## Resource responsibilities

| Resource | Responsibility |
|---|---|
| [Presentation rules](../../contract/report.md) | Business language, reading order, data labels and the output checks |
| [Report components](layouts.md) | Supported content blocks and their input structure |
| [Generator](scripts/render_report.py) | Validate component data, embed local images, render charts and fill the template |
| [Page template](assets/template.html) | Shared page structure, styles, responsive layout and print styles |

## Generate and deliver a report

1. Use the confirmed question and available findings. In Expert Sessions, also use that expert's relevant report outline. Read the presentation rules if they are not already loaded. Read the component reference when preparing the report; resolve the linked generator and template by path. Read their source only to diagnose a rendering error.
2. Arrange the relevant content using the documented components. Keep the input JSON and any newly downloaded images in a temporary working directory. Write the finished HTML to the delivery directory. Open the fictional [example](example.json) only for a layout demonstration or when a component input remains unclear.
3. Apply the [whole-report review](../../contract/report.md#review-the-complete-report) to the assembled draft. Correct the JSON content before running the generator.
4. Run `python3 <generator-path> <data.json> <report.html>`, resolving the linked generator relative to this document. Supply only already obtained or user-provided images saved as local files.
5. Open the generated file in an available preview. Check headings, table width, chart labels and image size, then correct any rendering issue. If preview is unavailable, inspect the generated HTML and its embedded resources directly. Do not query more data just to complete presentation.
6. Finish the turn using the [HTML handoff](../../contract/report.md#hand-off-the-html-report) for the actual file-presentation result. If generation fails, correct the reported input or file problem; if it cannot be resolved, state that the HTML file was not produced and deliver the available result in the conversation.
