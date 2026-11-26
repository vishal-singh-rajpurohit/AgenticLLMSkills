"""Tests for search intent decoding, SERP format recommendation, and mixed-intent rules."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIT_DIR = SKILL_ROOT / "scripts" / "technical-seo-audit"
if str(AUDIT_DIR) not in sys.path:
    sys.path.insert(0, str(AUDIT_DIR))

from seo_metrics import decode_semrush_intent, recommend_page_format  # noqa: E402


class TestSearchIntent(unittest.TestCase):
    """Verify intent classification accuracy and Semrush numeric intent decoding."""

    def test_decode_semrush_intent_codes(self) -> None:
        self.assertEqual(decode_semrush_intent("0"), "Commercial")
        self.assertEqual(decode_semrush_intent(1), "Informational")
        self.assertEqual(decode_semrush_intent("2"), "Navigational")
        self.assertEqual(decode_semrush_intent("3"), "Transactional")
        self.assertEqual(decode_semrush_intent("1,0"), "Mixed (Informational, Commercial)")
        self.assertEqual(decode_semrush_intent("99"), "Unresolved (99)")
        self.assertEqual(decode_semrush_intent(None), "Unavailable")

    def test_recommend_page_format_by_serp_and_query(self) -> None:
        local = recommend_page_format("custom software agency in pune", serp_features=["local_pack"])
        self.assertEqual(local["format"], "Service or Location Page")

        comp = recommend_page_format("datadog vs grafana alternatives")
        self.assertEqual(comp["format"], "Comparison Article or Buying Guide")

        ecom = recommend_page_format("4k usb-c monitor", serp_types=["category_page"], serp_features=["shopping"])
        self.assertIn("Category", ecom["format"])

        hybrid = recommend_page_format("how to automate invoice ocr", serp_types=["service_page"])
        self.assertIn("Hybrid", hybrid["format"])

        guide = recommend_page_format("how to write an xml sitemap", serp_features=["featured_snippet"])
        self.assertEqual(guide["format"], "Tutorial, Guide, or Documentation")

    def test_search_intent_reference_covers_ai_features_truthfully(self) -> None:
        text = (SKILL_ROOT / "references" / "search-intent-analysis.md").read_text(encoding="utf-8")
        self.assertIn("AI Overviews", text)
        self.assertIn("query fan-out", text.lower())
        self.assertIn("Search Essentials", text)


if __name__ == "__main__":
    unittest.main()
