"""Structural and specification compliance tests for seo-skill."""

from __future__ import annotations

import csv
import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

EXPECTED_REFERENCES = [
    "business-discovery.md",
    "customer-persona-research.md",
    "keyword-research.md",
    "search-intent-analysis.md",
    "competitor-analysis.md",
    "technical-seo.md",
    "on-page-seo.md",
    "content-strategy.md",
    "local-seo.md",
    "ecommerce-seo.md",
    "saas-seo.md",
    "off-page-seo.md",
    "ai-search-visibility.md",
    "analytics-and-reporting.md",
    "seo-implementation.md",
]

EXPECTED_TEMPLATES = [
    "discovery-profile.md",
    "keyword-research.csv",
    "keyword-mapping.csv",
    "competitor-analysis.md",
    "technical-audit.md",
    "content-brief.md",
    "seo-roadmap.md",
    "monthly-report.md",
]

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md must begin with YAML frontmatter delimited by ---")
    raw = match.group(1)
    fields: dict[str, str] = {}
    current_key = None
    buf: list[str] = []
    for line in raw.splitlines():
        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if key_match and not line.startswith((" ", "\t")):
            if current_key is not None:
                fields[current_key] = " ".join(buf).strip()
            current_key = key_match.group(1)
            val = key_match.group(2).strip()
            buf = [] if val in {">-", ">", "|", "|-"} else [val]
        elif current_key is not None and line.startswith((" ", "\t")):
            buf.append(line.strip())
    if current_key is not None:
        fields[current_key] = " ".join(buf).strip()
    return fields


class TestSkillStructure(unittest.TestCase):
    """Validate Agent Skills spec compliance, links, references, and templates."""

    def test_skill_md_frontmatter_and_conciseness(self) -> None:
        skill_md = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_md.is_file(), "SKILL.md missing")
        text = skill_md.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)

        name = fm.get("name", "")
        self.assertEqual(name, SKILL_ROOT.name, "Frontmatter `name` must match parent directory name")
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)

        desc = fm.get("description", "")
        self.assertTrue(desc, "Frontmatter `description` must be non-empty")
        self.assertLessEqual(len(desc), 1024)

        line_count = len(text.splitlines())
        self.assertLessEqual(line_count, 300, f"SKILL.md should remain concise (got {line_count} lines)")

    def test_expected_references_and_templates_exist(self) -> None:
        for ref in EXPECTED_REFERENCES:
            p = SKILL_ROOT / "references" / ref
            self.assertTrue(p.is_file() and p.stat().st_size > 200, f"Missing or empty reference: {ref}")

        for tpl in EXPECTED_TEMPLATES:
            p = SKILL_ROOT / "templates" / tpl
            self.assertTrue(p.is_file() and p.stat().st_size > 50, f"Missing or empty template: {tpl}")

        audit_tpl = (SKILL_ROOT / "templates" / "technical-audit.md").read_text(encoding="utf-8")
        self.assertIn("| Issue | Severity | Affected URLs | Evidence | Recommended Fix |", audit_tpl)

        for csv_name in ("keyword-research.csv", "keyword-mapping.csv"):
            with (SKILL_ROOT / "templates" / csv_name).open("r", encoding="utf-8", newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertGreaterEqual(len(rows), 1)
            self.assertGreaterEqual(len(rows[0]), 10)

    def test_all_relative_markdown_links_resolve(self) -> None:
        md_files = list(SKILL_ROOT.rglob("*.md"))
        self.assertGreater(len(md_files), 15)
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            # Strip fenced code blocks so example snippets do not trigger false link checks
            stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
            for raw_target in MD_LINK_RE.findall(stripped):
                target = raw_target.split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                    continue
                resolved = (md_file.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"Broken relative markdown link `{raw_target}` inside {md_file.relative_to(SKILL_ROOT)}",
                )

    def test_adapter_json_manifests_valid(self) -> None:
        for rel in ("adapters/claude/plugin.json", "adapters/antigravity/plugin.json"):
            data = json.loads((SKILL_ROOT / rel).read_text(encoding="utf-8"))
            self.assertIn("name", data)


if __name__ == "__main__":
    unittest.main()
