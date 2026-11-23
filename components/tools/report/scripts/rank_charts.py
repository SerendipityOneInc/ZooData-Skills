"""Build main- and subcategory rank blocks from a saved products/history response."""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path


def rank_blocks(data, asin, lang="zh-CN", *, start_date=None, end_date=None):
    zh = lang.startswith("zh")
    levels = (("bsr", "大类排名" if zh else "Main category rank"),
              ("subBsr", "小类排名" if zh else "Subcategory rank"))
    if data is None:
        return [{"type": "text", "measure": field, "observationCount": 0,
                 "paragraphs": [level + (" · 所选期间未获取排名" if zh else " · No rank for this period")]}
                for field, level in levels]
    context = data["context"]
    if data["asin"] != asin or context["granularity"] != "day":
        raise ValueError("Expected daily product history for the selected ASIN")
    first, last = (date.fromisoformat(context[key]) for key in ("requestedDateFrom", "requestedDateTo"))
    start = date.fromisoformat(start_date) if start_date else first
    end = date.fromisoformat(end_date) if end_date else last
    if not first <= start <= end <= last:
        raise ValueError("Report dates must be within the requested history period")
    labels = [(start + timedelta(days=i)).isoformat() for i in range((end - start).days + 1)]
    stamps = data["timestamps"]
    if len(stamps) != len(set(stamps)):
        raise ValueError("Duplicate observation day")

    blocks = []
    for field, level in levels:
        ranks = data.get(field) or []
        if ranks and len(ranks) != len(stamps):
            raise ValueError(f"{field} must align with timestamps")
        observed = dict(zip(stamps, ranks))
        events = sorted(data.get(field + "Category") or [], key=lambda entry: entry["date"])
        event_index = 0
        segments = []
        active = None
        current = None
        for index, day in enumerate(labels):
            while event_index < len(events) and events[event_index]["date"] <= day:
                current = events[event_index]["value"]
                event_index += 1
            category = current or {}
            identity = category.get("nodeId") or category.get("link") or category.get("name")
            if identity != active:
                active = identity
                if active:
                    name = category.get("name") or str(active)
                    segments.append((name, [None] * len(labels)))
            rank = observed.get(day)
            if active and rank is not None and rank > 0:
                segments[-1][1][index] = rank

        known = [(name, values) for name, values in segments if any(v is not None for v in values)]
        if not known:
            note = f"{level} · 未获取可对应到具体类目的名次" if zh else f"{level} · No rank with an identified category"
            blocks.append({"type": "text", "measure": field, "observationCount": 0, "paragraphs": [note]})
        for name, values in known:
            title = f"{level} · {name}"
            points = [(d, v) for d, v in zip(labels, values) if v is not None]
            if len(points) == 1:
                day, rank = points[0]
                blocks.append({"type": "text", "measure": field, "observationCount": 1, "paragraphs": [f"{title} · {day} · #{rank}"]})
                continue
            blocks.append({"type": "chart", "measure": field, "kind": "line", "title": title,
                           "unit": "名次，越小越靠前" if zh else "Rank, lower is better",
                           "yScale": "observed", "labels": labels,
                           "series": [{"name": name, "values": values}]})
    return blocks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    parser.add_argument("asin")
    parser.add_argument("--lang", default="zh-CN")
    parser.add_argument("--start-date", help="First report day (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Last report day (YYYY-MM-DD)")
    args = parser.parse_args()
    response = json.loads(args.history.read_text(encoding="utf-8"))
    record = response["data"]
    if response.get("success") is False or (record is None and response.get("success") is not True):
        parser.exit(1, "Expected a successful product history response\n")
    print(json.dumps(rank_blocks(record, args.asin, args.lang, start_date=args.start_date,
                                 end_date=args.end_date), ensure_ascii=False))
