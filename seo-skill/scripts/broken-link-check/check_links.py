"""Broken link, redirect hop, and internal anchor checker.

Supports:
  - Local HTML files / directories (checks internal file targets and #fragment IDs)
  - Live HTTP/HTTPS URLs (bounded same-host crawl + optional external link check)
"""

from __future__ import annotations

import argparse
import concurrent.futures
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    fetch_url,
    format_report,
    is_http_url,
    iter_repo_files,
    parse_html,
    read_text_safe,
)

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "sms:", "data:")


def _check_local_html_links(root: Path, files: List[Path]) -> Tuple[List[Issue], int]:
    issues: List[Issue] = []
    checked_count = 0
    file_ids_cache: Dict[Path, Set[str]] = {}

    def get_ids(target_file: Path) -> Set[str]:
        if target_file not in file_ids_cache:
            parsed = parse_html(read_text_safe(target_file))
            file_ids_cache[target_file] = parsed.ids
        return file_ids_cache[target_file]

    for html_file in files:
        rel_src = str(html_file.relative_to(root)) if root.is_dir() else html_file.name
        parsed = parse_html(read_text_safe(html_file))
        get_ids(html_file)

        for link in parsed.links:
            href = link["href"].strip()
            if not href or href.lower().startswith(SKIP_SCHEMES):
                continue
            if is_http_url(href) or href.startswith("//"):
                continue

            checked_count += 1
            path_part, _, frag = href.partition("#")
            if not path_part:
                if frag and frag not in get_ids(html_file):
                    issues.append(
                        Issue(
                            "Broken in-page anchor link",
                            "Low",
                            rel_src,
                            f'href="#{frag}" target ID not found in page',
                            f'Add id="{frag}" to the target element or fix the anchor link.',
                        )
                    )
                continue

            clean_path = urllib.parse.unquote(path_part.split("?", 1)[0])
            if clean_path.startswith("/") and root.is_dir():
                candidate = (root / clean_path.lstrip("/")).resolve()
            else:
                candidate = (html_file.parent / clean_path).resolve()

            resolved_target = None
            for opt in (candidate, candidate / "index.html", candidate.with_suffix(".html")):
                if opt.is_file():
                    resolved_target = opt
                    break

            if resolved_target is None:
                issues.append(
                    Issue(
                        "Broken internal link",
                        "High",
                        rel_src,
                        f'Link href="{href}" does not resolve to an existing file',
                        "Update the href to the correct target route or restore the missing page.",
                    )
                )
            elif frag and resolved_target.suffix.lower() in {".html", ".htm"} and frag not in get_ids(resolved_target):
                issues.append(
                    Issue(
                        "Broken cross-page anchor fragment",
                        "Low",
                        rel_src,
                        f'href="{href}" points to missing #{frag} on target page',
                        "Verify the target section ID matches the link fragment.",
                    )
                )

    return issues, checked_count


def _evaluate_link_response(
    target_url: str,
    resp,
    sources_set: Set[str],
    start_host: str,
) -> List[Issue]:
    """Convert an HTTP response for a linked URL into standardized Issue entries."""
    issues: List[Issue] = []
    sources = ", ".join(sorted(sources_set)[:3])
    is_internal = urllib.parse.urlparse(target_url).netloc.lower() == start_host

    if resp.error or (resp.status and resp.status >= 400):
        issues.append(
            Issue(
                "Broken outbound/internal link (4xx/5xx or unreachable)",
                "High" if is_internal else "Low",
                target_url,
                f"{resp.error or f'HTTP {resp.status}'} (linked from: {sources})",
                "Update the href to the valid destination URL or remove the broken reference.",
            )
        )
    elif len(resp.redirect_chain) > 1:
        issues.append(
            Issue(
                "Redirect chain (>1 hop) on linked URL",
                "Medium",
                target_url,
                f"{len(resp.redirect_chain)} hops -> {resp.final_url} (from: {sources})",
                "Update links to point directly to the final canonical 200 OK URL.",
            )
        )
    elif resp.redirect_chain and is_internal:
        issues.append(
            Issue(
                "Internal link hits a redirect instead of canonical URL",
                "Medium",
                target_url,
                f"Redirects to {resp.final_url} (linked from: {sources})",
                "Update internal anchor hrefs directly to the canonical final URL.",
            )
        )
    return issues


def _check_live_links(
    start_url: str,
    max_pages: int = 15,
    check_external: bool = False,
) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []
    start_host = urllib.parse.urlparse(start_url).netloc.lower()
    queue: List[str] = [start_url]
    crawled: Set[str] = set()
    link_sources: Dict[str, Set[str]] = {}

    while queue and len(crawled) < max_pages:
        current = queue.pop(0)
        if current in crawled:
            continue
        crawled.add(current)

        resp = fetch_url(current, timeout=10.0)
        if current in link_sources:
            issues.extend(_evaluate_link_response(current, resp, link_sources[current], start_host))
        elif resp.error or (resp.status and resp.status >= 400):
            issues.append(
                Issue(
                    "Seed/crawled page returned error",
                    "High",
                    current,
                    resp.error or f"HTTP {resp.status}",
                    "Verify URL routing and server availability.",
                )
            )
            continue

        if resp.error or (resp.status and resp.status >= 400):
            continue

        if "text/html" not in resp.headers.get("content-type", ""):
            continue

        parsed = parse_html(resp.text)
        for link in parsed.links:
            href = link["href"].strip()
            if not href or href.lower().startswith(SKIP_SCHEMES) or href.startswith("#"):
                continue
            absolute = urllib.parse.urljoin(resp.final_url, href).split("#", 1)[0]
            if not is_http_url(absolute):
                continue
            target_host = urllib.parse.urlparse(absolute).netloc.lower()
            is_internal = target_host == start_host
            if not is_internal and not check_external:
                continue
            link_sources.setdefault(absolute, set()).add(resp.final_url)
            if is_internal and absolute not in crawled and absolute not in queue and len(crawled) + len(queue) < max_pages * 3:
                queue.append(absolute)

    targets_to_verify = [url for url in link_sources if url not in crawled]
    checked = len(crawled) + len(targets_to_verify)

    def _probe(url: str):
        return url, fetch_url(url, timeout=8.0, method="GET")

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for target_url, resp in pool.map(_probe, targets_to_verify):
            issues.extend(_evaluate_link_response(target_url, resp, link_sources[target_url], start_host))

    return issues, {"Mode": "Live URL Crawl", "Pages Crawled": str(len(crawled)), "Links Verified": str(checked)}


def run_broken_link_check(
    target: str,
    max_pages: int = 15,
    check_external: bool = False,
) -> Tuple[List[Issue], Dict[str, str]]:
    """Run broken-link verification on a live site or local HTML file/directory."""
    if is_http_url(target):
        return _check_live_links(target, max_pages=max_pages, check_external=check_external)

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    files = [path] if path.is_file() else iter_repo_files(path, {".html", ".htm"})
    root = path.parent if path.is_file() else path
    issues, count = _check_local_html_links(root, files)
    return issues, {"Mode": "Local HTML Files", "Files Scanned": str(len(files)), "Internal Links Checked": str(count)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check for broken links and redirect hops.")
    parser.add_argument("target", help="Live URL or local HTML file/directory")
    parser.add_argument("--max-pages", type=int, default=15, help="Max same-host pages to crawl in live mode")
    parser.add_argument("--check-external", action="store_true", help="Also verify external http(s) links in live mode")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_broken_link_check(args.target, args.max_pages, args.check_external)
    except Exception as exc:
        print(f"Error checking links: {exc}", file=sys.stderr)
        return 1

    print(format_report("Broken Link & Redirect Check", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
