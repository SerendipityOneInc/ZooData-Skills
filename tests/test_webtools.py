"""Unit tests for web-extract's standalone webtools.py CLI — specifically the
credit tracker ported from zoodata.py so multi-call commands (crawl-wait) report
an accurate total instead of no credit info at all."""
import importlib.util
import os
import unittest

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


if __name__ == "__main__":
    unittest.main()
