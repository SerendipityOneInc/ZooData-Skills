"""Market skill module boundaries introduced by the markets API upgrade."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestMarketSkillOwnership(unittest.TestCase):
    def test_market_workflow_modules_are_dispatched_by_their_skills(self):
        modules = {
            "amazon-market-entry-analyzer": "market-workflow.md",
            "amazon-market-trend-scanner": "scan-workflow.md",
            "amazon-opportunity-discoverer": "category-selection.md",
        }
        for skill, module in modules.items():
            with self.subTest(skill=skill):
                skill_text = (ROOT / skill / "SKILL.md").read_text()
                workflow = ROOT / skill / "references" / module
                self.assertTrue(workflow.is_file())
                self.assertIn(f"references/{module}", skill_text)
                self.assertIn("markets/", (ROOT / skill / "references" /
                                       "reference.md").read_text())

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

    def test_removed_overview_is_absent_from_runtime_skills(self):
        for skill_dir in (ROOT / "zoodata", *ROOT.glob("amazon-*")):
            for path in skill_dir.rglob("*"):
                if path.suffix not in {".md", ".py", ".json"}:
                    continue
                with self.subTest(path=path.relative_to(ROOT)):
                    content = path.read_text()
                    self.assertNotIn("markets/overview", content)
                    self.assertNotIn("market-overview", content)

    def test_new_workflow_modules_do_not_include_repo_process(self):
        modules = (
            "amazon-market-entry-analyzer/references/market-workflow.md",
            "amazon-market-trend-scanner/references/scan-workflow.md",
            "amazon-opportunity-discoverer/references/category-selection.md",
        )
        for name in modules:
            with self.subTest(module=name):
                text = (ROOT / name).read_text().lower()
                for forbidden in ("contributing.md", "agents.md", "pull request",
                                  "ci check", "repository maintenance"):
                    self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
