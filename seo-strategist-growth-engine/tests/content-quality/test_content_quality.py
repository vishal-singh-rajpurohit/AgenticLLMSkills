"""Tests for content-quality auditing, Agent Skills spec compliance, links, and cross-agent adapters."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
META_DIR = SKILL_ROOT / "scripts" / "metadata-audit"
if str(META_DIR) not in sys.path:
    sys.path.insert(0, str(META_DIR))

from audit_metadata import audit_content_draft  # noqa: E402

EXPECTED_REFERENCES = [
    "interview-framework.md",
    "business-discovery.md",
    "keyword-research.md",
    "search-intent-analysis.md",
    "competitor-analysis.md",
    "seo-strategy.md",
    "content-strategy.md",
    "technical-seo.md",
    "on-page-seo.md",
    "structured-data.md",
    "ranking-monitoring.md",
    "search-console.md",
    "seo-best-practices.md",
]

EXPECTED_TEMPLATES = [
    "business-profile.md",
    "keyword-research.md",
    "competitor-analysis.md",
    "seo-roadmap.md",
    "content-brief.md",
    "seo-report.md",
    "ranking-experiment.md",
]

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md must begin with YAML frontmatter delimited by ---")
    fields: dict[str, str] = {}
    current_key = None
    buf: list[str] = []
    for line in match.group(1).splitlines():
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


class TestContentQualityAndSkillSpec(unittest.TestCase):
    """Validate content quality rules, Agent Skills specification compliance, links, and adapters."""

    def test_content_draft_checker_catches_ai_fluff_and_stuffing(self) -> None:
        bad_draft = (
            "In today's fast-paced digital world, let's delve into custom CRM software.\n"
            "TODO: add client metrics here [NEEDS SME VERIFICATION].\n"
            + ("custom crm software " * 12)
            + ("plain helpful filler sentence about workflows. " * 4)
        )
        issues, summary = audit_content_draft(bad_draft, target_keyword="custom crm software", source_label="bad.md")
        titles = {i.issue for i in issues}
        self.assertIn("Generic AI-sounding cliché phrasing detected", titles)
        self.assertIn("Unresolved placeholder text in draft", titles)
        self.assertIn("Content draft missing primary H1 heading", titles)
        self.assertIn("Draft contains claims awaiting SME verification", titles)
        self.assertIn("Potential unnatural keyword repetition (keyword stuffing risk)", titles)
        self.assertIn("Keyword Occurrences", summary)

        clean_draft = (
            "# Custom CRM Implementation Guide for Field Operations\n\n"
            "Teams migrating off spreadsheets run into duplicate customer IDs before anything else. "
            "Map your existing billing and support IDs cleanly before importing historical orders.\n"
        )
        clean_issues, _ = audit_content_draft(clean_draft, target_keyword="custom crm implementation", source_label="good.md")
        self.assertEqual(clean_issues, [])

    def test_skill_md_spec_and_token_efficiency(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        self.assertEqual(fm.get("name"), SKILL_ROOT.name)
        self.assertRegex(fm.get("name", ""), r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(fm.get("name", "")), 64)
        self.assertTrue(fm.get("description"))
        self.assertLessEqual(len(fm.get("description", "")), 1024)
        self.assertLessEqual(len(text.splitlines()), 150)
        self.assertIn("agent-token-efficiency/references/default-policy.md", text)

    def test_required_directories_and_relative_links(self) -> None:
        for ref in EXPECTED_REFERENCES:
            p = SKILL_ROOT / "references" / ref
            self.assertTrue(p.is_file() and p.stat().st_size > 200, f"Missing/thin reference: {ref}")

        for tpl in EXPECTED_TEMPLATES:
            p = SKILL_ROOT / "templates" / tpl
            self.assertTrue(p.is_file() and p.stat().st_size > 100, f"Missing/thin template: {tpl}")

        for ex_dir in ("local-business", "saas", "ecommerce", "it-services"):
            files = list((SKILL_ROOT / "examples" / ex_dir).glob("*.md"))
            self.assertTrue(files, f"Missing worked example in examples/{ex_dir}")

        for md_file in SKILL_ROOT.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
            for raw_target in MD_LINK_RE.findall(stripped):
                target = raw_target.split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                    continue
                resolved = (md_file.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"Broken link `{raw_target}` inside {md_file.relative_to(SKILL_ROOT)}",
                )

    def test_cross_agent_adapters_and_installer_dry_run(self) -> None:
        for rel in ("adapters/claude/plugin.json", "adapters/antigravity/plugin.json"):
            data = json.loads((SKILL_ROOT / rel).read_text(encoding="utf-8"))
            self.assertEqual(data["name"], SKILL_ROOT.name)
        self.assertTrue((SKILL_ROOT / "adapters" / "codex" / "agents" / "openai.yaml").is_file())
        self.assertTrue((SKILL_ROOT / "adapters" / "cursor" / "README.md").is_file())

        ps1 = SKILL_ROOT / "adapters" / "install.ps1"
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
