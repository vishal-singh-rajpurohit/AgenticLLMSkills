"""Tests for skill specification compliance, references, templates, and repository discovery."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"

EXPECTED_REFERENCES = [
    "repository-discovery.md",
    "multi-project-documentation.md",
    "documentation-standards.md",
    "architecture-documentation.md",
    "api-documentation.md",
    "database-documentation.md",
    "developer-onboarding.md",
    "documentation-maintenance.md",
]

EXPECTED_TEMPLATES = [
    "root-readme.md",
    "project-readme.md",
    "architecture.md",
    "api.md",
    "database.md",
    "environment.md",
    "deployment.md",
    "troubleshooting.md",
]


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md must begin with YAML frontmatter")
    fields: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in match.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km and not line.startswith((" ", "\t")):
            if key is not None:
                fields[key] = " ".join(buf).strip()
            key = km.group(1)
            val = km.group(2).strip()
            buf = [] if val in {">-", ">", "|", "|-"} else [val]
        elif key is not None and line.startswith((" ", "\t")):
            buf.append(line.strip())
    if key is not None:
        fields[key] = " ".join(buf).strip()
    return fields


class TestDiscoveryAndStructure(unittest.TestCase):
    """Validate skill structure and inspect_repo.py single-project detection."""

    def test_skill_frontmatter_and_inventory(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        fm = _parse_frontmatter(skill_text)
        self.assertEqual(fm.get("name"), SKILL_ROOT.name)
        self.assertRegex(fm.get("name", ""), r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertTrue(fm.get("description"))
        self.assertLessEqual(len(fm["description"]), 1024)
        self.assertLessEqual(len(skill_text.splitlines()), 200)

        for ref in EXPECTED_REFERENCES:
            self.assertTrue((SKILL_ROOT / "references" / ref).is_file(), f"Missing reference: {ref}")
        for tpl in EXPECTED_TEMPLATES:
            self.assertTrue((SKILL_ROOT / "templates" / tpl).is_file(), f"Missing template: {tpl}")
        for ex in ("single-project", "monorepo", "multi-service"):
            self.assertTrue((SKILL_ROOT / "examples" / ex).is_dir(), f"Missing example dir: {ex}")

    def test_skill_internal_markdown_links_clean(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "validate-markdown-links" / "validate_links.py"), str(SKILL_ROOT), "--format", "json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["broken_count"], 0, data["findings"])

    def test_single_nextjs_project_discovery_scenario_1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                json.dumps(
                    {
                        "name": "taskflow-web",
                        "scripts": {"dev": "next dev", "build": "next build", "test": "vitest"},
                        "dependencies": {"next": "15.1.0", "react": "19.0.0", "@prisma/client": "6.0.0"},
                    }
                ),
                encoding="utf-8",
            )
            (repo / "tsconfig.json").write_text("{}", encoding="utf-8")
            (repo / "prisma").mkdir()
            (repo / "prisma" / "schema.prisma").write_text("model User { id Int @id }", encoding="utf-8")
            (repo / "src" / "app").mkdir(parents=True)
            (repo / "src" / "app" / "layout.tsx").write_text("export default function L() {}", encoding="utf-8")
            (repo / ".env.example").write_text("DATABASE_URL=\nAUTH_SECRET=\n", encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "inspect-repository" / "inspect_repo.py"), str(repo), "--format", "json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            self.assertEqual(report["topology"], "Single Application")
            self.assertEqual(report["project_count"], 1)
            proj = report["projects"][0]
            self.assertIn("Next.js", proj["frameworks"])
            self.assertIn("Prisma", proj["databases"])
            self.assertEqual(proj["env_vars"], ["DATABASE_URL", "AUTH_SECRET"])


if __name__ == "__main__":
    unittest.main()
