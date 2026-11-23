"""Build the read plan for the latest three completed months. No network I/O."""

import argparse
from datetime import date, datetime, timedelta, timezone
import json
import re


def plan(asins, today):
    selected = list(dict.fromkeys(value.strip().upper() for value in asins))
    if not 1 <= len(selected) <= 3 or any(
        not re.fullmatch(r"[A-Z0-9]{10}", asin) for asin in selected
    ):
        return {"status": "confirm_asins", "candidates": selected, "requests": []}

    # The newest served month is provisional, including the prior month on days 1–2.
    provisional = today - timedelta(days=2)
    current = provisional.year * 12 + provisional.month - 1
    months = []
    for index in range(current - 3, current):
        year, month = divmod(index, 12)
        months.append(f"{year:04d}-{month + 1:02d}")
    available = [month for month in months if month >= "2026-02"]
    if not available:
        return {"status": "outside_coverage", "months": months, "requests": []}
    return {
        "status": "ready",
        "months": months,
        "requests": [
            {"asin": asin, "marketplace": "US", "startMonth": available[0], "endMonth": available[-1]}
            for asin in selected
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asins", nargs="*")
    parser.add_argument("--as-of", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    args = parser.parse_args()
    print(json.dumps(plan(args.asins, args.as_of)))
