"""Unified technical SEO audit runner orchestrating modular checks.

Combines metadata, canonical/heading, robots/sitemap, internal link, and JSON-LD
checks for either a local repository/HTML folder or a live website URL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
for subdir in (
    "",
    "metadata-check",
    "sitemap-validation",
    "broken-link-check",
    "structured-data-validation",
):
    candidate = str(SCRIPTS_ROOT / subdir) if subdir else str(SCRIPTS_ROOT)
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

from _shared import Issue, detect_repo_stack, format_report, is_http_url  # noqa: E402
from check_links import run_broken_link_check  # noqa: E402
from check_metadata import run_metadata_check  # noqa: E402
from validate_jsonld import run_structured_data_validation  # noqa: E402
from validate_sitemap import run_sitemap_validation  # noqa: E402


def run_full_audit(
    target: str,
    check_status: bool = False,
    max_pages: int = 10,
) -> Tuple[List[Issue], Dict[str, str]]:
    """Run all technical SEO modules against a local repo/directory or live URL."""
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

    meta_issues, _ = run_metadata_check(target)
    sitemap_issues, _ = run_sitemap_validation(target, check_status=check_status)
    link_issues, _ = run_broken_link_check(target, max_pages=max_pages)
    schema_issues, schema_summary = run_structured_data_validation(target)

    issues.extend(meta_issues)
    issues.extend(sitemap_issues)
    issues.extend(link_issues)
    issues.extend(schema_issues)
    if "Types Found" in schema_summary:
        summary["Schema Types"] = schema_summary["Types Found"]

    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a unified technical SEO audit on a codebase or live URL.")
    parser.add_argument("target", help="Local repository path, HTML file, or live http(s) URL")
    parser.add_argument("--check-status", action="store_true", help="Verify live sitemap URL status codes")
    parser.add_argument("--max-pages", type=int, default=10, help="Max live pages to crawl for links")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_full_audit(args.target, check_status=args.check_status, max_pages=args.max_pages)
    except Exception as exc:
        print(f"Error running SEO audit: {exc}", file=sys.stderr)
        return 1

    print(format_report("Technical SEO Audit", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
