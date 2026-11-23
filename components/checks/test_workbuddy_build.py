"""Verify native submission artifacts, independent resources and install bindings."""

from datetime import date
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


COMPONENTS = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workbuddy_builder", COMPONENTS / "build_workbuddy.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
MANIFEST = BUILDER.read_json(COMPONENTS / "targets.json")
PLATFORM = BUILDER.read_json(COMPONENTS / "workbuddy.json")


def metadata(content):
    """Read the builder's YAML mapping of JSON-compatible field values."""
    text = content.decode("utf-8")
    header = text.split("---\n", 2)[1]
    return {key: value if key == "name" else json.loads(value) for key, value in
            (line.split(": ", 1) for line in header.strip().splitlines())}


class TestWorkBuddyBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix="workbuddy-build-tests-")
        cls.output = (Path(cls.workspace.name) / "release").resolve()
        cls.report = BUILDER.build(cls.output, include_components=True)

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def test_keyword_expert_loads_workflow_and_shares_all_workflow_files(self):
        name = "zoodata-keyword-research"
        plugin_root = self.output / "experts" / name
        plugin = BUILDER.read_json(plugin_root / ".codebuddy-plugin/plugin.json")
        agent = metadata((plugin_root / plugin["agents"][0]).read_bytes())
        self.assertEqual(agent["skills"], [name, MANIFEST["report_skill"]["export_name"]])
        workflow = MANIFEST["workflows"]["keyword-research"]
        data_names = {MANIFEST["endpoint_skills"][key]["export_name"] for key in workflow["data_skills"]}
        self.assertEqual({Path(path).name for path in plugin["skills"]}, set(agent["skills"]) | data_names)
        source = self.output / "skills" / name
        embedded = plugin_root / "skills" / name
        def contents(root):
            return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        self.assertEqual(contents(source), contents(embedded))
        for language in ("en", "zh"):
            prompts = [q[language] for q in plugin["quickPrompts"]]
            self.assertEqual(prompts, metadata((source / "SKILL.md").read_bytes())["examples_" + language])

    def test_all_submission_zips_include_their_hidden_files_and_match_loose_files(self):
        artifacts = self.report["artifacts"]
        expected_count = sum(len(MANIFEST[key]) for key in
                             ("professionals", "endpoint_skills", "workflows", "experts")) + 2
        self.assertEqual(len(artifacts), expected_count)
        self.assertFalse(self.report["platform_publication_performed"])
        self.assertFalse(self.report["live_binding_verified"])
        for artifact in artifacts:
            archive = self.output / artifact["zip"]
            root = self.output / artifact["kind"] / artifact["name"]
            with self.subTest(package=artifact["name"]), zipfile.ZipFile(archive) as bundle:
                expected = {artifact["name"] + "/" + str(path.relative_to(root))
                            for path in root.rglob("*") if path.is_file()}
                self.assertEqual(set(bundle.namelist()), expected)
                for entry in bundle.namelist():
                    self.assertNotIn("..", Path(entry).parts)
                    self.assertEqual(bundle.read(entry), (root.parent / entry).read_bytes())

    def test_report_generator_dependency_belongs_to_expert_archives(self):
        report_name = MANIFEST["report_skill"]["export_name"]
        for artifact in self.report["artifacts"]:
            name = artifact["name"]
            with self.subTest(package=name), zipfile.ZipFile(self.output / artifact["zip"]) as bundle:
                if artifact["kind"] == "experts":
                    plugin = json.loads(bundle.read(f"{name}/.codebuddy-plugin/plugin.json"))
                    self.assertIn(f"./skills/{report_name}", plugin["skills"])
                    for relative in plugin["agents"]:
                        agent = bundle.read(f"{name}/{relative.removeprefix('./')}")
                        self.assertIn(report_name, metadata(agent)["skills"])
                    entry = bundle.read(f"{name}/skills/{report_name}/SKILL.md")
                    self.assertEqual(metadata(entry)["name"], report_name)
                elif artifact["kind"] == "skills" and name != report_name:
                    for path in bundle.namelist():
                        if path.endswith(".md"):
                            self.assertNotIn(report_name.encode(), bundle.read(path), path)

    def test_standalone_skill_archives_fit_two_directory_levels(self):
        for artifact in self.report["artifacts"]:
            if artifact["kind"] != "skills":
                continue
            with self.subTest(skill=artifact["name"]), zipfile.ZipFile(
                    self.output / artifact["zip"]) as bundle:
                too_deep = [entry for entry in bundle.namelist()
                            if len(PurePosixPath(entry).parent.parts) > 2]
                self.assertFalse(too_deep, f"WorkBuddy rejects nested references: {too_deep[:3]}")

    def test_embedded_skills_match_standalone_skill_contents_and_depth(self):
        for root in (self.output / "experts").iterdir():
            if not root.is_dir():
                continue
            plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
            expert_id = next(key for key, item in PLATFORM["experts"].items() if item["name"] == root.name)
            workflow_key = MANIFEST["experts"][expert_id].get("workflow")
            for relative in plugin["skills"]:
                skill_root = root / relative
                standalone = self.output / "skills" / skill_root.name
                actual = {str(path.relative_to(skill_root)): path.read_bytes()
                          for path in skill_root.rglob("*") if path.is_file()}
                expected = {str(path.relative_to(standalone)): path.read_bytes()
                            for path in standalone.rglob("*") if path.is_file()}
                workflow_config = MANIFEST["workflows"].get(workflow_key, {})
                if workflow_config.get("bind_mcp_tools") and skill_root.name in {
                        MANIFEST["endpoint_skills"][key]["export_name"] for key in workflow_config["data_skills"]}:
                    expected["SKILL.md"] = BUILDER.bind_mcp_operations(
                        expected["SKILL.md"].decode(), PLATFORM["connector"]["source"]).encode()
                if skill_root.name == MANIFEST["report_skill"]["export_name"] and workflow_key:
                    workflow = MANIFEST["workflows"][workflow_key]["export_name"]
                    example = "references/example.json"
                    expected[example] = (self.output / "skills" / workflow / example).read_bytes()
                with self.subTest(expert=root.name, skill=skill_root.name):
                    self.assertEqual(actual, expected)
                    self.assertTrue(all(len(PurePosixPath(path).parts) <= 2
                                        for path in actual))

    def test_skills_have_workbuddy_metadata_and_self_contained_references(self):
        required = {"name", "display_name", "display_name_en", "description",
                    "description_zh", "description_en", "version", "author"}
        for domain, component in MANIFEST["professionals"].items():
            root = self.output / "skills" / component["export_name"]
            entry = (root / "SKILL.md").read_bytes()
            fields = metadata(entry)
            with self.subTest(domain=domain):
                self.assertTrue(required <= set(fields))
                self.assertEqual(fields["name"], root.name)
                self.assertEqual(fields["version"], MANIFEST["source_version"])
                self.assertEqual(fields["author"], PLATFORM["author"]["name"])
                self.assertEqual(fields["description"], component["description"])
                for key in ("description_zh", "description_en", "examples_zh", "examples_en"):
                    self.assertEqual(fields[key], PLATFORM["professionals"][domain][key])
                for reference in re.findall(r"@([a-zA-Z0-9_./-]+)", entry.decode()):
                    self.assertTrue((root / reference).is_file(), reference)
                for path in root.rglob("*.md"):
                    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                        if target.startswith(("https://", "http://", "#", "mailto:")):
                            continue
                        resolved = (path.parent / target.split("#", 1)[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(root))
                        self.assertTrue(resolved.is_file(), target)
                self.assertFalse((root / "references/contracts-api-reference.md").exists())
                eager = set(re.findall(r"@([a-zA-Z0-9_./-]+)", entry.decode()))
                self.assertEqual(eager, {
                    f"references/skills-{domain}-definition.md",
                    "references/contracts-evidence.md",
                    "references/contracts-reporting.md",
                })
                names = {str(path.relative_to(root)) for path in root.rglob("*")}
                self.assertFalse(any(part in name.split("/") for name in names
                                     for part in ("agent-core", "experts", "checks")))

    def test_standalone_comparison_resolves_data_tasks_without_other_installed_skills(self):
        workflow = MANIFEST["workflows"]["competitor-comparison"]
        root = self.output / "skills" / workflow["export_name"]
        self.assertEqual(metadata((root / "SKILL.md").read_bytes())["name"], root.name)
        for page in root.rglob("*.md"):
            for target in BUILDER.LINKS.findall(page.read_text()):
                link = target[1]
                if link.startswith(("http://", "https://", "mailto:")):
                    continue
                filename, _, fragment = link.partition("#")
                destination = (page.parent / filename).resolve() if filename else page
                self.assertTrue(destination.is_relative_to(root.resolve()))
                self.assertTrue(destination.is_file(), (page.name, link))
                if fragment:
                    headings = re.findall(r"^#{1,6} (.+)$", destination.read_text(), re.M)
                    anchors = {re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-")
                               for h in headings}
                    self.assertIn(fragment, anchors, (page.name, link))
        self.assertTrue((root / "scripts/render_report.py").is_file())
        self.assertFalse((root / "references/skills-product-methods.md").exists())
        self.assertFalse((root / "references/skills-traffic-methods.md").exists())
        self.assertFalse(list(root.rglob("*agent-core*")))

    def test_selection_examples_and_single_sort_query_in_shipped_package(self):
        root = self.output / "skills/zoodata-product-selection"
        planner = root / "scripts/plan_screening.py"
        catalog = root / "references/skills-product-selection-modes.json"
        self.assertFalse(catalog.exists())
        entry = metadata((root / "SKILL.md").read_bytes())
        expert = self.output / "experts/zoodata-product-selection"
        plugin = BUILDER.read_json(expert / ".codebuddy-plugin/plugin.json")
        for language in ("zh", "en"):
            examples = [item[language] for item in plugin["quickPrompts"]]
            skill_examples = entry[f"examples_{language}"]
            self.assertEqual(examples, skill_examples)
            self.assertEqual(examples, [q[language] for q in PLATFORM["experts"]["product-selection"]["quickPrompts"]])
            self.assertEqual(plugin["defaultInitPrompt"][language], examples[0])
            anchors = {
                "zh": (("细分市场", "销量环比"), ("10 款商品", "购买量"), ("近半年上架", "前 100 名")),
                "en": (("subcategories", "month-over-month"), ("10 products", "purchase volumes"), ("past six months", "top 100")),
            }
            for example, required in zip(skill_examples, anchors[language], strict=True):
                for term in required:
                    self.assertIn(term, example)

        spec = importlib.util.spec_from_file_location("selection_planner", planner)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        selection = {"scope": ["Home & Kitchen", "Kitchen"], "filters": {"priceMax": 30},
                     "sortBy": "monthlySalesFloor", "sortOrder": "desc", "pageSize": 10}
        with tempfile.TemporaryDirectory() as tmp:
            args = Path(tmp) / "selection.json"
            args.write_text(json.dumps(selection))
            output = subprocess.check_output([sys.executable, planner, args], text=True)
        self.assertEqual(json.loads(output), {
            "categoryPath": selection["scope"], "priceMax": 30, "sortBy": "monthlySalesFloor",
            "sortOrder": "desc", "page": 1, "pageSize": 10, "marketplace": "US"})
        unrestricted = {"scope": "all", "sortBy": "price", "sortOrder": "asc"}
        self.assertNotIn("categoryPath", module.prepare(unrestricted))
        numeric = module.prepare(unrestricted | {"filters": {"priceMin": "9", "priceMax": "30", "monthlySalesMin": "50"}})
        self.assertEqual((numeric["priceMin"], numeric["priceMax"], numeric["monthlySalesMin"]), (9, 30, 50))
        for value in ("30d", "90d", "180d", "1y", "2y", "6m"):
            planned = module.prepare(unrestricted | {"filters": {"listingAge": value}})
            self.assertEqual(planned["listingAge"], "180d" if value == "6m" else value)
        self.assertNotIn("listingAge", module.prepare(unrestricted | {"filters": {"listingAge": None}}))
        for value in ("6w", 180, [], False):
            with self.subTest(age=value), self.assertRaisesRegex(ValueError, "180d"):
                module.prepare(unrestricted | {"filters": {"listingAge": value}})
        for day in (1, 2, 3):
            for today, prior in ((date(2026, 11, day), "2026-10"), (date(2027, 1, day), "2026-12")):
                self.assertEqual(module.checked_period(prior, today), prior)
                with self.assertRaises(ValueError):
                    module.checked_period(today.strftime("%Y-%m"), today)
        for period in ("30d", "2026-02", None):
            request = module.prepare(unrestricted | {"dateRange": period, "filters": {"fulfillments": ["FBA"]}})
            self.assertEqual(request.get("dateRange"), period)
            self.assertEqual(request["fulfillments"], ["FBA"])
        for change in ({"dateRange": "2026-13"}, {"dateRange": "2025-12"}, {"dateRange": 30},
                       {"dateRange": "2999-01"}, {"dateRange": "bad-date"},
                       {"filters": {"fulfillments": "FBA"}}, {"filters": {"fulfillments": ["unknown"]}},
                       {"filters": {"onlyCategoryRank": "false"}}, {"filters": {"buyBoxSellerCountryCodes": ["USA"]}},
                       {"filters": {"ratingMin": 6}}, {"filters": {"priceMin": -1}},
                       {"filters": {"categoryScope": "exactOnly"}},
                       {"filters": {"badges": ["video"], "excludeBadges": ["video"]}}):
            with self.subTest(invalid=change), self.assertRaises(ValueError):
                module.prepare(unrestricted | change)
        for change in ({"sortBy": "sales"}, {"filters": {"monthlySalesMin": 0.5}},
                       {"filters": {"priceMin": "NaN"}}, {"filters": {"unsupported": 0}}, {"scope": []}, {"mode": 2}, {"pageSize": 0}, {"sortOrder": "both"},
                       {"filters": {"priceMin": 70, "priceMax": 30}}, {"filters": {"sortBy": "price"}}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                module.prepare(unrestricted | change)

    def test_report_hides_month_end_storage_terms(self):
        script = self.output / "skills/zoodata-product-selection/scripts/render_report.py"
        spec = importlib.util.spec_from_file_location("report_labels", script)
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)
        for label in ("2026 年 10 月的月末快照", "September and October month-end snapshots"):
            with self.subTest(label=label), self.assertRaises(ValueError):
                renderer.scope_items([{"label": "比较期间", "value": label}])
        self.assertIn("10 月与 9 月", renderer.scope_items([{"label": "比较期间", "value": "2026 年 10 月与 9 月"}]))

    def test_shipped_parent_and_child_product_templates(self):
        root = self.output / "skills/zoodata-product-selection"
        spec = importlib.util.spec_from_file_location("product_renderer", root / "scripts/render_report.py")
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)
        base = {"title": "Basket", "brand": "Example", "image": None,
                "parentAsin": "B000000001", "parentSales": "800+", "price": 9,
                "rating": None, "ratingCount": 0, "scope": "parent"}
        block = {"monthly": True, "period": "2026-10", "currency": "USD", "items": [base]}
        def render(item):
            return renderer.product_list(dict(block, items=[item]), root, "未获取", "zh-CN")

        parent = render(base)
        for expected in ("父体商品", "父体 ASIN B000000001", "父体月销量", "800+", "暂无图片", "未获取", "<dd>0</dd>"):
            self.assertIn(expected, parent)
        self.assertNotIn("商品 ASIN", parent)
        self.assertNotIn("商品月销量", parent)
        representative = dict(base, representativeFields=["image", "title", "brand"])
        self.assertIn("标题和品牌来自代表款。", render(representative))
        self.assertIn("标题来自代表款。", render(dict(representative, brand=None)))
        self.assertNotIn("来自代表款", render(dict(representative, title=None, brand=None)))
        self.assertLess(render(representative).index("来自代表款"), render(representative).index("父体月销量"))
        child = dict(base, scope="product", asin="B000000002", sales="100+")
        self.assertIn("商品 ASIN B000000002", render(child))
        self.assertIn("父体 ASIN B000000001", render(child))
        self.assertIn("商品月销量", render(child))
        with self.assertRaises(ValueError):
            render(dict(child, scope="parent"))
        with self.assertRaises(ValueError):
            render({k: v for k, v in child.items() if k != "brand"})

    def test_selection_uses_exact_names_in_published_and_dev_builds(self):
        for server in ("zoodata", "zoodata-amazon"):
            with self.subTest(server=server):
                manifest, packages = BUILDER.render_packages(mcp_source=server)
                name = "zoodata-product-selection"
                workflow = packages["skills", name]
                expert = packages["experts", name]
                self.assertEqual(list(json.loads(expert[".mcp.json"])["mcpServers"]), [server])
                self.assertIn(f"server `{server}`", workflow["SKILL.md"].decode())
                shared = workflow["references/contracts-mcp.md"].decode()
                self.assertIn("host explicitly reports that ZooData is disconnected", shared)
                for key in manifest["workflows"]["product-selection"]["data_skills"]:
                    config = manifest["endpoint_skills"][key]
                    source = (COMPONENTS / config["entry"]).read_text()
                    ids = set(re.findall(r"`(openapi_v[0-9]+_[a-z0-9_]+)`", source))
                    self.assertTrue(ids, key)
                    endpoints = 1 + int("fallback_endpoint" in config)
                    self.assertEqual(len(ids), endpoints, key)
                    documents = [workflow[f"references/skills-{key}-definition.md"],
                                 expert[f"skills/{name}/references/skills-{key}-definition.md"],
                                 expert[f"skills/{config['export_name']}/SKILL.md"]]
                    for doc in documents:
                        found = set(re.findall(r"`mcp__([a-z0-9-]+)__(openapi_v[0-9]+_[a-z0-9_]+)`",
                                               doc.decode()))
                        self.assertEqual(found, {(server, op) for op in ids}, key)
                        self.assertNotRegex(doc.decode(), r"`openapi_v[0-9]+_")
                self.assertEqual(metadata(workflow["SKILL.md"])["version"],
                                 json.loads(expert[".codebuddy-plugin/plugin.json"])["version"])

    def test_market_workflow_ships_identically_standalone_and_in_merged_expert(self):
        name = "zoodata-product-selection"
        standalone = self.output / "skills" / name
        package = self.output / "experts" / name
        self.assertFalse((self.output / "experts/zoodata-market-opportunity.zip").exists())
        for source in standalone.rglob("*"):
            if source.is_file():
                bundled = package / "skills" / name / source.relative_to(standalone)
                self.assertEqual(bundled.read_bytes(), source.read_bytes())
        manifest = BUILDER.read_json(self.output / "experts" / name / ".codebuddy-plugin/plugin.json")
        self.assertEqual(manifest["displayName"]["zh"], "选品与市场专家·ZooData")
        self.assertLessEqual(len(manifest["displayName"]["zh"]), 15)
        self.assertEqual(metadata((standalone / "SKILL.md").read_bytes())["display_name"], "选品与市场研究·ZooData")
        endpoint_keys = MANIFEST["workflows"]["product-selection"]["data_skills"]
        reads = {MANIFEST["endpoint_skills"][k]["endpoint"] for k in endpoint_keys}
        self.assertLessEqual(set(MANIFEST["professionals"]["market"]["capabilities"]), reads)
        self.assertIn("market-review-profile", endpoint_keys)

    def test_candidate_assessment_scope_and_evidence_are_packaged(self):
        root = self.output / "skills/zoodata-product-selection"
        expert = self.output / "experts/zoodata-product-selection/skills/zoodata-product-selection"
        refs = root / "references"
        self.assertEqual(set(BUILDER.read_json(refs / "report-tasks.json")), {"screening", "market-growth", "market-research", "assessment", "new-launches"})
        for key in ("product-sales-trend", "product-history", "traffic-structure", "traffic-trend",
                    "traffic-weeks", "product-review-profile"):
            method = refs / f"skills-{key}-definition.md"
            self.assertEqual(method.read_bytes(), (expert / "references" / method.name).read_bytes())
        plan = root / "scripts/assessment_scope.py"
        self.assertEqual(plan.read_bytes(), (expert / "scripts" / plan.name).read_bytes())
        a, b, c, d = [f"B{i:09d}" for i in range(4)]
        for args, expected in [([], []), ([a], [a]), ([a.lower(), a], [a]),
                               ([a, b], []), (["--compare", a, b, c], [a, b, c]),
                               (["--compare", a, b, c, d], []), (["bad-asin"], [])]:
            with self.subTest(args=args):
                result = json.loads(subprocess.check_output([sys.executable, plan, *args]))
                self.assertEqual(result["asins"], expected)
                self.assertEqual(result["status"], "ready" if expected else "choose_candidates")

    def test_competitor_example_renders_directly_from_submission_archives(self):
        workflow = "zoodata-competitor-comparison"
        expert = "zoodata-competitor-insight"
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            for name, kind in [(workflow, "skills"), (expert, "experts")]:
                with zipfile.ZipFile(self.output / kind / (name + ".zip")) as archive:
                    archive.extractall(base)
            reports = []
            embedded = base / expert / "skills" / workflow
            for root in [base / workflow, embedded, base / expert / "skills/zoodata-report-generator"]:
                output = root / "demo.html"
                subprocess.run([sys.executable, root / "scripts/render_report.py",
                                root / "references/example.json", output], check=True,
                               cwd=base, capture_output=True, text=True)
                reports.append(output.read_text())
            self.assertEqual(len(set(reports)), 1)
            self.assertIn("每件少付 1 美元", reports[0])
            self.assertIn("虚构示例", reports[0])

    def test_marketplace_upload_archives(self):
        """Test the upload ZIPs, optionally with WorkBuddy's installed validators."""
        upload_dir = os.environ.get("WORKBUDDY_RELEASE_DIR")
        release = Path(upload_dir) if upload_dir else self.output
        builtin = Path(os.environ.get("WORKBUDDY_BUILTIN_SKILLS",
            "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/"
            "resources/plugins/workbuddy-builtin/skills"))
        native = {"experts": builtin / "expert-manager/scripts/validate_expert.py",
                  "skills": builtin / "skill-creator/scripts/quick_validate.py"}
        if upload_dir:
            for validator in native.values():
                self.assertTrue(validator.is_file(), f"WorkBuddy validator unavailable: {validator}")
        report = BUILDER.read_json(release / "build-report.json")
        digests = {entry["zip"]: entry["sha256"] for entry in report["artifacts"]}
        for expert_id in ("competitor-insight", "product-selection", "keyword-research"):
            workflow_id = MANIFEST["experts"][expert_id]["workflow"]
            workflow = MANIFEST["workflows"][workflow_id]["export_name"]
            expert = PLATFORM["experts"][expert_id]["name"]
            results = []
            with self.subTest(expert=expert), tempfile.TemporaryDirectory() as temp:
                base = Path(temp).resolve()
                for kind, name in (("skills", workflow), ("experts", expert)):
                    relative = f"{kind}/{name}.zip"
                    archive = release / relative
                    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
                    self.assertEqual(digest, digests[relative], relative)
                    self.assertEqual(digest, hashlib.sha256((self.output / relative).read_bytes()).hexdigest(),
                                     f"{relative} differs from the reviewed build")
                    dest = base / ("plugins/marketplaces/my-experts/plugins" if kind == "experts" else "skills")
                    with zipfile.ZipFile(archive) as bundle:
                        bundle.extractall(dest)
                    root = dest / name
                    if native[kind].is_file():
                        result = subprocess.run([sys.executable, native[kind], root], capture_output=True,
                                                text=True, env={**os.environ, "WORKBUDDY_CONFIG_DIR": str(base)})
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    if kind == "experts":
                        root = root / "skills" / MANIFEST["report_skill"]["export_name"]
                    html = base / f"{kind}.html"
                    subprocess.run([sys.executable, root / "scripts/render_report.py",
                                    root / "references/example.json", html], check=True, cwd=base)
                    results.append(html.read_bytes())
                self.assertEqual(*results)
                self.assertIn("虚构", results[0].decode())

    def test_selection_evaluation_uses_current_marketplace_questions(self):
        selection = PLATFORM["experts"]["product-selection"]
        for folder, questions in [
            ("market-selection-eval", PLATFORM["workflows"]["product-selection"]["examples_zh"]),
            ("market-expert-eval", [q["zh"] for q in selection["quickPrompts"]]),
        ]:
            fixture = COMPONENTS / "checks/fixtures" / folder
            dimensions = {d["key"] for d in BUILDER.read_json(fixture / "header.json")["profile"]["dimensions"]}
            cases = [json.loads(line) for line in (fixture / "cases.jsonl").read_text().splitlines()]
            self.assertEqual([case["user_question"] for case in cases], questions)
            for case in cases:
                self.assertTrue(case["expected"])
                self.assertEqual(set(case["checklist_by_dim"]), dimensions)
                self.assertEqual(set(case["anchors_by_dim"]), dimensions)
            self.assertEqual(len(cases), 3)

    def test_monitoring_summary_preserves_gaps_zero_and_requested_scope(self):
        root = self.output / "skills/zoodata-competitor-comparison"
        script = root / "scripts/summarize_changes.py"
        start, end = "2026-11-01", "2026-11-04"
        record = {"asin": "B000000001", "currency": "USD",
                  "context": {"requestedDateFrom": start, "requestedDateTo": end, "granularity": "day"},
                  "timestamps": [end, start, "2026-11-02"], "price": [8, 0, None],
                  "imageUrl": [{"date": start, "value": "image-a"}]}
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "history.json"
            def run(*fields):
                source.write_text(json.dumps({"success": True, "data": record}))
                return subprocess.run([sys.executable, script, source, record["asin"], start, end, *fields],
                                      check=False, capture_output=True, text=True)

            result = run("price", "imageUrl", "title")
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary["changes"], [{"field": "price", "beforeDate": start, "before": 0,
                                                   "afterDate": end, "after": 8}])
            self.assertEqual(summary["fields"]["price"]["observedChanges"], 1)
            self.assertEqual(summary["fields"]["imageUrl"]["observations"], 1)
            self.assertIsNone(summary["fields"]["imageUrl"]["observedChanges"])
            self.assertEqual(summary["fields"]["title"]["observations"], 0)
            record["context"]["requestedDateFrom"] = "2026-10-01"
            for field in ("title", "imageUrl"):
                record[field] = [{"date": "2026-10-01", "value": "old"}, {"date": end, "value": "new"}]
                changed = json.loads(run(field).stdout)
                self.assertEqual(changed["changes"], [{"field": field, "beforeDate": "2026-10-01", "before": "old",
                                                       "afterDate": end, "after": "new"}])
                self.assertEqual(changed["fields"][field]["observations"], 1)
                self.assertEqual(changed["fields"][field]["observedChanges"], 1)
            record["timestamps"].append("2026-10-31")
            record["price"].append(42)
            self.assertEqual(json.loads(run("price").stdout)["fields"]["price"]["observedChanges"], 1)
            record["price"].pop()
            self.assertIn("aligned", run("price").stderr)
            record["context"]["requestedDateFrom"] = end
            self.assertIn("outside", run("title").stderr)

    def test_new_launch_report_requires_three_distinct_product_histories_or_a_visible_gap(self):
        root = self.output / "skills/zoodata-product-selection"
        data = json.loads((root / "references/example.json").read_text())
        data.update(task="new-launches", sections=[{"title": "Category counts", "blocks": []}])
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "draft.json"
            html = path.with_suffix(".html")

            def run(skill_root=root):
                path.write_text(json.dumps(data))
                return subprocess.run([sys.executable, skill_root / "scripts/render_report.py", path, html],
                                      capture_output=True, text=True)

            self.assertNotEqual(run().returncode, 0)
            data["productCoverageNote"] = "No identified listings were returned."
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(data.pop("productCoverageNote"), html.read_text())
            for index in range(3):
                asin = f"B{index:09d}"
                blocks = [{"type": "text", "measure": key, "observationCount": 0, "paragraphs": [key + " unavailable"]}
                          for key in ["price", "bsr", "subBsr", "exposure"]]
                blocks.append({"type": "chart", "kind": "line", "measure": "sales", "title": asin,
                               "unit": "units", "labels": [f"2026-{month:02d}" for month in range(5, 11)],
                               "series": [{"name": asin, "values": [None, None, 0, 20, 40, 80]}]})
                data["sections"].append({"title": asin, "parentAsin": asin, "blocks": blocks})
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            expert_report = self.output / "experts/zoodata-product-selection/skills/zoodata-report-generator"
            result = run(expert_report)
            self.assertEqual(result.returncode, 0, result.stderr)
            charts = [section["blocks"][-1] for section in data["sections"][1:]]
            for chart in charts:
                chart["labels"] = ["2026-10", "2026-11"]
                chart["series"][0]["values"] = [40, 80]
            self.assertIn("six complete months", run().stderr)
            data["monthlySalesPeriod"] = {"startMonth": "2026-10", "endMonth": "2026-11"}
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            charts[-1]["kind"] = "bar"
            self.assertIn("line chart", run().stderr)
            charts[-1]["kind"] = "line"
            charts[-1]["labels"][0] = "2026-09"
            self.assertIn("consecutive", run().stderr)
            charts[-1]["labels"][0] = "2026-10"
            note = data["sections"][-1]["blocks"][0]
            note["observationCount"] = 2
            self.assertIn("observed period", run().stderr)
            note["observationCount"] = 0
            data["sections"][-1]["blocks"].append(data["sections"][-1]["blocks"][0])
            self.assertIn("Duplicate report block", run().stderr)
            data["sections"][-1]["blocks"].pop()
            data["sections"][-1]["blocks"].pop()
            self.assertIn("sales", run().stderr)

    def test_ranked_new_listings_link_directly_to_trend_measures_in_both_packages(self):
        for root in (self.output / "skills/zoodata-product-selection",
                     self.output / "experts/zoodata-product-selection/skills/zoodata-product-selection"):
            market = next((root / "references").glob("*market-research.md"))
            section = market.read_text().split("## Show how the newly ranked products developed")[1].split("## ")[0]
            link = next(target for _, target in BUILDER.LINKS.findall(section) if "#" in target)
            file, heading = link.split("#")
            self.assertEqual(heading, "trace-how-each-product-grew")
            method = (market.parent / file).read_text().split("## Trace how each product grew")[1].split("## ")[0]
            self.assertNotIn("assessment_scope.py", method)
            for field in ("Purchase volume", "Price", "Organic exposure", "Ad exposure", "BSR"):
                self.assertIn(field, method)

    def test_packaged_selection_rank_script_accepts_only_successful_empty_history(self):
        script = self.output / "skills/zoodata-product-selection/scripts/rank_charts.py"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.json"
            for success in (True, False, None):
                path.write_text(json.dumps({"success": success, "data": None}))
                result = subprocess.run([sys.executable, script, path, "B000000001"],
                                        capture_output=True, text=True)
                if success:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    blocks = json.loads(result.stdout)
                    self.assertEqual([b["measure"] for b in blocks], ["bsr", "subBsr"])
                    self.assertTrue(all("未获取" in b["paragraphs"][0] for b in blocks))
                else:
                    self.assertNotEqual(result.returncode, 0)

    def test_selection_report_renders_same_html_from_both_shipped_entries(self):
        standalone = self.output / "skills/zoodata-product-selection"
        embedded = self.output / "experts/zoodata-product-selection/skills"
        report = embedded / MANIFEST["report_skill"]["export_name"]
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            outputs = []
            for index, root in enumerate((standalone, report)):
                html = work / f"report-{index}.html"
                subprocess.run([sys.executable, root / "scripts/render_report.py",
                                root / "references/example.json", html],
                               check=True, capture_output=True)
                outputs.append(html.read_bytes())
            self.assertEqual(*outputs)
            self.assertIn("DEMO-A", outputs[0].decode())

    def test_all_reviewed_competitor_endpoints_have_one_skill_and_two_delivery_routes(self):
        contracts = BUILDER.read_json(COMPONENTS / "checks/fixtures/mcp-contracts.json")["contracts"]
        workflow = MANIFEST["workflows"]["competitor-comparison"]
        bundle = self.output / "skills" / workflow["export_name"] / "references"
        keys = workflow["data_skills"]
        self.assertNotIn("product-live", keys)
        self.assertFalse((bundle / "skills-product-live-definition.md").exists())
        for key in keys:
            component = MANIFEST["endpoint_skills"][key]
            operation = component["endpoint"]
            with self.subTest(operation=operation):
                name = component["export_name"]
                standalone = self.output / "skills" / name
                embedded = self.output / "experts/zoodata-competitor-insight/skills" / name
                capabilities = BUILDER.read_json(standalone / "references/capabilities.json")
                expected_endpoints = [operation]
                if "fallback_endpoint" in component:
                    expected_endpoints.append(component["fallback_endpoint"])
                self.assertEqual(capabilities["logical_read_endpoints"], expected_endpoints)
                entry = (standalone / "SKILL.md").read_bytes()
                self.assertEqual((embedded / "SKILL.md").read_bytes(), entry)
                body = entry.decode().split("---\n", 2)[2].lstrip("\n")
                self.assertEqual((bundle / f"skills-{key}-definition.md").read_text(),
                                 body.replace("](references/", "]("))
                self.assertIn(f"`{operation}`", body)
                if operation not in contracts:
                    continue
                self.assertIn(contracts[operation]["operation_id"], body)
                example = json.loads(re.search(r"```json\n(.*?)\n```", body, re.S)[1])
                inputs = contracts[operation]["input_schema"]
                self.assertLessEqual(set(inputs.get("required", [])), set(example))
                self.assertLessEqual(set(example), set(inputs["properties"]))

    def test_workflow_rejects_implicit_reads_and_invalid_fallbacks(self):
        bad = copy.deepcopy(MANIFEST)
        bad["workflows"]["competitor-comparison"]["allowed_checks"] = {"product": ["Product facts"]}
        with self.assertRaisesRegex(ValueError, "select data Skills directly"):
            BUILDER.validate_sources(bad, PLATFORM)
        bad = copy.deepcopy(MANIFEST)
        bad["endpoint_skills"]["product-detail"]["fallback_skill"] = "product-live"
        with self.assertRaisesRegex(ValueError, "cannot depend on other data Skills"):
            BUILDER.validate_sources(bad, PLATFORM)
        for endpoint in ("products/detail", "undeclared/service"):
            bad = copy.deepcopy(MANIFEST)
            bad["endpoint_skills"]["product-detail"]["fallback_endpoint"] = endpoint
            with self.assertRaisesRegex(ValueError, "Invalid fallback endpoint"):
                BUILDER.render_endpoint_skill("product-detail", bad, PLATFORM)

    def test_endpoint_skill_format_and_review_profile_output(self):
        for language, headings in [
            ("", ("Task input", "Endpoints and call order", "Request parameters", "Response handling", "Deliverable")),
            ("zh-CN", ("任务输入", "接口与调用顺序", "查询参数", "返回处理", "交付结果")),
        ]:
            profiles = []
            for key, skill in MANIFEST["endpoint_skills"].items():
                text = (COMPONENTS / language / skill["entry"]).read_text()
                titles = re.findall(r"^## (.+)$", text, re.M)
                endpoints = [skill["endpoint"]]
                if "fallback_endpoint" in skill:
                    endpoints.append(skill["fallback_endpoint"])
                with self.subTest(skill=key, language=language):
                    self.assertEqual(titles[:2], list(headings[:2]))
                    self.assertEqual(titles[-1], headings[-1])
                    self.assertEqual(len(titles[2:-1]), len(endpoints))
                    for title, endpoint in zip(titles[2:-1], endpoints):
                        self.assertIn(f"`{endpoint}`", title)
                        section = text.split(f"\n## {title}\n", 1)[1].split("\n## ", 1)[0]
                        self.assertEqual(re.findall(r"^### (.+)$", section, re.M), list(headings[2:4]))
                        example = re.search(r"```json\n(.*?)\n```", section, re.S)
                        self.assertIsNotNone(example)
                        self.assertIsInstance(json.loads(example[1]), dict)
                    if key in ("product-review-profile", "market-review-profile"):
                        profiles.append(text.split("## " + headings[-1] + "\n", 1)[1])
            self.assertEqual(profiles[0], profiles[1])

    def test_review_profiles_use_separate_populations_and_sources(self):
        expert = self.output / "experts/zoodata-competitor-insight/skills"
        for name, mode, selection, endpoints in [
            ("product-review-profile", "asin", "asins", ["voc/analysis", "realtime/reviews"]),
            ("market-review-profile", "category", "categoryPath", ["voc/analysis"]),
        ]:
            root = self.output / "skills" / ("zoodata-" + name)
            self.assertEqual((expert / root.name).exists(), mode == "asin")
            capabilities = BUILDER.read_json(root / "references/capabilities.json")
            self.assertEqual(capabilities["logical_read_endpoints"], endpoints)
            for lang in ("", "zh-CN"):
                definition = COMPONENTS / lang / MANIFEST["endpoint_skills"][name]["entry"]
                examples = [json.loads(value) for value in re.findall(r"```json\n(.*?)\n```", definition.read_text(), re.S)]
                self.assertEqual(len(examples), len(endpoints))
                self.assertEqual(examples[0]["mode"], mode)
                self.assertEqual(examples[0]["period"], "1y")
                self.assertEqual(set(examples[0]), {"mode", selection, "period", "marketplace"})

    def test_product_detail_calls_both_endpoints_without_a_sibling_skill(self):
        root = self.output / "skills/zoodata-product-detail"
        expert = self.output / "experts/zoodata-competitor-insight"
        for language in ("", "zh-CN"):
            definition = COMPONENTS / language / MANIFEST["endpoint_skills"]["product-detail"]["entry"]
            text = definition.read_text()
            examples = [json.loads(value) for value in re.findall(r"```json\n(.*?)\n```", text, re.S)]
            self.assertEqual([set(example) for example in examples], [{"asins", "marketplace"}, {"asin", "marketplace"}])
        self.assertEqual(BUILDER.read_json(root / "references/capabilities.json")["logical_read_endpoints"],
                         ["products/detail", "realtime/product"])
        self.assertFalse((expert / "skills/zoodata-product-live").exists())
        self.assertFalse(list(root.rglob("*product-live*")))

    def test_trend_skills_include_the_shared_window_owner(self):
        rule = (COMPONENTS / "contract/query.md").read_text()
        self.assertIn("6 months for monthly trends, 3 months for weekly trends, and 1 month for daily trends", rule)
        for key in ("product-sales-trend", "product-history", "traffic-trend", "traffic-weeks",
                    "traffic-term-weeks", "query-weeks"):
            root = self.output / "skills" / MANIFEST["endpoint_skills"][key]["export_name"]
            self.assertIn("#select-the-trend-period", (root / "SKILL.md").read_text())
            self.assertEqual(rule, (root / "references/contracts-mcp.md").read_text())

    def test_each_workflow_data_skill_loads_its_packaged_contracts(self):
        for key in {key for workflow in MANIFEST["workflows"].values() for key in workflow["data_skills"]}:
            root = self.output / "skills" / MANIFEST["endpoint_skills"][key]["export_name"]
            links = {target.partition("#")[0] for _, target in BUILDER.LINKS.findall((root / "SKILL.md").read_text())}
            for filename, source in (("evidence", "evidence"), ("mcp", "query"), ("reporting", "report")):
                relative = f"references/contracts-{filename}.md"
                with self.subTest(skill=key, contract=source):
                    self.assertIn(relative, links)
                    self.assertEqual((root / relative).read_bytes(), (COMPONENTS / f"contract/{source}.md").read_bytes())

    def test_purchase_workflow_loads_one_endpoint_and_plans_only_selected_asins(self):
        workflow = self.output / "skills/zoodata-competitor-comparison"
        data = self.output / "skills/zoodata-product-sales-trend"
        endpoint = "products/sales-trend"
        contract = BUILDER.read_json(COMPONENTS / "checks/fixtures/mcp-contracts.json")["contracts"][endpoint]
        self.assertEqual(BUILDER.read_json(data / "references/capabilities.json")["logical_read_endpoints"],
                         [endpoint])
        body = (data / "SKILL.md").read_text().split("---\n", 2)[2]
        self.assertIn(contract["operation_id"], body)
        for state in ("monthEnd", "monthToDate", "inCatalog=false", "inCatalog=true"):
            self.assertIn(state, body)
        example = json.loads(re.search(r"```json\n(.*?)\n```", body, re.S)[1])
        self.assertEqual(set(example), set(contract["input_schema"]["properties"]))
        self.assertEqual(example["marketplace"], contract["input_schema"]["properties"]["marketplace"]["const"])
        self.assertRegex(example["asin"], r"^[A-Z0-9]{10}$")
        branch = next((workflow / "references").glob("*-monthly-purchases.md"))
        targets = [link for _, link in BUILDER.LINKS.findall(branch.read_text())]
        self.assertEqual(len(targets), 2)
        planner, fallback = [(branch.parent / target).resolve() for target in targets]
        self.assertEqual(fallback.read_text(), body.lstrip("\n").replace("](references/", "]("))
        self.assertIn("select-the-trend-period", fallback.read_text())
        self.assertEqual(planner.parent, workflow / "scripts")
        asins = [f"B{i:09d}" for i in range(4)]
        def run(args, as_of="2026-11-19"):
            result = subprocess.run([sys.executable, str(planner), "--as-of", as_of, *args],
                                    text=True, capture_output=True, check=True)
            return json.loads(result.stdout)

        for count in (1, 2, 3):
            plan = run(asins[:count])
            self.assertEqual(plan["months"], ["2026-08", "2026-09", "2026-10"])
            self.assertEqual(plan["requests"], [
                {"asin": asin, "marketplace": "US", "startMonth": "2026-08", "endMonth": "2026-10"}
                for asin in asins[:count]])
            self.assertLessEqual(set(plan["requests"][0]), set(contract["input_schema"]["properties"]))
        for candidates in ([], asins, [asins[0], "invalid"]):
            plan = run(candidates)
            self.assertEqual(plan["status"], "confirm_asins")
            self.assertEqual(plan["requests"], [])
        self.assertEqual(run([asins[0].lower(), *asins[:3]])["requests"], run(asins[:3])["requests"])
        for day in ("2027-01-01", "2027-01-02"):
            self.assertEqual(run(asins[:1], day)["months"], ["2026-09", "2026-10", "2026-11"])
        self.assertEqual(run(asins[:1], "2027-01-03")["months"], ["2026-10", "2026-11", "2026-12"])
        self.assertEqual(run(asins[:1], "2026-04-01")["requests"][0]["startMonth"], "2026-02")
        self.assertEqual(run(asins[:1], "2026-02-01")["requests"], [])

    def test_flattened_links_preserve_peer_and_shared_targets_and_fragments(self):
        component = MANIFEST["professionals"]["traffic"]
        paths = BUILDER.skill_resource_paths(component)
        source = COMPONENTS / component["entry"]
        text = ("[product](../product/semantics.md#history) "
                "[keyword](../keyword/semantics.md) "
                "[seller](../../../contract/seller-evidence.md#funnel) "
                "[external](https://example.com/docs#section) [section](#local)")
        result = BUILDER.rewrite_resource_links(source, text, paths)
        self.assertEqual(result,
                         "[product](skills-product-semantics.md#history) "
                         "[keyword](skills-keyword-semantics.md) "
                         "[seller](contracts-seller-evidence.md#funnel) "
                         "[external](https://example.com/docs#section) [section](#local)")
        self.assertNotEqual(paths[COMPONENTS / "skill/datas/product/semantics.md"],
                            paths[COMPONENTS / "skill/datas/keyword/semantics.md"])
        with self.assertRaisesRegex(ValueError, "Unbundled Skill reference"):
            BUILDER.rewrite_resource_links(source, "[missing](missing.md)", paths)

    def test_packager_rejects_nested_resources_and_flat_name_collisions(self):
        with self.assertRaisesRegex(ValueError, "two-level limit"):
            BUILDER.validate_skill_layout({"SKILL.md": b"entry",
                                           "references/nested/resource.md": b"content"})
        with mock.patch.object(BUILDER, "source_file", side_effect=lambda path: Path(path)):
            with self.assertRaisesRegex(ValueError, "Colliding flattened Skill resource"):
                BUILDER.skill_resource_paths({"resources": ["a/b-c.md", "a-b/c.md"]})

    def test_expert_plugin_agent_and_bundled_skills_agree(self):
        for expert_id, source in MANIFEST["experts"].items():
            name = PLATFORM["experts"][expert_id]["name"]
            root = self.output / "experts" / name
            plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
            agent = root / plugin["agents"][0]
            fields = metadata(agent.read_bytes())
            with self.subTest(expert=expert_id):
                self.assertEqual(plugin["name"], plugin["plugin"])
                self.assertEqual(plugin["agentName"], agent.stem)
                self.assertEqual(fields["name"], agent.stem)
                self.assertEqual(plugin["defaultInitPrompt"], plugin["quickPrompts"][0])
                self.assertEqual(len(plugin["quickPrompts"]), 3)
                self.assertEqual(len(plugin["tags"]), 3)
                self.assertTrue(40 <= len(plugin["displayDescription"]["zh"]) <= 50)
                self.assertNotIn("tools", fields)
                self.assertNotIn("tools", plugin)
                shipped_names = {p.name for p in root.rglob("*") if p.is_file()}
                self.assertFalse(shipped_names & {"DEVELOPMENT.md", "AGENTS.md", "CONTRIBUTING.md"})
                self.assertTrue((root / plugin["avatar"]).is_file())
                report_name = MANIFEST["report_skill"]["export_name"]
                if "workflow" in source:
                    workflow_name = MANIFEST["workflows"][source["workflow"]]["export_name"]
                    primary = [workflow_name]
                    names = {workflow_name, report_name}
                    dependencies = MANIFEST["workflows"][source["workflow"]]["data_skills"]
                    for key in dependencies:
                        names.add(MANIFEST["endpoint_skills"][key]["export_name"])
                    all_domains = []
                else:
                    primary = [MANIFEST["professionals"][domain]["export_name"]
                               for domain in source["primary_professionals"]]
                    all_domains = source["primary_professionals"] + source["optional_professionals"]
                    names = {MANIFEST["professionals"][domain]["export_name"] for domain in all_domains}
                    names.add(report_name)
                self.assertEqual(fields["skills"], primary + [report_name])
                self.assertEqual({Path(path).name for path in plugin["skills"]}, names)
                for path in plugin["skills"]:
                    skill = root / path / "SKILL.md"
                    self.assertEqual(metadata(skill.read_bytes())["name"], skill.parent.name)
                bundled_names = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
                self.assertEqual(bundled_names, names, "Do not ship unlisted Skill directories")
                body = agent.read_text()
                approved = re.findall(r"^  Approved checks: (.+)$", body, re.M)
                self.assertEqual(approved, [", ".join(f"`{check}`" for check in
                                 source["allowed_checks"][domain]) for domain in all_domains])
                self.assertNotRegex(body, r"\.\./(?:agent-core|professional|components)/")
                for relative in MANIFEST["agent_sources"]:
                    shared = (COMPONENTS / relative).read_text().strip()
                    self.assertEqual(body.count(shared), 1,
                                     f"{expert_id}: shared owner must be inlined exactly once: {relative}")

    def test_shared_interaction_precedes_skill_loading_in_every_expert(self):
        interaction = (COMPONENTS / "expert/agent-core/interaction.md").read_text().strip()
        for item in self.report["artifacts"]:
            if item["kind"] != "experts":
                continue
            root = self.output / "experts" / item["name"]
            plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
            body = (root / plugin["agents"][0]).read_text()
            with self.subTest(expert=item["name"]):
                self.assertEqual(body.count(interaction), 1)
                self.assertLess(body.index(interaction),
                                body.index("# Professional Skill composition"))

    def test_shared_delivery_is_the_final_expert_presentation_owner(self):
        delivery = (COMPONENTS / "expert/agent-core/delivery.md").read_text().strip()
        for item in self.report["artifacts"]:
            if item["kind"] != "experts":
                continue
            root = self.output / "experts" / item["name"]
            plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
            body = (root / plugin["agents"][0]).read_text()
            with self.subTest(expert=item["name"]):
                self.assertTrue(body.rstrip().endswith(delivery))
                self.assertEqual(body.count(delivery), 1)

    def test_shared_report_owner_is_independent_and_reused_by_every_expert(self):
        report_path = COMPONENTS / "contract/report.md"
        report_source = report_path.read_text()
        for domain, component in MANIFEST["professionals"].items():
            skill = self.output / "skills" / component["export_name"]
            with self.subTest(domain=domain):
                expected = BUILDER.rewrite_resource_links(report_path, report_source,
                              BUILDER.skill_resource_paths(component))
                self.assertEqual((skill / "references/contracts-reporting.md").read_text(),
                                 expected)
                references = re.findall(r"@([a-zA-Z0-9_./-]+)",
                                        (skill / "SKILL.md").read_text())
                self.assertIn("references/contracts-reporting.md", references)
        for expert_id, item in PLATFORM["experts"].items():
            root = self.output / "experts" / item["name"]
            plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
            body = (root / plugin["agents"][0]).read_text()
            with self.subTest(expert=expert_id):
                expected = report_source.strip()
                self.assertEqual(body.count(expected), 1)
                for target in re.findall(r"\]\(([^)]+)\)", expected):
                    if not target.startswith(("http://", "https://", "#")):
                        resolved = (root / plugin["agents"][0]).parent / target
                        self.assertTrue(resolved.is_file(), target)
                        self.assertTrue(resolved.resolve().is_relative_to(root.resolve()))

    def test_report_resources_have_one_owner_and_are_shared_by_all_experts(self):
        report = MANIFEST["report_skill"]
        standalone = self.output / "skills" / report["export_name"]
        for source, relative in report["resources"].items():
            if not source.endswith(".md"):
                self.assertEqual((standalone / relative).read_bytes(), (COMPONENTS / source).read_bytes())
            for key, item in PLATFORM["experts"].items():
                bundled = self.output / "experts" / item["name"] / "skills" / report["export_name"]
                owner = standalone
                workflow_key = MANIFEST["experts"][key].get("workflow")
                if relative == "references/example.json" and workflow_key:
                    owner = self.output / "skills" / MANIFEST["workflows"][workflow_key]["export_name"]
                self.assertEqual((bundled / relative).read_bytes(), (owner / relative).read_bytes())
        for component in MANIFEST["professionals"].values():
            root = self.output / "skills" / component["export_name"]
            self.assertFalse(list(root.rglob("*.py")))
            self.assertFalse(list(root.rglob("*.html")))

    def test_report_skill_links_resolve_and_bundled_generator_runs_with_its_template(self):
        item = PLATFORM["experts"]["product-selection"]
        root = self.output / "experts" / item["name"]
        plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
        skill = root / "skills" / MANIFEST["report_skill"]["export_name"]
        for path in skill.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.is_relative_to(skill))
                self.assertTrue(resolved.is_file(), target)
                if "#" in target:
                    content = resolved.read_text()
                    anchors = {re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")
                               for heading in re.findall(r"^#{1,6} (.+)$", content, re.M)}
                    anchors.update(re.findall(r'<a id="([^"]+)">', content))
                    self.assertIn(target.split("#", 1)[1], anchors, target)
        entry = (skill / "SKILL.md").read_text()
        reviews = [match for match in re.finditer(r"\]\(([^)]+)\)", entry)
                   if match.group(1).endswith("#review-the-complete-report")]
        self.assertEqual(len(reviews), 1, "Route whole-draft review to one policy owner")
        owner = (skill / reviews[0].group(1).split("#", 1)[0]).resolve()
        self.assertEqual(owner, (skill / "references/reporting.md").resolve())
        self.assertLess(reviews[0].start(), entry.index("python3 <generator-path>"),
                        "Complete-draft review must precede HTML generation")
        fields = metadata((skill / "SKILL.md").read_bytes())
        self.assertEqual(fields["name"], MANIFEST["report_skill"]["export_name"])
        self.assertEqual(fields["version"], MANIFEST["source_version"])
        self.assertFalse(list(skill.rglob("*mcp*")))
        renderer = skill / "scripts/render_report.py"
        example = skill / "references/example.json"
        output = self.output / "example-report.html"
        result = subprocess.run([sys.executable, str(renderer), str(example), str(output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("版式示例", output.read_text())

    def test_packaged_teardown_requires_original_daily_price_observations(self):
        expert = self.output / "experts" / PLATFORM["experts"]["competitor-insight"]["name"]
        generator = expert / "skills/zoodata-report-generator/scripts/render_report.py"
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            output = base / "report.html"
            draft = {"title": "Teardown", "expert": "ZooData", "scope": [], "sections": [
                {"title": "Price", "blocks": [{"type": "chart", "kind": "line", "title": "Price",
                 "unit": "USD", "labels": ["2026-05", "2026-06"], "series": [
                     {"name": "Month end", "values": [11, 12]}]}]}]}
            workflow = self.output / "skills" / MANIFEST["workflows"]["competitor-comparison"]["export_name"]
            def run():
                (base / "data.json").write_text(json.dumps(draft))
                standalone_output = base / "standalone.html"
                results = []
                for renderer, destination in [(generator, output), (workflow / "scripts/render_report.py", standalone_output)]:
                    destination.unlink(missing_ok=True)
                    results.append(subprocess.run([sys.executable, str(renderer), str(base / "data.json"), str(destination)],
                                                  capture_output=True, text=True))
                expert_result, standalone_result = results
                self.assertEqual(expert_result.returncode, standalone_result.returncode)
                if expert_result.returncode == 0:
                    self.assertEqual(output.read_bytes(), standalone_output.read_bytes())
                else:
                    self.assertEqual(expert_result.stderr.splitlines()[-1], standalone_result.stderr.splitlines()[-1])
                    self.assertFalse(standalone_output.exists())
                return expert_result

            self.assertIn("Select a report task", run().stderr)
            draft["task"] = "teardown"
            self.assertIn("requires one daily-history", run().stderr)
            daily = {"type": "daily-history", "asin": "B000000001", "field": "price",
                     "name": "Page price", "title": "Daily price", "source": "history.json",
                     "startDate": "2026-05-01", "endDate": "2026-05-04"}
            draft["sections"][0]["blocks"] = [daily]
            record = {"asin": daily["asin"], "currency": "USD", "context": {"granularity": "day",
                      "requestedDateFrom": daily["startDate"], "requestedDateTo": daily["endDate"]},
                      "timestamps": ["2026-05-01", "2026-05-03", "2026-05-04"], "price": [11, 13]}
            def save():
                (base / "history.json").write_text(json.dumps({"success": True, "data": record}))

            save()
            self.assertIn("equal-length arrays", run().stderr)
            self.assertFalse(output.exists())
            record["price"].append(12)
            save()
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text()
            self.assertEqual(html.count("<polyline"), 2)
            self.assertEqual(html.count("<circle"), 3)
            self.assertIn("2026-05-02", html)
            self.assertIn("上升 1 次、下降 1 次", html)
            record["timestamps"].insert(0, record["timestamps"][0])
            record["price"].insert(0, record["price"][0])
            save()
            self.assertEqual(run().returncode, 0)
            self.assertEqual(output.read_text(), html)
            command = [sys.executable, workflow / "scripts/summarize_changes.py", base / "history.json",
                       daily["asin"], daily["startDate"], daily["endDate"], "price"]
            summary = json.loads(subprocess.check_output(command, text=True))
            self.assertEqual(summary["fields"]["price"]["observedChanges"], 2)
            self.assertEqual(summary["fields"]["price"]["observations"], 3)
            record["price"][0] += 1
            save()
            self.assertIn("Conflicting price", run().stderr)
            draft["sections"].append({"title": "Sales", "blocks": [
                {"type": "text", "paragraphs": ["Other available findings"]}]})
            for payload in ({"success": False, "data": None}, {"data": None}, {"success": True}):
                (base / "history.json").write_text(json.dumps(payload))
                self.assertNotEqual(run().returncode, 0)
            (base / "history.json").write_text(json.dumps({"success": True, "data": None}))
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Daily price · 未获取", output.read_text())
            self.assertIn("Other available findings", output.read_text())
            summary = json.loads(subprocess.check_output(command, text=True))
            self.assertIsNone(summary["fields"]["price"]["observedChanges"])
            draft["task"] = "comparison"
            draft["sections"][0]["blocks"] = [{"type": "text", "paragraphs": ["Comparison"]}]
            self.assertEqual(run().returncode, 0)

    def test_professional_procedures_remain_in_skill_resources_not_agent_body(self):
        for expert_id, source in MANIFEST["experts"].items():
            root = self.output / "experts" / PLATFORM["experts"][expert_id]["name"]
            plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
            agent_body = (root / plugin["agents"][0]).read_text()
            for domain in source.get("primary_professionals", []) + source.get("optional_professionals", []):
                component = MANIFEST["professionals"][domain]
                method_source = COMPONENTS / f"skill/datas/{domain}/methods.md"
                paths = BUILDER.skill_resource_paths(component)
                relative = paths[method_source]
                skill = root / "skills" / component["export_name"]
                procedure = (skill / relative).read_text()
                with self.subTest(expert=expert_id, domain=domain):
                    self.assertEqual(procedure, BUILDER.rewrite_resource_links(
                        method_source, method_source.read_text(), paths))
                    self.assertNotIn(procedure.strip(), agent_body)
                    references = re.findall(r"\]\(([^)]+)\)",
                                            (skill / "SKILL.md").read_text())
                    self.assertIn(relative, references)

    def test_embedded_and_standalone_mcp_use_their_native_token_schemas(self):
        key = PLATFORM["connector"]["token_key"]
        for root in (self.output / "experts").iterdir():
            if not root.is_dir():
                continue
            config = BUILDER.read_json(root / ".mcp.json")
            self.assertEqual(len(config["mcpServers"]), 1)
            self.assertEqual(set(config["mcpServers"]), {PLATFORM["connector"]["source"]})
            server = next(iter(config["mcpServers"].values()))
            self.assertEqual(server["type"], "http")
            self.assertEqual(server["headers"], {"Authorization": "Bearer ${" + key + "}"})
            extra = server["x-workbuddy"]
            self.assertTrue((root / extra["icon"]).is_file())
            self.assertEqual(extra["auth"]["type"], "token")
            schema = extra["auth"]["tokenSchema"]
            self.assertIsInstance(schema["title"], dict)
            self.assertEqual(schema["fields"][0]["key"], key)
            self.assertEqual(schema["fields"][0]["type"], "password")
        connector_name = PLATFORM["connector"].get("package_name", PLATFORM["connector"]["source"])
        connector = self.output / "connectors" / connector_name
        meta = BUILDER.read_json(connector / "connector-meta.json")
        self.assertEqual(meta["source"], PLATFORM["connector"]["source"])
        self.assertEqual(meta["auth_mode"], "token")
        self.assertEqual(meta["minWorkbuddyVersion"], "4.24.0")
        schema = BUILDER.read_json(connector / "token-schema.json")
        self.assertIsInstance(schema["title"], str)
        self.assertIsInstance(schema["title_en"], str)
        self.assertEqual(schema["fields"][0]["key"], key)
        config = BUILDER.read_json(connector / "mcp.json")
        self.assertEqual(len(config["mcpServers"]), 1)
        self.assertEqual(set(config["mcpServers"]), {meta["source"]})
        server = next(iter(config["mcpServers"].values()))
        self.assertEqual(server["type"], "streamableHttp")
        self.assertNotIn("skills", {path.name for path in connector.iterdir()})

    def test_expert_rejects_unknown_duplicate_or_missing_primary_bindings(self):
        for invalid in ("unknown", "duplicate", "missing-primary"):
            manifest = copy.deepcopy(MANIFEST)
            expert = manifest["experts"]["traffic-diagnosis"]
            if invalid == "unknown":
                expert["optional_professionals"].append("unknown-domain")
            elif invalid == "duplicate":
                expert["optional_professionals"].append(expert["primary_professionals"][0])
            else:
                expert["primary_professionals"] = []
            with self.subTest(invalid=invalid), self.assertRaisesRegex(
                    ValueError, "Invalid professional bindings"):
                BUILDER.validate_sources(manifest, PLATFORM)

    def test_expert_check_scope_matches_bindings_and_owned_catalogs(self):
        for invalid in ("missing-domain", "extra-domain", "unknown-check", "empty", "duplicate"):
            manifest = copy.deepcopy(MANIFEST)
            expert = manifest["experts"]["traffic-diagnosis"]
            scope = expert["allowed_checks"]
            if invalid == "missing-domain":
                scope.pop("traffic")
            elif invalid == "extra-domain":
                scope["review"] = ["Consumer-theme profile"]
            elif invalid == "unknown-check":
                scope["keyword"].append("Invented check")
            elif invalid == "empty":
                scope["keyword"] = []
            else:
                scope["keyword"].append(scope["keyword"][0])
            with self.subTest(invalid=invalid), self.assertRaisesRegex(
                    ValueError, "Invalid expert check scope"):
                BUILDER.validate_sources(manifest, PLATFORM)

    def test_published_connector_mode_uses_only_the_supplied_dependency(self):
        _, packages = BUILDER.render_packages(connector_id="actual-published-id")
        for (kind, _), files in packages.items():
            if kind != "experts":
                continue
            plugin = json.loads(files[".codebuddy-plugin/plugin.json"])
            self.assertEqual(plugin["dependencies"], {"connectors": ["actual-published-id"]})
            self.assertNotIn(".mcp.json", files)
            self.assertNotIn("avatars/connector.svg", files)

    def test_connector_package_name_is_independent_of_connection_identity(self):
        platform = copy.deepcopy(PLATFORM)
        platform["connector"]["package_name"] = "brand-data-package"
        platform["connector"]["source"] = "registered-connection"
        read_json = BUILDER.read_json
        with mock.patch.object(BUILDER, "read_json", side_effect=lambda path:
                               platform if Path(path).name == "workbuddy.json" else read_json(path)):
            _, packages = BUILDER.render_packages()
        connector = packages[("connectors", "brand-data-package")]
        self.assertEqual(json.loads(connector["connector-meta.json"])["source"],
                         "registered-connection")
        for (kind, _), files in packages.items():
            if kind == "experts":
                self.assertEqual(set(json.loads(files[".mcp.json"])["mcpServers"]),
                                 {"registered-connection"})
        platform["connector"]["package_name"] = "../outside"
        with self.assertRaisesRegex(ValueError, "connector package name"):
            BUILDER.validate_sources(MANIFEST, platform)

    def test_repeated_builds_are_deterministic_and_do_not_overwrite_artifacts(self):
        second = BUILDER.build(Path(self.workspace.name) / "second", include_components=True)
        self.assertEqual(self.report, second)
        before = (self.output / "build-report.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "never overwritten"):
            BUILDER.build(self.output)
        self.assertEqual(before, (self.output / "build-report.json").read_bytes())

    def test_default_target_rebuilds_only_archives_and_preserves_other_files(self):
        self.assertEqual(BUILDER.DEFAULT_OUTPUT, COMPONENTS / "targets")
        output = (Path(self.workspace.name) / "default-target").resolve()
        with mock.patch.object(BUILDER, "DEFAULT_OUTPUT", output):
            report = BUILDER.build()
            self.assertFalse(report["unpacked_copies"])
            workflows = {item["export_name"] for item in MANIFEST["workflows"].values()}
            self.assertEqual({p.stem for p in (output / "skills").glob("*.zip")}, workflows)
            self.assertFalse((output / "experts/zoodata-market-opportunity.zip").exists())
            self.assertEqual(len(list(output.rglob("*.zip"))), len(workflows) + len(MANIFEST["experts"]) + 1)
            with self.assertRaisesRegex(ValueError, "external --output"):
                BUILDER.build(include_components=True)
            self.assertFalse(list(output.rglob("SKILL.md")))
            self.assertEqual({path.suffix for path in output.rglob("*") if path.is_file()},
                             {".json", ".zip"})
            for item in report["artifacts"]:
                with zipfile.ZipFile(output / item["zip"]) as archive:
                    self.assertIsNone(archive.testzip())
            note = output / "notes.txt"
            note.write_text("Keep this user file")
            archive = output / report["artifacts"][0]["zip"]
            original = archive.read_bytes()
            archive.write_bytes(b"previous archive")
            rebuilt = BUILDER.build(output)
            self.assertEqual(report, rebuilt)
            self.assertEqual(archive.read_bytes(), original)
            self.assertEqual(note.read_text(), "Keep this user file")
            self.assertFalse(list(output.rglob("SKILL.md")))

    def test_default_build_retires_only_unchanged_previously_managed_archives(self):
        output = (Path(self.workspace.name) / "retired-target").resolve()
        (output / "skills").mkdir(parents=True)
        unchanged = output / "skills/amazon-listing-audit-pro.zip"
        changed = output / "skills/user-modified-skill.zip"
        unlisted = output / "skills/user-backup.zip"
        outside = output.parent / "outside.zip"
        unchanged.write_bytes(b"previous generated archive")
        changed.write_bytes(b"user edited archive")
        unlisted.write_bytes(b"user backup")
        outside.write_bytes(b"outside file")
        previous = {"artifacts": [
            {"kind": "skills", "name": "amazon-listing-audit-pro",
             "zip": "skills/amazon-listing-audit-pro.zip",
             "sha256": hashlib.sha256(unchanged.read_bytes()).hexdigest()},
            {"kind": "skills", "name": "user-modified-skill",
             "zip": "skills/user-modified-skill.zip",
             "sha256": hashlib.sha256(b"original generated bytes").hexdigest()},
            {"kind": "skills", "name": "outside", "zip": "../outside.zip",
             "sha256": hashlib.sha256(outside.read_bytes()).hexdigest()},
        ]}
        (output / "build-report.json").write_bytes(BUILDER.json_bytes(previous))
        with mock.patch.object(BUILDER, "DEFAULT_OUTPUT", output):
            report = BUILDER.build()
        self.assertFalse(unchanged.exists())
        self.assertEqual(changed.read_bytes(), b"user edited archive")
        self.assertEqual(unlisted.read_bytes(), b"user backup")
        self.assertEqual(outside.read_bytes(), b"outside file")
        self.assertEqual(len(report["artifacts"]), len(MANIFEST["workflows"]) + len(MANIFEST["experts"]) + 1)
        self.assertNotIn("amazon-listing-audit-pro", {a["name"] for a in report["artifacts"]})

    def test_product_expert_uses_product_and_traffic_without_a_listing_skill(self):
        self.assertNotIn("listing", MANIFEST["professionals"])
        self.assertNotIn("listing", PLATFORM["professionals"])
        expert = MANIFEST["experts"]["product-research"]
        self.assertEqual(expert["primary_professionals"], ["product"])
        self.assertIn("Product content", expert["allowed_checks"]["product"])
        self.assertIn("Traffic contributors", expert["allowed_checks"]["traffic"])
        for source in MANIFEST["experts"].values():
            self.assertNotIn("listing", source.get("allowed_checks", {}))
        name = PLATFORM["experts"]["product-research"]["name"]
        root = self.output / "experts" / name
        plugin = BUILDER.read_json(root / ".codebuddy-plugin/plugin.json")
        packaged = {Path(p).name for p in plugin["skills"]}
        self.assertEqual(packaged, {MANIFEST["professionals"][domain]["export_name"]
                                   for domain in ("product", "review", "traffic")} |
                         {MANIFEST["report_skill"]["export_name"]})

    def test_repository_output_and_invalid_market_metadata_fail_before_writes(self):
        for output in (COMPONENTS / "generated", COMPONENTS / "targets/unpacked"):
            with self.subTest(output=output), self.assertRaisesRegex(ValueError, "components/targets"):
                BUILDER.build(output)
        invalid = copy.deepcopy(PLATFORM)
        invalid["experts"]["product-selection"]["displayDescription"]["zh"] = "太短"
        with self.assertRaisesRegex(ValueError, "40–50"):
            BUILDER.validate_sources(MANIFEST, invalid)
        with self.assertRaisesRegex(ValueError, "actual published connector ID"):
            BUILDER.render_packages(connector_id="not a valid ID")


if __name__ == "__main__":
    unittest.main()
