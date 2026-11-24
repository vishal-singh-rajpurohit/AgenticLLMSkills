"""Shared utilities for the Universal SEO Strategist skill scripts.

Pure Python 3.9+ standard library helpers for HTML parsing, HTTP fetching,
framework detection, and structured Markdown/JSON reporting.
"""

from __future__ import annotations

import json
import os
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "out",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "coverage",
}

DEFAULT_USER_AGENT = "UniversalSEOStrategistBot/1.0 (+https://agentskills.io)"
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}


@dataclass
class Issue:
    """Single standardized SEO audit finding."""

    issue: str
    severity: str
    affected_urls: str
    evidence: str
    recommended_fix: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def sort_issues(issues: List[Issue]) -> List[Issue]:
    """Sort issues from Critical -> Informational, preserving insertion order within ties."""
    return sorted(issues, key=lambda item: SEVERITY_ORDER.get(item.severity, 99))


def _escape_md_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\r\n", " ").replace("\n", " ").strip()


def render_markdown_table(issues: List[Issue]) -> str:
    """Render findings using the standard 5-column technical audit Markdown table."""
    lines = [
        "| Issue | Severity | Affected URLs | Evidence | Recommended Fix |",
        "|---|---|---|---|---|",
    ]
    if not issues:
        lines.append("| No issues detected in scanned scope | Informational | N/A | Automated checks passed | Continue manual and Search Console verification |")
        return "\n".join(lines)

    for item in sort_issues(issues):
        lines.append(
            f"| {_escape_md_cell(item.issue)} "
            f"| {_escape_md_cell(item.severity)} "
            f"| {_escape_md_cell(item.affected_urls)} "
            f"| {_escape_md_cell(item.evidence)} "
            f"| {_escape_md_cell(item.recommended_fix)} |"
        )
    return "\n".join(lines)


def format_report(
    title: str,
    target: str,
    issues: List[Issue],
    summary: Optional[Dict[str, Any]] = None,
    fmt: str = "markdown",
) -> str:
    """Serialize audit results to JSON or Markdown."""
    ordered = sort_issues(issues)
    counts: Dict[str, int] = {k: 0 for k in SEVERITY_ORDER}
    for item in ordered:
        counts[item.severity] = counts.get(item.severity, 0) + 1

    payload = {
        "title": title,
        "target": target,
        "summary": summary or {},
        "severity_counts": counts,
        "issues": [item.to_dict() for item in ordered],
    }
    if fmt == "json":
        return json.dumps(payload, indent=2, ensure_ascii=False)

    parts = [f"# {title}", "", f"**Target:** `{target}`"]
    if summary:
        for key, value in summary.items():
            parts.append(f"**{key}:** {value}")
    parts.extend(
        [
            "",
            (
                f"**Counts:** Critical={counts['Critical']} | High={counts['High']} | "
                f"Medium={counts['Medium']} | Low={counts['Low']} | Informational={counts['Informational']}"
            ),
            "",
            render_markdown_table(ordered),
        ]
    )
    return "\n".join(parts)


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class HttpResponse:
    """Result of an HTTP/HTTPS fetch with optional redirect trace."""

    requested_url: str
    final_url: str
    status: Optional[int]
    headers: Dict[str, str]
    body: bytes
    redirect_chain: List[Tuple[int, str]]
    error: Optional[str] = None

    @property
    def text(self) -> str:
        charset = "utf-8"
        ctype = self.headers.get("content-type", "")
        match = re.search(r"charset=([A-Za-z0-9._-]+)", ctype, re.IGNORECASE)
        if match:
            charset = match.group(1)
        try:
            return self.body.decode(charset, errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")


def is_http_url(target: str) -> bool:
    """Return True when target is an HTTP or HTTPS URL."""
    parsed = urllib.parse.urlparse(target.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def fetch_url(
    url: str,
    timeout: float = 10.0,
    method: str = "GET",
    max_redirects: int = 5,
    max_bytes: int = 5_000_000,
) -> HttpResponse:
    """Fetch a URL safely, recording every redirect hop without unhandled exceptions."""
    if not is_http_url(url):
        return HttpResponse(url, url, None, {}, b"", [], f"Invalid HTTP/HTTPS URL: {url}")

    chain: List[Tuple[int, str]] = []
    current_url = url
    opener = urllib.request.build_opener(_NoRedirectHandler())

    for _ in range(max_redirects + 1):
        req = urllib.request.Request(
            current_url,
            method=method,
            headers={
                "User-Agent": DEFAULT_USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        try:
            with opener.open(req, timeout=timeout) as resp:
                status = getattr(resp, "status", resp.getcode())
                headers = {k.lower(): v for k, v in resp.headers.items()}
                body = b"" if method == "HEAD" else resp.read(max_bytes)
                return HttpResponse(url, current_url, status, headers, body, chain, None)
        except urllib.error.HTTPError as exc:
            headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
            if exc.code in {301, 302, 303, 307, 308} and "location" in headers:
                next_url = urllib.parse.urljoin(current_url, headers["location"])
                chain.append((exc.code, next_url))
                current_url = next_url
                continue
            body = exc.read(max_bytes) if method != "HEAD" else b""
            return HttpResponse(url, current_url, exc.code, headers, body, chain, None)
        except (urllib.error.URLError, TimeoutError, ssl.SSLError, ValueError, OSError) as exc:
            return HttpResponse(url, current_url, None, {}, b"", chain, str(exc))

    return HttpResponse(url, current_url, None, {}, b"", chain, f"Exceeded {max_redirects} redirects (possible loop)")


class HTMLSeoParser(HTMLParser):
    """Lightweight HTML parser extracting SEO metadata, headings, links, images, and JSON-LD."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: Optional[str] = None
        self.title: Optional[str] = None
        self.meta_description: Optional[str] = None
        self.meta_robots: Optional[str] = None
        self.viewport: Optional[str] = None
        self.canonical: Optional[str] = None
        self.hreflangs: List[Tuple[str, str]] = []
        self.open_graph: Dict[str, str] = {}
        self.twitter_tags: Dict[str, str] = {}
        self.headings: List[Tuple[str, str]] = []
        self.images: List[Dict[str, Optional[str]]] = []
        self.links: List[Dict[str, str]] = []
        self.jsonld_blocks: List[str] = []
        self.ids: set[str] = set()

        self._in_title = False
        self._title_buf: List[str] = []
        self._active_heading: Optional[str] = None
        self._heading_buf: List[str] = []
        self._in_link = False
        self._link_attrs: Dict[str, str] = {}
        self._link_buf: List[str] = []
        self._in_jsonld = False
        self._jsonld_buf: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if "id" in attr_map and attr_map["id"]:
            self.ids.add(attr_map["id"])

        if t == "html":
            self.lang = attr_map.get("lang") or attr_map.get("xml:lang")
        elif t == "title":
            self._in_title = True
            self._title_buf = []
        elif t == "meta":
            name = attr_map.get("name", "").lower()
            prop = attr_map.get("property", "").lower()
            content = attr_map.get("content", "")
            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.meta_robots = content
            elif name == "viewport":
                self.viewport = content
            if prop.startswith("og:"):
                self.open_graph[prop] = content
            if name.startswith("twitter:") or prop.startswith("twitter:"):
                self.twitter_tags[name or prop] = content
        elif t == "link":
            rels = {r.lower() for r in attr_map.get("rel", "").split()}
            href = attr_map.get("href", "")
            if "canonical" in rels and href:
                self.canonical = href
            if "alternate" in rels and "hreflang" in attr_map and href:
                self.hreflangs.append((attr_map["hreflang"], href))
        elif t in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._active_heading = t
            self._heading_buf = []
        elif t == "img":
            self.images.append(
                {
                    "src": attr_map.get("src"),
                    "alt": attr_map.get("alt") if "alt" in attr_map else None,
                    "loading": attr_map.get("loading"),
                }
            )
        elif t == "a":
            self._in_link = True
            self._link_attrs = attr_map
            self._link_buf = []
        elif t == "script" and attr_map.get("type", "").lower().split(";")[0].strip() == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "title" and self._in_title:
            self._in_title = False
            self.title = "".join(self._title_buf).strip()
        elif t == self._active_heading:
            text = re.sub(r"\s+", " ", "".join(self._heading_buf)).strip()
            self.headings.append((t, text))
            self._active_heading = None
        elif t == "a" and self._in_link:
            self._in_link = False
            if "href" in self._link_attrs:
                self.links.append(
                    {
                        "href": self._link_attrs.get("href", ""),
                        "rel": self._link_attrs.get("rel", ""),
                        "text": re.sub(r"\s+", " ", "".join(self._link_buf)).strip(),
                    }
                )
        elif t == "script" and self._in_jsonld:
            self._in_jsonld = False
            raw = "".join(self._jsonld_buf).strip()
            if raw:
                self.jsonld_blocks.append(raw)

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_buf.append(data)
        if self._active_heading:
            self._heading_buf.append(data)
        if self._in_link:
            self._link_buf.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)


def parse_html(html_text: str) -> HTMLSeoParser:
    """Parse an HTML document into an HTMLSeoParser instance."""
    parser = HTMLSeoParser()
    parser.feed(html_text)
    parser.close()
    return parser


def iter_repo_files(root: Path, extensions: Iterable[str]) -> List[Path]:
    """Walk a local workspace skipping build/vendor/VCS directories."""
    ext_set = {e.lower() for e in extensions}
    results: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in filenames:
            path = Path(dirpath) / fname
            if path.suffix.lower() in ext_set:
                results.append(path)
    return sorted(results)


def read_text_safe(path: Path) -> str:
    """Read UTF-8 text safely with replacement fallback."""
    return path.read_text(encoding="utf-8", errors="replace")


def detect_repo_stack(root: Path) -> Dict[str, Any]:
    """Inspect a local project directory and report framework, version, router, and key SEO files."""
    info: Dict[str, Any] = {
        "framework": "Unknown / Static",
        "version": None,
        "router": None,
        "app_dir": None,
        "pages_dir": None,
        "robots_files": [],
        "sitemap_files": [],
    }
    pkg_path = root / "package.json"
    if pkg_path.is_file():
        try:
            pkg = json.loads(read_text_safe(pkg_path))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            for dep, label in [
                ("next", "Next.js"),
                ("astro", "Astro"),
                ("nuxt", "Nuxt"),
                ("@sveltejs/kit", "SvelteKit"),
                ("@angular/core", "Angular"),
                ("react", "React"),
            ]:
                if dep in deps:
                    info["framework"] = label
                    info["version"] = deps[dep]
                    break
        except json.JSONDecodeError:
            info["framework"] = "Node.js (invalid package.json)"
    elif (root / "wp-config.php").is_file() or (root / "wp-content").is_dir():
        info["framework"] = "WordPress"
    elif list(root.glob("*.html")) or (root / "index.html").is_file():
        info["framework"] = "Static HTML"

    for candidate in ["app", "src/app"]:
        if (root / candidate).is_dir():
            info["app_dir"] = candidate
            break
    for candidate in ["pages", "src/pages"]:
        if (root / candidate).is_dir():
            info["pages_dir"] = candidate
            break

    if info["framework"] == "Next.js":
        if info["app_dir"] and info["pages_dir"]:
            info["router"] = "Hybrid (App + Pages Router)"
        elif info["app_dir"]:
            info["router"] = "App Router"
        elif info["pages_dir"]:
            info["router"] = "Pages Router"

    for pattern in ["robots.txt", "public/robots.txt", "app/robots.*", "src/app/robots.*"]:
        info["robots_files"].extend(str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file())
    for pattern in [
        "sitemap*.xml",
        "public/sitemap*.xml",
        "app/sitemap.*",
        "src/app/sitemap.*",
        "pages/sitemap.xml.*",
        "src/pages/sitemap.xml.*",
    ]:
        info["sitemap_files"].extend(str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file())

    info["robots_files"] = sorted(set(info["robots_files"]))
    info["sitemap_files"] = sorted(set(info["sitemap_files"]))
    return info
