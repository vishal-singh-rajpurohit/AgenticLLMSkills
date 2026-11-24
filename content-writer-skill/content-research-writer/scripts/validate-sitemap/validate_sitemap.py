"""XML Sitemap, robots.txt, and newly published URL inclusion validator."""

from __future__ import annotations

import argparse
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
    detect_publishing_architecture,
    fetch_url,
    format_report,
    is_http_url,
    parse_html,
    read_text_safe,
)

MAX_URLS = 50_000
MAX_BYTES = 50 * 1024 * 1024
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def _local_tag(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def validate_sitemap_bytes(
    label: str,
    raw: bytes,
    require_url: Optional[str] = None,
    check_status: bool = False,
) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []
    if len(raw) > MAX_BYTES:
        issues.append(Issue("Sitemap exceeds 50 MB limit", "Critical", label, f"{len(raw):,} bytes", "Split across sitemapindex."))

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return [Issue("Malformed XML sitemap", "Critical", label, str(exc), "Fix XML syntax errors.")], {"URL Count": "0"}

    if SITEMAP_NS not in root.tag:
        issues.append(Issue("Missing standard sitemaps.org namespace", "Medium", label, root.tag, f'Declare xmlns="{SITEMAP_NS}".'))

    locs = [(sub.text or "").strip() for child in root for sub in child if _local_tag(sub.tag) == "loc" and (sub.text or "").strip()]
    if len(locs) > MAX_URLS:
        issues.append(Issue("Sitemap exceeds 50,000 URL limit", "Critical", label, f"{len(locs):,} URLs", "Split across sitemapindex."))
    elif not locs:
        issues.append(Issue("Empty XML sitemap", "High", label, "0 URLs listed", "Include canonical indexable URLs."))

    non_abs = [u for u in locs if not urllib.parse.urlparse(u).scheme or not urllib.parse.urlparse(u).netloc]
    if non_abs:
        issues.append(Issue("Relative URLs in XML sitemap", "High", label, non_abs[0], "Use full absolute HTTPS URLs in <loc>."))

    if require_url:
        matched = any(u == require_url or u.rstrip("/").endswith(require_url.rstrip("/")) for u in locs)
        if not matched:
            issues.append(
                Issue(
                    "Published URL missing from XML sitemap",
                    "High",
                    label,
                    f'Required URL/path "{require_url}" not present among {len(locs)} <loc> entries',
                    "Ensure sitemap generator includes the newly published URL and updates <lastmod>.",
                )
            )

    if check_status and _local_tag(root.tag) == "urlset":
        for u in [x for x in locs if is_http_url(x)][:20]:
            resp = fetch_url(u, timeout=8.0)
            if resp.error or (resp.status and resp.status >= 400):
                issues.append(Issue("Sitemap URL returned error", "High", u, str(resp.error or resp.status), "Remove dead URL or fix route."))
            elif "text/html" in resp.headers.get("content-type", ""):
                parsed = parse_html(resp.text)
                if parsed.meta_robots and "noindex" in parsed.meta_robots.lower():
                    issues.append(Issue("Sitemap lists noindex URL", "High", u, parsed.meta_robots, "Exclude noindex URLs from sitemaps."))

    return issues, {"Root Tag": _local_tag(root.tag), "URL Count": str(len(locs))}


def run_sitemap_validation(
    target: str,
    require_url: Optional[str] = None,
    check_status: bool = False,
) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []
    if is_http_url(target):
        p = urllib.parse.urlparse(target)
        sm_url = target if p.path not in {"", "/"} else f"{p.scheme}://{p.netloc}/sitemap.xml"
        robots_url = f"{p.scheme}://{p.netloc}/robots.txt"
        r_resp = fetch_url(robots_url)
        if r_resp.status == 200 and "sitemap:" not in r_resp.text.lower():
            issues.append(Issue("robots.txt omits Sitemap directive", "Low", robots_url, "No Sitemap: line found", f"Add Sitemap: {sm_url}"))
        sm_resp = fetch_url(sm_url)
        if sm_resp.error or (sm_resp.status and sm_resp.status >= 400):
            return issues + [Issue("Sitemap unreachable", "High", sm_url, str(sm_resp.error or sm_resp.status), "Serve valid XML at /sitemap.xml.")], {"Mode": "Live Sitemap"}
        sm_issues, summary = validate_sitemap_bytes(sm_resp.final_url, sm_resp.body, require_url=require_url, check_status=check_status)
        return issues + sm_issues, {**summary, "Mode": "Live Sitemap"}

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")
    if path.is_file():
        if path.suffix.lower() == ".xml":
            return validate_sitemap_bytes(path.name, path.read_bytes(), require_url=require_url)
        txt = read_text_safe(path)
        if require_url and require_url not in txt:
            issues.append(Issue("Required route/slug not explicitly found in sitemap source", "Informational", path.name, f'"{require_url}" not matched statically', "Confirm dynamic map/collection query emits this URL."))
        return issues, {"Mode": "Dynamic Sitemap Source"}

    arch = detect_publishing_architecture(path)
    if not arch["sitemap_files"]:
        issues.append(Issue("No sitemap found in repository", "High", str(path), "Missing sitemap.xml or app/sitemap.ts", "Add dynamic or static XML sitemap generation."))
    for sm in arch["sitemap_files"]:
        sm_path = path / sm
        if sm_path.suffix.lower() == ".xml":
            sm_issues, _ = validate_sitemap_bytes(sm, sm_path.read_bytes(), require_url=require_url)
            issues.extend(sm_issues)
        else:
            txt = read_text_safe(sm_path)
            if "localhost" in txt:
                issues.append(Issue("Hardcoded localhost in sitemap source", "Critical", sm, "Contains localhost", "Use canonical production base URL."))
    return issues, {"Mode": "Repository Sitemap Check", "Sitemaps": ", ".join(arch["sitemap_files"]) or "None"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate XML sitemap, robots.txt, and published URL inclusion.")
    parser.add_argument("target", help="Live URL, sitemap.xml file, or repository root")
    parser.add_argument("--require-url", help="Verify this newly published URL or path slug appears in the sitemap")
    parser.add_argument("--check-status", action="store_true", help="Verify live HTTP 200 and indexability for sampled sitemap URLs")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_sitemap_validation(args.target, require_url=args.require_url, check_status=args.check_status)
    except Exception as exc:
        print(f"Error validating sitemap: {exc}", file=sys.stderr)
        return 1

    print(format_report("Sitemap & Discoverability Validation", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
