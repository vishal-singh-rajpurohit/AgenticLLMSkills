"""XML Sitemap and robots.txt validator for seo-strategist-growth-engine.

Validates XML syntax, sitemaps.org namespace, Google 50,000 URL / 50 MB limits,
duplicates, relative/HTTP URLs, robots.txt crawl blocks, AI crawler rules,
Next.js sitemap/robots code hygiene, and optional live HTTP status sampling.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
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
    parse_html,
    read_text_safe,
)

MAX_SITEMAP_URLS = 50_000
MAX_SITEMAP_BYTES = 50 * 1024 * 1024
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?)?$")


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def validate_robots_txt(source_label: str, text: str, expected_sitemap: Optional[str] = None) -> List[Issue]:
    """Inspect robots.txt content for crawl blockers, asset blocks, and sitemap declarations."""
    issues: List[Issue] = []
    lines = [line.split("#", 1)[0].strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]

    current_agent: str = ""
    wildcard_disallow_root = False
    blocked_assets: List[str] = []
    has_sitemap_line = False

    for line in lines:
        if ":" not in line:
            continue
        key, val = [part.strip() for part in line.split(":", 1)]
        low_key = key.lower()
        if low_key == "user-agent":
            current_agent = val.lower()
        elif low_key == "disallow":
            if current_agent == "*" and val == "/":
                wildcard_disallow_root = True
            if current_agent in {"*", "googlebot"} and any(tok in val.lower() for tok in ("/_next/static", "/assets", ".css", ".js")):
                blocked_assets.append(val)
        elif low_key == "sitemap" and val:
            has_sitemap_line = True

    if wildcard_disallow_root:
        issues.append(
            Issue(
                "robots.txt blocks entire site for all crawlers",
                "Critical",
                source_label,
                "Contains `User-agent: *` with `Disallow: /`",
                "Allow public pages in production robots.txt (keep Disallow: / only on staging environments).",
            )
        )
    if blocked_assets:
        issues.append(
            Issue(
                "robots.txt may block CSS/JS rendering assets",
                "High",
                source_label,
                f"Disallow rule matches render resources: {', '.join(blocked_assets[:3])}",
                "Allow Googlebot access to JS, CSS, and static bundle assets required for rendering.",
            )
        )
    if not has_sitemap_line:
        hint = f"Add `Sitemap: {expected_sitemap}`" if expected_sitemap else "Add a `Sitemap: https://.../sitemap.xml` directive"
        issues.append(
            Issue(
                "robots.txt does not declare a Sitemap directive",
                "Low",
                source_label,
                "No Sitemap: directive found in robots.txt",
                f"{hint} (helpful discovery signal alongside Search Console submission).",
            )
        )
    return issues


def validate_xml_sitemap_content(
    source_label: str,
    raw_bytes: bytes,
    check_status: bool = False,
    max_status_checks: int = 20,
) -> Tuple[List[Issue], Dict[str, str]]:
    """Validate an XML sitemap or sitemap index payload."""
    issues: List[Issue] = []
    byte_size = len(raw_bytes)
    if byte_size > MAX_SITEMAP_BYTES:
        issues.append(
            Issue(
                "XML sitemap exceeds Google 50 MB uncompressed limit",
                "Critical",
                source_label,
                f"Size is {byte_size:,} bytes (limit: {MAX_SITEMAP_BYTES:,} bytes)",
                "Split into smaller sitemaps referenced by a <sitemapindex>.",
            )
        )

    try:
        root = ET.fromstring(raw_bytes)
    except ET.ParseError as exc:
        issues.append(
            Issue(
                "Malformed XML sitemap",
                "Critical",
                source_label,
                f"XML parse error: {exc}",
                "Fix XML syntax errors, unescaped ampersands (&amp;), or stray characters.",
            )
        )
        return issues, {"Root Tag": "Invalid XML", "URL Count": "0"}

    root_local = _strip_ns(root.tag)
    if root_local not in {"urlset", "sitemapindex"}:
        issues.append(
            Issue(
                "Invalid sitemap root element",
                "Critical",
                source_label,
                f"Expected <urlset> or <sitemapindex>, found <{root_local}>",
                f'Use <urlset xmlns="{SITEMAP_NS}"> or <sitemapindex xmlns="{SITEMAP_NS}">.',
            )
        )

    if SITEMAP_NS not in root.tag:
        issues.append(
            Issue(
                "Missing standard sitemaps.org XML namespace",
                "Medium",
                source_label,
                f"Root element tag is {root.tag}",
                f'Declare xmlns="{SITEMAP_NS}" on the root element.',
            )
        )

    locs: List[str] = []
    bad_lastmod = 0
    for child in root:
        for sub in child:
            name = _strip_ns(sub.tag)
            text = (sub.text or "").strip()
            if name == "loc" and text:
                locs.append(text)
            elif name == "lastmod" and text and not ISO_DATE_RE.match(text):
                bad_lastmod += 1

    if len(locs) > MAX_SITEMAP_URLS:
        issues.append(
            Issue(
                "XML sitemap exceeds 50,000 URL limit",
                "Critical",
                source_label,
                f"Contains {len(locs):,} URLs (limit: {MAX_SITEMAP_URLS:,})",
                "Split URLs across multiple sitemaps under a <sitemapindex>.",
            )
        )
    elif not locs:
        issues.append(
            Issue(
                "Empty XML sitemap",
                "High",
                source_label,
                "Contains 0 <loc> entries",
                "Populate the sitemap with canonical, indexable URLs.",
            )
        )

    seen = set()
    duplicates = []
    non_absolute = []
    non_https = []
    for loc in locs:
        if loc in seen:
            duplicates.append(loc)
        seen.add(loc)
        parsed = urllib.parse.urlparse(loc)
        if not parsed.scheme or not parsed.netloc:
            non_absolute.append(loc)
        elif parsed.scheme == "http":
            non_https.append(loc)

    if duplicates:
        issues.append(
            Issue(
                "Duplicate URLs in XML sitemap",
                "Low",
                source_label,
                f"{len(duplicates)} duplicate <loc> entries (e.g., {duplicates[0]})",
                "Deduplicate URLs in the sitemap generator.",
            )
        )
    if non_absolute:
        issues.append(
            Issue(
                "Non-absolute URLs in XML sitemap",
                "High",
                source_label,
                f"{len(non_absolute)} relative or invalid URL(s) (e.g., {non_absolute[0]})",
                "Use full absolute HTTPS URLs in every <loc> element.",
            )
        )
    if non_https:
        issues.append(
            Issue(
                "Non-HTTPS URLs in XML sitemap",
                "Medium",
                source_label,
                f"{len(non_https)} HTTP URL(s) listed (e.g., {non_https[0]})",
                "List canonical HTTPS URLs consistently.",
            )
        )
    if bad_lastmod:
        issues.append(
            Issue(
                "Invalid <lastmod> date format in sitemap",
                "Low",
                source_label,
                f"{bad_lastmod} entry(ies) use non-W3C/ISO-8601 dates",
                "Format <lastmod> as YYYY-MM-DD or full ISO-8601 timestamp.",
            )
        )

    if check_status and root_local == "urlset" and locs:
        sample = [u for u in locs if is_http_url(u)][:max_status_checks]
        non_200, redirected, noindexed = [], [], []
        for url in sample:
            resp = fetch_url(url, timeout=8.0)
            if resp.error or (resp.status and resp.status >= 400):
                non_200.append(f"{url} ({resp.error or resp.status})")
            elif resp.redirect_chain:
                redirected.append(f"{url} -> {resp.final_url}")
            elif "text/html" in resp.headers.get("content-type", ""):
                parsed = parse_html(resp.text)
                x_robots = resp.headers.get("x-robots-tag", "").lower()
                if (parsed.meta_robots and "noindex" in parsed.meta_robots.lower()) or "noindex" in x_robots:
                    noindexed.append(url)
        if non_200:
            issues.append(
                Issue(
                    "Sitemap contains broken (4xx/5xx) URLs",
                    "High",
                    ", ".join(non_200[:3]),
                    f"{len(non_200)} of {len(sample)} sampled URLs failed",
                    "Remove dead/error URLs from the sitemap or restore/redirect them cleanly.",
                )
            )
        if redirected:
            issues.append(
                Issue(
                    "Sitemap lists redirecting URLs instead of final canonical URLs",
                    "Medium",
                    ", ".join(redirected[:3]),
                    f"{len(redirected)} of {len(sample)} sampled URLs redirected",
                    "List only final 200 OK canonical URLs in XML sitemaps.",
                )
            )
        if noindexed:
            issues.append(
                Issue(
                    "Sitemap includes noindex URLs",
                    "High",
                    ", ".join(noindexed[:3]),
                    f"{len(noindexed)} sampled URL(s) return noindex",
                    "Exclude noindex pages from sitemaps so sitemap and indexing signals agree.",
                )
            )

    return issues, {
        "Root Tag": root_local,
        "URL Count": str(len(locs)),
        "Bytes": f"{byte_size:,}",
    }


def _check_dynamic_sitemap_source(root: Path, rel_path: str) -> List[Issue]:
    issues: List[Issue] = []
    text = read_text_safe(root / rel_path)
    if "localhost" in text or "127.0.0.1" in text:
        issues.append(
            Issue(
                "Hardcoded localhost URL in dynamic sitemap source",
                "Critical",
                rel_path,
                "Contains localhost or 127.0.0.1 inside sitemap code",
                "Use an environment-backed production base URL (e.g., process.env.NEXT_PUBLIC_SITE_URL).",
            )
        )
    if "example.com" in text:
        issues.append(
            Issue(
                "Placeholder example.com domain in sitemap source",
                "High",
                rel_path,
                "Contains example.com inside sitemap generator",
                "Replace example.com with the verified production domain.",
            )
        )
    if "lastModified: new Date()" in text:
        issues.append(
            Issue(
                "Dynamic sitemap sets lastModified to current timestamp for all routes",
                "Low",
                rel_path,
                "Uses `lastModified: new Date()` unconditionally",
                "Use actual content/CMS modification dates for <lastmod>.",
            )
        )
    return issues


def run_sitemap_audit(
    target: str,
    check_status: bool = False,
    max_status_checks: int = 20,
) -> Tuple[List[Issue], Dict[str, str]]:
    """Audit sitemap files, robots configuration, or live sitemap/robots URLs."""
    issues: List[Issue] = []

    if is_http_url(target):
        parsed_target = urllib.parse.urlparse(target)
        robots_url = f"{parsed_target.scheme}://{parsed_target.netloc}/robots.txt"
        sitemap_url = target
        if parsed_target.path in {"", "/"}:
            sitemap_url = f"{parsed_target.scheme}://{parsed_target.netloc}/sitemap.xml"

        robots_resp = fetch_url(robots_url)
        if robots_resp.status == 200:
            issues.extend(validate_robots_txt(robots_url, robots_resp.text, expected_sitemap=sitemap_url))
        elif robots_resp.status and robots_resp.status >= 500:
            issues.append(
                Issue(
                    "robots.txt returned 5xx server error",
                    "Critical",
                    robots_url,
                    f"HTTP status {robots_resp.status}",
                    "Ensure /robots.txt returns 200 OK (or intentional 404), never 5xx.",
                )
            )

        sm_resp = fetch_url(sitemap_url)
        if sm_resp.error or (sm_resp.status and sm_resp.status >= 400):
            issues.append(
                Issue(
                    "XML sitemap unreachable",
                    "High",
                    sitemap_url,
                    sm_resp.error or f"HTTP status {sm_resp.status}",
                    "Publish an accessible XML sitemap at /sitemap.xml and submit it in Search Console.",
                )
            )
            return issues, {"Mode": "Live Sitemap URL"}

        sm_issues, summary = validate_xml_sitemap_content(
            sm_resp.final_url,
            sm_resp.body,
            check_status=check_status,
            max_status_checks=max_status_checks,
        )
        issues.extend(sm_issues)
        summary["Mode"] = "Live Sitemap URL"
        return issues, summary

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    if path.is_file():
        if path.name.lower() == "robots.txt":
            r_issues = validate_robots_txt(path.name, read_text_safe(path))
            return r_issues, {"Mode": "Local robots.txt File"}
        sm_issues, summary = validate_xml_sitemap_content(
            path.name,
            path.read_bytes(),
            check_status=check_status,
            max_status_checks=max_status_checks,
        )
        summary["Mode"] = "Local Sitemap File"
        return sm_issues, summary

    stack = detect_repo_stack(path)
    summary = {"Mode": "Repository Sitemap & Robots Audit", "Framework": stack["framework"]}
    if not stack["robots_files"]:
        issues.append(
            Issue(
                "No robots configuration found in repository",
                "Medium",
                str(path),
                "No robots.txt or app/robots.ts found",
                "Add robots.txt (or app/robots.ts in Next.js App Router) declaring crawl rules and sitemap URL.",
            )
        )
    else:
        for rf in stack["robots_files"]:
            rf_path = path / rf
            if rf_path.suffix.lower() == ".txt":
                issues.extend(validate_robots_txt(rf, read_text_safe(rf_path)))

    if not stack["sitemap_files"]:
        issues.append(
            Issue(
                "No XML sitemap or generator found in repository",
                "High",
                str(path),
                "No sitemap.xml, app/sitemap.ts, or pages/sitemap.xml.ts found",
                "Implement sitemap generation listing canonical indexable URLs.",
            )
        )
    for sm_rel in stack["sitemap_files"]:
        sm_path = path / sm_rel
        if sm_path.suffix.lower() == ".xml":
            sm_issues, _ = validate_xml_sitemap_content(sm_rel, sm_path.read_bytes(), False, 0)
            issues.extend(sm_issues)
        else:
            issues.extend(_check_dynamic_sitemap_source(path, sm_rel))

    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit XML sitemaps and robots configuration.")
    parser.add_argument("target", help="Sitemap URL, root URL, local .xml/.txt file, or repository path")
    parser.add_argument("--check-status", action="store_true", help="Sample sitemap URLs for live HTTP status")
    parser.add_argument("--max-status-checks", type=int, default=20, help="Maximum sampled URLs for --check-status")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_sitemap_audit(args.target, args.check_status, args.max_status_checks)
    except Exception as exc:
        print(f"Error auditing sitemap: {exc}", file=sys.stderr)
        return 1

    print(format_report("Sitemap & Robots Audit", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
