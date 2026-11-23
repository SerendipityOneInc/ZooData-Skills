"""Summarize dated observations from one saved products/history response."""

import argparse
from datetime import date
import json
import math
from pathlib import Path


def observations(record, field, start, end):
    series = record.get(field)
    if series is None:
        return None, []
    if not isinstance(series, list):
        raise ValueError(f"Expected an array for {field}")
    if field == "price":
        dates = record["timestamps"]
        if not isinstance(dates, list) or len(dates) != len(series):
            raise ValueError("Price and timestamp arrays must be aligned")
        pairs = zip(dates, series)
    else:
        pairs = ((event["date"], event["value"]) for event in series)
    by_day = {}
    for stamp, value in pairs:
        day = date.fromisoformat(stamp)
        if day > end or (field == "price" and day < start) or value is None or value == "":
            continue
        if field == "price":
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError("Expected a numeric price")
        elif not isinstance(value, str):
            raise ValueError(f"Expected text for {field}")
        if day in by_day and by_day[day] != value:
            raise ValueError(f"Conflicting {field} observations on {stamp}")
        by_day[day] = value
    points = sorted(by_day.items())
    in_window = [point for point in points if point[0] >= start]
    baseline = next((point for point in reversed(points) if point[0] < start), None)
    return baseline, in_window


def summarize(response, asin, start, end, fields):
    if not isinstance(response, dict):
        raise ValueError("Expected a saved products/history response object")
    if response.get("success") is False:
        raise ValueError("The history read failed")
    record = response.get("data")
    if not isinstance(record, dict) or not isinstance(record.get("context"), dict):
        raise ValueError("Use the original response with data.asin and data.context "
                         "(granularity, requestedDateFrom, requestedDateTo)")
    context = record["context"]
    if record["asin"] != asin or context["granularity"] != "day":
        raise ValueError("Expected daily history for the requested ASIN")
    first = date.fromisoformat(context["requestedDateFrom"])
    last = date.fromisoformat(context["requestedDateTo"])
    if not first <= start <= end <= last:
        raise ValueError("Requested dates are outside the saved response")
    result = {"asin": asin, "startDate": start.isoformat(), "endDate": end.isoformat(),
              "fields": {}, "changes": []}
    for field in dict.fromkeys(fields):
        baseline, points = observations(record, field, start, end)
        comparable = [baseline, *points] if baseline else points
        count = 0
        for (before_date, before), (after_date, after) in zip(comparable, comparable[1:]):
            if before != after:
                result["changes"].append({"field": field, "beforeDate": before_date.isoformat(),
                                          "before": before, "afterDate": after_date.isoformat(), "after": after})
                count += 1
        result["fields"][field] = {
            "observations": len(points),
            "firstObserved": points[0][0].isoformat() if points else None,
            "lastObserved": points[-1][0].isoformat() if points else None,
            "observedChanges": count if len(comparable) >= 2 else None,
        }
        if field == "price":
            result["fields"][field]["currency"] = record.get("currency")
    result["changes"].sort(key=lambda row: row["afterDate"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path)
    parser.add_argument("asin")
    parser.add_argument("start", type=date.fromisoformat)
    parser.add_argument("end", type=date.fromisoformat)
    parser.add_argument("fields", nargs="+", choices=["price", "title", "imageUrl"])
    args = parser.parse_args()
    try:
        result = summarize(json.loads(args.response.read_text(encoding="utf-8")), args.asin,
                           args.start, args.end, args.fields)
    except (OSError, KeyError, TypeError, ValueError) as error:
        parser.exit(1, f"Cannot summarize history: {error}\n")
    print(json.dumps(result, ensure_ascii=False))
