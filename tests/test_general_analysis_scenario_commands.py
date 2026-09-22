"""Every general-analysis scenario command must be allowed and parseable."""

import argparse
import importlib.util
import json
import shlex
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "amazon-analysis"
CLI_PATH = SKILL / "scripts" / "zoodata.py"


class ParsedCommand(Exception):
    def __init__(self, unknown):
        self.unknown = unknown


class TestGeneralAnalysisScenarioCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("general_analysis_cli", CLI_PATH)
        cls.cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.cli)
        cls.allowed = set(json.loads(
            (SKILL / "scripts" / "allowed-commands.json").read_text()
        )["allowedCommands"])

    def test_scenario_cli_examples_are_allowed_and_parseable(self):
        original_parse = argparse.ArgumentParser.parse_known_args

        def stop_after_parse(parser, args=None, namespace=None):
            _, unknown = original_parse(parser, args, namespace)
            raise ParsedCommand(unknown)

        examples = 0
        for path in sorted((SKILL / "references").glob("scenarios-*.md")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if not line.startswith("python3 scripts/zoodata.py "):
                    continue
                examples += 1
                with self.subTest(path=path.name, line=number):
                    lexer = shlex.shlex(line, posix=True, punctuation_chars="<>")
                    lexer.whitespace_split = True
                    tokens = list(lexer)
                    self.assertFalse({"<", ">"} & set(tokens),
                                     "quote placeholders to prevent shell redirection")
                    self.assertEqual(tokens[:2], ["python3", "scripts/zoodata.py"])
                    self.assertIn(tokens[2], self.allowed)
                    with patch.object(sys, "argv", [str(CLI_PATH), *tokens[2:]]), \
                         patch.object(self.cli, "_schedule_stale_result_cleanup"), \
                         patch.object(argparse.ArgumentParser, "parse_known_args",
                                      stop_after_parse):
                        with self.assertRaises(ParsedCommand) as parsed:
                            self.cli.main()
                    self.assertEqual(parsed.exception.unknown, [],
                                     "example uses unsupported CLI options")
        self.assertGreater(examples, 50)
