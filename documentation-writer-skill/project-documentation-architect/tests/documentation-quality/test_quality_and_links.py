"""Tests for broken links, bloated README, outdated scripts, env coverage, and secret checks."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"


class TestDocumentationQuality(unittest.TestCase):
    """Verify link validation, secret detection, command verification, and error handling."""

    def test_broken_links_anchors_local_paths_and_stale_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                json.dumps({"name": "demo", "scripts": {"dev": "vite", "test": "vitest"}}),
                encoding="utf-8",
            )
            (repo / ".env.example").write_text("DATABASE_URL=\nSTRIPE_WEBHOOK_SECRET=\n", encoding="utf-8")
            (repo / "docs").mkdir()
            (repo / "docs" / "guide.md").write_text("# Guide\n\n## Valid Section\n\nRun `npm run nonexistent-cmd`.\n", encoding="utf-8")
            (repo / "README.md").write_text(
                "# Demo\n\n"
                "Uses `DATABASE_URL`.\n"
                "Broken file: [Missing](docs/missing.md)\n"
                "Broken anchor: [Anchor](docs/guide.md#missing-heading)\n"
                "Local path: [Local](C:/Users/dev/secret.txt)\n",
                encoding="utf-8",
            )

            link_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "validate-markdown-links" / "validate_links.py"), str(repo), "--format", "json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(link_proc.returncode, 2)
            link_data = json.loads(link_proc.stdout)
            self.assertEqual(link_data["broken_count"], 3)

            audit_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "documentation-audit" / "audit_docs.py"), str(repo), "--format", "json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(audit_proc.returncode, 0, audit_proc.stderr)
            checks = {c["check"]: c for c in json.loads(audit_proc.stdout)["checks"]}
            self.assertEqual(checks["Broken links"]["status"], "Fail")
            self.assertEqual(checks["Environment docs"]["status"], "Review")
            self.assertIn("STRIPE_WEBHOOK_SECRET", checks["Environment docs"]["details"])
            self.assertEqual(checks["Command verification"]["status"], "Review")
            self.assertIn("nonexistent-cmd", checks["Command verification"]["details"])

    def test_bloated_readme_and_secret_pattern_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(json.dumps({"name": "demo"}), encoding="utf-8")
            long_lines = ["# Huge Repo"] + [f"Line {i}" for i in range(280)] + ["API_KEY=ghp_1234567890abcdefghijklmno"]
            (repo / "README.md").write_text("\n".join(long_lines), encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "documentation-audit" / "audit_docs.py"), str(repo), "--format", "json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(proc.returncode, 0)
            checks = {c["check"]: c for c in json.loads(proc.stdout)["checks"]}
            self.assertEqual(checks["Root README"]["status"], "Review")
            self.assertEqual(checks["Environment docs"]["status"], "Fail")

    def test_clean_error_handling_for_missing_path(self) -> None:
        for script in (
            "inspect-repository/inspect_repo.py",
            "validate-markdown-links/validate_links.py",
            "documentation-audit/audit_docs.py",
        ):
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / script), "/nonexistent/doc_arch_path_999"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
