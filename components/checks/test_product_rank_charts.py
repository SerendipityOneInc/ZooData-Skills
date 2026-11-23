"""Exercise the selection report's daily ranking panels against product history."""

import importlib.util
from pathlib import Path
import unittest


script = Path(__file__).resolve().parents[1] / "tools/report/scripts/rank_charts.py"
spec = importlib.util.spec_from_file_location("rank_charts", script)
ranks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ranks)


class TestProductRankCharts(unittest.TestCase):
    def setUp(self):
        def category(day, node, name):
            return {"date": day, "value": {"nodeId": node, "name": name}}

        self.data = {
            "asin": "B000000001",
            "context": {"requestedDateFrom": "2026-10-01", "requestedDateTo": "2026-10-06",
                        "granularity": "day"},
            "timestamps": ["2026-10-01", "2026-10-03", "2026-10-04", "2026-10-06"],
            "bsr": [12000, 11000, None, 9800], "subBsr": [3, 2, 30, 27],
            "bsrCategory": [category("2026-10-01", None, "Home")],
            "subBsrCategory": [category("2026-10-01", "11", "Baskets"),
                               category("2026-10-04", "12", "Bins")],
        }

    def test_report_window_preserves_previous_category_and_clips_both_axes(self):
        blocks = ranks.rank_blocks(self.data, self.data["asin"], start_date="2026-10-02",
                                   end_date="2026-10-05")
        self.assertTrue(all("10-01" not in str(b) and "10-06" not in str(b) for b in blocks))
        self.assertIn("Home", str(blocks))
        self.assertIn("Baskets", str(blocks))
        with self.assertRaises(ValueError):
            ranks.rank_blocks(self.data, self.data["asin"], start_date="2026-09-30")

    def test_levels_use_separate_axes_and_break_at_missing_days_and_category_changes(self):
        main, first, second = ranks.rank_blocks(self.data, self.data["asin"])
        self.assertEqual([b["title"] for b in (main, first, second)],
                         ["大类排名 · Home", "小类排名 · Baskets", "小类排名 · Bins"])
        self.assertEqual(main["series"][0]["values"], [12000, None, 11000, None, None, 9800])
        self.assertEqual(first["series"][0]["values"], [3, None, 2, None, None, None])
        self.assertEqual(second["series"][0]["values"], [None, None, None, 30, None, 27])
        self.assertEqual(main["labels"], second["labels"])

    def test_unknown_category_and_single_observation(self):
        self.data["bsrCategory"] = []
        self.data["subBsrCategory"][1]["value"] = None
        self.data["subBsr"][0] = None
        main, sub = ranks.rank_blocks(self.data, self.data["asin"], "en")
        self.assertIn("No rank", main["paragraphs"][0])
        self.assertEqual(sub["paragraphs"], ["Subcategory rank · Baskets · 2026-10-03 · #2"])
