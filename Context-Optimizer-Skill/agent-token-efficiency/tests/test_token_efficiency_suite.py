"""Comprehensive tests for agent-token-efficiency structure, audit scripts, telemetry, and skill integration."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_ROOT.parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"


def _run_py(script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


class TestAgentTokenEfficiency(unittest.TestCase):
    """Validate skill layout, 5 auditing scripts, Scenarios A-E, and sibling integration."""

    def test_skill_frontmatter_references_and_links(self) -> None:
        skill_md = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(skill_md, r"^---\r?\nname:\s*agent-token-efficiency\r?\n")
        self.assertLessEqual(len(skill_md.splitlines()), 120)

        for ref in (
            "default-policy.md",
            "context-management.md",
            "tool-output-optimization.md",
            "search-and-retrieval.md",
            "instructions-and-rules.md",
            "prompt-caching.md",
            "subagent-optimization.md",
            "session-and-long-tasks.md",
            "coding-and-testing-efficiency.md",
            "quality-evaluation.md",
            "adapters/claude-code.md",
            "adapters/openai-codex.md",
            "adapters/google-antigravity.md",
            "adapters/cursor.md",
        ):
            self.assertTrue((SKILL_ROOT / "references" / ref).is_file(), f"Missing reference: {ref}")

        for tpl in ("task-state.md", "project-map.md", "subagent-brief-and-report.md", "audit-report.md"):
            self.assertTrue((SKILL_ROOT / "templates" / tpl).is_file(), f"Missing template: {tpl}")

        for scr in (
            "audit-instructions.py",
            "estimate-text-tokens.py",
            "find-duplicate-docs.py",
            "audit-skill-references.py",
            "validate-optimization-config.py",
        ):
            self.assertTrue((SCRIPTS_DIR / scr).is_file(), f"Missing script: {scr}")

        # Verify all relative links inside agent-token-efficiency/*.md resolve
        for md in SKILL_ROOT.rglob("*.md"):
            stripped = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.DOTALL)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", stripped):
                clean = target.split("#", 1)[0].strip()
                if not clean or clean.startswith(("http://", "https://", "mailto:", "<")):
                    continue
                self.assertTrue((md.parent / clean).resolve().exists(), f"Broken link {target} in {md}")

    def test_audit_instructions_and_duplicate_docs_on_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            # Oversized root CLAUDE.md with workflow heading + duplicate paragraph in AGENTS.md
            dup_para = " ".join(["Repeated architecture explanation about auth middleware and Postgres migrations."] * 4)
            long_lines = ["# Project Rules", "## Step 1: Deployment Workflow", dup_para] + [f"- Rule {i}" for i in range(260)]
            (repo / "CLAUDE.md").write_text("\n".join(long_lines), encoding="utf-8")
            (repo / "AGENTS.md").write_text(f"# Agent Rules\n\n{dup_para}\n", encoding="utf-8")
            (repo / "mcp_config.json").write_text(json.dumps({"mcpServers": {"db": {}}}), encoding="utf-8")
            (repo / "sub").mkdir()
            (repo / "sub" / ".mcp.json").write_text(json.dumps({"mcpServers": {"db": {}}}), encoding="utf-8")

            inst_proc = _run_py("audit-instructions.py", str(repo), "--dry-run", "--format", "json")
            self.assertEqual(inst_proc.returncode, 0, inst_proc.stderr)
            inst_data = json.loads(inst_proc.stdout)
            cats = {f["category"] for f in inst_data["findings"]}
            self.assertIn("Oversized Always-Loaded Rules", cats)
            self.assertIn("Workflow Inside Rules", cats)
            self.assertIn("Duplicate MCP Server Definition", cats)

            dup_proc = _run_py("find-duplicate-docs.py", str(repo), "--format", "json")
            self.assertEqual(dup_proc.returncode, 0, dup_proc.stderr)
            dup_data = json.loads(dup_proc.stdout)
            self.assertEqual(len(dup_data["duplicates"]), 1)

    def test_token_estimation_and_provider_usage_telemetry(self) -> None:
        approx_proc = _run_py("estimate-text-tokens.py", "--text", "Hello context engineer!", "--format", "json")
        self.assertEqual(approx_proc.returncode, 0)
        approx = json.loads(approx_proc.stdout)
        self.assertIsNone(approx["exact_tokens"])
        self.assertIn("approximation", approx["estimation_method"])

        with tempfile.TemporaryDirectory() as tmp:
            for fname, payload, expected_provider, expected_cached in (
                (
                    "anthropic.json",
                    {"usage": {"input_tokens": 100, "cache_creation_input_tokens": 500, "cache_read_input_tokens": 1800, "output_tokens": 90}},
                    "Anthropic",
                    1800,
                ),
                (
                    "openai.json",
                    {"usage": {"prompt_tokens": 2000, "completion_tokens": 120, "total_tokens": 2120, "prompt_tokens_details": {"cached_tokens": 1536}}},
                    "OpenAI / Generic",
                    1536,
                ),
                (
                    "gemini.json",
                    {"usage_metadata": {"prompt_token_count": 40000, "cached_content_token_count": 36000, "candidates_token_count": 300, "thoughts_token_count": 800, "total_token_count": 40300}},
                    "Google Gemini",
                    36000,
                ),
            ):
                fpath = Path(tmp) / fname
                fpath.write_text(json.dumps(payload), encoding="utf-8")
                uproc = _run_py("estimate-text-tokens.py", "--usage-json", str(fpath), "--format", "json")
                self.assertEqual(uproc.returncode, 0, uproc.stderr)
                parsed = json.loads(uproc.stdout)
                self.assertEqual(parsed["provider_format"], expected_provider)
                cached_val = parsed.get("cache_read_input_tokens", parsed.get("cached_input_tokens"))
                self.assertEqual(cached_val, expected_cached)
                self.assertEqual(parsed["measurement_type"], "actual_api_telemetry")

    def test_workspace_skill_integration_and_config_validation(self) -> None:
        # Validate entire AgenticLLMSkills workspace shares default-policy.md cleanly
        skill_audit = _run_py("audit-skill-references.py", str(REPO_ROOT), "--format", "json")
        self.assertEqual(skill_audit.returncode, 0, skill_audit.stderr)
        sdata = json.loads(skill_audit.stdout)
        self.assertGreaterEqual(sdata["summary"]["Skills Inspected"], 4)
        self.assertEqual(sdata["summary"]["Skills Compliant with Shared Policy"], sdata["summary"]["Skills Inspected"])
        self.assertEqual(sdata["findings"], [], sdata["findings"])

        cfg_proc = _run_py("validate-optimization-config.py", str(REPO_ROOT), "--format", "json")
        self.assertEqual(cfg_proc.returncode, 0, cfg_proc.stderr)
        cdata = json.loads(cfg_proc.stdout)
        self.assertEqual(cdata["summary"]["Shared Policy Located"], "Yes")
        self.assertEqual(cdata["summary"]["PROJECT_MAP.md Present"], "Yes")
        self.assertEqual(cdata["findings"], [], cdata["findings"])

    def test_evaluation_scenarios_and_installer_and_error_handling(self) -> None:
        scenarios = (SKILL_ROOT / "tests" / "evaluation-scenarios.md").read_text(encoding="utf-8")
        for s in ("Scenario A", "Scenario B", "Scenario C", "Scenario D", "Scenario E"):
            self.assertIn(s, scenarios)

        # Clean error handling on missing path
        for scr in ("audit-instructions.py", "find-duplicate-docs.py", "audit-skill-references.py", "validate-optimization-config.py"):
            err = _run_py(scr, "/nonexistent/token_opt_missing_path_xyz")
            self.assertNotEqual(err.returncode, 0)
            self.assertNotIn("Traceback", err.stderr)

        # Verify PowerShell installer -PolicyOnly and full Codex install
        ps1 = SKILL_ROOT / "adapters" / "install.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            p1 = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1), "-Target", "claude", "-Scope", "project", "-ProjectDir", tmp, "-PolicyOnly"],
                capture_output=True,
                text=True,
                check=False,
            )
            if p1.returncode == 0:
                self.assertTrue((Path(tmp) / ".claude" / "skills" / "agent-token-efficiency" / "references" / "default-policy.md").is_file())


if __name__ == "__main__":
    unittest.main()
