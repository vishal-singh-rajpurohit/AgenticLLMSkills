"""Unified technical SEO audit and tool-discovery CLI runner.

Supports:
  - `--discover-tools`: Inspect workspace & environment to output the SEO Capability Matrix
  - Auditing a local repository/HTML folder or live website URL across metadata,
    sitemaps/robots, broken links/orphans, and JSON-LD structured data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
for subdir in (
    "",
    "metadata-audit",
    "sitemap-audit",
    "broken-link-audit",
    "structured-data-validation",
):
    candidate = str(SCRIPTS_ROOT / subdir) if subdir else str(SCRIPTS_ROOT)
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

from _shared import (  # noqa: E402
    Issue,
    detect_repo_stack,
    discover_seo_capabilities,
    format_report,
    is_http_url,
)
from audit_links import run_broken_link_audit  # noqa: E402
from audit_metadata import run_metadata_audit  # noqa: E402
from audit_sitemap import run_sitemap_audit  # noqa: E402
from validate_structured_data import run_structured_data_validation  # noqa: E402


def render_capability_matrix_markdown(discovery: Dict) -> str:
    """Format discovered tools and capability matrix cleanly in Markdown."""
    lines = [
        "# SEO Tool & Plugin Discovery Matrix",
        "",
        f"**Workspace Root:** `{discovery['workspace_root']}`",
        f"**Sibling `content-research-writer` Detected:** `{'Yes' if discovery['sibling_content_research_writer'] else 'No'}`",
        f"**Project `.mcp.json` Keys:** `{', '.join(discovery['detected_project_mcp_keys']) or 'None detected on disk (check active session MCP tools)'}`",
        "",
        "| SEO Capability | Existing Tool | Available | Alternative |",
        "|---|---|---|---|",
    ]
    for row in discovery["capability_matrix"]:
        lines.append(
            f"| {row['capability']} | {row['existing_tool']} | {row['available']} | {row['alternative']} |"
        )
    return "\n".join(lines)


def run_full_technical_audit(
    target: str,
    check_status: bool = False,
    max_pages: int = 10,
) -> Tuple[List[Issue], Dict[str, str]]:
    """Run unified technical SEO checks across metadata, sitemaps, links, and JSON-LD."""
    issues: List[Issue] = []
    summary: Dict[str, str] = {}

    if not is_http_url(target):
        root = Path(target).resolve()
        if not root.exists():
            raise FileNotFoundError(f"Target does not exist: {target}")
        if root.is_dir():
            stack = detect_repo_stack(root)
            summary["Framework"] = f"{stack['framework']} ({stack['version'] or 'unknown version'})"
            if stack["router"]:
                summary["Router"] = stack["router"]
            summary["Robots Found"] = ", ".join(stack["robots_files"]) or "None"
            summary["Sitemaps Found"] = ", ".join(stack["sitemap_files"]) or "None"
        else:
            summary["Scope"] = "Single Local File"
    else:
        summary["Scope"] = f"Sampled Live URL Audit (up to {max_pages} internal pages)"

    meta_issues, _ = run_metadata_audit(target)
    sitemap_issues, _ = run_sitemap_audit(target, check_status=check_status)
    link_issues, _ = run_broken_link_audit(target, max_pages=max_pages)
    schema_issues, schema_summary = run_structured_data_validation(target)

    issues.extend(meta_issues)
    issues.extend(sitemap_issues)
    issues.extend(link_issues)
    issues.extend(schema_issues)
    if "Types Found" in schema_summary:
        summary["Schema Types"] = schema_summary["Types Found"]

    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover SEO tools/integrations or run a unified technical SEO audit."
    )
    parser.add_argument("target", nargs="?", default=".", help="Repo path, HTML file, or live http(s) URL")
    parser.add_argument("--discover-tools", action="store_true", help="Output SEO capability discovery matrix")
    parser.add_argument(
        "--connected",
        default="",
        help="Comma-separated connected providers observed in session (e.g. semrush,gsc,ga4,psi)",
    )
    parser.add_argument("--check-status", action="store_true", help="Check live HTTP status codes for sampled sitemap URLs")
    parser.add_argument("--max-pages", type=int, default=10, help="Max live internal pages to crawl")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    if args.discover_tools:
        repo_path: Optional[Path] = None
        if args.target and not is_http_url(args.target):
            candidate = Path(args.target).resolve()
            if not candidate.exists():
                print(f"Error discovering tools: target path does not exist: {args.target}", file=sys.stderr)
                return 1
            repo_path = candidate if candidate.is_dir() else candidate.parent
        connected_list = [item.strip() for item in args.connected.split(",") if item.strip()]
        discovery = discover_seo_capabilities(repo_root=repo_path, connected_tools=connected_list)
        if args.format == "json":
            print(json.dumps(discovery, indent=2, ensure_ascii=False))
        else:
            print(render_capability_matrix_markdown(discovery))
        return 0

    try:
        issues, summary = run_full_technical_audit(
            args.target,
            check_status=args.check_status,
            max_pages=args.max_pages,
        )
    except Exception as exc:
        print(f"Error running technical SEO audit: {exc}", file=sys.stderr)
        return 1

    print(format_report("Technical SEO Audit", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
