"""Unit tests for web-extract's standalone webtools.py CLI — the credit
tracker ported from zoodata.py (so multi-call commands like crawl-wait report
an accurate total) and credential resolution (the legacy APICLAW sources must
not resolve)."""
import contextlib
import importlib.util
import io
import os
import unittest
from unittest.mock import mock_open, patch

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "web-extract", "scripts", "webtools.py")
spec = importlib.util.spec_from_file_location("webtools", SCRIPT_PATH)
webtools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(webtools)


class TestWebtoolsCreditAggregation(unittest.TestCase):
    def setUp(self):
        webtools._CREDITS.__init__()

    def tearDown(self):
        webtools._CREDITS.__init__()

    def test_tracker_sums_across_calls(self):
        webtools._CREDITS.record({"creditsConsumed": 1, "creditsRemaining": 100})
        webtools._CREDITS.record({"creditsConsumed": 1, "creditsRemaining": 99})
        self.assertEqual(webtools._CREDITS.consumed, 2)
        self.assertEqual(webtools._CREDITS.calls, 2)
        self.assertEqual(webtools._CREDITS.remaining, 99)

    def test_annotate_synthesises_meta_and_preserves_existing_keys(self):
        # crawl-wait emits meta={"polled": True} with no credits; the total must
        # be stamped in WITHOUT dropping the existing key.
        webtools._CREDITS.record({"creditsConsumed": 1, "creditsRemaining": 100})
        webtools._CREDITS.record({"creditsConsumed": 1, "creditsRemaining": 99})
        payload = {"success": True, "data": {}, "meta": {"polled": True}}
        webtools._annotate_credits(payload)
        self.assertEqual(payload["meta"]["polled"], True)
        self.assertEqual(payload["meta"]["creditsConsumed"], 2)
        self.assertEqual(payload["meta"]["apiCalls"], 2)

    def test_annotate_noop_without_calls(self):
        payload = {"meta": {"polled": True}}
        webtools._annotate_credits(payload)
        self.assertNotIn("creditsConsumed", payload["meta"])


class TestWebtoolsCredentialResolution(unittest.TestCase):
    """`get_api_key()` resolves the key from exactly two sources, in order:
    ZOODATA_API_KEY env, ~/.zoodata/config.json. The legacy APICLAW sources
    (APICLAW_API_KEY env, ~/.apiclaw/config.json) were removed; with no valid
    source the CLI exits 2."""

    def _get_key_capturing_exit(self):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            try:
                return webtools.get_api_key(), buf.getvalue(), None
            except SystemExit as e:
                return None, buf.getvalue(), e.code

    def test_env_zoodata_resolves(self):
        with patch.dict("os.environ", {"ZOODATA_API_KEY": "z"}, clear=True):
            self.assertEqual(webtools.get_api_key(), "z")

    def test_zoodata_home_config_resolves_when_no_env(self):
        home_zoodata = os.path.expanduser("~/.zoodata/config.json")
        with patch.dict("os.environ", {}, clear=True), \
             patch("os.path.exists", side_effect=lambda p: p == home_zoodata), \
             patch("builtins.open", mock_open(read_data='{"api_key":"home"}')):
            self.assertEqual(webtools.get_api_key(), "home")

    def test_legacy_apiclaw_env_is_not_a_source(self):
        """Regression: a key present ONLY in the deprecated APICLAW_API_KEY
        env var must not resolve — the CLI exits 2 as if unconfigured."""
        with patch.dict("os.environ", {"APICLAW_API_KEY": "legacy"}, clear=True), \
             patch("os.path.exists", return_value=False):
            key, _stderr, exit_code = self._get_key_capturing_exit()
        self.assertIsNone(key)
        self.assertEqual(exit_code, 2)

    def test_legacy_apiclaw_home_config_is_not_a_source(self):
        """Regression: a key present ONLY in the deprecated
        ~/.apiclaw/config.json must not resolve, and the file must not even
        be opened — the CLI exits 2 as if unconfigured."""
        apiclaw_home = os.path.expanduser("~/.apiclaw/config.json")
        opened = mock_open(read_data='{"api_key":"legacy_home"}')
        with patch.dict("os.environ", {}, clear=True), \
             patch("os.path.exists", side_effect=lambda p: p == apiclaw_home), \
             patch("builtins.open", opened):
            key, _stderr, exit_code = self._get_key_capturing_exit()
        self.assertIsNone(key)
        self.assertEqual(exit_code, 2)
        for call in opened.call_args_list:
            self.assertNotIn(".apiclaw", str(call))


if __name__ == "__main__":
    unittest.main()
