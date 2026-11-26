"""Tests for controlled ranking experiments, baseline integrity, and scenario coverage."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIT_DIR = SKILL_ROOT / "scripts" / "technical-seo-audit"
if str(AUDIT_DIR) not in sys.path:
    sys.path.insert(0, str(AUDIT_DIR))

from seo_metrics import evaluate_ranking_experiment  # noqa: E402


class TestRankingEvaluation(unittest.TestCase):
    """Ensure experiments require real baselines, adequate observation windows, and honest conclusions."""

    def test_awaiting_data_when_post_change_missing(self) -> None:
        exp = {
            "baseline": {"clicks": 20, "impressions": 1500, "tracker_position": 14},
            "post_change": {"observation_window_days": 0, "clicks": None, "tracker_position": None},
        }
        res = evaluate_ranking_experiment(exp)
        self.assertEqual(res["status"], "awaiting-data")

    def test_inconclusive_when_window_too_short_or_baseline_unavailable(self) -> None:
        short_window = {
            "baseline": {"clicks": 20, "impressions": 1500, "tracker_position": 14},
            "post_change": {"observation_window_days": 5, "clicks": 35, "tracker_position": 8},
        }
        self.assertEqual(evaluate_ranking_experiment(short_window)["status"], "inconclusive")

        no_baseline = {
            "baseline": {"clicks": "unavailable", "impressions": "unavailable", "tracker_position": "unavailable"},
            "post_change": {"observation_window_days": 28, "clicks": 35, "tracker_position": 8},
        }
        self.assertEqual(evaluate_ranking_experiment(no_baseline)["status"], "inconclusive")

    def test_improved_and_declined_outcomes_over_full_window(self) -> None:
        improved = {
            "baseline": {"clicks": 18, "impressions": 2150, "tracker_position": 12, "conversions": 1},
            "post_change": {"observation_window_days": 28, "clicks": 42, "impressions": 2480, "tracker_position": 7, "conversions": 4},
            "evaluation": {"confounding_factors": ["Q4 seasonality"]},
        }
        res_up = evaluate_ranking_experiment(improved)
        self.assertEqual(res_up["status"], "improved")
        self.assertEqual(res_up["next_action"], "keep")
        self.assertIn("Q4 seasonality", res_up["confounding_factors_noted"])

        declined = {
            "baseline": {"clicks": 60, "impressions": 3000, "tracker_position": 5, "conversions": 5},
            "post_change": {"observation_window_days": 28, "clicks": 25, "impressions": 2800, "tracker_position": 11, "conversions": 1},
        }
        res_down = evaluate_ranking_experiment(declined)
        self.assertEqual(res_down["status"], "declined")
        self.assertEqual(res_down["next_action"], "iterate")

    def test_examples_cover_all_six_scenarios(self) -> None:
        it_text = (SKILL_ROOT / "examples" / "it-services" / "workflow.md").read_text(encoding="utf-8")
        ecom_text = (SKILL_ROOT / "examples" / "ecommerce" / "case-study.md").read_text(encoding="utf-8")
        saas_text = (SKILL_ROOT / "examples" / "saas" / "case-study.md").read_text(encoding="utf-8")
        local_text = (SKILL_ROOT / "examples" / "local-business" / "case-study.md").read_text(encoding="utf-8")

        self.assertIn("Scenario 1", it_text)
        self.assertIn("Scenario 2", ecom_text)
        self.assertIn("Scenario 3", saas_text)
        self.assertIn("Scenario 4", local_text)
        self.assertIn("Scenario 5", local_text)
        self.assertIn("Scenario 6", local_text)
        self.assertIn("gsc_avg_position", local_text)
        self.assertIn("tracker_position", local_text)


if __name__ == "__main__":
    unittest.main()
