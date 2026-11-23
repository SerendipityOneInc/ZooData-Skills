#!/usr/bin/env python3
"""Render evidence-backed report JSON as portable HTML; stdlib, no network."""

import argparse
import base64
from datetime import date, timedelta
from html import escape
import json
import math
import re
import runpy
from pathlib import Path


COLORS = ("#16736b", "#e69b38", "#6684bf", "#b36b86", "#738d4c", "#977bb8")
TEMPLATE = Path(__file__).resolve().parents[1] / "assets/template.html"


INTERNAL_MONTH_END_LABEL = re.compile(r"月末(?:数据|目录)?快照|\bmonth[- ]end (?:data )?snapshots?\b", re.I)


def text(value):
    content = str(value)
    if INTERNAL_MONTH_END_LABEL.search(content):
        raise ValueError("Describe the business period using month names or monthly data")
    return escape(content, quote=True)


def display(value, missing):
    return text(missing if value is None else value)


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Chart values must be finite numbers or null")
    return value


def image_data(value, base):
    path = Path(value)
    path = path if path.is_absolute() else base / path
    if path.stat().st_size > 10_000_000:
        raise ValueError("Report image exceeds 10 MB")
    raw = path.read_bytes()
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        mime = "image/png"
    elif raw.startswith(b"\xff\xd8\xff"):
        mime = "image/jpeg"
    else:
        raise ValueError("Report images must be local PNG or JPEG files")
    return "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")


def table(block, missing):
    columns = block["columns"]
    if not 1 <= len(columns) <= 6:
        raise ValueError("Split report tables into one to six columns")
    heading = "<thead><tr>" + "".join('<th scope="col">' + text(c) + "</th>" for c in columns) + "</tr></thead>"
    if "groups" in block:
        groups = block["groups"]
        if "rows" in block or not groups:
            raise ValueError("A grouped table needs groups in place of rows")
        bodies = []
        header_count = len(groups[0]["headers"])
        if not 1 <= header_count < len(columns):
            raise ValueError("A grouped table needs row headers and measure columns")
        for group in groups:
            headers, rows = group["headers"], group["rows"]
            if len(headers) != header_count or not rows:
                raise ValueError("Each group needs the same number of headers and at least one row")
            cells = "".join(f'<th scope="rowgroup" rowspan="{len(rows)}">{display(v, missing)}</th>' for v in headers)
            lines = []
            for row in rows:
                if len(row) + header_count != len(columns):
                    raise ValueError("Grouped row width does not match its columns")
                lines.append("<tr>" + cells + "".join("<td>" + display(v, missing) + "</td>" for v in row) + "</tr>")
                cells = ""
            bodies.append("<tbody>" + "".join(lines) + "</tbody>")
        return '<table class="grouped">' + heading + "".join(bodies) + "</table>"
    body = []
    for row in block["rows"]:
        if len(row) != len(columns):
            raise ValueError("Table row width does not match its columns")
        body.append("<tr>" + "".join("<td>" + display(v, missing) + "</td>" for v in row) + "</tr>")
    return "<table>" + heading + "<tbody>" + "".join(body) + "</tbody></table>"


def chart(block, missing):
    kind, labels, series, unit = block["kind"], block["labels"], block["series"], block["unit"]
    if kind not in {"bar", "line", "pie"} or not labels or not 1 <= len(series) <= 6 or not unit:
        raise ValueError("Chart needs bar/line/pie, labels, one to six series and a unit")
    values = []
    for item in series:
        if not item["name"] or len(item["values"]) != len(labels):
            raise ValueError("Chart series need names and a value for each label")
        values.extend(number(v) for v in item["values"] if v is not None)
    if not values:
        raise ValueError("Chart has no observed numeric values; use a missing-data note")
    legend = "<div class=\"legend\">" + "".join(
        '<span><i class="key" style="background:' + COLORS[i] + '"></i>' + text(s["name"]) + "</span>"
        for i, s in enumerate(series)) + "</div>"
    title = block.get("title", "")
    head = "<figure><figcaption>" + text(title) + " <span class=\"unit\">(" + text(unit) + ")</span></figcaption>"
    if kind == "bar":
        if min(values) < 0:
            raise ValueError("Bar reports require nonnegative values; use a line or table for signed changes")
        high = max(values) or 1
        bars = []
        for j, label in enumerate(labels):
            group = []
            for i, item in enumerate(series):
                v = item["values"][j]
                width = 0 if v is None else v / high * 70
                group.append('<div class="bar-track"><i class="bar" style="width:' + f"{width:.3f}%"
                             + ";background:" + COLORS[i] + '"></i><span class="bar-value">'
                             + display(v, missing) + "</span></div>")
            bars.append('<div class="bar-row"><span>' + text(label) + "</span><div>" + "".join(group) + "</div></div>")
        plot = "".join(bars)
    elif kind == "line":
        if block.get("yScale") == "observed":
            low, high = min(values), max(values)
            margin = (high - low) * 0.1 or max(abs(low) * 0.01, 0.01)
            low, high = low - margin, high + margin
        else:
            low, high = min(0, min(values)), max(0, max(values))
        if high == low:
            high = low + 1
        def px(index):
            return 110 + index * 750 / max(1, len(labels) - 1)
        def py(v):
            return 245 - (v - low) / (high - low) * 210
        radius = 2 if len(labels) > 60 else 4
        marks = []
        for i in range(5):
            v = low + (high - low) * i / 4
            y = py(v)
            marks.append(f'<line x1="110" y1="{y:.2f}" x2="860" y2="{y:.2f}" stroke="#dfe8e3"/>')
            marks.append(f'<text x="100" y="{y+7:.2f}" text-anchor="end">{v:,.1f}</text>')
        indexes = sorted({round(i * (len(labels) - 1) / min(5, len(labels) - 1))
                          for i in range(min(6, len(labels)))}) if len(labels) > 1 else [0]
        for j in indexes:
            marks.append(f'<text x="{px(j):.2f}" y="275" text-anchor="middle">{text(labels[j])}</text>')
        for i, item in enumerate(series):
            run = []
            for j, v in enumerate(item["values"] + [None]):
                if v is None:
                    if run:
                        marks.append('<polyline fill="none" stroke="' + COLORS[i]
                                     + '" stroke-width="3" points="' + " ".join(run) + '"/>')
                    run = []
                    continue
                x, y = px(j), py(v)
                run.append(f"{x:.2f},{y:.2f}")
                marks.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{COLORS[i]}"/>')
        plot = '<svg class="plot" viewBox="0 0 940 300" role="img" aria-label="' + text(title) + '"><g font-family="sans-serif" font-size="24" fill="#52655e">' + "".join(marks) + "</g></svg>"
        for item in series:
            if all(v is None for v in item["values"]):
                plot += '<p class="note">' + text(item["name"]) + ": " + text(missing) + "</p>"
    else:
        if len(series) != 1 or len(labels) > 6 or len(values) != len(labels) or min(values) < 0:
            raise ValueError("Pie requires one complete nonnegative series and at most six exclusive parts")
        total = number(block["total"])
        if total <= 0 or not math.isclose(sum(values), total, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Pie parts must sum to the stated whole")
        offset, wedges, keys = 0, [], []
        for i, (label, v) in enumerate(zip(labels, series[0]["values"])):
            fraction = v / total
            wedges.append(f'<circle cx="150" cy="150" r="100" fill="none" stroke="{COLORS[i]}" stroke-width="75" pathLength="100" stroke-dasharray="{fraction*100:.6f} {100-fraction*100:.6f}" stroke-dashoffset="{-offset*100:.6f}" transform="rotate(-90 150 150)"/>')
            offset += fraction
            keys.append('<span><i class="key" style="background:' + COLORS[i] + '"></i>' + text(label)
                        + ": " + text(v) + f" ({fraction:.1%})</span>")
        plot = '<svg class="plot" style="max-width:300px" viewBox="0 0 300 300" role="img" aria-label="' + text(title) + '">' + "".join(wedges) + '</svg><div class="legend">' + "".join(keys) + "</div>"
        legend = ""
    return head + legend + plot + ("<p class=\"note\">" + text(block["note"]) + "</p>" if block.get("note") else "") + "</figure>"


def daily_history(block, base, missing, lang):
    """Build the line directly from dated observations; the draft supplies no points."""
    if {"labels", "series", "values"} & block.keys():
        raise ValueError("daily-history takes original observations, not draft chart points")
    start, end = (date.fromisoformat(block[key]) for key in ("startDate", "endDate"))
    if end < start:
        raise ValueError("Invalid daily-history period")
    if "source" not in block:
        raise ValueError("daily-history requires a source")
    if block["source"] is None:
        reason = block.get("unavailable")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Supply the original history response or a reason it was unavailable")
        return "<p>" + text(reason) + "</p>"
    # In an installed package the builder places the data module beside this script.
    module = Path(__file__).with_name("summarize_changes.py")
    if not module.is_file():
        module = Path(__file__).resolve().parents[3] / "skill/datas/product-history/summarize_changes.py"
    history = runpy.run_path(str(module))
    response = json.loads((base / block["source"]).read_text(encoding="utf-8"))
    record = history["history_record"](response, block["asin"], start, end)
    _, valid = history["observations"](record, block["field"], start, end, numeric=True)
    if not valid:
        return "<p>" + text(block["title"]) + " · " + text(missing) + "</p>"
    unit = record["currency"] if block["field"] == "price" else block["unit"]
    if len(valid) == 1:
        day, value = valid[0]
        return "<p>" + text(f"{block['title']} · {day} · {value} {unit}") + "</p>"
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    observations = dict(valid)
    points = [observations.get(day) for day in days]
    moves = history["changes_between"](valid)
    up = sum(after > before for (_, before), (_, after) in moves)
    across = sum((day - prev_day).days > 1 for (prev_day, _), (day, _) in moves)
    if lang.startswith("zh"):
        note = f"{len(valid)} 天有记录，观察到 {len(moves)} 次变化，上升 {up} 次、下降 {len(moves)-up} 次。"
        if across:
            note += f"其中 {across} 次跨过缺测日。"
    else:
        note = f"{len(valid)} observed days; {len(moves)} changes ({up} up, {len(moves)-up} down)."
        if across:
            note += f" {across} changes span gaps."
    return chart({"kind": "line", "title": block["title"], "unit": unit, "yScale": "observed",
                  "labels": [day.isoformat() for day in days],
                  "series": [{"name": block["name"], "values": points}], "note": note}, missing)


# Older report drafts used a human-readable label in place of a period marker.
LEGACY_PERIOD_LABELS = {
    "数据口径", "统计期间", "时间范围", "比较期间", "销量月份",
    "data basis", "period", "time range", "comparison period", "sales period",
}
PERIOD_IN_TEXT = re.compile(
    r"\d{4}\s*(?:[-/.年]|$)|\d+\s*(?:天|日|周|月|年|days?\b|weeks?\b|months?\b|years?\b)"
    r"|(?:本|上|当)(?:月|周|年)|\b(?:this|last|current|previous) (?:week|month|year)\b"
    r"|\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|"
    r"aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?\s+\d{4}\b", re.I,
)


def sales_periods(scope):
    periods = []
    for item in scope:
        value = item["value"]
        if not isinstance(value, str) or not value.strip():
            continue
        if item.get("kind") == "period":
            periods.append(value)
        elif item["label"].strip().lower() in LEGACY_PERIOD_LABELS and PERIOD_IN_TEXT.search(value):
            periods.append(value)
    return periods


def product_list(block, base, missing, lang, opening_periods=()):
    """Render comparable products with their complete identity and core measures."""
    zh = lang.startswith("zh")
    labels = {
        "sales": "商品销量（件）" if zh else "Product sales (units)",
        "parentSales": "父体销量（件）" if zh else "Parent sales (units)",
        "price": ("价格" if zh else "Price") + " (" + block["currency"] + ")",
        "rating": "评分（星）" if zh else "Rating (stars)",
        "ratingCount": "评分数（条）" if zh else "Number of ratings",
    }
    if block.get("monthly") is True:
        labels.update(sales="商品月销量（件）" if zh else "Monthly product sales (units)",
                      parentSales="父体月销量（件）" if zh else "Monthly parent sales (units)")
    if not (block.get("period") or opening_periods) or not block.get("items"):
        raise ValueError("A product list needs its sales period and at least one product")
    out = ['<div class="product-list">']
    if block.get("period") and block["period"] not in opening_periods:
        out.append('<p class="note">' + text(block["period"]) + '</p>')
    for item in block["items"]:
        scope = item.get("scope")
        if scope not in ("product", "parent"):
            raise ValueError("Set product scope to product or parent")
        fields = {k: v for k, v in labels.items() if scope == "product" or k != "sales"}
        required = {"image", "title", "brand", "parentAsin", *fields}
        if scope == "product":
            required.add("asin")
        elif item.get("asin") is not None or item.get("sales") is not None:
            raise ValueError("A parent listing cannot supply child ASIN or child sales")
        if required - item.keys():
            raise ValueError("Missing product fields: " + ", ".join(sorted(required - item.keys())))
        picture = None
        if item["image"]:
            try:
                picture = image_data(item["image"], base)
            except (OSError, ValueError):
                pass
        thumb = ('<img alt="' + text(item["title"] or "Product") + '" src="' + picture + '">'
                 if picture else '<span class="no-photo">' + ("暂无图片" if zh else "No image") + '</span>')
        out.append('<article class="product-summary">' + thumb + '<div class="product-info">')
        if item.get("group"):
            out.append('<div class="product-group">' + text(item["group"]) + '</div>')
        if scope == "parent":
            out.append('<div class="product-group">' + ("父体商品" if zh else "Parent listing") + '</div>')
        identity = ("品牌 " if zh else "Brand ") + display(item["brand"], missing)
        if scope == "product":
            identity += (" · 商品 ASIN " if zh else " · Product ASIN ") + display(item["asin"], missing)
        identity += (" · 父体 ASIN " if zh else " · Parent ASIN ") + display(item["parentAsin"], missing)
        out.append('<h3>' + display(item["title"], missing) + '</h3><div class="identifier">'
                   + identity + '</div>')
        note = item.get("visualNote")
        if "representativeFields" in item:
            names = {"image": "图片" if zh else "Photo", "title": "标题" if zh else "Title",
                     "brand": "品牌" if zh else "Brand"}
            supplied = item["representativeFields"]
            if scope != "parent" or not isinstance(supplied, list) or any(key not in names for key in supplied):
                raise ValueError("Declare only image, title or brand as representative fields of a parent")
            visible = [label for key, label in names.items()
                       if key in supplied and (picture if key == "image" else item[key])]
            if visible and zh:
                subject = "、".join(visible[:-1]) + "和" + visible[-1] if len(visible) > 1 else visible[0]
                note = subject + "来自代表款。"
            elif visible:
                note = "From the representative variant: " + ", ".join(visible) + "."
            else:
                note = None
        if note:
            out.append('<small class="identifier">' + text(note) + '</small>')
        out.append('<dl>')
        facts = [(label, item[key]) for key, label in fields.items()]
        facts.extend((fact["label"], fact["value"]) for fact in item.get("facts", []))
        for label, value in facts:
            out.append('<div><dt>' + text(label) + '</dt><dd>' + display(value, missing) + '</dd></div>')
        out.append('</dl>')
        out.append('</div></article>')
    return "".join(out) + '</div>'


def scope_items(items):
    if not isinstance(items, list):
        raise ValueError("scope must be a list of label/value items, one fact per item")
    rows = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("label"), str) or not item["label"].strip() or item.get("value") is None:
            raise ValueError("Each scope item needs a label and an obtained value")
        rows.append("<div><dt>" + text(item["label"]) + "</dt><dd>" + text(item["value"]) + "</dd></div>")
    return '<dl class="report-scope">' + "".join(rows) + "</dl>"


def findings_list(items):
    if (not isinstance(items, list) or not items
            or any(not isinstance(item, str) or not item.strip() for item in items)):
        raise ValueError("Report list needs a nonempty list of finding strings")
    return '<ol class="report-findings">' + "".join(
        "<li>" + text(item) + "</li>" for item in items) + "</ol>"


def validate_content_reuse(data):
    """Reject exact repeated blocks; business meaning still needs a content review."""
    unknown = set(data) - {"title", "expert", "lang", "scope", "metrics", "sections", "footer", "missing_label", "task", "productCoverageNote"}
    if unknown:
        raise ValueError("Unsupported report fields: " + ", ".join(sorted(unknown)))
    cards = [json.dumps(metric, sort_keys=True, ensure_ascii=False, allow_nan=False)
             for metric in data.get("metrics", [])]
    if len(cards) != len(set(cards)):
        raise ValueError("Duplicate headline card: keep one presentation of this content")
    seen = set()
    for section in data["sections"]:
        for block in section["blocks"]:
            # Product lists carry their own identifiers and sales period. A
            # renamed heading alone does not make a second copy a new result.
            if block["type"] == "products":
                scope = None
                content = {key: value for key, value in block.items() if key != "title"}
            else:
                scope = (section.get("parentAsin"), section.get("title"))
                content = block
            signature = (scope, json.dumps(content, sort_keys=True, ensure_ascii=False, allow_nan=False))
            if signature in seen:
                raise ValueError("Duplicate report block: keep one presentation of this content")
            seen.add(signature)


def validate_product_trends(data, requested):
    sections = data["sections"]
    products = [section for section in sections if "parentAsin" in section]
    ids = [section["parentAsin"] for section in products]
    if len(products) > requested or len(set(ids)) != len(ids):
        raise ValueError("Use one trend section per distinct ranked listing")
    if len(products) < requested and not str(data.get("productCoverageNote") or "").strip():
        raise ValueError("Show the ranked products or explain the coverage shortfall")
    if products and (not sections or "parentAsin" in sections[0]):
        raise ValueError("Present the category comparison before product trends")
    for section in products:
        asin = section["parentAsin"]
        if not re.fullmatch(r"[A-Z0-9]{10}", asin) or asin not in section["title"]:
            raise ValueError("Identify the ranked parent ASIN in its section title")
        measures = set()
        for block in section["blocks"]:
            measure = block.get("measure")
            if not measure:
                continue
            kind = block["type"]
            if kind == "text" and any(str(t).strip() for t in block.get("paragraphs", [])):
                measures.add(measure)
            elif measure == "price" and kind == "daily-history" and block.get("field") == "price":
                measures.add(measure)
            elif measure != "price" and kind == "chart" and block.get("kind") == "line":
                measures.add(measure)
        missing = {"sales", "price", "exposure", "bsr", "subBsr"} - measures
        if missing:
            raise ValueError(f"{asin} lacks trend panels: {', '.join(sorted(missing))}")


def render(data, base=Path(".")):
    skill_root = TEMPLATE.parent.parent
    policy = skill_root / "references/report-tasks.json"
    if not policy.is_file() and skill_root.parent.name == "skills":
        policy = skill_root.parent.parent / ".codebuddy-plugin/report-tasks.json"
    if policy.is_file():
        task_rules = json.loads(policy.read_text(encoding="utf-8"))
        task = data.get("task")
        if task not in task_rules:
            raise ValueError("Select a report task: " + ", ".join(task_rules))
        field = task_rules[task]
        if isinstance(field, dict):
            validate_product_trends(data, field["productTrends"])
        elif field:
            sections = [section for section in data["sections"] if any(
                block["type"] == "daily-history" and block.get("field") == field for block in section["blocks"])]
            if len(sections) != 1 or sum(block["type"] in {"daily-history", "chart"}
                                         for block in sections[0]["blocks"]) != 1:
                raise ValueError(f"{task} requires one daily-history {field} block in its own chart section")
    validate_content_reuse(data)
    missing = data.get("missing_label", "未获取" if data.get("lang", "zh-CN").startswith("zh") else "Not obtained")
    body = ['<header><div class="eyebrow">' + text(data["expert"]) + "</div><h1>" + text(data["title"])
            + "</h1>" + scope_items(data["scope"]) + "</header>"]
    if data.get("metrics"):
        body.append('<div class="metrics">' + "".join(
            '<div class="metric"><div class="metric-label">' + text(m["label"]) + '</div><div class="metric-value">'
            + display(m["value"], missing) + '<span class="unit">' + text(m.get("unit", ""))
            + '</span></div><div class="note">' + text(m.get("note", "")) + "</div></div>" for m in data["metrics"]) + "</div>")
    for index, section in enumerate(data["sections"], 1):
        body.append('<section><h2>' + text(f"{index:02d}  {section['title']}") + "</h2>")
        for block in section["blocks"]:
            kind = block["type"]
            if kind == "text":
                body += ["<p>" + text(p) + "</p>" for p in block["paragraphs"]]
            elif kind == "callout":
                for field in ("heading", "evidence"):
                    if not isinstance(block.get(field), str) or not block[field].strip():
                        raise ValueError(f"Conclusion card needs a nonempty {field}")
                body.append('<aside class="conclusion-card"><h3>' + text(block["heading"])
                            + "</h3><p>" + text(block["evidence"]) + "</p></aside>")
            elif kind == "list":
                body.append(findings_list(block["items"]))
            elif kind == "table":
                body.append(table(block, missing))
            elif kind == "daily-history":
                body.append(daily_history(block, base, missing, data.get("lang", "zh-CN")))
            elif kind == "chart":
                body.append(chart(block, missing))
            elif kind == "products":
                body.append(product_list(block, base, missing, data.get("lang", "zh-CN"), sales_periods(data["scope"])))
            elif kind == "profiles":
                body.append('<div class="profiles">')
                for item in block["items"]:
                    pic = ('<img alt="' + text(item["name"]) + '" src="' + image_data(item["image"], base) + '"/>') if item.get("image") else ""
                    body.append('<article class="profile"><div class="profile-head">' + pic + "<div><h3>"
                                + text(item["name"]) + '</h3><div class="identifier">' + text(item["id"]) + "</div></div></div><dl>")
                    for fact in item["facts"]:
                        body.append("<div><dt>" + text(fact["label"]) + "</dt><dd>" + display(fact["value"], missing) + "</dd></div>")
                    body.append("</dl>" + ('<p class="finding">' + text(item["finding"]) + "</p>" if item.get("finding") else "") + "</article>")
                body.append("</div>")
            else:
                raise ValueError("Unknown report block: " + str(kind))
        body.append("</section>")
    if data.get("productCoverageNote"):
        body.append('<p class="note">' + text(data["productCoverageNote"]) + "</p>")
    if data.get("footer"):
        body.append("<footer>" + text(data["footer"]) + "</footer>")
    return inject_template("".join(body), data["title"], data.get("lang", "zh-CN"))


def inject_template(content, title, lang):
    """Fill the owned shell once; substituted user text never becomes a token."""
    template = TEMPLATE.read_text(encoding="utf-8")
    slots = {"LANG": text(lang), "TITLE": text(title), "CONTENT": content}
    if sorted(re.findall(r"\{\{([A-Z]+)\}\}", template)) != sorted(slots):
        raise ValueError("Report template must contain LANG, TITLE and CONTENT once each")
    return re.sub(r"\{\{([A-Z]+)\}\}", lambda match: slots[match.group(1)], template)



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.resolve() in {args.data.resolve(), TEMPLATE.resolve()}:
        parser.error("Output must differ from input and template paths")
    try:
        report = render(json.loads(args.data.read_text(encoding="utf-8")), args.data.resolve().parent)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f"Report generation failed: {error}\n")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
