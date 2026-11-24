"""Metadata, canonical, heading, and accessibility alt-text checker.

Supports:
  - Live HTTP/HTTPS URLs
  - Local static HTML files or directories
  - Source repositories (Next.js App/Pages Router, Astro, Nuxt, SvelteKit)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    detect_repo_stack,
    fetch_url,
    format_report,
    is_http_url,
    iter_repo_files,
    parse_html,
    read_text_safe,
)

NEXT_PAGE_NAMES = {"page.tsx", "page.ts", "page.jsx", "page.js"}


def audit_html_document(label: str, html_text: str) -> Tuple[List[Issue], Dict[str, Optional[str]]]:
    """Audit a single rendered HTML document for core metadata and heading issues."""
    parsed = parse_html(html_text)
    issues: List[Issue] = []

    if not parsed.lang:
        issues.append(
            Issue(
                "Missing html lang attribute",
                "Low",
                label,
                "No lang attribute found on <html>",
                'Add an explicit BCP-47 language attribute such as <html lang="en">.',
            )
        )

    if not parsed.title:
        issues.append(
            Issue(
                "Missing page <title>",
                "High",
                label,
                "<title> tag is missing or empty",
                "Add a unique, search-intent-aligned <title> tag (~50-60 characters).",
            )
        )
    elif len(parsed.title) > 65 or len(parsed.title) < 15:
        issues.append(
            Issue(
                "Suboptimal <title> length",
                "Low",
                label,
                f'Title length is {len(parsed.title)} chars: "{parsed.title}"',
                "Aim for concise, clear titles (~30-60 characters) with the core topic up front.",
            )
        )

    if not parsed.meta_description:
        issues.append(
            Issue(
                "Missing meta description",
                "Medium",
                label,
                'No <meta name="description"> tag present',
                "Write a concise, unique meta description (~120-155 characters) summarizing value and CTA.",
            )
        )
    elif len(parsed.meta_description) > 165:
        issues.append(
            Issue(
                "Long meta description",
                "Low",
                label,
                f"Meta description is {len(parsed.meta_description)} characters",
                "Tighten meta description under ~155-160 characters so key details stay visible.",
            )
        )

    if not parsed.canonical:
        issues.append(
            Issue(
                "Missing canonical tag",
                "Medium",
                label,
                'No <link rel="canonical"> found in HTML head',
                "Include a self-referencing absolute HTTPS canonical URL in server-rendered HTML.",
            )
        )
    elif not parsed.canonical.startswith(("http://", "https://")):
        issues.append(
            Issue(
                "Relative canonical URL",
                "Medium",
                label,
                f'Canonical uses non-absolute href="{parsed.canonical}"',
                "Use a full absolute HTTPS URL in rel=canonical to avoid host/protocol ambiguity.",
            )
        )

    if parsed.meta_robots and "noindex" in parsed.meta_robots.lower():
        issues.append(
            Issue(
                "Page carries noindex directive",
                "High",
                label,
                f'<meta name="robots" content="{parsed.meta_robots}">',
                "Confirm this URL is intentionally excluded (e.g., checkout/admin); remove noindex on public landing pages.",
            )
        )

    h1s = [text for tag, text in parsed.headings if tag == "h1"]
    if not h1s:
        issues.append(
            Issue(
                "Missing <h1> heading",
                "Medium",
                label,
                "No <h1> found in HTML document",
                "Add one clear <h1> reflecting the page's primary search intent.",
            )
        )
    elif len(h1s) > 1:
        issues.append(
            Issue(
                "Multiple <h1> elements",
                "Low",
                label,
                f"Found {len(h1s)} <h1> tags",
                "Keep a single primary <h1> per page and use <h2>/<h3> for sub-sections.",
            )
        )

    prev_level = 0
    for tag, text in parsed.headings:
        level = int(tag[1])
        if prev_level and level > prev_level + 1:
            issues.append(
                Issue(
                    "Skipped heading hierarchy level",
                    "Low",
                    label,
                    f"Jumped from <h{prev_level}> to <h{level}> ({text[:50]})",
                    "Use sequential heading levels (h1 -> h2 -> h3) and style sizes via CSS.",
                )
            )
            break
        prev_level = level

    missing_alt = [img.get("src") or "(inline)" for img in parsed.images if img.get("alt") is None]
    if missing_alt:
        sample = ", ".join(missing_alt[:3])
        issues.append(
            Issue(
                "Images missing alt attribute",
                "Medium",
                label,
                f"{len(missing_alt)} <img> tag(s) lack alt attributes (e.g., {sample})",
                'Add descriptive alt text for informative images or alt="" for purely decorative graphics.',
            )
        )

    missing_og = [key for key in ("og:title", "og:description", "og:image") if not parsed.open_graph.get(key)]
    if missing_og:
        issues.append(
            Issue(
                "Incomplete Open Graph metadata",
                "Low",
                label,
                f"Missing {', '.join(missing_og)}",
                "Populate og:title, og:description, og:url, and og:image for reliable link previews.",
            )
        )

    return issues, {
        "title": parsed.title,
        "description": parsed.meta_description,
        "canonical": parsed.canonical,
    }


def _audit_nextjs_app_router(root: Path, app_rel: str) -> List[Issue]:
    issues: List[Issue] = []
    app_dir = root / app_rel
    layout_files = [p for p in iter_repo_files(app_dir, {".tsx", ".ts", ".jsx", ".js"}) if p.stem == "layout"]
    root_layout = next((p for p in layout_files if p.parent == app_dir), None)

    if root_layout:
        root_text = read_text_safe(root_layout)
        if "metadataBase" not in root_text:
            issues.append(
                Issue(
                    "Next.js root layout missing metadataBase",
                    "Medium",
                    str(root_layout.relative_to(root)),
                    "No metadataBase property found in root layout metadata export",
                    "Set metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://yourdomain.com') in root layout.",
                )
            )
    else:
        issues.append(
            Issue(
                "Missing Next.js root layout",
                "High",
                app_rel,
                "No root layout.(tsx|ts|jsx|js) found in App Router directory",
                "Create a root layout defining html lang, base metadata, and metadataBase.",
            )
        )

    page_files = [p for p in iter_repo_files(app_dir, {".tsx", ".ts", ".jsx", ".js"}) if p.name in NEXT_PAGE_NAMES]
    seen_titles: Dict[str, List[str]] = {}

    for page_path in page_files:
        rel_path = str(page_path.relative_to(root))
        content = read_text_safe(page_path)
        has_static_meta = bool(re.search(r"export\s+(const|let)\s+metadata\b", content))
        has_dynamic_meta = bool(re.search(r"export\s+(async\s+)?function\s+generateMetadata\b", content))
        is_dynamic_route = "[" in rel_path and "]" in rel_path

        if has_static_meta and has_dynamic_meta:
            issues.append(
                Issue(
                    "Conflicting static and dynamic metadata exports",
                    "Critical",
                    rel_path,
                    "Exports both `metadata` and `generateMetadata` (invalid in Next.js App Router)",
                    "Remove static `metadata` and compute all metadata fields inside `generateMetadata`.",
                )
            )

        if is_dynamic_route and not has_dynamic_meta:
            issues.append(
                Issue(
                    "Dynamic route lacks generateMetadata",
                    "High",
                    rel_path,
                    "Dynamic segment route does not export generateMetadata",
                    "Export async generateMetadata({ params }) to generate unique title, description, and canonical per item.",
                )
            )
        elif not is_dynamic_route and not has_static_meta and not has_dynamic_meta:
            issues.append(
                Issue(
                    "Static route lacks route-level metadata export",
                    "Medium",
                    rel_path,
                    "Page exports neither `metadata` nor `generateMetadata` (falls back to layout defaults)",
                    "Export route-specific `metadata` with unique title, description, and alternates.canonical.",
                )
            )

        if "next/head" in content:
            issues.append(
                Issue(
                    "Deprecated next/head used inside App Router page",
                    "Medium",
                    rel_path,
                    "Imports next/head inside App Router segment",
                    "Replace next/head with Next.js App Router Metadata API (`metadata` / `generateMetadata`).",
                )
            )

        title_match = re.search(r'title\s*:\s*["\']([^"\']+)["\']', content)
        if title_match:
            seen_titles.setdefault(title_match.group(1), []).append(rel_path)

    for title_val, paths in seen_titles.items():
        if len(paths) > 1:
            issues.append(
                Issue(
                    "Duplicate hardcoded page title across App Router routes",
                    "High",
                    ", ".join(paths),
                    f'Identical title "{title_val}" found in {len(paths)} route files',
                    "Assign a unique, intent-specific title to each indexable route.",
                )
            )

    return issues


def run_metadata_check(target: str) -> Tuple[List[Issue], Dict[str, str]]:
    """Run metadata check against a live URL, local HTML file, or project directory."""
    issues: List[Issue] = []
    if is_http_url(target):
        resp = fetch_url(target)
        if resp.error or (resp.status and resp.status >= 400):
            issues.append(
                Issue(
                    "Failed to fetch target URL",
                    "Critical",
                    target,
                    resp.error or f"HTTP status {resp.status}",
                    "Verify DNS, TLS, server availability, and non-blocking firewall rules.",
                )
            )
            return issues, {"Mode": "Live URL"}
        doc_issues, _ = audit_html_document(resp.final_url, resp.text)
        return doc_issues, {"Mode": "Live URL", "HTTP Status": str(resp.status)}

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    if path.is_file():
        doc_issues, _ = audit_html_document(path.name, read_text_safe(path))
        return doc_issues, {"Mode": "Single HTML File"}

    stack = detect_repo_stack(path)
    summary = {
        "Mode": "Local Repository / Directory",
        "Framework": f"{stack['framework']} ({stack['version'] or 'unknown version'})",
    }
    if stack["router"]:
        summary["Router"] = stack["router"]

    if stack["app_dir"]:
        issues.extend(_audit_nextjs_app_router(path, stack["app_dir"]))

    html_files = iter_repo_files(path, {".html", ".htm"})
    seen_html_titles: Dict[str, List[str]] = {}
    seen_html_descs: Dict[str, List[str]] = {}
    for html_file in html_files:
        rel = str(html_file.relative_to(path))
        doc_issues, meta = audit_html_document(rel, read_text_safe(html_file))
        issues.extend(doc_issues)
        if meta["title"]:
            seen_html_titles.setdefault(meta["title"], []).append(rel)
        if meta["description"]:
            seen_html_descs.setdefault(meta["description"], []).append(rel)

    for title_val, paths in seen_html_titles.items():
        if len(paths) > 1:
            issues.append(
                Issue(
                    "Duplicate <title> across HTML pages",
                    "High",
                    ", ".join(paths),
                    f'Title "{title_val}" is duplicated on {len(paths)} pages',
                    "Give every indexable HTML page a distinct <title> matching its search intent.",
                )
            )
    for desc_val, paths in seen_html_descs.items():
        if len(paths) > 1:
            issues.append(
                Issue(
                    "Duplicate meta description across HTML pages",
                    "Medium",
                    ", ".join(paths),
                    f"Identical meta description reused on {len(paths)} pages",
                    "Write unique meta descriptions summarizing each page's distinct content.",
                )
            )

    if stack["framework"] == "React" and not stack["app_dir"] and not stack["pages_dir"]:
        issues.append(
            Issue(
                "Client-side rendered React SPA detected",
                "High",
                str(path),
                "React project without SSR/SSG framework (Next.js/Astro/Remix)",
                "Ensure public SEO pages render metadata and primary copy server-side or via pre-rendering.",
            )
        )

    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SEO metadata, headings, canonicals, and image alt attributes.")
    parser.add_argument("target", help="URL, HTML file, or project repository directory")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_metadata_check(args.target)
    except Exception as exc:
        print(f"Error running metadata check: {exc}", file=sys.stderr)
        return 1

    print(format_report("Metadata & On-Page Check", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
