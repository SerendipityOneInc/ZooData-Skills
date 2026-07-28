"""Execution smoke tests for every skill's bundled CLI.

Goal: verify each of the 12 skills actually *executes* — the CLI imports and
builds its argparse tree, every subcommand the skill's SKILL.md declares it
uses really exists and its parser is well-formed, and `check` runs without a
Python traceback. All of this is **credit-free** (no API calls).

An optional live tier (one cheap real call per CLI) runs only when
`RUN_LIVE_SKILL_TESTS=1` and a `ZOODATA_API_KEY` is present.

Run: `python3 -m pytest tests/test_skill_execution.py -v`
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _discover_skills():
    """Return [(skill_name, cli_path)] for every skill that ships a CLI."""
    out = []
    for skill_md in sorted(REPO.glob("*/SKILL.md")):
        d = skill_md.parent
        for cli_name in ("zoodata.py", "webtools.py"):
            cli = d / "scripts" / cli_name
            if cli.exists():
                out.append((d.name, cli))
                break
    return out


SKILLS = _discover_skills()


def _declared_subcommands(skill_dir: Path):
    """Parse the "this skill's workflows use: a, b, ..." line from SKILL.md.

    Returns a set of subcommand tokens, or None if the skill declares the full
    surface ("all subcommands") or has no such line.
    """
    text = (skill_dir / "SKILL.md").read_text()
    # Match only to end of the declaration line — NOT across blank lines (re.S
    # would over-capture later bullets and could inject false subcommands).
    m = re.search(r"this skill's workflows use:\s*(.+)", text)
    if not m:
        return None
    frag = m.group(1)
    if "all subcommands" in frag.lower():
        return None
    return set(re.findall(r"`([a-z0-9\-]+)`", frag))


def _actual_subcommands(cli: Path):
    """Extract argparse subcommand names from the CLI source (add_parser calls)."""
    src = cli.read_text()
    return set(re.findall(r"add_parser\(\s*[\"']([a-z0-9\-]+)[\"']", src))


def _run(cli: Path, *args, timeout=30):
    return subprocess.run(
        [sys.executable, str(cli), *args],
        capture_output=True, text=True, timeout=timeout,
        cwd=str(cli.parent.parent),
        env={**os.environ, "ZOODATA_API_KEY": os.environ.get("ZOODATA_API_KEY", "")},
    )


class TestSkillCliExecutes(unittest.TestCase):
    def test_at_least_all_twelve_skills_discovered(self):
        # Guard: the suite must actually cover every skill, not silently skip.
        self.assertEqual(len(SKILLS), 12, f"discovered {len(SKILLS)}: {[s for s,_ in SKILLS]}")

    def test_cli_help_runs(self):
        """`<cli> --help` exits 0 with no Python traceback (CLI imports + builds)."""
        for name, cli in SKILLS:
            with self.subTest(skill=name):
                r = _run(cli, "--help")
                self.assertEqual(r.returncode, 0, f"{name} --help exit {r.returncode}\n{r.stderr}")
                self.assertNotIn("Traceback (most recent call last)", r.stderr, name)

    def test_declared_subcommands_exist_in_cli(self):
        """Every subcommand a SKILL.md claims to use must exist in its CLI."""
        for name, cli in SKILLS:
            declared = _declared_subcommands(cli.parent.parent)
            if declared is None:
                continue  # full-surface skill (zoodata) or no declaration
            actual = _actual_subcommands(cli)
            with self.subTest(skill=name):
                missing = declared - actual
                self.assertEqual(missing, set(),
                                 f"{name} declares subcommands not in its CLI: {sorted(missing)}")

    def test_declared_subcommand_parsers_are_wellformed(self):
        """`<cli> <subcmd> --help` exits 0 for each declared subcommand (parser builds)."""
        for name, cli in SKILLS:
            declared = _declared_subcommands(cli.parent.parent)
            subcmds = sorted(declared) if declared else sorted(_actual_subcommands(cli))
            for sub in subcmds:
                with self.subTest(skill=name, sub=sub):
                    r = _run(cli, sub, "--help")
                    self.assertEqual(r.returncode, 0,
                                     f"{name} {sub} --help exit {r.returncode}\n{r.stderr}")
                    self.assertNotIn("Traceback (most recent call last)", r.stderr)

    def test_check_runs_without_crash(self):
        """`<cli> check` must not crash with a traceback (exit code is env-dependent:
        0 when a key is configured, non-zero when not — both are 'normal')."""
        for name, cli in SKILLS:
            with self.subTest(skill=name):
                r = _run(cli, "check")
                self.assertNotIn("Traceback (most recent call last)", r.stderr,
                                 f"{name} check crashed:\n{r.stderr}")
                self.assertIn(r.returncode, (0, 1, 2), f"{name} check exit {r.returncode}")


@unittest.skipUnless(
    os.environ.get("RUN_LIVE_SKILL_TESTS") == "1" and os.environ.get("ZOODATA_API_KEY"),
    "live tier: set RUN_LIVE_SKILL_TESTS=1 and ZOODATA_API_KEY to run real API calls",
)
class TestSkillCliLive(unittest.TestCase):
    """One cheap real call per zoodata CLI: `categories --marketplace US` is a
    zero/low-cost endpoint. Confirms the end-to-end HTTP + auth path works."""

    def test_categories_call_succeeds(self):
        for name, cli in SKILLS:
            if cli.name != "zoodata.py":
                continue
            with self.subTest(skill=name):
                r = _run(cli, "categories", "--marketplace", "US", timeout=60)
                self.assertEqual(r.returncode, 0, f"{name} categories failed:\n{r.stderr}")
                self.assertNotIn("Traceback (most recent call last)", r.stderr)

    def test_composite_workflow_reports_aggregated_credits(self):
        """A real composite run (market-entry fans out over ~all endpoints) must
        execute end-to-end AND surface an aggregated credit total in its meta —
        the regression the _CreditTracker fix targets (was reported as 1)."""
        import json
        cli = REPO / "amazon-market-entry-analyzer" / "scripts" / "zoodata.py"
        r = _run(cli, "market-entry", "--keyword", "yoga mat", timeout=300)
        self.assertEqual(r.returncode, 0, f"market-entry failed:\n{r.stderr[:400]}")
        meta = json.loads(r.stdout).get("meta", {})
        self.assertGreater(meta.get("apiCalls", 0), 1, "composite should fan out to many calls")
        self.assertGreaterEqual(meta.get("creditsConsumed", 0), meta.get("apiCalls", 0),
                                "aggregated credits must cover every internal call, not just one")


if __name__ == "__main__":
    unittest.main()
