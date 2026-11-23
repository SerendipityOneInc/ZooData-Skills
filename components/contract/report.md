# Report presentation

These rules cover reports and every user-facing message, including progress and necessary clarification.

## Choose the delivery format

1. For expert reports and standalone workflows with an HTML report outline, deliver one HTML file using the task outline.
2. For standalone data Skills, deliver the selected task's data report as Markdown in the conversation unless the user requests another format. Intermediate Skill results in Expert Sessions feed the final report without creating separate files for every task.
3. Necessary input questions, progress updates and short factual replies stay in the conversation. A new analytical question after delivery receives a focused report using compatible existing evidence. Honor explicit requests for another format.

## Hand off the HTML report

1. Present the finished HTML once. With WorkBuddy’s `present_files`, pass the final HTML file and use its report title as the explanation.
2. When the host confirms that the file was presented, the file card completes delivery. End the turn there. If the host requires final text, send only a short acknowledgment in the conversation language (for example, “报告已生成。”).
3. If file presentation is unavailable or fails, send one working link labeled with the report title. Keep findings, figures and caveats in the HTML. Add a chat summary or extra attachment only if the user explicitly asks for it; a request to analyze or summarize findings in the report does not request a second copy in chat.

## Organize the answer

1. Organize research from the overall scope to its groups, key objects and supported conclusions. Put scope and headline figures at the top, then begin the body with substantive analysis. Use only outline content needed for the confirmed question; the outline is not a workflow requiring every section. Do not repeat the overview or acquire unrelated data to fill the outline.
2. Choose one display for each answer. When a labeled chart or table answers the question, the section can end there. Put units, dates and necessary scope in its labels or legend. Add a business interpretation only if it answers a remaining part of the question with supporting evidence.
3. Write for ordinary business users in plain, direct language. State the specific subject and action or finding, using familiar, consistent business names rather than invented shorthand, figurative wording or vague substitutes. Remove introductory wording and embellishments that do not help explain the result. Throughout the report, present results and necessary interpretations; include acquisition, processing, calculation or validation procedures only when the user explicitly requests them. This applies to every report component.
4. Replace abstract metric names with concrete descriptions of what is measured or compared. Translate returned grades and category labels into the conversation language. Use labels that preserve each metric's meaning, scope and units. Explain only abbreviations or classifications needed to understand the result.
5. Present independent findings as a numbered list, with one finding per item. Keep each item to one or two short sentences. Do not pack unrelated indicators into a paragraph; use a table when several objects share those indicators.
6. Summarize supporting history as the change that matters to the current answer, retaining the period and values needed to understand it. Show full sequences and field-by-field explanations only when requested.
7. End the report once the confirmed question is answered.

## Present objects and data

1. Prefer tables for object lists so the same indicators align in consistent columns. Give each object its own row, with a readable name, identifiers needed to recognize or act on it, and the task's baseline indicators. Keep technical codes internal unless requested. Add other indicators only when they answer the question; honor names-only requests. Use the shared parent or child product template for product lists, candidates and representative items. Display the basic information once per item; subsequent charts or comparisons can identify it by ASIN.
2. Reconcile displayed values, metric labels, units and aggregates to the source records. Give each comparison metric its own labeled row or column, with consistent meaning and units across objects. Split distinct metrics packed into one cell so no value depends on another object's cell to explain what it measures.
3. Label units beside the corresponding values, column headers or chart axes. For dated results, label the actual data date or period returned by the source. Keep the requested period separate when it differs. If the actual date is missing, state the available period only; never substitute the request timestamp. Add denominators or sample scope only when needed to interpret the displayed result. Remove standalone scope notes that do not apply to the current indicators or repeat their existing labels.
4. Display measured zero as zero and unavailable values as not obtained or no data, rather than using the same blank or dash. Label rating counts separately from written-review counts.
5. State a shared sample definition once in the opening scope. For a Top N, give the ranking measure, cutoff and any group with fewer items. Add row-level sample counts only if the user asks for counts or the denominators are needed to interpret the values. Label any other coverage differences beside the affected result. Show an overall count or ranking only when a compatible aggregate or complete coverage supports it; otherwise label the supported sample result. Do not extrapolate a page into the whole result.
6. Present report context as labeled items, one fact per line. Include only the confirmed scope, effective filters and period, order or coverage needed to interpret the result. Derive effective conditions from the actual retrieval and local filtering, not every option in a preset. Omit options whose required inputs are absent, unused settings and technical processing details.
7. Split wide or dense tables, retaining the same object order and business identifiers. If requested facts do not fit a concise comparison, place them beside the relevant analysis without repeating the comparison values.
8. Use detail cards only when the question requires object details beyond the comparison. Include only facts needed to answer that question; an undisplayed field alone does not justify a card. Add available product images when they help identify those objects. Use bounded thumbnails with their original aspect ratio. The product template shows a placeholder for unavailable photos.
9. Make each headline card understandable on its own: name the measured subject, property and metric, and put necessary sample coverage or percentage denominator in that card. Do not rely on another card or "same as above" to explain its value. Table headers must name what is checked; cells must state the observed outcome rather than an unexplained yes/no.

10. In reports and messages, describe the business period and measure. Keep snapshot storage, partitions and retrieval mechanics internal. For completed months use the month names directly; use “monthly data” (“月度数据”) only when the frequency matters. Use year and month for comparisons and trend ranges; retain day precision for actual daily observations or partial-month cutoffs. Label sales for the 30 days ending at month end as “monthly unit sales” (Chinese: “月销量”). Identify the month and units. Retain source qualifiers: show a lower bound as “at least” or N+, an estimate as estimated, and an average as an average.
11. For reports based only on ZooData Amazon US data, use “数据来源：ZooData 亚马逊美国站数据” in Chinese or “Source: ZooData Amazon US data” in English. For mixed sources name the other sources used. State the common observation period once in the opening scope. If the data-basis item already covers it, reuse that item. Label only exceptions locally; retain units and lower bounds with the values.

## Show product purchase volume

1. Show the selected ASIN and the parent listing together for the same measure and period. In dedicated period comparison tables, use the product name and product ASIN (Chinese label: “商品ASIN”) as row headers spanning two rows: “Selected product” and “Parent total”. Use those same scope labels in charts. For product displays use the shared HTML product list. Show both product ASIN and parent ASIN on a child item. A parent-only item identifies the parent ASIN and shows parent sales only. The parent total includes the selected variant. Count each parent only once when aggregating.
2. Compare each scope with its own baseline. Keep the selected sorting metric and scope. Mark missing figures unavailable, preserve zeroes and separate periods belonging to different parents.
3. Use the coverage supplied by the data Skill. For rolling observations outside month end, show the past 30 days and the purchase lower bound, with the actual cutoff if provided. Label a provisional point with its returned month and available cutoff, including when the previous month is still provisional. Use month-over-month growth only for adjacent completed months.

## Present rates and their bases

1. Display growth rates as percentages in filters, tables, charts, cards and prose. Convert once according to the source unit: a decimal 0.1 displays as 10%, and 159.0 as 15,900%. A value already in percent units takes a percent sign directly. Preserve the direction of a decline and display an observed zero as 0%. For other rates or shares, show the percentage and identify its denominator. Express a difference between two shares in percentage points.
2. Identify the subject and metric, and the reference subject or period for the same measure. For rows comparing each product with its own history, label the common baseline in the column header and identify the product in each row. Give standalone cards and findings their own comparison context. For an observed growth rate, show the baseline value, current value and percentage together in one row or card, with units. Prefer observed values. If the metric definition and source precision uniquely determine a missing value, label it as calculated. Otherwise mark it unavailable. For a filter threshold, the comparison basis and percentage suffice.
3. Label an unspecified baseline as unavailable. Relative growth from a zero base is undefined. Show a rate only if supplied or calculable from comparable observations; preserve missing values.

## Describe a share of a total

1. In progress updates and reports, name the component, the total it belongs to and the percentage. For a group, name its members and use their combined share. Add shares only for non-overlapping components of the same population, measure and period. For overlapping components, use a deduplicated group total if available.
2. Apply these labels only to a component’s share of one whole, using the unrounded value. From 0% to below 40% is a minority, 40% to below 60% is roughly on par with the rest, and 60% through 100% is predominant. Show enough precision to keep the displayed percentage in the same band.
3. If the share cannot be established, report only the available figures. A ranking alone supports only the relative order. Interpret growth rates, conversion rates and changes over time using their own metric definitions.

## Use charts and files

1. Use a chart only when it explains the point more clearly than prose or a narrow table. Use lines for changes, bars for comparisons and pies only for mutually exclusive parts of a known whole. Display time series with different units or markedly different scales in vertically stacked charts with matching time labels and independent, labeled value axes; do not use other chart types or dual axes.
2. Identify plotted objects by business identifiers and explain series, colors and abbreviations visibly, without requiring hover. For ranks, state that lower numbers are ahead. Do not label chart row indexes as data ranks.
3. Use source numeric values, leaving missing points as gaps. Use only returned or user-supplied product assets.
4. Combine short text, compact tables and useful charts in the HTML report. Use a responsive layout, readable font sizes, visible headings and print styles; no scripts, external fonts or CDN dependencies. Embed PNG/JPEG image data and inline SVG charts so the file remains readable offline.
5. Use host-supported file links for completed files. Independent Markdown reports use inline charts when supported, otherwise narrow tables or short text.

## Remove inappropriate prompts and caveats

1. Remove any request for sellers to verify ZooData-returned data or any label saying it awaits seller confirmation. Display obtained values as returned; unknown is reserved for information not obtained.
2. Describe missing information or an unresolved data contradiction only when it prevents answering an explicit user question or changes the interpretation of a finding you present. State the specific limitation once beside the affected finding. Omit unrelated unknowns, generic disclaimers and default unresolved-conditions sections.

## Check each message before sending

1. Before sending any visible message, including the first progress update, check its narration against the session's conversation language and the wording rules above. In Expert Sessions, use the language established by the preloaded "Communicate with the user and report progress" instructions; in independent Skill Sessions, use the host conversation language. Preserve original keywords, brands and business identifiers; apply a requested different language only to that deliverable. Correct mismatches before sending. For an expert progress message, apply the preloaded progress rule to the draft before it becomes visible, including messages between tool calls. Remove internal narration and any repeated plan. If nothing remains, skip the message.
2. Before sending any message, check that every shortened name or collective reference maps unambiguously to subjects already identified in the user-visible conversation or earlier in that message. Tool results and internal reasoning do not introduce subjects to the user. If the reference is unclear, introduce the subjects using readable names and any identifiers needed to distinguish them before using that reference. Reuse established names when the context is already clear.

## Review the complete report

1. After drafting the complete content and before rendering or delivering it, reread the title, scope and every section together. Identify the distinct part of the user's question answered by each section. Remove sections with no distinct answer. Name each remaining section for its actual question, comparison or finding, correcting headings that promise content the section does not provide.
2. Read in display order. Introduce objects, groups and necessary metric meanings before using them in interpretations. Put supporting results before or beside the findings that depend on them. Reorder or merge sections when a reader must skip ahead to understand an earlier statement; reconcile contradictory descriptions of the same result.
3. Correct mismatched labels, ambiguous values, population/sample confusion and mixed-metric comparison cells. For each comparison, match the reported measure, population, period and ranking basis to the question. Omit other windows unless they help answer the question. Keep ties on the requested measure unless the user specifies a secondary sort. When the user asks to compare windows, put the requested windows together in one display, including the primary window. Remove ineffective filters. Check every rate and comparison against the percentage and baseline rules above.
4. Read each chart with its title, axes and legend, then read the surrounding cards, tables and prose. Remove repeated values, descriptions of the visible pattern and tables that reproduce the same series. If a table also provides a requested comparison unavailable in the chart, keep the measures needed to read that comparison together and remove the overlapping display. Retain a separate data table when explicitly requested.
5. Correct these issues in the draft before delivery; regenerate HTML when its content changes. Verify the actual file exists and its charts and images are embedded. Review internally without adding a review log to the report or querying additional data.
