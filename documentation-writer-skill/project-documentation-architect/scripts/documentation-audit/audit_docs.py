"""Read-only repository documentation quality auditor."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
for sub in ("", "validate-markdown-links"):
    candidate = str(SCRIPTS_ROOT / sub) if sub else str(SCRIPTS_ROOT)
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

from _shared import discover_projects, iter_repo_files, read_text_safe  # noqa: E402
from validate_links import validate_markdown_links  # noqa: E402

SECRET_PATTERNS = [
    r"\bsk-[A-Za-z0-9]{20,}\b",
    r"\bghp_[A-Za-z0-9]{20,}\b",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
]

CMD_SCRIPT_RE = re.compile(r"\b(?:npm|pnpm|yarn)\s+run\s+([A-Za-z0-9:_-]+)")


def audit_repository_docs(target: str, max_root_lines: int = 250) -> Dict[str, Any]:
    root = Path(target).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Repository directory does not exist: {target}")

    units, infra = discover_projects(root)
    md_files = iter_repo_files(root, {".md"})
    all_md_text = "\n".join(read_text_safe(f) for f in md_files)
    broken_links, _ = validate_markdown_links(str(root))

    checks: List[Dict[str, str]] = []
    details_notes: List[str] = []

    checks.append(
        {
            "check": "Project discovery",
            "status": "Pass" if units else "Review",
            "details": f"{infra['topology']}; {len(units)} project(s) detected",
        }
    )

    root_readme = root / "README.md"
    if not root_readme.is_file():
        checks.append({"check": "Root README", "status": "Fail", "details": "Root README.md is missing"})
    else:
        lines = len(read_text_safe(root_readme).splitlines())
        if lines > max_root_lines:
            checks.append(
                {
                    "check": "Root README",
                    "status": "Review",
                    "details": f"Root README.md has {lines} lines (target <= {max_root_lines} lines for a compact entry point)",
                }
            )
        else:
            checks.append({"check": "Root README", "status": "Pass", "details": f"Compact entry point ({lines} lines)"})

    if len(units) <= 1:
        checks.append(
            {
                "check": "Project documentation",
                "status": "Pass" if root_readme.is_file() else "Review",
                "details": "Single-application documentation checked via root README/docs",
            }
        )
    else:
        missing_proj = [u.location for u in units if not u.has_readme or u.doc_paths == ["README.md"]]
        if missing_proj:
            checks.append(
                {
                    "check": "Project documentation",
                    "status": "Review",
                    "details": f"Missing separated README/docs for: {', '.join(missing_proj)}",
                }
            )
        else:
            checks.append(
                {
                    "check": "Project documentation",
                    "status": "Pass",
                    "details": f"All {len(units)} projects have dedicated documentation",
                }
            )

    if infra["topology"] == "Monorepo / Multi-Service":
        has_arch = any(p.endswith("architecture.md") for p in infra["docs_files"])
        checks.append(
            {
                "check": "Architecture",
                "status": "Pass" if has_arch else "Review",
                "details": "System flow documented" if has_arch else "Missing docs/architecture.md for coupled multi-service repo",
            }
        )
    else:
        checks.append(
            {
                "check": "Architecture",
                "status": "Pass",
                "details": f"Appropriate for {infra['topology']} topology",
            }
        )

    if broken_links:
        checks.append(
            {
                "check": "Broken links",
                "status": "Fail",
                "details": f"{len(broken_links)} broken link/anchor issue(s) found",
            }
        )
        for bl in broken_links:
            details_notes.append(f"[{bl['file']}] `{bl['link']}` -> {bl['issue']}")
    else:
        checks.append({"check": "Broken links", "status": "Pass", "details": "No broken internal links"})

    all_env_vars = set(infra["root_env_vars"])
    for u in units:
        all_env_vars.update(u.env_vars)
    secret_hits = [pat for pat in SECRET_PATTERNS if re.search(pat, all_md_text)]
    if secret_hits:
        checks.append({"check": "Environment docs", "status": "Fail", "details": "Potential real secret/key pattern detected in Markdown!"})
    elif all_env_vars:
        missing_env = sorted(v for v in all_env_vars if v not in all_md_text)
        if missing_env:
            checks.append(
                {
                    "check": "Environment docs",
                    "status": "Review",
                    "details": f"{len(missing_env)} env var(s) from .env.example undocumented: {', '.join(missing_env[:5])}",
                }
            )
        else:
            checks.append({"check": "Environment docs", "status": "Pass", "details": f"All {len(all_env_vars)} .env.example variables documented"})
    else:
        checks.append({"check": "Environment docs", "status": "Unknown", "details": "No .env.example found; confirm env requirements with developers"})

    known_scripts = set()
    for u in units:
        known_scripts.update(u.scripts.keys())
    if (root / "package.json").is_file():
        try:
            root_pkg = json.loads(read_text_safe(root / "package.json"))
            known_scripts.update((root_pkg.get("scripts") or {}).keys())
        except json.JSONDecodeError:
            pass

    if known_scripts:
        referenced_scripts = set(CMD_SCRIPT_RE.findall(all_md_text))
        unknown_cmds = sorted(cmd for cmd in referenced_scripts if cmd not in known_scripts)
        if unknown_cmds:
            checks.append(
                {
                    "check": "Command verification",
                    "status": "Review",
                    "details": f"Unverified npm/pnpm/yarn script(s) in docs: {', '.join(unknown_cmds)}",
                }
            )
        else:
            checks.append({"check": "Command verification", "status": "Pass", "details": "Documented run scripts match package manifests"})
    else:
        checks.append({"check": "Command verification", "status": "Unknown", "details": "No package.json scripts detected to cross-check"})

    return {
        "repository": str(root),
        "topology": infra["topology"],
        "checks": checks,
        "link_issues": broken_links,
        "notes": details_notes,
    }


def _render_markdown(audit: Dict[str, Any]) -> str:
    lines = [
        "# Documentation Quality Report",
        "",
        f"**Repository:** `{audit['repository']}`",
        f"**Topology:** {audit['topology']}",
        "",
        "| Check | Status | Details |",
        "|---|---|---|",
    ]
    for row in audit["checks"]:
        lines.append(f"| {row['check']} | {row['status']} | {row['details']} |")
    if audit["notes"]:
        lines.extend(["", "## Detailed Findings"])
        for n in audit["notes"]:
            lines.append(f"- {n}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Markdown documentation accuracy, separation, env coverage, and links.")
    parser.add_argument("target", nargs="?", default=".", help="Path to repository root directory")
    parser.add_argument("--max-root-lines", type=int, default=250, help="Compactness threshold for root README.md")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        audit = audit_repository_docs(args.target, max_root_lines=args.max_root_lines)
    except Exception as exc:
        print(f"Error auditing documentation: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(audit, indent=2, ensure_ascii=False))
    else:
        print(_render_markdown(audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
