"""Confirm the candidate set before any paid assessment reads."""

import argparse
import json
import re


def scope(asins, *, compare=False):
    selected = list(dict.fromkeys(asin.strip().upper() for asin in asins))
    valid = all(re.fullmatch(r"[A-Z0-9]{10}", asin) for asin in selected)
    if valid and (len(selected) == 1 or compare and 2 <= len(selected) <= 3):
        return {"status": "ready", "asins": selected}
    return {"status": "choose_candidates", "asins": []}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asins", nargs="*")
    parser.add_argument("--compare", action="store_true", help="Seller explicitly selected the ASINs together.")
    args = parser.parse_args()
    print(json.dumps(scope(args.asins, compare=args.compare)))
