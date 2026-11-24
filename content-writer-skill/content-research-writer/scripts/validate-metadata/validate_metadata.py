"""Content SEO metadata validator for Markdown/MDX frontmatter, HTML files, and live URLs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    fetch_url,
    format_report,
    is_http_url,
    iter_repo_files,
    parse_frontmatter_and_body,
    parse_html,
    read_text_safe,
)

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _validate_markdown_meta(rel: str, fm: Dict[str, str], seen_titles: Dict[str, List[str]]) -> List[Issue]:
    issues: List[Issue] = []
    if not fm:
        issues.append(Issue("Missing YAML frontmatter", "High", rel, "No frontmatter block found", "Add title, description, slug, dates, author, and OG metadata."))
        return issues

    title = fm.get("title", "").strip()
    desc = fm.get("description", "").strip()
    slug = fm.get("slug", "").strip()
    canonical = fm.get("canonicalUrl", fm.get("canonical", "")).strip()
    robots = fm.get("robots", "").lower()

    if not title:
        issues.append(Issue("Missing metadata title", "High", rel, "Frontmatter `title` missing", "Provide a clear, unique SEO title."))
    else:
        seen_titles.setdefault(title, []).append(rel)

    if not desc:
        issues.append(Issue("Missing metadata description", "Medium", rel, "Frontmatter `description` missing", "Write an accurate meta description."))

    if slug and not SLUG_RE.match(slug):
        issues.append(Issue("Non-standard URL slug format", "Medium", rel, f'Slug "{slug}" is not lowercase hyphenated', "Use lowercase letters, numbers, and hyphens only."))

    if not fm.get("author"):
        issues.append(Issue("Missing author metadata", "Low", rel, "Frontmatter `author` missing", "Credit a real verified author or organization."))

    if not (fm.get("publishedAt") or fm.get("date")):
        issues.append(Issue("Missing publication date metadata", "Low", rel, "Neither `publishedAt` nor `date` specified", "Set accurate ISO-8601 publication date."))

    if canonical and "example.com" in canonical.lower():
        issues.append(Issue("Placeholder example.com in canonicalUrl", "High", rel, f"canonicalUrl={canonical}", "Replace with the real canonical production domain."))

    if "noindex" in robots:
        issues.append(Issue("Content marked noindex", "High", rel, f"robots={robots}", "Confirm noindex is intentional before publishing public content."))

    return issues


def _validate_html_meta(rel: str, html_text: str, seen_titles: Dict[str, List[str]]) -> List[Issue]:
    parsed = parse_html(html_text)
    issues: List[Issue] = []
    if not parsed.title:
        issues.append(Issue("Missing <title>", "High", rel, "<title> empty or absent", "Add a descriptive <title> tag."))
    else:
        seen_titles.setdefault(parsed.title, []).append(rel)
    if not parsed.meta_description:
        issues.append(Issue("Missing meta description", "Medium", rel, '<meta name="description"> absent', "Add a concise page description."))
    if not parsed.canonical:
        issues.append(Issue("Missing canonical tag", "Medium", rel, '<link rel="canonical"> absent', "Include absolute HTTPS canonical link."))
    if parsed.meta_robots and "noindex" in parsed.meta_robots.lower():
        issues.append(Issue("HTML carries noindex", "High", rel, parsed.meta_robots, "Remove accidental noindex on public pages."))
    missing_og = [k for k in ("og:title", "og:description", "og:image") if not parsed.open_graph.get(k)]
    if missing_og:
        issues.append(Issue("Missing Open Graph tags", "Low", rel, ", ".join(missing_og), "Populate og:title, og:description, and og:image."))
    return issues


def run_metadata_validation(target: str) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []
    seen_titles: Dict[str, List[str]] = {}

    if is_http_url(target):
        resp = fetch_url(target)
        if resp.error or (resp.status and resp.status >= 400):
            return [Issue("Failed to fetch URL", "Critical", target, resp.error or f"HTTP {resp.status}", "Confirm public URL resolves.")], {"Mode": "Live URL"}
        issues.extend(_validate_html_meta(resp.final_url, resp.text, seen_titles))
        return issues, {"Mode": "Live URL", "HTTP Status": str(resp.status)}

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    files = [path] if path.is_file() else iter_repo_files(path, {".md", ".mdx", ".html", ".htm"})
    for f in files:
        rel = f.name if path.is_file() else str(f.relative_to(path))
        txt = read_text_safe(f)
        if f.suffix.lower() in {".html", ".htm"}:
            issues.extend(_validate_html_meta(rel, txt, seen_titles))
        else:
            fm, _ = parse_frontmatter_and_body(txt)
            issues.extend(_validate_markdown_meta(rel, fm, seen_titles))

    for title, locations in seen_titles.items():
        if len(locations) > 1:
            issues.append(Issue("Duplicate title across pages", "High", ", ".join(locations), f'Title "{title}" repeated', "Ensure every page has a unique title."))

    return issues, {"Mode": "Local Content Files", "Files Scanned": str(len(files))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate content metadata, slugs, canonicals, and Open Graph tags.")
    parser.add_argument("target", help="Live URL, .md/.mdx/.html file, or directory")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_metadata_validation(args.target)
    except Exception as exc:
        print(f"Error validating metadata: {exc}", file=sys.stderr)
        return 1

    print(format_report("Content Metadata Validation", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
