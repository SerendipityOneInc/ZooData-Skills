"""Prepare one products/search request from a confirmed screening choice, without network access."""

import json
import math
import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
import sys
from pathlib import Path


SORT_FIELDS = {
    "monthlySalesFloor", "monthlyRevenueFloor", "salesGrowthRate", "bsrGrowthRate",
    "bsr", "price", "rating", "ratingCount", "listingDate", "grossMarginRate",
    "monthlyRevenueGrowthRate", "bsrGrowth",
}
INTEGER_RANGES = {
    "monthlySales", "parentMonthlySales", "bsr", "subBsr", "bsrGrowth", "subBsrGrowth",
    "ratingCount", "variantCount", "qaCount", "monthlyRatingCount", "sellerCount",
}
DECIMAL_RANGES = {
    "monthlyRevenue", "salesGrowthRate", "bsrGrowthRate", "monthlyRevenueGrowthRate",
    "price", "rating", "fbaFee", "ratingToSalesRate", "lqs", "packageWeight", "grossMarginRate",
}
ENUMS = {
    "categoryScope": ("includeChildren", "exactOnly"),
    "ratingFilterTarget": ("self", "mostRated"),
    "keywordMatchType": ("fuzzy", "phrase", "exact"),
}
ARRAY_FILTERS = {
    "packageSizeTypes": ("smallStandard", "largeStandard", "largeBulky", "extraLarge"),
    "fulfillments": ("AMZ", "FBA", "FBM"),
    "badges": ("bestSeller", "amazonChoice", "newRelease", "aPlus", "video"),
    "excludeBadges": ("aPlus", "video"),
    "includeBrands": (), "excludeBrands": (), "includeSellers": (), "excludeSellers": (),
    "buyBoxSellerCountryCodes": (), "excludeKeywords": (),
}
SIGNED_RANGES = {"salesGrowthRate", "bsrGrowthRate", "monthlyRevenueGrowthRate",
                 "bsrGrowth", "subBsrGrowth", "ratingToSalesRate"}


def checked_array(key, values):
    if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
        raise ValueError(f"{key} requires an array of strings.")
    if not values and key in ("packageSizeTypes", "buyBoxSellerCountryCodes"):
        raise ValueError(f"{key} requires at least one value.")
    choices = ARRAY_FILTERS[key]
    if choices and any(v not in choices for v in values):
        raise ValueError(f"{key} accepts only {', '.join(choices)}.")
    if key == "buyBoxSellerCountryCodes" and any(not re.fullmatch("[A-Z]{2}", v) for v in values):
        raise ValueError(f"{key} requires two-letter uppercase country codes.")
    return values


def checked_period(value, today):
    if value == "30d":
        return value
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", value):
        raise ValueError("dateRange requires 30d or a published YYYY-MM.")
    # The prior month's catalog becomes available on the third of the month.
    latest = (today - timedelta(days=2)).replace(day=1) - timedelta(days=1)
    if not "2026-02" <= value <= latest.strftime("%Y-%m"):
        raise ValueError("dateRange is outside the published catalog months.")
    return value


def normalize_filters(overrides):
    if not isinstance(overrides, dict):
        raise ValueError("Supply product filters as an object.")
    filters = {}
    for key, value in overrides.items():
        if key == "listingAge":
            if value is None:
                continue
            if value == "6m":
                value = "180d"
            if value not in ("30d", "90d", "180d", "1y", "2y"):
                raise ValueError("Unsupported listingAge. Choose 30d, 90d, 180d, 1y or 2y.")
            filters[key] = value
            continue
        if key in ARRAY_FILTERS:
            filters[key] = checked_array(key, value)
            continue
        if key == "onlyCategoryRank" and type(value) is not bool:
            raise ValueError("onlyCategoryRank requires a boolean.")
        if key in ENUMS and value not in ENUMS[key]:
            raise ValueError(f"{key} accepts only {', '.join(ENUMS[key])}.")
        if key == "onlyCategoryRank" or key in ENUMS:
            filters[key] = value
            continue
        field = key[:-3]
        if not key.endswith(("Min", "Max")) or field not in INTEGER_RANGES | DECIMAL_RANGES:
            raise ValueError(f"Unsupported product filter: {key}")
        if value is None:
            continue
        try:
            number = Decimal(str(value))
        except InvalidOperation:
            raise ValueError(f"{key} requires a number.") from None
        if not number.is_finite() or not math.isfinite(float(number)):
            raise ValueError(f"{key} requires a finite number.")
        if field not in SIGNED_RANGES and number < 0:
            raise ValueError(f"{key} must be nonnegative.")
        ceiling = {"rating": 5, "grossMarginRate": 1}.get(field)
        if ceiling is not None and number > ceiling:
            raise ValueError(f"{key} must not exceed {ceiling}.")
        if field in INTEGER_RANGES:
            if number != number.to_integral_value():
                raise ValueError(f"{key} requires a whole number.")
            filters[key] = int(number)
        else:
            filters[key] = float(number)
    for key, lower in filters.items():
        if key.endswith("Min") and key[:-3] + "Max" in filters and lower > filters[key[:-3] + "Max"]:
            raise ValueError("Resolve the conflicting bounds for " + key[:-3] + ".")
    if set(filters.get("badges", [])) & set(filters.get("excludeBadges", [])):
        raise ValueError("A badge cannot be both included and excluded.")
    return filters


def prepare(selection):
    """Build a single ordered search from the seller's confirmed scope and conditions."""
    known = {"filters", "scope", "sortBy", "sortOrder", "keyword", "dateRange", "pageSize"}
    if not isinstance(selection, dict) or set(selection) - known:
        raise ValueError("Supply the supported selection fields for Amazon US.")
    filters = normalize_filters(selection.get("filters", {}))

    scope = selection.get("scope")
    if scope == "all" and filters.get("categoryScope") == "exactOnly":
        raise ValueError("exactOnly requires a resolved category path.")
    if scope != "all":
        if (not isinstance(scope, list) or not scope
                or not all(isinstance(part, str) and part.strip() for part in scope)):
            raise ValueError("Confirm all categories or supply one resolved category path.")
        filters["categoryPath"] = scope
    sort = selection.get("sortBy")
    order = selection.get("sortOrder")
    if not isinstance(sort, str) or sort not in SORT_FIELDS or order not in ("asc", "desc"):
        raise ValueError("Supply one supported sort field and its direction.")
    keyword = selection.get("keyword", "")
    if not isinstance(keyword, str):
        raise ValueError("Supply a product keyword as text.")
    keyword = keyword.strip()
    if keyword:
        filters["keyword"] = keyword
    else:
        filters.pop("keywordMatchType", None)

    request = dict(filters, marketplace="US", sortBy=sort, sortOrder=order, page=1)
    if selection.get("dateRange") is not None:
        request["dateRange"] = checked_period(selection["dateRange"], date.today())
    page_size = selection.get("pageSize", 20)
    if type(page_size) is not int or not 1 <= page_size <= 100:
        raise ValueError("Use a page size from 1 to 100.")
    request["pageSize"] = page_size
    return request


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: plan_screening.py SELECTION.json")
    try:
        print(json.dumps(prepare(json.loads(Path(sys.argv[1]).read_text())), ensure_ascii=False))
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
