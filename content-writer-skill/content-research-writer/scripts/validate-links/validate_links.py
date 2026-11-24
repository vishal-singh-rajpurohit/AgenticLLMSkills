"""Internal and external link validator catching invented internal URLs and broken links."""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    discover_known_internal_routes,
    fetch_url,
    format_report,
    is_http_url,
    iter_repo_files,
    parse_frontmatter_and_body,
    parse_html,
    read_text_safe,
)

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "sms:", "data:")
MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _slugify_heading(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", slug)


def _extract_links_from_file(path: Path) -> Tuple[List[Tuple[str, str]], Set[str]]:
    raw = read_text_safe(path)
    if path.suffix.lower() in {".html", ".htm"}:
        parsed = parse_html(raw)
        return [(lnk["href"], lnk["text"]) for lnk in parsed.links], parsed.ids

    _, body = parse_frontmatter_and_body(raw)
    stripped = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    links = [(m.group(2), m.group(1)) for m in MD_LINK_RE.finditer(stripped)]
    anchors: Set[str] = set()
    for line in stripped.splitlines():
        hm = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if hm:
            anchors.add(_slugify_heading(hm.group(1)))
    return links, anchors


def _route_matches_known(path_only: str, known_routes: Set[str]) -> bool:
    clean = path_only.rstrip("/") or "/"
    if clean in known_routes or path_only in known_routes:
        return True
    for route in known_routes:
        if "[" in route and "]" in route:
            pattern = "^" + re.sub(r"\\\[[^\]]+\\\]", r"[^/]+", re.escape(route)) + "$"
            if re.match(pattern, clean):
                return True
    return False


def run_link_validation(
    target: str,
    repo_root: Optional[str] = None,
    check_external: bool = False,
    max_pages: int = 15,
) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []

    if is_http_url(target):
        start_host = urllib.parse.urlparse(target).netloc.lower()
        queue = [target]
        crawled: Set[str] = set()
        link_sources: Dict[str, Set[str]] = {}
        while queue and len(crawled) < max_pages:
            cur = queue.pop(0)
            if cur in crawled:
                continue
            crawled.add(cur)
            resp = fetch_url(cur)
            if cur in link_sources:
                src_list = ", ".join(sorted(link_sources[cur])[:3])
                if resp.error or (resp.status and resp.status >= 400):
                    issues.append(Issue("Broken link", "High", cur, f"{resp.error or resp.status} (from {src_list})", "Fix or remove broken link."))
                elif resp.redirect_chain:
                    issues.append(Issue("Internal link redirects", "Medium", cur, f"Redirects to {resp.final_url} (from {src_list})", "Link directly to canonical URL."))
            if resp.error or (resp.status and resp.status >= 400) or "text/html" not in resp.headers.get("content-type", ""):
                continue
            parsed = parse_html(resp.text)
            for lnk in parsed.links:
                href = lnk["href"].strip()
                if not href or href.lower().startswith(SKIP_SCHEMES) or href.startswith("#"):
                    continue
                abs_url = urllib.parse.urljoin(resp.final_url, href).split("#", 1)[0]
                if not is_http_url(abs_url):
                    continue
                is_int = urllib.parse.urlparse(abs_url).netloc.lower() == start_host
                if not is_int and not check_external:
                    continue
                link_sources.setdefault(abs_url, set()).add(resp.final_url)
                if is_int and abs_url not in crawled and abs_url not in queue and len(crawled) + len(queue) < max_pages * 3:
                    queue.append(abs_url)
        return issues, {"Mode": "Live URL Crawl", "Pages Crawled": str(len(crawled))}

    target_path = Path(target).resolve()
    if not target_path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    repo_path = Path(repo_root).resolve() if repo_root else (target_path if target_path.is_dir() else target_path.parent)
    known_routes = discover_known_internal_routes(repo_path)
    files = [target_path] if target_path.is_file() else iter_repo_files(target_path, {".md", ".mdx", ".html", ".htm"})

    external_urls: Dict[str, Set[str]] = {}
    for f in files:
        rel = f.name if target_path.is_file() else str(f.relative_to(target_path))
        links, anchors = _extract_links_from_file(f)
        for href, anchor_text in links:
            href = href.strip()
            if not href or href.lower().startswith(SKIP_SCHEMES):
                continue
            if not anchor_text or anchor_text.lower() in {"click here", "read more", "here", "link"}:
                issues.append(
                    Issue(
                        "Non-descriptive anchor text",
                        "Low",
                        rel,
                        f'Anchor "{anchor_text}" for "{href}"',
                        "Use descriptive anchor text explaining what the destination page covers.",
                    )
                )
            if is_http_url(href):
                if check_external:
                    external_urls.setdefault(href, set()).add(rel)
                continue
            if href.startswith("#"):
                frag = href[1:]
                if frag and frag not in anchors:
                    issues.append(Issue("Broken in-page anchor", "Low", rel, f'Missing heading/ID for "{href}"', "Fix anchor fragment."))
                continue

            path_only = urllib.parse.unquote(href.split("#", 1)[0].split("?", 1)[0])
            if path_only.startswith("/"):
                disk_candidate = repo_path / path_only.lstrip("/")
                public_candidate = repo_path / "public" / path_only.lstrip("/")
                if not disk_candidate.exists() and not public_candidate.exists() and not _route_matches_known(path_only, known_routes):
                    issues.append(
                        Issue(
                            "Unverified or invented internal URL",
                            "High",
                            rel,
                            f'Internal link "{href}" does not match any known route or file in {repo_path.name}',
                            "Link only to verified existing routes or approved new pages in this release.",
                        )
                    )
            else:
                resolved = (f.parent / path_only).resolve()
                if not any(opt.exists() for opt in (resolved, resolved.with_suffix(".md"), resolved.with_suffix(".mdx"), resolved.with_suffix(".html"))):
                    issues.append(Issue("Broken relative internal link", "High", rel, f'Target "{href}" missing on disk', "Fix relative file link."))

    if check_external and external_urls:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for url, resp in pool.map(lambda u: (u, fetch_url(u, timeout=8.0)), external_urls.keys()):
                if resp.error or (resp.status and resp.status >= 400):
                    issues.append(
                        Issue(
                            "Broken external reference link",
                            "Medium",
                            ", ".join(sorted(external_urls[url])[:3]),
                            f"{url} -> {resp.error or resp.status}",
                            "Replace with a live primary source URL.",
                        )
                    )

    return issues, {"Mode": "Local Content / Repo", "Files Checked": str(len(files)), "Known Internal Routes": str(len(known_routes))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate internal/external links and detect invented internal URLs.")
    parser.add_argument("target", help="Live URL, content file, or directory")
    parser.add_argument("--repo", help="Repository root directory for validating absolute /path internal links")
    parser.add_argument("--check-external", action="store_true", help="Verify external http(s) URLs over HTTP")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_link_validation(args.target, repo_root=args.repo, check_external=args.check_external)
    except Exception as exc:
        print(f"Error validating links: {exc}", file=sys.stderr)
        return 1

    print(format_report("Internal & External Link Validation", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
