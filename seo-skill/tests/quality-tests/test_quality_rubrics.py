"""Verification tests ensuring quality-test scenarios and guardrails stay wired into the skill."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent


class TestQualityRubrics(unittest.TestCase):
    """Check that all 5 QA scenarios, worked examples, and key behavioral rules exist."""

    def test_all_five_scenarios_documented(self) -> None:
        scenarios = (SKILL_ROOT / "tests" / "quality-tests" / "scenarios.md").read_text(encoding="utf-8")
        for header in (
            "Test 1 — Local Service Business",
            "Test 2 — E-Commerce Store",
            "Test 3 — SaaS Company",
            "Test 4 — Existing Next.js Website",
            "Test 5 — Existing Website with 3-Month Ranking & Traffic Decline",
        ):
            self.assertIn(header, scenarios)

    def test_worked_examples_cover_local_ecommerce_saas(self) -> None:
        self.assertTrue((SKILL_ROOT / "examples" / "local-business" / "case-study.md").is_file())
        self.assertTrue((SKILL_ROOT / "examples" / "local-business" / "keyword-mapping.csv").is_file())
        self.assertTrue((SKILL_ROOT / "examples" / "ecommerce" / "case-study.md").is_file())
        self.assertTrue((SKILL_ROOT / "examples" / "saas" / "case-study.md").is_file())

    def test_core_guardrails_present_across_skill(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Never fabricate search volumes", skill_text)
        self.assertIn("one meaningful question at a time", skill_text.lower())
        self.assertIn("Fast-track scoped tasks", skill_text)

        tech_text = (SKILL_ROOT / "references" / "technical-seo.md").read_text(encoding="utf-8")
        self.assertIn("INP", tech_text)
        self.assertIn("50,000 URLs", tech_text)
        self.assertIn("FAQPage", tech_text)

        ai_text = (SKILL_ROOT / "references" / "ai-search-visibility.md").read_text(encoding="utf-8")
        self.assertIn("AI Overviews", ai_text)
        self.assertIn("query fan-out", ai_text)

    def test_installer_dry_run_powershell_if_available(self) -> None:
        ps1 = SKILL_ROOT / "adapters" / "install.ps1"
        self.assertTrue(ps1.is_file())
        try:
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1), "-Target", "antigravity", "-DryRun"],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode == 0:
                self.assertIn("[Dry Run]", proc.stdout)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
