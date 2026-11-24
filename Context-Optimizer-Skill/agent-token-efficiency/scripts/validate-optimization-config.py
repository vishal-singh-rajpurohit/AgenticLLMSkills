"""Validate workspace optimization configuration (.agent indexes, shared policy, and skill compliance)."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPTS_ROOT = Path(__file__).resolve().parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import AuditFinding, format_report, read_text_safe  # noqa: E402


def _load_sibling(filename: str, mod_name: str):
    spec = importlib.util.spec_from_file_location(mod_name, SCRIPTS_ROOT / filename)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_optimization_config(target: str) -> Dict[str, Any]:
    root = Path(target).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Repository directory does not exist: {target}")

    findings: List[AuditFinding] = []
    inst_mod = _load_sibling("audit-instructions.py", "audit_instructions_mod")
    skill_mod = _load_sibling("audit-skill-references.py", "audit_skill_refs_mod")

    inst_res = inst_mod.audit_instructions(str(root), include_global=False, dry_run=True)
    skill_res = skill_mod.audit_skills(str(root))
    findings.extend(inst_res["findings"])
    findings.extend(skill_res["findings"])

    policy_candidates = list(root.rglob("agent-token-efficiency/references/default-policy.md"))
    if not policy_candidates:
        findings.append(
            AuditFinding(
                "Shared Policy Availability",
                "High",
                str(root),
                "Could not locate `agent-token-efficiency/references/default-policy.md` in repository",
                "Ensure `agent-token-efficiency` is present or synced into agent skills directory.",
            )
        )

    project_map = root / ".agent" / "PROJECT_MAP.md"
    if project_map.is_file():
        pm_lines = len(read_text_safe(project_map).splitlines())
        if pm_lines > 150:
            findings.append(
                AuditFinding(
                    "Bloated PROJECT_MAP",
                    "Medium",
                    ".agent/PROJECT_MAP.md",
                    f"{pm_lines} lines (should remain a compact navigation index)",
                    "Trim .agent/PROJECT_MAP.md to directories, entry points, commands, and doc links only.",
                )
            )

    summary = {
        "Target": str(root),
        "Shared Policy Located": "Yes" if policy_candidates else "No",
        "PROJECT_MAP.md Present": "Yes" if project_map.is_file() else "No",
        "Total Findings": len(findings),
    }
    return {"summary": summary, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate optimization configuration across instructions, skills, and .agent/ indexes.")
    parser.add_argument("target", nargs="?", default=".", help="Repository root directory")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        res = validate_optimization_config(args.target)
    except Exception as exc:
        print(f"Error validating optimization config: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(
            json.dumps(
                {"summary": res["summary"], "findings": [f.to_dict() for f in res["findings"]]},
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(format_report("Token Optimization Configuration Validation", res["summary"], res["findings"], "markdown"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
