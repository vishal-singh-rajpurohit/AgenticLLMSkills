"""Tests for multi-project monorepo (Scenario 2) and unrelated workspace (Scenario 3)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"


def _run_json(script_rel: str, target: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_rel), str(target), "--format", "json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(f"Command failed: {proc.stderr}")
    return json.loads(proc.stdout)


class TestMultiProjectDocumentation(unittest.TestCase):
    """Verify detection and separated-doc auditing for monorepos and unrelated workspaces."""

    def test_monorepo_scenario_2_missing_vs_separated_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for js_app, fw in (("frontend", "next"), ("admin", "react"), ("backend", "express"), ("shared", "zod")):
                (repo / js_app).mkdir()
                (repo / js_app / "package.json").write_text(
                    json.dumps({"name": js_app, "scripts": {"dev": "echo dev"}, "dependencies": {fw: "1.0.0"}}),
                    encoding="utf-8",
                )
            (repo / "worker").mkdir()
            (repo / "worker" / "pyproject.toml").write_text('[project]\nname = "worker"\ndependencies = ["celery"]\n', encoding="utf-8")
            (repo / "docker-compose.yml").write_text("services:\n  backend:\n    build: ./backend\n  worker:\n    build: ./worker\n", encoding="utf-8")
            (repo / "README.md").write_text("# Monorepo\n\nCompact landing page.\n", encoding="utf-8")

            insp = _run_json("inspect-repository/inspect_repo.py", repo)
            self.assertEqual(insp["topology"], "Monorepo / Multi-Service")
            self.assertEqual(insp["project_count"], 5)

            audit_before = _run_json("documentation-audit/audit_docs.py", repo)
            checks_before = {c["check"]: c for c in audit_before["checks"]}
            self.assertEqual(checks_before["Project documentation"]["status"], "Review")
            self.assertEqual(checks_before["Architecture"]["status"], "Review")

            # Add separated docs + architecture.md
            (repo / "docs").mkdir()
            (repo / "docs" / "architecture.md").write_text("# System Architecture\n\nFrontend -> Backend -> Worker.\n", encoding="utf-8")
            for app in ("frontend", "admin", "backend", "worker", "shared"):
                pdir = repo / "docs" / "projects" / app
                pdir.mkdir(parents=True)
                (pdir / "README.md").write_text(f"# {app}\n\nIndependent project docs.\n", encoding="utf-8")

            audit_after = _run_json("documentation-audit/audit_docs.py", repo)
            checks_after = {c["check"]: c for c in audit_after["checks"]}
            self.assertEqual(checks_after["Project documentation"]["status"], "Pass")
            self.assertEqual(checks_after["Architecture"]["status"], "Pass")

    def test_unrelated_projects_workspace_scenario_3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            (ws / "ecommerce").mkdir()
            (ws / "ecommerce" / "package.json").write_text(json.dumps({"name": "shop", "dependencies": {"next": "15.0.0"}}), encoding="utf-8")
            (ws / "ecommerce" / "README.md").write_text("# Ecommerce Store\n", encoding="utf-8")

            (ws / "portfolio").mkdir()
            (ws / "portfolio" / "package.json").write_text(json.dumps({"name": "portfolio", "dependencies": {"astro": "5.0.0"}}), encoding="utf-8")
            (ws / "portfolio" / "README.md").write_text("# Portfolio\n", encoding="utf-8")

            (ws / "chatbot").mkdir()
            (ws / "chatbot" / "requirements.txt").write_text("fastapi==0.115.0\n", encoding="utf-8")
            (ws / "chatbot" / "README.md").write_text("# Chatbot\n", encoding="utf-8")

            (ws / "README.md").write_text(
                "# Workspace Index\n\n- [Shop](ecommerce/README.md)\n- [Portfolio](portfolio/README.md)\n- [Chatbot](chatbot/README.md)\n",
                encoding="utf-8",
            )

            insp = _run_json("inspect-repository/inspect_repo.py", ws)
            self.assertEqual(insp["topology"], "Multiple Independent Projects")
            self.assertEqual(insp["project_count"], 3)

            audit = _run_json("documentation-audit/audit_docs.py", ws)
            checks = {c["check"]: c for c in audit["checks"]}
            self.assertEqual(checks["Project documentation"]["status"], "Pass")
            self.assertEqual(checks["Broken links"]["status"], "Pass")
            self.assertEqual(checks["Architecture"]["status"], "Pass")


if __name__ == "__main__":
    unittest.main()
