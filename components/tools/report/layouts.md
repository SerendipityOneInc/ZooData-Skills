# Report components

The [generator](scripts/render_report.py) accepts structured JSON and fills the shared [template](assets/template.html). Use these components rather than writing page styles. Chapter titles, order and findings come from the current question and selected report outline.

## Fixed structure and content placement

| Position | Content |
|---|---|
| Header | `title`, `expert` and `scope`; the template renders this area once |
| Headline cards | `metrics`, rendered once below the header when supplied |
| Analysis sections | `sections`, in the supplied order, with a title and supported content blocks |
| Optional details | `profiles` blocks inside a relevant analysis section |

1. Map content to these positions using the selected task outline and the shared presentation rules. There is no separate introduction or closing-summary slot; place an explanation inside its relevant section.
2. The generator always supplies one page header. It checks for identical headline cards and repeated blocks within the same product and section. Product lists identify their own subjects and sales period and are checked across sections. The presentation check in the shared rules handles repeated meaning expressed in different words.

## Report data

| Field | Structure |
|---|---|
| `title` | Report title |
| `expert` | Display name of the expert or analysis capability |
| `lang` | Reader's language code, such as `zh-CN` or `en` |
| `scope` | List of `{ "label": "…", "value": "…" }` items, rendered one fact per line |
| `metrics` | Optional headline cards: `{ "label": "…", "value": 120, "unit": "…", "note": "…" }` |
| `task` | Workflow task identifier when required by the selected report outline |
| `sections` | Ordered list of `{ "title": "…", "blocks": […] }` |
| `footer` | Optional short source or closing note |

## Content blocks

| `type` | Required fields | Presentation |
|---|---|---|
| `text` | `paragraphs`: list of strings | A short explanation attached to the relevant result |
| `callout` | `heading` and `evidence`: nonempty strings | A highlighted judgment beside the evidence it interprets. Use a short headline and one or two sentences explaining the decisive comparison. |
| `list` | `items`: nonempty list of strings | Numbered findings, one finding per item |
| `table` | `columns`: one to six labels; `rows`: equal-width value lists, or use `groups` as described below | Comparisons with aligned indicators |
| `chart` | `kind`, `title`, `unit`, `labels`, `series` | Bar, line or pie chart |
| `daily-history` | `title`, `name`, `field`, `asin`, `startDate`, `endDate`, `source` | Dated series from a source JSON file (path relative to report JSON). Use YYYY-MM-DD dates. For price, currency comes from the response. For an unavailable read use `source: null` and a short `unavailable` explanation. |
| `products` | `currency`, `items`, optional `period`; set `monthly: true` for monthly unit sales | Compact product rows with two templates, selected per item by `scope` |
| `profiles` | `items`, each with `name`, `id`, `facts` | Optional object detail cards when the question needs them |

1. Table cells and metric values use strings or numbers. Represent unavailable values with JSON `null`; the generator displays the translated missing-value label. Supply business labels and translated classifications as text.
2. Every chart series has `name` and `values`, with one numeric value or `null` per label. Series in one chart share a unit and comparable scale. Use separate aligned charts for different units or markedly different scales.
3. `bar` accepts nonnegative values. `line` accepts signed values and shows gaps for missing periods. A fully missing series is labeled once. Include individual missing dates only if requested. `pie` accepts one complete nonnegative series of at most six mutually exclusive parts; provide `total` equal to their sum. Set `yScale="observed"` on a line chart to zoom the labeled axis to the observed range; the default includes zero.
4. Profile `facts` contain `label`/`value` pairs. Optional `finding` adds a short interpretation already supported by the analysis. Optional `image` is a local PNG/JPEG path, resolved relative to the JSON file, with a maximum size of 10 MB.
5. Chart `note` and the top-level `missing_label` can provide a reader-language explanation. Numbers, labels and findings are supplied inputs; the generator does not select candidates, compute business indicators or fetch data.

6. For grouped tables, replace `rows` with `groups`. Each group has `headers` (left-hand cells spanning its rows) and `rows` (remaining cells only). Use the same number of headers in every group. For example, with columns Product, ASIN, Scope and Units, supply `{"headers":["Basket","B000000001"],"rows":[["Selected product",50],["Parent total",200]]}`.

See the [layout example](example.json) for a minimal report. The generator rejects unknown block types, inconsistent chart lengths and tables wider than six columns before writing a report.

## Parent and child product templates

Use `type: "products"` for product presentations. Each item has `scope`, full `title`, `brand`, `image`, `parentAsin`, `parentSales`, `price`, `rating` and `ratingCount`. A child (`scope: "product"`) also has its own `asin` and `sales`. For a parent (`scope: "parent"`), omit both child fields. For a parent row, pass the subset of `["image","title","brand"]` obtained from its representative variant as `representativeFields`. The renderer labels the visible fields beside the identity. The parent identifier remains visible on both. Set missing values to null; zero is a measured value. Keep lower bounds such as "800+" and supply the currency. Mark the opening scope item that identifies the sales period with `"kind": "period"` and use any reader-friendly label. Give its value as the actual month, date range or rolling window. Inherit it by omitting block.period. Supply block.period when the product list covers another period or has no common period in the header. Use `group` for a category and optional `facts` for additional labeled measures. Save the returned product photo to a local PNG/JPEG for offline embedding; use null if unavailable. Rows wrap on narrow screens and keep title, brand and all measures together.
