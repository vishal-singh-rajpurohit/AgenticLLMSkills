"""Selective repository inspector for documentation planning."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import discover_projects  # noqa: E402


def inspect_repository(target: str) -> Dict[str, Any]:
    root = Path(target).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Repository directory does not exist: {target}")
    units, infra = discover_projects(root)
    return {
        "repository": str(root),
        "topology": infra["topology"],
        "project_count": len(units),
        "projects": [u.to_dict() for u in units],
        "infrastructure": infra,
    }


def _render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Repository Discovery Report",
        "",
        f"**Repository:** `{report['repository']}`",
        f"**Detected Topology:** {report['topology']}",
        f"**Detected Projects / Packages:** {report['project_count']}",
        "",
        "## Projects",
        "",
        "| Name | Location | Kind | Stack | Pkg Manager | Existing Docs |",
        "|---|---|---|---|---|---|",
    ]
    if not report["projects"]:
        lines.append("| (none detected) | . | unknown | Unknown | - | - |")
    else:
        for p in report["projects"]:
            stack = ", ".join(p["languages"] + p["frameworks"])
            docs = ", ".join(p["doc_paths"]) or "None"
            lines.append(
                f"| {p['name']} | `{p['location']}` | {p['kind']} | {stack} | {p['package_manager'] or '-'} | {docs} |"
            )

    infra = report["infrastructure"]
    lines.extend(
        [
            "",
            "## Infrastructure & Existing Docs",
            f"- **Root README.md:** {'Present' if infra['root_readme'] else 'Missing'}",
            f"- **Docker Compose:** {'Present (' + ', '.join(infra['compose_services']) + ')' if infra['docker_compose'] else 'Not found'}",
            f"- **CI Workflows:** {', '.join(infra['ci_workflows']) or 'None found'}",
            f"- **Root Env Vars (.env.example):** {', '.join(infra['root_env_vars']) or 'None found'}",
            f"- **All Markdown Files ({len(infra['docs_files'])}):** {', '.join(infra['docs_files']) or 'None'}",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a codebase for documentation architecture.")
    parser.add_argument("target", nargs="?", default=".", help="Path to repository root directory")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        report = inspect_repository(args.target)
    except Exception as exc:
        print(f"Error inspecting repository: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(_render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
