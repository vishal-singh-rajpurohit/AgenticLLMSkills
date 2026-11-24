"""Audit SKILL.md progressive disclosure, reference links, and shared token-efficiency policy adoption."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPTS_ROOT = Path(__file__).resolve().parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    AuditFinding,
    MD_LINK_RE,
    estimate_tokens,
    format_report,
    iter_repo_files,
    parse_skill_frontmatter,
    read_text_safe,
)

SHARED_POLICY_REF = "agent-token-efficiency/references/default-policy.md"


def audit_skills(target: str) -> Dict[str, Any]:
    root = Path(target).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Repository directory does not exist: {target}")

    skill_files = [p for p in iter_repo_files(root, {".md"}) if p.name == "SKILL.md"]
    findings: List[AuditFinding] = []
    skill_stats: List[Dict[str, Any]] = []

    for sf in skill_files:
        skill_dir = sf.parent
        rel = str(sf.relative_to(root)).replace("\\", "/")
        txt = read_text_safe(sf)
        fm, body = parse_skill_frontmatter(txt)
        stats = estimate_tokens(txt)
        has_refs_dir = (skill_dir / "references").is_dir()
        has_shared_policy = SHARED_POLICY_REF in txt or skill_dir.name == "agent-token-efficiency"

        skill_stats.append(
            {
                "skill": fm.get("name", skill_dir.name),
                "path": rel,
                "lines": stats["lines"],
                "approx_tokens": stats["approx_tokens"],
                "description_chars": len(fm.get("description", "")),
                "has_references_dir": has_refs_dir,
                "references_shared_policy": has_shared_policy,
            }
        )

        if fm.get("name") != skill_dir.name:
            findings.append(
                AuditFinding(
                    "Skill Naming Compliance",
                    "High",
                    rel,
                    f'Frontmatter name "{fm.get("name")}" != parent dir "{skill_dir.name}"',
                    "Align YAML `name` with parent folder name per agentskills.io specification.",
                )
            )

        if not has_refs_dir and stats["lines"] > 120:
            findings.append(
                AuditFinding(
                    "Missing Progressive Disclosure",
                    "Medium",
                    rel,
                    f"SKILL.md has {stats['lines']} lines with no references/ directory",
                    "Split bulky guidelines into references/*.md and load on demand.",
                )
            )

        if not has_shared_policy:
            findings.append(
                AuditFinding(
                    "Shared Policy Adoption",
                    "Medium",
                    rel,
                    f"Missing reference to `{SHARED_POLICY_REF}`",
                    f"Add concise `## Token Efficiency` block pointing to `{SHARED_POLICY_REF}`.",
                )
            )

        stripped = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
        for m in MD_LINK_RE.finditer(stripped):
            raw_link = m.group(1).strip().split(" ", 1)[0].split("#", 1)[0]
            if not raw_link or raw_link.startswith(("http://", "https://", "mailto:", "<")):
                continue
            if not (skill_dir / raw_link).resolve().exists():
                findings.append(
                    AuditFinding(
                        "Broken Skill Reference Link",
                        "High",
                        rel,
                        f'Link "{raw_link}" does not resolve inside {skill_dir.name}/',
                        "Fix relative reference path so on-demand disclosure succeeds.",
                    )
                )

    summary = {
        "Target": str(root),
        "Skills Inspected": len(skill_files),
        "Skills Compliant with Shared Policy": sum(1 for s in skill_stats if s["references_shared_policy"]),
    }
    return {"summary": summary, "skills": skill_stats, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit SKILL.md progressive disclosure, links, and shared policy adoption.")
    parser.add_argument("target", nargs="?", default=".", help="Repository root containing one or more skills")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        res = audit_skills(args.target)
    except Exception as exc:
        print(f"Error auditing skill references: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(
            json.dumps(
                {
                    "summary": res["summary"],
                    "skills": res["skills"],
                    "findings": [f.to_dict() for f in res["findings"]],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(format_report("Skill Progressive Disclosure & Policy Audit", res["summary"], res["findings"], "markdown"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
