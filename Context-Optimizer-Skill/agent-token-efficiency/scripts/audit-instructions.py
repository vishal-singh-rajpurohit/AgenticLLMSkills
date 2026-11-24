"""Read-only auditor for global, root, nested instruction files, skills, and MCP configs."""

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
    discover_instruction_files,
    estimate_tokens,
    format_report,
    parse_skill_frontmatter,
    read_text_safe,
)

MAX_ROOT_INSTRUCTION_LINES = 250
MAX_SKILL_MD_LINES = 200
MAX_SKILL_DESC_CHARS = 1024


def audit_instructions(
    target: str,
    include_global: bool = False,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """Audit instruction, rule, skill, and MCP config files without modifying disk."""
    _ = dry_run  # Explicitly read-only regardless of flag
    root = Path(target).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Repository directory does not exist: {target}")

    files = discover_instruction_files(root, include_global=include_global)
    findings: List[AuditFinding] = []
    inventory: List[Dict[str, Any]] = []

    always_loaded_approx = 0
    for bucket, paths in files.items():
        for p in paths:
            rel = str(p.relative_to(root)).replace("\\", "/") if str(p).startswith(str(root)) else str(p)
            txt = read_text_safe(p)
            stats = estimate_tokens(txt)
            inventory.append({"bucket": bucket, "path": rel, **stats})

            if bucket in {"root_instructions", "global_instructions"}:
                always_loaded_approx += stats["approx_tokens"]
                if stats["lines"] > MAX_ROOT_INSTRUCTION_LINES:
                    findings.append(
                        AuditFinding(
                            "Oversized Always-Loaded Rules",
                            "High",
                            rel,
                            f"{stats['lines']} lines (~{stats['approx_tokens']} approx tokens)",
                            "Trim root/global rules to strict invariants and move procedures into on-demand skills.",
                        )
                    )
                if re.search(r"##\s*(?:step\s*1|workflow\s*steps|seo\s*checklist|blog\s*publishing)", txt, re.IGNORECASE):
                    findings.append(
                        AuditFinding(
                            "Workflow Inside Rules",
                            "Medium",
                            rel,
                            "Multi-step workflow headings detected inside always-loaded instruction file",
                            "Move specialized multi-step procedures into a dedicated SKILL.md.",
                        )
                    )

            if bucket == "skills":
                fm, _ = parse_skill_frontmatter(txt)
                desc = fm.get("description", "")
                if len(desc) > MAX_SKILL_DESC_CHARS:
                    findings.append(
                        AuditFinding(
                            "Oversized Skill Description",
                            "Medium",
                            rel,
                            f"Description is {len(desc)} chars (limit {MAX_SKILL_DESC_CHARS})",
                            "Shorten description to crisp trigger conditions only.",
                        )
                    )
                if stats["lines"] > MAX_SKILL_MD_LINES:
                    findings.append(
                        AuditFinding(
                            "Oversized SKILL.md",
                            "Medium",
                            rel,
                            f"{stats['lines']} lines (~{stats['approx_tokens']} approx tokens)",
                            "Move detailed manuals into references/ and link them on demand.",
                        )
                    )

    # Detect duplicate MCP server entries across configs
    mcp_servers: Dict[str, List[str]] = {}
    for mcp_path in files["mcp_configs"]:
        rel = str(mcp_path.relative_to(root)).replace("\\", "/")
        try:
            data = json.loads(read_text_safe(mcp_path))
            for srv in (data.get("mcpServers") or {}).keys():
                mcp_servers.setdefault(srv, []).append(rel)
        except json.JSONDecodeError:
            findings.append(AuditFinding("Invalid MCP JSON", "High", rel, "Malformed JSON", "Fix MCP configuration syntax."))
    for srv, locs in mcp_servers.items():
        if len(locs) > 1:
            findings.append(
                AuditFinding(
                    "Duplicate MCP Server Definition",
                    "Low",
                    ", ".join(locs),
                    f'MCP server "{srv}" configured in {len(locs)} files',
                    "Keep a single canonical MCP server definition to avoid duplicate schema overhead.",
                )
            )

    largest = sorted(inventory, key=lambda x: x["bytes"], reverse=True)[:5]
    summary = {
        "Target": str(root),
        "Mode": "Dry-Run (Read-Only)",
        "Instruction & Skill Files": sum(len(v) for v in files.values()),
        "Always-Loaded Rules Approx Tokens": f"~{always_loaded_approx} (heuristic chars/4 approximation)",
        "Largest File": f"{largest[0]['path']} ({largest[0]['bytes']} bytes)" if largest else "None",
    }
    return {"summary": summary, "inventory": inventory, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit global, root, nested instructions, skills, and MCP configs.")
    parser.add_argument("target", nargs="?", default=".", help="Repository directory path")
    parser.add_argument("--include-global", action="store_true", help="Also inspect standard user-home instruction files (read-only)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run non-mutating audit (default)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        res = audit_instructions(args.target, include_global=args.include_global, dry_run=args.dry_run)
    except Exception as exc:
        print(f"Error auditing instructions: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(
            json.dumps(
                {
                    "summary": res["summary"],
                    "inventory": res["inventory"],
                    "findings": [f.to_dict() for f in res["findings"]],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(format_report("Instruction & Context Efficiency Audit", res["summary"], res["findings"], "markdown"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
