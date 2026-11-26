"""Metadata, canonical, heading, image alt/dimension, and content-quality auditor.

Supports:
  - Live HTTP/HTTPS URLs
  - Local static HTML files or directories
  - Source repositories (Next.js App/Pages Router, React SPA, Astro, Nuxt, WordPress, Shopify)
  - Markdown/HTML content draft QA (`--check-draft`)
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

AI_CLICHE_PHRASES = (
    "in today's fast-paced digital",
    "in today's digital landscape",
    "in the ever-evolving world of",
    "let's delve into",
    "unlock the full potential",
    "game-changer",
    "revolutionize your",
)

DRAFT_PLACEHOLDER_PATTERNS = (
    "lorem ipsum",
    "[insert ",
    "todo:",
    "tbd",
    "your company name",
)


def audit_html_document(
    label: str,
    html_text: str,
    expected_final_url: Optional[str] = None,
) -> Tuple[List[Issue], Dict[str, Optional[str]]]:
    """Audit a single HTML document for metadata, headings, canonicals, images, and copy depth."""
    parsed = parse_html(html_text)
    issues: List[Issue] = []

    if not parsed.lang:
        issues.append(
            Issue(
                "Missing html lang attribute",
                "Low",
                label,
                "No lang attribute found on <html>",
                'Declare an explicit BCP-47 language attribute such as <html lang="en">.',
            )
        )

    if not parsed.viewport:
        issues.append(
            Issue(
                "Missing mobile viewport meta tag",
                "Medium",
                label,
                'No <meta name="viewport"> found',
                'Include <meta name="viewport" content="width=device-width, initial-scale=1"> for mobile-first indexing.',
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
                "Aim for concise, descriptive titles (~30-60 characters) with the core topic up front.",
            )
        )

    if not parsed.meta_description:
        issues.append(
            Issue(
                "Missing meta description",
                "Medium",
                label,
                'No <meta name="description"> tag present',
                "Write a unique meta description (~120-155 characters) summarizing value and CTA.",
            )
        )
    elif len(parsed.meta_description) > 165:
        issues.append(
            Issue(
                "Long meta description",
                "Low",
                label,
                f"Meta description is {len(parsed.meta_description)} characters",
                "Tighten meta description under ~155-160 characters so key details remain visible.",
            )
        )

    if not parsed.canonical:
        issues.append(
            Issue(
                "Missing canonical tag",
                "Medium",
                label,
                'No <link rel="canonical"> found in HTML head',
                "Add a self-referencing absolute HTTPS canonical link in server-rendered HTML.",
            )
        )
    elif not parsed.canonical.startswith(("http://", "https://")):
        issues.append(
            Issue(
                "Relative canonical URL",
                "Medium",
                label,
                f'Canonical uses non-absolute href="{parsed.canonical}"',
                "Use a full absolute HTTPS URL in rel=canonical.",
            )
        )
    elif expected_final_url and parsed.canonical.rstrip("/") != expected_final_url.rstrip("/"):
        issues.append(
            Issue(
                "Canonical differs from fetched URL",
                "Informational",
                label,
                f'Page canonical is "{parsed.canonical}" while fetched URL is "{expected_final_url}"',
                "Confirm cross-canonicalization is intentional; otherwise align canonical to this URL.",
            )
        )

    if parsed.meta_robots and "noindex" in parsed.meta_robots.lower():
        issues.append(
            Issue(
                "Page carries noindex directive",
                "High",
                label,
                f'<meta name="robots" content="{parsed.meta_robots}">',
                "Confirm exclusion is intentional (checkout/internal); remove noindex on indexable pages.",
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
                "Add one clear <h1> matching the page's primary search intent.",
            )
        )
    elif len(h1s) > 1:
        issues.append(
            Issue(
                "Multiple <h1> elements",
                "Low",
                label,
                f"Found {len(h1s)} <h1> tags",
                "Keep one primary <h1> per page and use <h2>/<h3> for subsections.",
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
                    "Use sequential heading levels (h1 -> h2 -> h3) and control visuals with CSS.",
                )
            )
            break
        prev_level = level

    missing_alt = [img.get("src") or "(inline)" for img in parsed.images if img.get("alt") is None]
    if missing_alt:
        issues.append(
            Issue(
                "Images missing alt attribute",
                "Medium",
                label,
                f"{len(missing_alt)} <img> tag(s) lack alt attributes (e.g., {', '.join(missing_alt[:3])})",
                'Add descriptive alt text for informative images or alt="" for decorative graphics.',
            )
        )

    missing_dims = [
        img.get("src") or "(inline)"
        for img in parsed.images
        if not img.get("width") or not img.get("height")
    ]
    if missing_dims:
        issues.append(
            Issue(
                "Images missing explicit width/height attributes",
                "Low",
                label,
                f"{len(missing_dims)} <img> tag(s) omit width/height (CLS risk, e.g., {', '.join(missing_dims[:3])})",
                "Specify intrinsic width and height (or CSS aspect-ratio) to reduce Cumulative Layout Shift.",
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
                "Populate og:title, og:description, og:url, and og:image for clean social previews.",
            )
        )

    if 0 < parsed.visible_word_count < 80 and not (parsed.meta_robots and "noindex" in parsed.meta_robots.lower()):
        issues.append(
            Issue(
                "Very low visible text on indexable HTML page",
                "Informational",
                label,
                f"Only {parsed.visible_word_count} visible body word(s) detected in static HTML",
                "Verify this is not thin content or client-only JS rendering hiding core copy from initial HTML.",
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
                    "Remove static `metadata` and return all metadata fields inside `generateMetadata`.",
                )
            )

        if is_dynamic_route and not has_dynamic_meta:
            issues.append(
                Issue(
                    "Dynamic route lacks generateMetadata",
                    "High",
                    rel_path,
                    "Dynamic segment route does not export generateMetadata",
                    "Export async generateMetadata({ params }) to compute unique title, description, and canonical per item.",
                )
            )
        elif not is_dynamic_route and not has_static_meta and not has_dynamic_meta:
            issues.append(
                Issue(
                    "Static route lacks route-level metadata export",
                    "Medium",
                    rel_path,
                    "Page exports neither `metadata` nor `generateMetadata`",
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
                    "Migrate from next/head to the Next.js App Router Metadata API.",
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
                    "Assign a unique, intent-aligned title to each indexable route.",
                )
            )

    return issues


def audit_content_draft(
    text: str,
    target_keyword: Optional[str] = None,
    source_label: str = "content-draft",
) -> Tuple[List[Issue], Dict[str, str]]:
    """Audit Markdown/article draft quality for AI clichés, placeholders, structure, and keyword stuffing."""
    issues: List[Issue] = []
    lower = text.lower()

    found_cliches = [phrase for phrase in AI_CLICHE_PHRASES if phrase in lower]
    if found_cliches:
        issues.append(
            Issue(
                "Generic AI-sounding cliché phrasing detected",
                "Medium",
                source_label,
                f"Detected cliché(s): {', '.join(found_cliches[:3])}",
                "Rewrite using direct, plainspoken human prose grounded in specific reader outcomes.",
            )
        )

    found_placeholders = [tok for tok in DRAFT_PLACEHOLDER_PATTERNS if tok in lower]
    if found_placeholders:
        issues.append(
            Issue(
                "Unresolved placeholder text in draft",
                "High",
                source_label,
                f"Contains placeholder marker(s): {', '.join(found_placeholders[:3])}",
                "Replace placeholders with verified details or mark pending items for SME input before preview.",
            )
        )

    has_h1 = bool(re.search(r"(^#\s+\S+|<h1\b[^>]*>)", text, re.MULTILINE | re.IGNORECASE))
    if not has_h1:
        issues.append(
            Issue(
                "Content draft missing primary H1 heading",
                "Medium",
                source_label,
                "No Markdown `# Heading` or `<h1>` found",
                "Add one clear reader-facing H1 aligned with search intent.",
            )
        )

    if "[NEEDS SME VERIFICATION]" in text:
        issues.append(
            Issue(
                "Draft contains claims awaiting SME verification",
                "Informational",
                source_label,
                "Marked `[NEEDS SME VERIFICATION]`",
                "Obtain user/SME confirmation on flagged statistics or technical claims prior to publication.",
            )
        )

    words = re.findall(r"\b[a-z0-9]+\b", lower)
    word_count = len(words)
    summary: Dict[str, str] = {"Word Count": str(word_count)}

    if target_keyword and word_count >= 50:
        kw_tokens = re.findall(r"\b[a-z0-9]+\b", target_keyword.lower())
        if kw_tokens:
            kw_phrase = " ".join(kw_tokens)
            joined_words = " ".join(words)
            occurrences = len(re.findall(rf"\b{re.escape(kw_phrase)}\b", joined_words))
            density_pct = (occurrences * len(kw_tokens) / word_count) * 100.0
            summary["Keyword Occurrences"] = f"{occurrences} ({density_pct:.2f}%)"
            if density_pct > 4.5 and occurrences >= 6:
                issues.append(
                    Issue(
                        "Potential unnatural keyword repetition (keyword stuffing risk)",
                        "High",
                        source_label,
                        f'"{target_keyword}" appears {occurrences} times ({density_pct:.2f}% token share)',
                        "Edit for natural human flow and semantic variety; never force exact keyword density.",
                    )
                )

    return issues, summary


def run_metadata_audit(target: str, target_keyword: Optional[str] = None) -> Tuple[List[Issue], Dict[str, str]]:
    """Audit live URL, HTML/Markdown file, or project directory."""
    if is_http_url(target):
        resp = fetch_url(target)
        if resp.error or (resp.status and resp.status >= 400):
            return (
                [
                    Issue(
                        "Failed to fetch target URL",
                        "Critical",
                        target,
                        resp.error or f"HTTP status {resp.status}",
                        "Verify DNS, TLS, server availability, and crawler accessibility.",
                    )
                ],
                {"Mode": "Live URL"},
            )
        doc_issues, _ = audit_html_document(resp.final_url, resp.text, expected_final_url=resp.final_url)
        return doc_issues, {"Mode": "Live URL", "HTTP Status": str(resp.status)}

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    if path.is_file():
        text = read_text_safe(path)
        if path.suffix.lower() in {".md", ".mdx", ".txt"}:
            d_issues, d_summary = audit_content_draft(text, target_keyword=target_keyword, source_label=path.name)
            d_summary["Mode"] = "Content Draft QA"
            return d_issues, d_summary
        doc_issues, _ = audit_html_document(path.name, text)
        return doc_issues, {"Mode": "Single HTML File"}

    stack = detect_repo_stack(path)
    issues: List[Issue] = []
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
                    f'Title "{title_val}" duplicated on {len(paths)} pages',
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
                "Ensure public SEO pages render metadata and primary copy via SSR/SSG/prerendering.",
            )
        )

    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit SEO metadata, headings, canonicals, images, and content quality.")
    parser.add_argument("target", help="URL, HTML/Markdown file, or project repository directory")
    parser.add_argument("--keyword", default=None, help="Optional target keyword when auditing a Markdown content draft")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_metadata_audit(args.target, target_keyword=args.keyword)
    except Exception as exc:
        print(f"Error running metadata audit: {exc}", file=sys.stderr)
        return 1

    print(format_report("Metadata & Content Quality Audit", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
