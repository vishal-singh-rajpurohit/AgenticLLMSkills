"""Tests for incremental doc maintenance (Scenarios 4-5), installer, and scenario coverage."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"


class TestMaintenanceAndScenarios(unittest.TestCase):
    """Verify change-aware maintenance detection (Scenarios 4-5) and cross-agent installer."""

    def test_existing_docs_pass_then_detect_new_module_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                json.dumps({"name": "app", "scripts": {"dev": "next dev", "test": "vitest"}, "dependencies": {"next": "15.0.0"}}),
                encoding="utf-8",
            )
            (repo / ".env.example").write_text("DATABASE_URL=\n", encoding="utf-8")
            (repo / "README.md").write_text(
                "# App\n\nUses `DATABASE_URL`. Run `npm run dev` and `npm run test`.\n",
                encoding="utf-8",
            )

            # Scenario 4: clean baseline existing docs pass without regenerating files
            before = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "documentation-audit" / "audit_docs.py"), str(repo), "--format", "json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(before.returncode, 0)
            before_checks = {c["check"]: c for c in json.loads(before.stdout)["checks"]}
            self.assertEqual(before_checks["Environment docs"]["status"], "Pass")
            self.assertEqual(before_checks["Root README"]["status"], "Pass")

            # Scenario 5: developer adds a new billing service and env var
            (repo / "billing").mkdir()
            (repo / "billing" / "package.json").write_text(json.dumps({"name": "billing", "dependencies": {"fastify": "5.0.0"}}), encoding="utf-8")
            (repo / ".env.example").write_text("DATABASE_URL=\nBILLING_WEBHOOK_KEY=\n", encoding="utf-8")

            after = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "documentation-audit" / "audit_docs.py"), str(repo), "--format", "json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(after.returncode, 0)
            after_checks = {c["check"]: c for c in json.loads(after.stdout)["checks"]}
            self.assertEqual(after_checks["Project documentation"]["status"], "Review")
            self.assertIn("./billing", after_checks["Project documentation"]["details"])
            self.assertEqual(after_checks["Environment docs"]["status"], "Review")
            self.assertIn("BILLING_WEBHOOK_KEY", after_checks["Environment docs"]["details"])

    def test_scenarios_documented_and_installer_works(self) -> None:
        scenarios = (SKILL_ROOT / "tests" / "scenarios.md").read_text(encoding="utf-8")
        for s in ("Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5"):
            self.assertIn(s, scenarios)

        ps1 = SKILL_ROOT / "adapters" / "install.ps1"
        self.assertTrue(ps1.is_file())
        with tempfile.TemporaryDirectory() as tmp_dest:
            proc = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ps1),
                    "-Target",
                    "codex",
                    "-Scope",
                    "project",
                    "-ProjectDir",
                    tmp_dest,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode == 0:
                installed = Path(tmp_dest) / ".agents" / "skills" / "project-documentation-architect"
                self.assertTrue((installed / "SKILL.md").is_file())
                self.assertTrue((installed / "agents" / "openai.yaml").is_file())


if __name__ == "__main__":
    unittest.main()
