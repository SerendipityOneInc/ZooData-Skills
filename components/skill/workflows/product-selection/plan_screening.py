"""Prepare one products/search request from a confirmed screening choice, without network access."""

import json
import math
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
OTHER_FILTERS = {
    "onlyCategoryRank", "categoryScope", "ratingFilterTarget", "packageSizeTypes",
    "includeBrands", "excludeBrands", "includeSellers", "excludeSellers", "buyBoxSellerCountryCodes",
    "fulfillments", "badges", "excludeBadges", "excludeKeywords", "keywordMatchType",
}


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
        if key in OTHER_FILTERS:
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
        if field in INTEGER_RANGES:
            if number != number.to_integral_value():
                raise ValueError(f"{key} requires a whole number.")
            filters[key] = int(number)
        else:
            filters[key] = float(number)
    for key, lower in filters.items():
        if key.endswith("Min") and key[:-3] + "Max" in filters and lower > filters[key[:-3] + "Max"]:
            raise ValueError("Resolve the conflicting bounds for " + key[:-3] + ".")
    return filters


def prepare(selection):
    """Build a single ordered search from the seller's confirmed scope and conditions."""
    known = {"filters", "scope", "sortBy", "sortOrder", "keyword", "dateRange", "pageSize"}
    if not isinstance(selection, dict) or set(selection) - known:
        raise ValueError("Supply the supported selection fields for Amazon US.")
    filters = normalize_filters(selection.get("filters", {}))

    scope = selection.get("scope")
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
    if "dateRange" in selection:
        request["dateRange"] = selection["dateRange"]
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
