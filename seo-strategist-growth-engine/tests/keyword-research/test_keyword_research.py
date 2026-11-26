"""Tests for transparent keyword opportunity scoring and anti-cannibalization clustering."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIT_DIR = SKILL_ROOT / "scripts" / "technical-seo-audit"
if str(AUDIT_DIR) not in sys.path:
    sys.path.insert(0, str(AUDIT_DIR))

from seo_metrics import cluster_by_serp_overlap, compute_opportunity_score  # noqa: E402


class TestKeywordResearch(unittest.TestCase):
    """Validate configurable scoring, missing-volume honesty, and SERP-overlap clustering."""

    def test_opportunity_score_with_and_without_volume(self) -> None:
        full = compute_opportunity_score(
            business_relevance=1.0,
            intent_conversion_fit=0.9,
            ranking_feasibility=0.8,
            search_demand=0.6,
            content_gap_geo_fit=0.8,
        )
        self.assertFalse(full["is_google_metric"])
        self.assertEqual(full["demand_input_status"], "measured")
        self.assertGreater(full["opportunity_score"], 75.0)

        qualitative = compute_opportunity_score(
            business_relevance=1.0,
            intent_conversion_fit=0.9,
            ranking_feasibility=0.8,
            search_demand=None,
            content_gap_geo_fit=0.8,
        )
        self.assertFalse(qualitative["is_google_metric"])
        self.assertIn("Unavailable", qualitative["demand_input_status"])
        self.assertNotIn("search_demand", qualitative["weights_used"])
        self.assertAlmostEqual(sum(qualitative["weights_used"].values()), 1.0, places=3)

    def test_serp_overlap_clustering_prevents_cannibalization(self) -> None:
        rows = [
            {
                "keyword": "custom software development company pune",
                "intent": "Local Commercial",
                "volume": 210,
                "urls": ["https://a.example/1", "https://b.example/2", "https://c.example/3", "https://d.example/4"],
            },
            {
                "keyword": "software development agency in pune",
                "intent": "Local Commercial",
                "volume": 140,
                "urls": ["https://a.example/1", "https://b.example/2", "https://c.example/3", "https://e.example/5"],
            },
            {
                "keyword": "custom software vs off the shelf cost",
                "intent": "Commercial Investigation",
                "volume": 90,
                "urls": ["https://blog.example/x", "https://blog.example/y", "https://blog.example/z"],
            },
        ]
        clusters = cluster_by_serp_overlap(rows, min_shared_urls=3)
        self.assertEqual(len(clusters), 2)
        first = clusters[0]
        self.assertEqual(first["primary_keyword"], "custom software development company pune")
        self.assertIn("software development agency in pune", first["supporting_keywords"])

    def test_keyword_docs_forbid_fabricated_metrics(self) -> None:
        kw_ref = (SKILL_ROOT / "references" / "keyword-research.md").read_text(encoding="utf-8")
        self.assertIn("Unavailable", kw_ref)
        self.assertIn("cannibalization", kw_ref.lower())


if __name__ == "__main__":
    unittest.main()
