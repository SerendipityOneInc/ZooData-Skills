"""Source composition invariants; no network, publisher or production writes."""

import hashlib
import json
from pathlib import Path
import re
import unittest


COMPONENTS = Path(__file__).resolve().parents[1]
REPOSITORY = COMPONENTS.parent
MANIFEST = json.loads((COMPONENTS / "targets.json").read_text(encoding="utf-8"))
LINKS = re.compile(r"\]\(([^)]+)\)")


def local_dependencies(path):
    """Return source file dependencies, excluding URLs and fragment-only links."""
    for target in LINKS.findall(path.read_text(encoding="utf-8")):
        if target.startswith(("https://", "http://", "#", "mailto:")):
            continue
        yield (path.parent / target.split("#", 1)[0]).resolve()


class TestComponentSources(unittest.TestCase):
    def test_agent_instruction_bridges_discover_development_standard(self):
        standard = (COMPONENTS / "DEVELOPMENT.md").resolve()
        self.assertTrue(standard.is_file())
        for bridge in (REPOSITORY / "AGENTS.md", COMPONENTS / "AGENTS.md"):
            self.assertIn(standard, set(local_dependencies(bridge)))
        for component in MANIFEST["professionals"].values():
            self.assertNotIn("DEVELOPMENT.md", component["resources"])

    def test_components_do_not_add_discoverable_skill_entrypoints(self):
        forbidden = {name.casefold() for name in
                     MANIFEST["publication"]["forbidden_entrypoint_filenames"]}
        for path in COMPONENTS.rglob("*"):
            self.assertNotIn(path.name.casefold(), forbidden, str(path))

    def test_existing_publication_roots_remain_the_declared_set(self):
        discovered = {path.parent.name for path in REPOSITORY.glob("*/SKILL.md")}
        self.assertEqual(discovered, set(MANIFEST["protected_publication_roots"]))

    def test_api_manual_remains_development_only(self):
        self.assertTrue((REPOSITORY / MANIFEST["development_reference"]).is_file())
        self.assertNotIn("api_snapshot", MANIFEST)
        self.assertFalse((COMPONENTS / "contract/api-reference.md").exists())
        for component in MANIFEST["professionals"].values():
            self.assertNotIn("contracts/api-reference.md", component["resources"])

    def test_chinese_prompts_mirror_current_runtime_sources(self):
        chinese = COMPONENTS / "zh-CN"
        declared = MANIFEST["agent_sources"] + MANIFEST["professional_contracts"]
        declared += [expert["configuration"] for expert in MANIFEST["experts"].values()]
        declared += [str(path.relative_to(COMPONENTS))
                     for folder in ("skill", "contract", "tools")
                     for path in (COMPONENTS / folder).rglob("*.md")]
        actual = {str(path.relative_to(chinese)) for folder in
                  ("skill", "expert", "contract", "tools")
                  for path in (chinese / folder).rglob("*.md")}
        self.assertEqual(actual, set(declared))
        sources = {path: [path] for path in declared}
        sources["templates/skill-entry.md"] = ["build_workbuddy.py"]
        sources["templates/expert-bindings.md"] = ["build_workbuddy.py", "targets.json"]
        for path, expected in sources.items():
            translated = (chinese / path).read_text()
            entries = re.findall(r"<!-- prompt-source: (\S+) ([a-f0-9]{64}) -->", translated)
            self.assertEqual([source for source, _ in entries], expected)
            for source, digest in entries:
                self.assertEqual(hashlib.sha256((COMPONENTS / source).read_bytes()).hexdigest(),
                                 digest, f"Chinese translation is stale: {path}")
        for component in MANIFEST["professionals"].values():
            self.assertFalse(any(name.startswith("zh-CN/") for name in component["resources"]))

    def test_every_source_markdown_dependency_resolves(self):
        for path in COMPONENTS.rglob("*.md"):
            for dependency in local_dependencies(path):
                with self.subTest(source=path, dependency=dependency):
                    self.assertTrue(dependency.is_file())
                    self.assertTrue(dependency.is_relative_to(COMPONENTS))

    def test_professional_resources_form_closed_independent_packages(self):
        for component_id, component in MANIFEST["professionals"].items():
            with self.subTest(component=component_id):
                resources = {(COMPONENTS / name).resolve()
                             for name in component["resources"]}
                self.assertEqual(len(resources), len(component["resources"]))
                self.assertIn((COMPONENTS / component["entry"]).resolve(), resources)
                for path in resources:
                    self.assertTrue(path.is_file(), str(path))
                    self.assertTrue(path.is_relative_to(COMPONENTS))
                    self.assertNotIn(path.relative_to(COMPONENTS).parts[0],
                                     {"expert", "checks"})
                    for dependency in local_dependencies(path):
                        self.assertIn(dependency, resources,
                                      f"{component_id}: unbundled {dependency}")

    def test_professional_capability_scopes_are_documented(self):
        api = (REPOSITORY / MANIFEST["development_reference"]).read_text()
        mcp = json.loads((COMPONENTS / "checks/fixtures/mcp-contracts.json").read_text())["contracts"]
        slugs = []
        for component in MANIFEST["professionals"].values():
            slugs.append(component["export_name"])
            self.assertTrue(component["capabilities"])
            self.assertEqual(len(component["capabilities"]),
                             len(set(component["capabilities"])))
            for capability in component["capabilities"]:
                if capability in mcp:
                    self.assertTrue(mcp[capability]["operation_id"])
                    self.assertTrue(mcp[capability]["description"])
                    self.assertEqual(mcp[capability]["input_schema"]["type"], "object")
                else:
                    self.assertIn(capability, api)
            for source in component["provenance"]:
                self.assertTrue((REPOSITORY / source).is_file(), source)
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_report_skill_is_closed_and_separate_from_analysis_and_data_access(self):
        report = MANIFEST["report_skill"]
        resources = {(COMPONENTS / name).resolve() for name in report["resources"]}
        for path in [(COMPONENTS / report["entry"]).resolve(), *resources]:
            self.assertTrue(path.is_file())
            self.assertTrue(path.is_relative_to(COMPONENTS / "tools/report") or
                            path == COMPONENTS / "contract/report.md")
            for dependency in local_dependencies(path) if path.suffix == ".md" else ():
                self.assertIn(dependency, resources)
        self.assertNotIn("capabilities", report)
        self.assertTrue(all(not path.endswith(".mcp.json") for path in report["resources"].values()))

    def test_check_catalog_routes_to_existing_owned_method_sections(self):
        for domain, component in MANIFEST["professionals"].items():
            entry = COMPONENTS / component["entry"]
            text = entry.read_text()
            targets = [target for target in LINKS.findall(text)
                       if target.startswith("methods.md#")]
            with self.subTest(domain=domain):
                self.assertTrue(targets, "Object Skill needs an explicit check catalog")
                headings = re.findall(r"^#{1,6} (.+)$",
                                      (entry.parent / "methods.md").read_text(), re.M)
                anchors = {re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")
                           for heading in headings}
                for target in targets:
                    self.assertIn(target.split("#", 1)[1], anchors)

    def test_capabilities_have_unique_methods_reachable_from_their_catalogs(self):
        for domain, component in MANIFEST["professionals"].items():
            with self.subTest(domain=domain):
                entry = COMPONENTS / component["entry"]
                methods = (entry.parent / "methods.md").read_text()
                sections = {}
                endpoints = {}
                for section in re.split(r"^## ", methods, flags=re.M)[1:]:
                    heading, _, body = section.partition("\n")
                    anchor = re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")
                    self.assertNotIn(anchor, sections)
                    sections[anchor] = body
                    endpoint = heading.split(":", 1)[0]
                    if endpoint in component["capabilities"]:
                        self.assertNotIn(endpoint, endpoints)
                        endpoints[endpoint] = anchor
                self.assertEqual(set(endpoints), set(component["capabilities"]))
                pending = [target.split("#", 1)[1] for target in LINKS.findall(entry.read_text())
                           if target.startswith("methods.md#")]
                reachable = set()
                while pending:
                    anchor = pending.pop()
                    if anchor in reachable:
                        continue
                    self.assertIn(anchor, sections)
                    reachable.add(anchor)
                    pending.extend(target.split("#", 1)[1]
                                   for target in LINKS.findall(sections[anchor])
                                   if target.startswith(("#", "methods.md#")))
                for endpoint, anchor in endpoints.items():
                    self.assertIn(anchor, reachable, f"Unrouted {domain} capability: {endpoint}")

    def test_chinese_method_routes_match_runtime_sources(self):
        for domain in MANIFEST["professionals"]:
            root = COMPONENTS / f"skill/datas/{domain}"
            translated_root = COMPONENTS / f"zh-CN/skill/datas/{domain}"
            anchors = set(re.findall(r'<a id="([^"]+)"></a>',
                                     (translated_root / "methods.md").read_text()))
            for filename in ("definition.md", "methods.md"):
                with self.subTest(domain=domain, file=filename):
                    routes = [target for target in LINKS.findall((root / filename).read_text())
                              if target.startswith(("methods.md#", "#"))]
                    translated_routes = [target for target in LINKS.findall(
                        (translated_root / filename).read_text())
                        if target.startswith(("methods.md#", "#"))]
                    self.assertEqual(routes, translated_routes)
                    for target in translated_routes:
                        self.assertIn(target.split("#", 1)[1], anchors)

    def test_market_numeric_intervals_match_each_dimension_in_both_languages(self):
        expected_counts = {"Rating": 7, "Rating count": 6, "Listing age (calendar months)": 5}
        zh_labels = {"星级": "Rating", "评分数": "Rating count", "上架年龄（日历月）": "Listing age (calendar months)"}
        parsed = []
        for root, labels in ((COMPONENTS, {}), (COMPONENTS / "zh-CN", zh_labels)):
            groups = {name: [] for name in expected_counts}
            for line in (root / "skill/datas/market/semantics.md").read_text().splitlines():
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if not line.startswith("|") or len(cells) != 4:
                    continue
                dimension = labels.get(cells[0], cells[0])
                if dimension not in groups:
                    continue
                _, lower, upper, interval = cells
                expected = (f"[{lower}, +∞)" if upper == "null" else
                            f"({lower}, {upper}]" if dimension == "Rating" else
                            f"[{lower}, {upper}]" if dimension == "Rating count" else
                            f"[{lower}, {upper})")
                self.assertEqual(interval, expected)
                groups[dimension].append((float(lower), None if upper == "null" else float(upper)))
            for name, count in expected_counts.items():
                self.assertEqual(len(groups[name]), count)
                if name == "Rating":
                    self.assertEqual(groups[name][-1][1], 5)
                else:
                    self.assertIsNone(groups[name][-1][1])
                for index, (lower, upper) in enumerate(groups[name]):
                    if index:
                        previous = groups[name][index - 1][1]
                        self.assertEqual(lower, previous + 1 if name == "Rating count" else previous)
                    if name == "Rating":
                        matches = [n for n, (lo, hi) in enumerate(groups[name]) if lo < upper <= hi]
                    elif name == "Rating count":
                        for value in (lower, upper) if upper is not None else (lower,):
                            matches = [n for n, (lo, hi) in enumerate(groups[name]) if lo <= value and (hi is None or value <= hi)]
                            self.assertEqual(matches, [index])
                    else:
                        matches = [n for n, (lo, hi) in enumerate(groups[name]) if lo <= lower and (hi is None or lower < hi)]
                    self.assertEqual(matches, [index])
            parsed.append(groups)
        self.assertEqual(parsed[0], parsed[1])

    def test_market_sort_fields_match_the_recorded_interface_contract(self):
        contract = json.loads((REPOSITORY / "tests/fixtures/market-spu-contract.json").read_text())
        methods = (COMPONENTS / "skill/datas/market/methods.md").read_text()
        fields = re.findall(r"\| `([A-Za-z0-9]+) (?:asc|desc)` \|", methods)
        self.assertTrue(fields)
        self.assertTrue(set(fields) <= set(contract["sortBy"]))

    def test_professional_export_metadata_and_source_inventory(self):
        declared = MANIFEST["professionals"]
        folders = {path.name for path in (COMPONENTS / "skill").iterdir()
                   if path.is_dir()}
        self.assertEqual(folders, {"workflows", "datas"})
        for group, entries in (("skill/datas", [*declared.values(), *MANIFEST["endpoint_skills"].values()]),
                               ("tools", [MANIFEST["report_skill"]]),
                               ("skill/workflows", MANIFEST["workflows"].values())):
            directory = COMPONENTS / group
            self.assertEqual({path for path in directory.iterdir() if path.is_dir()},
                             {(COMPONENTS / item["entry"]).parent for item in entries})
        for component in declared.values():
            self.assertRegex(component["export_name"], r"^[a-z0-9-]{1,64}$")
            self.assertGreater(len(component["description"].strip()), 0)
            self.assertLessEqual(len(component["description"]), 1024)

    def test_expert_bindings_match_their_source_references(self):
        professionals = MANIFEST["professionals"]
        used_as_primary = set()
        configured = set()
        for expert_id, expert in MANIFEST["experts"].items():
            with self.subTest(expert=expert_id):
                if "workflow" in expert:
                    path = (COMPONENTS / expert["configuration"]).resolve()
                    configured.add(path)
                    entry = COMPONENTS / MANIFEST["workflows"][expert["workflow"]]["entry"]
                    self.assertEqual(set(local_dependencies(path)), {entry})
                    continue
                primary = expert["primary_professionals"]
                optional = expert["optional_professionals"]
                self.assertEqual(len(primary), 1)
                self.assertFalse(set(primary) & set(optional))
                self.assertEqual(len(primary + optional), len(set(primary + optional)))
                self.assertLessEqual(set(primary + optional), set(professionals))
                self.assertEqual(set(expert["allowed_checks"]), set(primary + optional))
                path = (COMPONENTS / expert["configuration"]).resolve()
                configured.add(path)
                referenced = {component_id for component_id, component
                              in professionals.items()
                              if (COMPONENTS / component["entry"]).resolve()
                              in set(local_dependencies(path))}
                self.assertEqual(referenced, set(primary + optional))
                used_as_primary.update(primary)
        self.assertEqual(used_as_primary, set(professionals) - {"market", "keyword"})
        self.assertEqual(configured, set((COMPONENTS / "expert").glob("*.md")))

    def test_product_discovery_and_workflow_do_not_ship_preset_catalog(self):
        workflow = MANIFEST["workflows"]["product-selection"]
        self.assertNotIn("catalog", workflow)
        resources = MANIFEST["professionals"]["product"]["resources"]
        self.assertFalse(any("selection-modes" in name for name in resources))

    def test_expert_question_routes_match_allowed_tasks_in_both_languages(self):
        skill_entries = {(COMPONENTS / item["entry"]).resolve(): domain
                         for domain, item in MANIFEST["professionals"].items()}
        for expert_id, expert in MANIFEST["experts"].items():
            if "workflow" in expert:
                continue  # Workflow bindings are checked by the data Skill routing tests.
            owner = expert
            route = expert["configuration"]
            expected = {(domain, task) for domain, tasks in owner["allowed_checks"].items()
                        for task in tasks}
            for prefix in ("", "zh-CN/"):
                path = COMPONENTS / (prefix + route)
                with self.subTest(expert=expert_id, language=prefix or "en"):
                    aliases = {}
                    for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", path.read_text()):
                        resolved = (path.parent / target.split("#", 1)[0]).resolve()
                        if prefix and resolved.is_relative_to(COMPONENTS / "zh-CN"):
                            resolved = COMPONENTS / resolved.relative_to(COMPONENTS / "zh-CN")
                        if resolved in skill_entries:
                            aliases[label.casefold()] = skill_entries[resolved]
                    actual = set()
                    text = path.read_text()
                    legacy_table = "| User question | Skill | Task |" in text or "| 用户问题 | 使用能力 | 分析任务 |" in text
                    if not legacy_table:
                        task_domains = {task: domain for domain, component in MANIFEST["professionals"].items()
                                        for task in re.findall(r"^\| ([^|]+?) \|", (COMPONENTS / component["entry"]).read_text(), re.M)
                                        if task not in {"Check", "---"}}
                        references = re.findall(r"`([^`\n]+)`", text)
                        self.assertTrue(references, "Expert methods must reference approved tasks")
                        for task in references:
                            self.assertIn(task, task_domains, f"Unknown task reference: {task}")
                            self.assertIn((task_domains[task], task), expected)
                            actual.add((task_domains[task], task))
                        self.assertEqual(actual, expected)
                        continue
                    for line in text.splitlines():
                        if not line.startswith("| "):
                            continue
                        cells = [cell.strip() for cell in line.strip("|").split("|")]
                        if len(cells) != 3 or cells[-1] in {"Task", "分析任务"}:
                            continue
                        self.assertTrue(cells[0])
                        self.assertIn(cells[1].casefold(), aliases)
                        domain = aliases[cells[1].casefold()]
                        task = cells[2].split("（", 1)[0].strip("`")
                        self.assertIn((domain, task), expected)
                        actual.add((domain, task))
                    self.assertEqual(actual, expected)

    def test_competitor_scope_uses_named_product_facts_and_only_category_benchmarks(self):
        workflow = MANIFEST["workflows"]["competitor-comparison"]
        self.assertNotIn("allowed_checks", workflow)
        names = set(workflow["data_skills"])
        self.assertEqual({key for key in names if key.startswith("market-")},
                         {"market-profile", "market-price-distribution"})
        self.assertIn("product-detail", names)
        self.assertEqual(MANIFEST["endpoint_skills"]["product-detail"]["fallback_endpoint"],
                         "realtime/product")
        self.assertNotIn("product-live", names)

    def test_product_detail_exposes_only_exact_product_lookup(self):
        for language in ("", "zh-CN"):
            definition = COMPONENTS / language / MANIFEST["endpoint_skills"]["product-detail"]["entry"]
            text = definition.read_text()
            with self.subTest(language=language):
                example = json.loads(re.search(r"```json\n(.+?)\n```", text, re.S)[1])
                self.assertIn("asins", example)
                self.assertNotRegex(text, r"(?m)^\| `(?:parentAsin|pageSize|page)`")

    def test_competitor_dimensions_resolve_tasks_through_their_owning_skills(self):
        workflow = MANIFEST["workflows"]["competitor-comparison"]
        for prefix in ("", "zh-CN/"):
            folder = COMPONENTS / prefix / "skill/workflows/competitor-comparison"
            methods = (folder / "methods.md").read_text()
            refs = {Path(link).parent.name for link in LINKS.findall(methods)
                    if link.startswith("../../datas/")}
            self.assertEqual(refs, set(workflow["data_skills"]))
            for dimension in range(1, 6):
                row = next(line for line in methods.splitlines()
                           if line.startswith(f"| {dimension}."))
                self.assertTrue(LINKS.findall(row.split("|")[3]))
    def test_review_evidence_routes_historical_and_live_text_to_separate_sources(self):
        root = COMPONENTS / "skill/datas/review"
        row = next(line for line in (root / "definition.md").read_text().splitlines()
                   if line.startswith("| Theme evidence |"))
        anchor = LINKS.findall(row)[0].split("#", 1)[1]
        sections = {}
        for section in re.split(r"^## ", (root / "methods.md").read_text(), flags=re.M)[1:]:
            heading, _, body = section.partition("\n")
            key = re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")
            sections[key] = (heading.split(":", 1)[0], body)
        sources = {sections[link[1:]][0] for link in LINKS.findall(sections[anchor][1])
                   if link.startswith("#")}
        self.assertEqual(sources, {"reviews/search", "realtime/reviews"})
        contract = json.loads((COMPONENTS / "checks/fixtures/mcp-contracts.json").read_text())["contracts"]["reviews/search"]
        properties = contract["input_schema"]["properties"]
        self.assertTrue({"asin", "page", "pageSize", "dateStart", "dateEnd"} <= set(properties))
        self.assertNotIn("cursor", properties)

    def test_product_fact_and_sales_tasks_route_to_their_distinct_mcp_contracts(self):
        root = COMPONENTS / "skill/datas/product"
        headings = {}
        for heading in re.findall(r"^## (.+)$", (root / "methods.md").read_text(), re.M):
            anchor = re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")
            headings[anchor] = heading.split(":", 1)[0]
        routes = {}
        for line in (root / "definition.md").read_text().splitlines():
            if line.startswith("| "):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                routes[cells[0]] = {headings[link.split("#", 1)[1]]
                                    for link in LINKS.findall(line) if link.startswith("methods.md#")}
        self.assertEqual(routes["Product facts"], {"Local analysis"})
        fact_route = re.search(r"^\| Product facts \|.*?methods\.md#([^)]+)",
                               (root / "definition.md").read_text(), re.M).group(1)
        sections = {}
        for section in re.split(r"^## ", (root / "methods.md").read_text(), flags=re.M)[1:]:
            heading, _, body = section.partition("\n")
            anchor = re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")
            sections[anchor] = body
        fact_sources = [headings[link[1:]] for link in LINKS.findall(sections[fact_route])
                        if link.startswith("#")]
        self.assertEqual(fact_sources, ["products/detail", "realtime/product"])
        for check in ("Product content", "Product comparison"):
            row = next(line for line in (root / "definition.md").read_text().splitlines()
                       if line.startswith(f"| {check} |"))
            method = LINKS.findall(row)[0].split("#", 1)[1]
            dependencies = LINKS.findall(sections[method])
            with self.subTest(check=check):
                self.assertIn("#" + fact_route, dependencies)
                self.assertNotIn("#realtimeproduct-real-time-product-details", dependencies)
        self.assertEqual(routes["Product sales trend"], {"products/sales-trend"})
        self.assertEqual(routes["Product history"], {"products/history"})

    def test_mcp_product_contracts_keep_exact_reads_separate_from_monthly_trends(self):
        contracts = json.loads((COMPONENTS / "checks/fixtures/mcp-contracts.json").read_text())["contracts"]
        detail = contracts["products/detail"]["input_schema"]["properties"]
        self.assertEqual(detail["asins"]["type"], "array")
        self.assertEqual(detail["parentAsin"]["type"], "string")
        self.assertFalse({"sortBy", "sortOrder", "keyword", "categoryPath"} & set(detail))
        sales = contracts["products/sales-trend"]["input_schema"]
        self.assertEqual(sales["required"], ["asin"])
        self.assertTrue({"startMonth", "endMonth"} <= set(sales["properties"]))
        self.assertNotIn("dateRange", sales["properties"])

    def test_product_expert_uses_asin_traffic_without_keyword_research(self):
        product = MANIFEST["experts"]["product-research"]
        self.assertNotIn("keyword", product["optional_professionals"])
        self.assertNotIn("keyword", product["allowed_checks"])
        self.assertEqual(product["allowed_checks"]["traffic"],
                         ["Traffic contributors", "Seller search performance",
                          "Seller advertising performance"])

    def test_competitor_expert_keeps_keyword_markets_out_of_its_scope(self):
        competitor = MANIFEST["experts"]["competitor-insight"]
        scope = MANIFEST["workflows"][competitor["workflow"]]["data_skills"]
        self.assertIn("traffic-terms", scope)
        self.assertNotIn("keyword", scope)
        self.assertIn("query-weeks", scope)

    def test_selection_expert_covers_markets_without_keyword_market_research(self):
        self.assertNotIn("market-research", MANIFEST["experts"])
        workflow = MANIFEST["experts"]["product-selection"]["workflow"]
        endpoints = set(MANIFEST["workflows"][workflow]["data_skills"])
        self.assertIn("market-discovery", endpoints)
        self.assertIn("traffic-terms", endpoints)
        self.assertFalse({"query-weeks", "search-placements", "keyword"} & endpoints)

    def test_keyword_expert_uses_term_evidence_without_whole_asin_diagnosis(self):
        key = MANIFEST["experts"]["keyword-research"]["workflow"]
        self.assertEqual(set(MANIFEST["workflows"][key]["data_skills"]), {
            "keyword-expansion", "keyword-statistics", "keyword-profile", "keyword-trend-profile",
            "query-weeks", "traffic-terms", "traffic-term-weeks",
        })

    def test_keyword_expansion_routes_only_to_relevance_ordered_candidates(self):
        for language in ("", "zh-CN"):
            root = COMPONENTS / language / "skill"
            methods = (root / "workflows/keyword-research/methods.md").read_text()
            expansion = next(line for line in methods.splitlines() if line.startswith("1. "))
            self.assertEqual(LINKS.findall(expansion), ["../../datas/keyword-expansion/definition.md"])
            data_skill = (root / "datas/keyword-expansion/definition.md").read_text()
            request = json.loads(re.search(r"```json\n(.+?)\n```", data_skill, re.S)[1])
            self.assertEqual((request["queryType"], request["sortBy"], request["sortOrder"]),
                             ("fuzzy", "relevanceScore", "desc"))
            for field in ("relevanceScore", "estimateSearchCount", "abaRank"):
                self.assertIn(field, data_skill)

    def test_shared_agent_sources_are_complete_and_separate(self):
        declared = {(COMPONENTS / name).resolve()
                    for name in MANIFEST["agent_sources"]}
        self.assertEqual(declared, set((COMPONENTS / "expert/agent-core").glob("*.md")))
        self.assertEqual(set(MANIFEST["professional_contracts"]),
                         {str(path.relative_to(COMPONENTS))
                          for path in (COMPONENTS / "contract").glob("*.md")
                          if path.name not in {"query.md", "report.md"}})

    def test_expert_roles_leave_common_runtime_wiring_to_the_builder(self):
        for expert_id, expert in MANIFEST["experts"].items():
            with self.subTest(expert=expert_id):
                path = COMPONENTS / expert["configuration"]
                referenced = {dependency for dependency in local_dependencies(path)
                              if dependency.is_relative_to(COMPONENTS / "expert/agent-core")}
                self.assertEqual(referenced, set())

    def test_source_manifest_distinguishes_builder_from_live_publication(self):
        publication = MANIFEST["publication"]
        for flag in ("source_directory_is_skill",
                     "platform_publication_performed", "clawhub_package_writes_enabled"):
            self.assertFalse(publication[flag])
        self.assertTrue(publication["exporter_implemented"])
        self.assertTrue((COMPONENTS / "build_workbuddy.py").is_file())
        self.assertFalse(MANIFEST["workbuddy_binding"]["binding_verified"])
        self.assertFalse(MANIFEST["workbuddy_binding"]["endpoint_ids_are_callable_names"])


if __name__ == "__main__":
    unittest.main()
