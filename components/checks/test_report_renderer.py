"""Portable report rendering and failure behavior; no live data acquisition."""

import base64
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


COMPONENTS = Path(__file__).resolve().parents[1]
REPORT = COMPONENTS / "tools/report"
SCRIPT = REPORT / "scripts/render_report.py"
SPEC = importlib.util.spec_from_file_location("report_renderer", SCRIPT)
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


class TestReportRenderer(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((REPORT / "example.json").read_text())

    def test_example_is_portable_and_preserves_report_order(self):
        html = RENDERER.render(self.data)
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertNotIn("<script", html)
        self.assertNotIn('src="http', html)
        self.assertNotIn('href="http', html)
        self.assertIn("@media print", html)
        indexes = [html.index(section["title"]) for section in self.data["sections"]]
        self.assertEqual(indexes, sorted(indexes))

    def test_product_period_is_explicit_or_identifiable_in_legacy_scope(self):
        for scope in ({"label": "比较期间", "value": "2026 年 10 月"},
                      {"label": "数据口径", "value": "近 30 天"},
                      {"label": "Période", "value": "octobre 2026", "kind": "period"}):
            with self.subTest(scope=scope):
                self.data["scope"] = [scope]
                html = RENDERER.render(self.data)
                self.assertIn(f'<dd>{scope["value"]}</dd>', html)
                self.assertNotIn(f'<p class="note">{scope["value"]}</p>', html)
        for scope in ({"label": "数据口径", "value": "销量为下限"},
                      {"label": "上架时间", "value": "近 180 天"}):
            self.data["scope"] = [scope]
            with self.subTest(scope=scope), self.assertRaisesRegex(ValueError, "sales period"):
                RENDERER.render(self.data)
        self.data["sections"][0]["blocks"][0]["period"] = "2026-09"
        self.assertIn("2026-09", RENDERER.render(self.data))

    def test_all_user_text_is_escaped(self):
        payload = '<script src="https://example.invalid/x">&'
        self.data["title"] = payload
        self.data["sections"] = [{"title": payload, "blocks": [
            {"type": "text", "paragraphs": [payload]},
            {"type": "table", "columns": [payload], "rows": [[payload]]}]}]
        html = RENDERER.render(self.data)
        self.assertNotIn(payload, html)
        self.assertGreaterEqual(html.count("&lt;script"), 5)

    def test_section_conclusion_needs_a_judgment_and_escaped_evidence(self):
        card = {"type": "callout", "heading": "One variant fell", "evidence": "Orders < 100"}
        self.data["sections"] = [{"title": "Sales", "blocks": [card]}]
        html = RENDERER.render(self.data)
        self.assertIn('<aside class="conclusion-card"><h3>One variant fell</h3><p>Orders &lt; 100</p></aside>', html)
        for field in ("heading", "evidence"):
            with self.subTest(field=field):
                self.data["sections"][0]["blocks"] = [{**card, field: " "}]
                with self.assertRaisesRegex(ValueError, field):
                    RENDERER.render(self.data)

    def test_zero_is_not_replaced_with_missing(self):
        html = RENDERER.table({"columns": ["值"], "rows": [[0], [None]]}, "未获取")
        self.assertIn("<td>0</td>", html)
        self.assertIn("<td>未获取</td>", html)

    def test_grouped_table_shares_product_identity_across_measure_rows(self):
        group = {"headers": ["A & B", "B000000001"], "rows": [["Selected", 0], ["Parent", None]]}
        block = {"columns": ["Product", "ASIN", "Scope", "Units"], "groups": [group]}
        html = RENDERER.table(block, "Unavailable")
        self.assertEqual(html.count('scope="rowgroup" rowspan="2"'), 2)
        self.assertEqual(html.count("B000000001"), 1)
        self.assertIn("A &amp; B", html)
        self.assertIn("<td>0</td>", html)
        self.assertIn("<td>Unavailable</td>", html)
        with self.assertRaises(ValueError):
            RENDERER.table({**block, "rows": []}, "Unavailable")
        with self.assertRaises(ValueError):
            RENDERER.table({**block, "groups": [{**group, "rows": [["Parent"]]}]}, "Unavailable")

    def test_template_tokens_in_user_text_remain_literal(self):
        self.data["title"] = "{{CONTENT}} <script>"
        html = RENDERER.render(self.data)
        self.assertIn("<title>{{CONTENT}} &lt;script&gt;</title>", html)
        self.assertEqual(html.count("<header>"), 1)

    def test_duplicate_data_blocks_fail_but_equal_values_for_different_objects_do_not(self):
        duplicate = copy.deepcopy(self.data["sections"][0])
        duplicate["title"] = "重复数据换个章节"
        duplicate["blocks"][0]["title"] = "换个图标题"
        self.data["sections"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "Duplicate report block"):
            RENDERER.render(self.data)
        self.data["sections"] = [{"title": "比较", "blocks": [
            {"type": "table", "columns": ["对象", "数量"], "rows": [["A", 100]]},
            {"type": "table", "columns": ["对象", "数量"], "rows": [["B", 100]]}]}]
        self.assertEqual(RENDERER.render(self.data).count("<table>"), 2)

    def test_fixed_structure_rejects_extra_intro_and_duplicate_headline_cards(self):
        self.data["summary"] = ["重复总览"]
        with self.assertRaisesRegex(ValueError, "Unsupported report fields"):
            RENDERER.render(self.data)
        del self.data["summary"]
        self.data["metrics"].append(copy.deepcopy(self.data["metrics"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate headline card"):
            RENDERER.render(self.data)

    def test_scope_uses_separate_labeled_rows_and_escapes_values(self):
        html = RENDERER.scope_items([{"label": "站点", "value": "美国站"},
                                    {"label": "筛选条件", "value": "价格 < 30"},
                                    {"label": "数量下限", "value": 0}])
        self.assertEqual(html.count("<div><dt>"), 3)
        self.assertEqual(html.count("</dd></div>"), 3)
        self.assertIn("价格 &lt; 30", html)
        self.assertIn("<dd>0</dd>", html)
        for invalid in ("站点：美国｜模式：新品榜", [{"label": "站点"}], [{"label": "", "value": "美国"}]):
            with self.assertRaises(ValueError):
                RENDERER.scope_items(invalid)

    def test_findings_render_as_separate_numbered_items(self):
        from html.parser import HTMLParser

        class FindingsParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.list_count = 0
                self.items = []
                self.in_item = False

            def handle_starttag(self, tag, attrs):
                if tag == "ol" and ("class", "report-findings") in attrs:
                    self.list_count += 1
                if tag == "li":
                    self.items.append("")
                    self.in_item = True

            def handle_endtag(self, tag):
                if tag == "li":
                    self.in_item = False

            def handle_data(self, value):
                if self.in_item:
                    self.items[-1] += value

        items = ["销量增长率均为 700%。", '价格 < 30 美元，品牌名包含 <script>。']
        self.data["sections"] = [{"title": "比较结果", "blocks": [
            {"type": "list", "items": items}]}]
        html = RENDERER.render(self.data)
        parser = FindingsParser()
        parser.feed(html)
        self.assertEqual(parser.list_count, 1)
        self.assertEqual(parser.items, items)
        self.assertNotIn("<script>", html)
        self.assertNotIn("<p>", html)

    def test_empty_or_nontext_findings_fail_before_writing(self):
        for invalid in ([], "一条发现", [None], [0], ["  "]):
            self.data["sections"] = [{"title": "发现", "blocks": [
                {"type": "list", "items": invalid}]}]
            with self.subTest(items=invalid):
                with self.assertRaisesRegex(ValueError, "nonempty list"):
                    RENDERER.render(self.data)

    def test_images_are_embedded_and_not_remote_dependencies(self):
        # Valid 1x1 PNG, only used to test portable embedding.
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jF1sAAAAASUVORK5CYII=")
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "product.png").write_bytes(png)
            self.data["sections"].append({"title": "商品详情", "blocks": [{
                "type": "profiles", "items": [{"name": "示例商品", "id": "DEMO-A",
                                                 "facts": [], "image": "product.png"}]}]})
            html = RENDERER.render(self.data, base)
            self.assertIn('src="data:image/png;base64,', html)
            self.assertIn("object-fit:contain", html)
            (base / "bad.svg").write_text('<svg onload="alert(1)"/>')
            with self.assertRaisesRegex(ValueError, "PNG or JPEG"):
                RENDERER.image_data("bad.svg", base)

    def test_observed_line_scale_keeps_price_labels_and_missing_days(self):
        block = {"kind": "line", "unit": "USD", "labels": ["May 1", "May 2", "May 3"],
                 "series": [{"name": "Price", "values": [18, None, 20]}]}
        self.assertIn(">0.0</text>", RENDERER.chart(block, "Missing"))
        result = RENDERER.chart({**block, "yScale": "observed"}, "Missing")
        self.assertIn(">17.8</text>", result)
        self.assertIn(">20.2</text>", result)
        self.assertEqual(result.count("<polyline"), 2)

    def test_missing_line_points_break_connections(self):
        block = {"kind": "line", "title": "需求变化", "unit": "次/周", "labels": ["甲", "乙", "丙", "丁"],
                 "series": [{"name": "词 A", "values": [2, None, 0, 3]}]}
        html = RENDERER.chart(block, "未获取")
        self.assertEqual(html.count("<polyline"), 2)
        self.assertEqual(html.count("<circle"), 3)
        self.assertNotIn("未获取", html)
        block["series"].append({"name": "词 B", "values": [None] * 4})
        self.assertIn("词 B: 未获取</p>", RENDERER.chart(block, "未获取"))
        self.assertIn("次/周", html)
        self.assertIn("词 A", html)
        self.assertNotIn("<table", html)
        self.assertNotIn("<details", html)

    def test_pie_requires_exclusive_complete_parts_of_stated_whole(self):
        block = {"kind": "pie", "title": "类目分布", "unit": "个", "labels": ["甲", "乙"],
                 "series": [{"name": "商品", "values": [3, 1]}], "total": 4}
        self.assertIn("75.0%", RENDERER.chart(block, "未获取"))
        for values, total in (([3, 1], 5), ([3, None], 3), ([-1, 2], 1), ([0, 0], 0)):
            candidate = copy.deepcopy(block)
            candidate["series"][0]["values"], candidate["total"] = values, total
            with self.assertRaises(ValueError):
                RENDERER.chart(candidate, "未获取")

    def test_bad_charts_and_wide_tables_fail_before_delivery(self):
        base = {"kind": "bar", "title": "商品数", "unit": "个", "labels": ["甲"],
                "series": [{"name": "商品", "values": [1]}]}
        for values in ([float("nan")], [float("inf")], [True], [None], [1, 2], [-1]):
            candidate = copy.deepcopy(base)
            candidate["series"][0]["values"] = values
            with self.assertRaises(ValueError):
                RENDERER.chart(candidate, "未获取")
        with self.assertRaisesRegex(ValueError, "one to six"):
            RENDERER.table({"columns": list("1234567"), "rows": []}, "未获取")
        with self.assertRaisesRegex(ValueError, "row width"):
            RENDERER.table({"columns": ["甲"], "rows": [[1, 2]]}, "未获取")

    def test_cli_generates_one_file_and_does_not_clobber_input(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            data = base / "report.json"
            data.write_text(json.dumps(self.data))
            result = subprocess.run([sys.executable, str(SCRIPT), str(data), str(base / "report.html")],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("<!doctype html>", (base / "report.html").read_text())
            before = data.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(data), str(data)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(data.read_bytes(), before)
            broken = base / "broken.json"
            broken.write_text('{}')
            result = subprocess.run([sys.executable, str(SCRIPT), str(broken), str(base / "bad.html")], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((base / "bad.html").exists())


if __name__ == "__main__":
    unittest.main()
