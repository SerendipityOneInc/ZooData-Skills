"""Ownership and scenario routing for the unified market skill."""

import re
import json
import runpy
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "amazon-market-analysis"
RETIRED_MARKET_SOURCE_SKILLS = {
    "amazon-market-entry-analyzer",
    "amazon-market-trend-scanner",
    "amazon-opportunity-discoverer",
}


class TestMarketSkillOwnership(unittest.TestCase):
    def test_upgraded_market_request_metadata_matches_shared_cli(self):
        owner = (ROOT / "zoodata" / "references" /
                 "openapi-reference.md").read_text()
        fixture = json.loads((ROOT / "tests/fixtures/market-spu-contract.json").read_text())
        metadata = owner.split("#### Numeric filter names", 1)[1].split("#### Numeric sort names", 1)[0]
        documented = set(re.findall(r"`([^`]+)`", metadata))
        cli = runpy.run_path(str(ROOT / "zoodata/scripts/zoodata.py"))
        self.assertEqual(documented, set(fixture["numericFilters"]))
        self.assertEqual(set(cli["MARKET_FILTER_FIELDS"]), set(fixture["numericFilters"]))
        self.assertEqual(set(cli["MARKET_SORT_FIELDS"]), set(fixture["sortBy"]))
        self.assertEqual(len(documented), 28)
        sort_doc = owner.split("#### Numeric sort names", 1)[1].split("## 2a.", 1)[0]
        self.assertEqual(set(re.findall(r"`([^`]+)`", sort_doc)), set(fixture["sortBy"]))
        self.assertEqual(set(cli["MARKET_DETAIL_ENDPOINTS"]), set(fixture["detailEndpoints"]))
        self.assertEqual(len(cli["MARKET_DETAIL_ENDPOINTS"]), 12)

    def test_one_market_skill_dispatches_three_independent_scenarios(self):
        skill = (MARKET / "SKILL.md").read_text()
        self.assertIn("## Source-of-truth boundaries", skill)
        for module in (
            "reference.md", "execution-guide.md", "evidence-protocols.md",
            "market-metric-semantics.md", "seller-input-semantics.md",
            "output-rules.md", "scenarios-discover.md",
            "scenarios-evaluate.md", "scenarios-track.md",
        ):
            with self.subTest(module=module):
                self.assertTrue((MARKET / "references" / module).is_file())
                self.assertIn(f"references/{module}", skill)

        for scenario in ("discover", "evaluate", "track"):
            with self.subTest(scenario=scenario):
                text = (MARKET / "references" /
                        f"scenarios-{scenario}.md").read_text()
                self.assertIn("| Stage | Entry input | Evidence | Conclusion authority |", text)
                self.assertIn("## Section content requirements", text)

        for retired_source in RETIRED_MARKET_SOURCE_SKILLS:
            self.assertFalse((ROOT / retired_source / "SKILL.md").exists())
            retired = ROOT / retired_source / "RETIRED.md"
            self.assertTrue(retired.is_file())
            self.assertIn("**Retired:**", retired.read_text())

        sync_script = (ROOT / "scripts" / "sync-scripts.sh").read_text()
        self.assertNotIn("SKIP_SKILLS", sync_script)
        self.assertIn("without SKILL.md is retained source", sync_script)

    def test_only_active_skill_entrypoints_are_discoverable(self):
        expected = {
            "amazon-analysis", "amazon-competitor-intelligence-monitor",
            "amazon-daily-market-radar", "amazon-keyword-traffic-analysis",
            "amazon-listing-audit-pro", "amazon-market-analysis",
            "amazon-pricing-command-center",
            "amazon-review-intelligence-extractor", "web-extract", "zoodata",
        }
        discovered = {
            path.parent.name for path in ROOT.glob("*/SKILL.md")
        }
        self.assertEqual(discovered, expected)
        self.assertEqual(len(discovered), 10)

    def test_zoodata_market_schema_has_one_owner(self):
        skill = (ROOT / "zoodata" / "SKILL.md").read_text()
        summary = (ROOT / "zoodata" / "references" /
                   "reference.md").read_text()
        owner = (ROOT / "zoodata" / "references" /
                 "openapi-reference.md").read_text()
        self.assertIn("openapi-reference.md § 2", skill)
        self.assertIn("openapi-reference.md", summary)
        self.assertNotIn("### markets/search — discovery", summary)
        self.assertIn("## 2. markets/search", owner)
        self.assertIn("## 2b. markets/history", owner)

    def test_unavailable_overview_is_owned_by_reference_not_skill_router(self):
        skill = (MARKET / "SKILL.md").read_text()
        reference = (MARKET / "references" / "reference.md").read_text()
        manifest = (MARKET / "scripts" / "allowed-commands.json").read_text()
        self.assertNotIn("markets/overview", skill)
        self.assertIn("`markets/overview` is absent", reference)
        self.assertNotIn('"market-overview"', manifest)
        self.assertNotIn("market-overview --", skill)

    def test_market_modules_do_not_include_repo_process(self):
        for path in (MARKET / "references").glob("*.md"):
            if path.name == "cli-contract.md":
                continue
            with self.subTest(module=path.name):
                text = path.read_text().lower()
                for forbidden in ("contributing.md", "agents.md", "pull request",
                                  "ci check", "repository maintenance"):
                    self.assertNotIn(forbidden, text)

    def test_parent_scoped_discovery_uses_child_ids(self):
        scenario = (MARKET / "references" / "scenarios-discover.md").read_text()
        reference = (MARKET / "references" / "reference.md").read_text()
        evidence = (MARKET / "references" / "evidence-protocols.md").read_text()
        shared_contract = (MARKET / "references" /
                           "analysis-contract.md").read_text()
        self.assertIn("every direct child", scenario)
        self.assertIn("A parent-wide top K requires complete", scenario)
        self.assertIn("`category.ids` in one `markets/search` request", reference)
        self.assertIn("`--parent` requires a nonempty JSON string array", reference)
        self.assertIn("`meta.total` counts matching rows after filters", reference)
        self.assertIn("compare returned IDs with the requested set", evidence)
        self.assertIn("transcript folding or truncation", shared_contract)
        for foreign_contract in ("--parent", "--category-ids", "page-size",
                                 "`meta.total`", "JSON string array"):
            self.assertNotIn(foreign_contract, scenario)

    def test_market_handoff_closes_a_stage_without_automatic_progression(self):
        guide = (MARKET / "references" / "execution-guide.md").read_text()
        output = (MARKET / "references" / "output-rules.md").read_text()
        discover = (MARKET / "references" / "scenarios-discover.md").read_text()

        self.assertIn("### Handoff Gate", guide)
        self.assertIn("material remaining decision", guide)
        self.assertIn("### Stage-End Selection List Rule", guide)
        self.assertIn("Ask another question or end this analysis", guide)
        self.assertIn("A bare number selects only the most recent final-list item", guide)
        self.assertIn("Do not auto-select a route", guide)
        self.assertIn("one final numbered selection list", output)
        self.assertIn("material evidence gaps in `Conclusion`", discover)
        self.assertNotIn("the specific next validation question in `Conclusion`", discover)

    def test_market_history_renders_only_verified_completed_months(self):
        contract = (MARKET / "references" / "analysis-contract.md").read_text()
        scenario = (MARKET / "references" / "scenarios-track.md").read_text()
        evidence = (MARKET / "references" / "evidence-protocols.md").read_text()
        output = (MARKET / "references" / "output-rules.md").read_text()
        semantics = (MARKET / "references" /
                     "market-metric-semantics.md").read_text()

        self.assertIn("two supplied compatible snapshots", scenario)
        self.assertIn("Persistent watch", scenario)
        self.assertIn("SKU grain or a legacy market schema", scenario)
        self.assertIn("product grain", evidence)
        self.assertNotIn("former flat market schema", scenario)
        self.assertIn("one-time comparison of supplied snapshots remains a historical trend", scenario)
        self.assertIn("Render history rows and missing-period treatment only through `output-rules.md`", scenario)
        self.assertNotIn("placeholder row", scenario)
        self.assertNotIn("current incomplete month", scenario)
        self.assertIn("project every returned `data[].points[]` point", evidence)
        self.assertIn("projected point count and dates equal", evidence)
        self.assertIn("is not an API coverage gap", evidence)
        self.assertIn("do not offer another paid query", evidence)
        self.assertIn("### Historical table rendering", output)
        self.assertIn("actual returned SPU snapshots", output)
        self.assertIn("only for verified month-end observations", output)
        self.assertNotIn("contains only actual returned month-end points", output)
        self.assertIn("omit the current incomplete calendar month", output)
        self.assertIn("omit missingness commentary entirely", output)
        self.assertIn("Render valid zero values directly", output)
        self.assertIn("unless the requested range itself needs clarification", output)
        self.assertIn("The API did not return {field} for {YYYY-MM-DD}", output)
        self.assertIn("Vague placeholders", output)
        self.assertIn("localized equivalents are invalid", output)
        self.assertIn("current incomplete calendar month is outside", semantics)
        self.assertIn("**Local unread state**", contract)
        self.assertIn("do not use truthiness", contract)
        self.assertIn("documented business definition as the semantic identity", contract)
        self.assertIn("### Trust documented evidence", contract)
        self.assertIn("a concrete contradiction or contract violation", contract)

    def test_market_results_are_projected_from_cleaned_up_raw_files(self):
        contract = (ROOT / "zoodata" / "references" / "cli-contract.md").read_text()
        evidence = (MARKET / "references" / "evidence-protocols.md").read_text()
        guide = (MARKET / "references" / "execution-guide.md").read_text()

        self.assertIn("<YYYY-MM-DD>/run-<secure-random>/", contract)
        self.assertIn("`EXIT`, `HUP`, `INT`, and `TERM`", contract)
        self.assertIn("without waiting for it", contract)
        self.assertIn("whole date buckets older than 30 days", contract)
        self.assertIn("Delete the raw result as soon as classification", contract)
        self.assertIn("token-truncation marker", contract)
        self.assertIn("Projection is a local, zero-credit transformation", contract)
        self.assertIn("## Market result projection", evidence)
        self.assertIn("validate the requested ID set", evidence)
        self.assertIn("`success=true` and `meta.total=N`", evidence)
        self.assertIn("shared temporary-result procedure", guide)

    def test_market_output_gate_rejects_implementation_detail_leakage(self):
        canonical = (ROOT / "zoodata" / "references" /
                     "analysis-contract.md").read_bytes()
        contract_path = MARKET / "references" / "analysis-contract.md"
        shared_contract = contract_path.read_text()
        output = (MARKET / "references" / "output-rules.md").read_text()
        guide = (MARKET / "references" / "execution-guide.md").read_text()
        skill = (MARKET / "SKILL.md").read_text()

        self.assertEqual(contract_path.read_bytes(), canonical)
        self.assertIn("## Rule hierarchy", shared_contract)
        self.assertIn("### Keep implementation internal", shared_contract)
        self.assertIn("raw payload capture", shared_contract)
        self.assertIn("temporary paths", shared_contract)
        self.assertIn("projection, parsing, cleanup", shared_contract)
        self.assertIn("### 7. Final Response Gate", shared_contract)
        self.assertIn("discard the draft and render it again", shared_contract)
        self.assertIn("Do not patch a leaked sentence", shared_contract)
        self.assertIn("Read and apply `references/analysis-contract.md`", skill)
        self.assertIn("Apply `analysis-contract.md § 7. Final Response Gate`", guide)
        self.assertIn("owns market-specific language", output)
        self.assertNotIn("## User-Facing Output Boundary", output)
        self.assertNotIn("## Retrieval Progress Updates", output)

    def test_general_analysis_ownership_keeps_details_in_modules(self):
        root = ROOT / "amazon-analysis"
        skill = (root / "SKILL.md").read_text()
        guide = (root / "references" / "execution-guide.md").read_text()
        reference = (root / "references" / "reference.md").read_text()
        for heading in ("## Product Selection Mode Mapping", "## Market Health Assessment",
                        "## Output Standards — Full Specification"):
            self.assertIn(heading, guide)
            self.assertNotIn(heading, skill)
        self.assertIn("## Cross-endpoint field identity", reference)
        self.assertNotIn("## Interface Data Differences", guide)
        self.assertNotIn("## Output Spec", skill)

    def test_market_concentration_and_rank_meanings_have_one_local_owner(self):
        skill = (MARKET / "SKILL.md").read_text()
        self.assertIn("`references/market-metric-semantics.md` owns the meaning, denominator", skill)
        self.assertIn("`references/reference.md` owns only production API facts", skill)
        semantics = (MARKET / "references/market-metric-semantics.md").read_text()
        reference = (MARKET / "references/reference.md").read_text()
        self.assertIn("market-metric-semantics.md#structure-entry-and-concentration", reference)
        # API field inventories may name these fields; assigning their meaning
        # or denominator belongs only to the declared semantic owner.
        definitions = (
            r"`?concentrationRate`?\s+follows\s+the sample",
            r"Entity\s+`?rank`?\s+follows\s+(?:sampleType|the sample)",
            r"`?distributionRank`?\s+(?:is|are)\s+display order",
            r"Content and seller-country memberships\s+(?:can\s+)?overlap",
            r"unknown fulfillment\s+stays in the denominator",
        )
        for pattern in definitions:
            self.assertRegex(semantics, pattern)
            for path in (MARKET / "references").glob("*.md"):
                if path.name != "market-metric-semantics.md":
                    with self.subTest(pattern=pattern, module=path.name):
                        self.assertNotRegex(path.read_text(), pattern)

    def test_general_market_response_rules_stay_out_of_execution_guide(self):
        root = ROOT / "amazon-analysis"
        skill = (root / "SKILL.md").read_text()
        self.assertIn("`references/reference.md` owns endpoint availability, request and response fields", skill)
        reference = (root / "references/reference.md").read_text()
        guide = (root / "references/execution-guide.md").read_text()
        self.assertIn("reference.md#profile-distributions-and-concentration", guide)
        definitions = (
            r"Distribution bucket shares use .* denominator",
            r"Top N new-product monthlySalesRate/monthlyRevenueRate use .* denominators",
            r"(?:Price bands|Price buckets) use inclusive lower.*exclusive upper",
            r"(?:No bucket new-product or brand-concentration block is provided|distribution buckets do not provide new-product profiles)",
        )
        for pattern in definitions:
            with self.subTest(pattern=pattern):
                self.assertRegex(reference, pattern)
                self.assertNotRegex(guide, pattern)

    def test_market_temporal_inference_limits_have_one_owner(self):
        reference = (MARKET / "references/reference.md").read_text()
        semantics = (MARKET / "references/market-metric-semantics.md").read_text()
        launch = reference.split("### Listing launch composition", 1)[1].split("### History", 1)[0]
        history = reference.split("### History", 1)[1].split("### Credits", 1)[0]
        self.assertIn("market-metric-semantics.md#time-and-product-observations", launch)
        self.assertIn("market-metric-semantics.md#business-time-identity", launch)
        self.assertIn("market-metric-semantics.md#time-and-product-observations", history)
        # Schema availability belongs to the API reference; conclusions do not.
        self.assertIn("Each point has `date` (YYYY-MM or YYYY) and productCount", launch)
        self.assertIn("There is no returned resolvedDate", launch)
        for pattern in (r"not (?:repeated demand observations or )?historical market growth",
                        r"(?:not|or) all products launched", r"old SKU history is never substituted"):
            self.assertNotRegex(reference, pattern)
        self.assertIn("not repeated demand observations or historical market growth", semantics)
        self.assertIn("do not count all products launched", semantics)
        self.assertIn("does not fill gaps or substitute SKU history", semantics)

    def test_general_output_preserves_each_sources_business_time(self):
        guide = (ROOT / "amazon-analysis/references/execution-guide.md").read_text()
        reporting = guide.split("### Business-time reporting (all modes)", 1)[1].split("### Disclaimer", 1)[0]
        provenance = guide.split("### Data Provenance Block", 1)[1].split("### API Usage Summary", 1)[0]
        quick = guide.split("## Execution Mode", 1)[1].split("## Product Selection", 1)[0]
        self.assertIn("Business-time reporting", quick)
        self.assertIn("time-field meaning from `reference.md`", reporting)
        self.assertIn("Mixed reports retain separate time identities", reporting)
        self.assertIn("First-launch month/year", reporting)
        self.assertIn("must not stand in for data business time", reporting)
        self.assertIn("or block a valid answer", reporting)
        self.assertIn("Business dates / periods by source", provenance)
        self.assertIn("mixed market-profile, history and launch-composition reports", provenance)
        self.assertNotRegex(guide, r"\|\s*(?:Timestamp|Data Freshness)\s*\|")
        self.assertNotIn("DB data ~T+1, realtime = live", guide)
        self.assertNotIn("API data as of [date]", guide)

    def test_focused_market_discovery_routes_away_from_general_skill(self):
        general = (ROOT / "amazon-analysis" / "SKILL.md").read_text()
        general_description = general.split("description: >", 1)[1].split("metadata:", 1)[0]
        market_description = (MARKET / "SKILL.md").read_text().split(
            "description: >", 1)[1].split("metadata:", 1)[0]
        self.assertIn("category-market\n  discovery", general_description)
        self.assertIn("amazon-market-analysis", general_description)
        self.assertIn("discover\n  candidate niches and products", market_description)

    def test_market_field_and_history_names_match_spu_response(self):
        api_owners = [
            ROOT / "zoodata/references/openapi-reference.md",
            MARKET / "references/reference.md",
            *[ROOT / name / "references/reference.md" for name in (
                "amazon-analysis", "amazon-competitor-intelligence-monitor",
                "amazon-daily-market-radar", "amazon-listing-audit-pro",
                "amazon-pricing-command-center", "amazon-review-intelligence-extractor")],
        ]
        for path in api_owners:
            text = path.read_text()
            with self.subTest(path=path):
                for required in ("SPU", "includeDescendantCategoryProducts", "categoryIds", "dateRange",
                                 "sampleMonthlySales", "avgMonthlySales",
                                 "totalMonthlyRevenue", "sellerCountryCodes",
                                 "HTTP 410", "exact common snapshot", "two decimals"):
                    self.assertIn(required.lower(), text.lower())
                # This skill routes metric meanings to its semantic owner;
                # the other standalone skills keep them in their API reference.
                if path != MARKET / "references/reference.md":
                    self.assertIn("Content and seller-country memberships overlap", text)
                self.assertNotIn("Response `data.points[]`", text)
                self.assertNotIn("Required: `categoryId`, `dimension`", text)
                self.assertNotIn("sampleAvgMonthlySalesMin", text)
        for path in ROOT.glob("amazon-*/references/*.md"):
            if path.parent.parent.name in RETIRED_MARKET_SOURCE_SKILLS:
                continue
            text = path.read_text()
            for obsolete in ("sampleConservative", "actualStartDate", "actualEndDate"):
                self.assertNotIn(obsolete, text, str(path))
            self.assertIsNone(re.search(r"sampleNewProduct\w*6m", text), str(path))
        semantics = (MARKET / "references/market-metric-semantics.md").read_text()
        for required in ("SPUs", "per-SPU", "overlap", "unknown fulfillment",
                         "SKU history", "cohorts", "Missing baseline",
                         "rounded zero", "Full-market sales"):
            self.assertIn(required.lower(), semantics.lower())

    def test_upgraded_response_shapes_and_field_identity_are_documented(self):
        fixture = json.loads((ROOT / "tests/fixtures/market-spu-contract.json").read_text())
        fields = fixture["responseFields"]
        self.assertEqual(list(fields["MarketHistoryFact"]), ["date", "marketSize", "sampleProfile"])
        self.assertEqual(list(fields["MarketHistorySeries"]),
                         ["site", "category", "includeDescendantCategoryProducts",
                          "sampleType", "currency", "points"])
        for name in ("PriceBucket", "RatingBucket", "RatingCountBucket", "ListingAgeBucket",
                     "FulfillmentBucket", "SellerCountryBucket", "ContentBucket"):
            with self.subTest(model=name):
                self.assertTrue({"bucketProductCount", "bucketProductRate",
                                 "monthlySalesRate", "monthlyRevenueRate"} <= set(fields[name]))
                self.assertFalse({"membershipProductCnt", "productMembershipRate",
                                  "saleCntRate", "saleAmtRate"} & set(fields[name]))
        for model in ("MarketSearchFact", "MarketProfile"):
            self.assertIn("resolvedDate", fields[model])
            self.assertNotIn("dt", fields[model])
            self.assertNotIn("productGrain", fields[model])
        self.assertNotIn("sampleProductCount", fields["MarketProfile"])
        self.assertTrue({"productCount", "monthlySales", "monthlyRevenue",
                         "avgMonthlySales", "avgMonthlyRevenue"} <= set(fields["SampleProfile"]))
        self.assertTrue({"monthlySales", "monthlyRevenue"} <= set(fields["TopNConcentration"]))
        self.assertTrue({"productCount", "monthlySales", "monthlyRevenue"} <=
                        set(fields["MarketHistorySampleProfile"]))
        self.assertIn("avgMonthlySales", fields["MarketHistorySampleProfile"])
        self.assertNotIn("resolvedDate", fields["ListingLaunchTrend"])
        self.assertIn("points", fields["ListingLaunchTrend"])
        for model, entity_field in (("TopProductConcentration", "topProductList"),
                                    ("BrandConcentration", "topBrandList"),
                                    ("SellerConcentration", "topSellerList")):
            self.assertIn("topnMetrics", fields[model])
            self.assertIn(entity_field, fields[model])
            self.assertNotIn("topnBrandMetrics", fields[model])
        self.assertIn("topnBrandMetrics", fields["ConcentrationProfile"])
        for model in ("TopProduct", "TopBrand", "TopSeller"):
            self.assertIn("rank", fields[model])
            self.assertNotIn("distributionRank", fields[model])
        self.assertIn("distributionRank", fields["SellerCountryBucket"])
        evidence = (MARKET / "references/evidence-protocols.md").read_text()
        self.assertIn("data[].points[]", evidence)
        self.assertIn("complete identity", evidence)
        self.assertIn("Multiple series for one category ID", evidence)
        for path in [ROOT / "zoodata/references/openapi-reference.md",
                     *[p for p in ROOT.glob("amazon-*/references/reference.md")
                       if (p.parents[1] / "SKILL.md").exists() and "All 14 market endpoints" in p.read_text()]]:
            text = path.read_text()
            for required in ("resolvedDate", "data[]", "points[]", "bucketProductCount",
                             "bucketProductRate", "monthlySalesRate", "monthlyRevenueRate",
                             "no top-level sample totals", "Series are separated"):
                self.assertIn(required, text, str(path))
            for obsolete in ("categoryScope=direct|subtree", "productGrain=SPU",
                             "The returned `dt`", "Returns flat `data[]` rows"):
                self.assertNotIn(obsolete, text, str(path))

    def test_market_request_types_and_optional_response_shapes_are_pinned(self):
        fixture = json.loads((ROOT / "tests/fixtures/market-spu-contract.json").read_text())
        self.assertEqual(len(fixture["endpointContracts"]), 14)
        requests = fixture["requestContracts"]
        self.assertEqual(len(requests), 4)
        self.assertEqual(requests["MarketSearchRequest"]["required"], [])
        self.assertEqual(requests["MarketHistoryRequest"]["required"],
                         ["categoryIds", "dateFrom", "dateTo"])
        for name in ("MarketIdentity", "MarketLaunchRequest"):
            self.assertEqual(requests[name]["required"], ["categoryIds"])
        self.assertEqual(requests["MarketIdentity"]["properties"]["date"]["type"], "string(date)|null")
        self.assertNotIn("date", requests["MarketLaunchRequest"]["properties"])
        for name in ("dateFrom", "dateTo"):
            self.assertEqual(requests["MarketLaunchRequest"]["properties"][name]["type"], "string(date)|null")
        self.assertNotIn("date", requests["MarketHistoryRequest"]["properties"])
        self.assertEqual(requests["MarketIdentity"]["properties"]["includeDescendantCategoryProducts"],
                         {"type": "boolean", "default": True})
        for model, fields in fixture["responseFields"].items():
            for field, kind in fields.items():
                with self.subTest(model=model, field=field):
                    self.assertTrue(kind.endswith("|null"), kind)
        self.assertEqual(fixture["responseFields"]["PriceBucket"]["bucketProductCount"], "integer|null")
        self.assertEqual(fixture["responseFields"]["PriceBucket"]["monthlyRevenue"], "number|null")
        self.assertEqual(fixture["responseFields"]["MarketHistorySeries"]["points"],
                         "array<MarketHistoryFact>|null")

    def test_market_legacy_search_compatibility_stays_in_api_owner(self):
        for path in [ROOT / "zoodata/references/openapi-reference.md", MARKET / "references/reference.md"]:
            text = path.read_text()
            self.assertIn("Search alone normalizes legacy", text)
            self.assertIn("current MCP inputSchema", text)
            self.assertIn("even `date=null` is rejected", text)
            self.assertNotIn("Old flat Min/Max filters are not accepted", text)
        semantics = (MARKET / "references/market-metric-semantics.md").read_text()
        self.assertIn("monthlySalesRate", semantics)
        self.assertIn("monthlyRevenueRate", semantics)
        self.assertIn("enclosing ranked group", semantics)
        self.assertIn("bucketIndex", semantics)
        self.assertNotIn("normalize_legacy_market_search", semantics)

    def test_market_router_and_scenarios_respect_declared_ownership(self):
        skill = (MARKET / "SKILL.md").read_text()
        discover = (MARKET / "references" / "scenarios-discover.md").read_text()
        evaluate = (MARKET / "references" / "scenarios-evaluate.md").read_text()
        track = (MARKET / "references" / "scenarios-track.md").read_text()
        for foreign_definition in ("markets/overview", "`total*`", "`sample*`"):
            self.assertNotIn(foreign_definition, skill)
        for api_syntax in ("--parent", "--category-ids", "page-size", "`meta.total`"):
            self.assertNotIn(api_syntax, discover)
        for foreign_definition in ("page-size", "--dimension", "`total*`", "`sample*`"):
            self.assertNotIn(foreign_definition, evaluate)
        for rendering_rule in ("placeholder row", "current incomplete month"):
            self.assertNotIn(rendering_rule, track)

    def test_readme_endpoint_counts_and_reference_only_reviews_route_are_explicit(self):
        readme = (ROOT / "README.md").read_text()
        readme_zh = (ROOT / "README.zh-CN.md").read_text()
        self.assertNotIn("Amazon Commerce Data, 11 Endpoints", readme)
        self.assertNotIn("数据层概览，11 个 API 接口", readme_zh)
        for path in (
            ROOT / "zoodata" / "references" / "reference.md",
            ROOT / "zoodata" / "references" / "openapi-reference.md",
        ):
            text = path.read_text()
            section = text.split("## 6c. reviews/search", 1)[1].split("\n---", 1)[0]
            self.assertIn("direct API reference only", section)
            self.assertIn("has no\n`reviews/search` subcommand", section)
            self.assertIn("not counted in the 36 CLI-backed", section)

    def test_market_endpoint_inventory_lists_all_14_active_routes(self):
        fixture = json.loads((ROOT / "tests/fixtures/market-spu-contract.json").read_text())
        expected = {"markets/search", "markets/history",
                    *("markets/" + name for name in fixture["detailEndpoints"])}
        for path in (ROOT / "zoodata/README.md", ROOT / "zoodata/SKILL.md"):
            routes = re.findall(r"^\| [0-9]+ \| `([^`]+)`", path.read_text(), re.M)
            routes = [route.removeprefix("/openapi/v2/") for route in routes]
            self.assertEqual(len(routes), 36, str(path))
            self.assertEqual({route for route in routes if route.startswith("markets/")},
                             expected, str(path))

    def test_general_analysis_usage_uses_cli_accumulated_metadata(self):
        guide = (ROOT / "amazon-analysis" / "references" /
                 "execution-guide.md").read_text()
        for field in ("meta.apiCalls", "meta.creditsConsumed",
                      "meta.creditsRemaining"):
            self.assertIn(field, guide)
        self.assertNotIn("_credits.consumed", guide)
        self.assertNotIn("_credits.remaining", guide)
        self.assertNotIn("📊 **API Usage**", guide)

    def test_business_time_identity_reaches_evidence_and_output_gates(self):
        semantics = (MARKET / "references/market-metric-semantics.md").read_text()
        self.assertIn("`resolvedDate` is the actual business date", semantics)
        self.assertIn("may differ from the returned business date", semantics)
        self.assertIn("each point's `date` is the business date", semantics)
        self.assertIn("valid without a separate sample business date", semantics)
        self.assertIn("Do not reinterpret a launch period", semantics)
        self.assertNotRegex(semantics, r"Every claim retains.*snapshot date")
        for module in ("evidence-protocols.md", "execution-guide.md", "output-rules.md"):
            text = (MARKET / "references" / module).read_text()
            with self.subTest(module=module):
                self.assertIn("market-metric-semantics.md § Business-time identity", text)
                self.assertNotRegex(text, r"require source, scope, returned date")
                self.assertNotRegex(text, r"returned date (?:alongside every|with every market) field")
        guide = (MARKET / "references/execution-guide.md").read_text()
        self.assertIn("accept a valid endpoint time identity without requiring additional date fields", guide)
        self.assertIn("Do not reject a contract-conforming response", guide)
        output = (MARKET / "references/output-rules.md").read_text()
        self.assertIn("首次上架月份/年份", output)
        self.assertIn("数据日期", output)
        self.assertIn("Do not add a missing-snapshot warning", output)
        evidence = (MARKET / "references/evidence-protocols.md").read_text()
        self.assertIn("project every relevant `points[].date` and productCount", evidence)

    def test_cross_endpoint_capabilities_distinguish_rating_counts_and_sample_bsr(self):
        fixture = json.loads((ROOT / "tests/fixtures/market-spu-contract.json").read_text())
        self.assertIn("avgBigBsr30d", fixture["responseFields"]["MarketSearchFact"])
        self.assertIn("avgBigBsr30d", fixture["numericFilters"])
        self.assertIn("avgBigBsr30d", fixture["sortBy"])
        for root in (ROOT / "amazon-analysis", ROOT / "zoodata"):
            text = (root / "references/reference.md").read_text()
            section = text.split("## Cross-endpoint field identity" if root.name == "amazon-analysis"
                                 else "## Field Differences Across Endpoints", 1)[1]
            rows = [line.split("|")[1:-1] for line in section.splitlines()
                    if line.startswith("|")]
            bsr = next(row for row in rows if row[0].strip() == "BSR")
            self.assertIn("avgBigBsr30d", bsr[1])
            self.assertIn("sample average", bsr[1])
            self.assertIn("individual product", bsr[2])
            for row in rows:
                if "avgRatingCount" in row[1] or "ratingCount" in row[2]:
                    self.assertEqual(row[0].strip(), "Rating count")
                    self.assertNotIn("reviewCount", row[4])
                if "reviewCount" in row[4]:
                    self.assertIn("Written-review", row[0])
                    self.assertNotIn("avgRatingCount", row[1])
        guide = (ROOT / "amazon-analysis/references/execution-guide.md").read_text()
        self.assertIn("平均评分数", guide)
        self.assertNotRegex(guide, r"(?i)avg review count.*avgRatingCount")
        # Check endpoint field inventories too, not just comparison-table labels.
        references = [ROOT / "zoodata/references/reference.md",
                      ROOT / "zoodata/references/openapi-reference.md",
                      *[p.parent / "references/reference.md"
                        for p in ROOT.glob("amazon-*/SKILL.md")]]
        for path in references:
            for row in path.read_text().splitlines():
                if re.match(r"\|\s*`?ratingCount`?\s*\|", row):
                    with self.subTest(reference=path, row=row):
                        self.assertNotRegex(row, r"(?i)review count")

    def test_general_operations_routes_history_by_subject(self):
        ops = (ROOT / "amazon-analysis" / "references" /
               "scenarios-ops.md").read_text()
        self.assertIn("`history` for product-level ASIN history", ops)
        self.assertIn("`market-history` for category-market history", ops)
        self.assertIn("market-history --category-id", ops)
        self.assertIn("history --asins", ops)
        self.assertNotIn("snapshot data only (no historical comparison)", ops.lower())
        self.assertNotIn("compare results manually across snapshots", ops)

    def test_specialized_skill_descriptions_do_not_claim_total_endpoint_count(self):
        for skill_name in ("amazon-listing-audit-pro",
                           "amazon-review-intelligence-extractor"):
            skill = (ROOT / skill_name / "SKILL.md").read_text()
            description = skill.split("description: >", 1)[1].split("metadata:", 1)[0]
            self.assertIn("Uses up to 11 relevant ZooData endpoints", description)
            self.assertNotIn("Uses all 11 ZooData API endpoints", description)


if __name__ == "__main__":
    unittest.main()
