"""Shared stdlib utilities for content-research-writer validation scripts."""

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
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

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

DEFAULT_USER_AGENT = "ContentResearchWriterBot/1.0 (+https://agentskills.io)"
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}


@dataclass
class Issue:
    """Standardized editorial or technical validation finding."""

    issue: str
    severity: str
    location: str
    evidence: str
    fix: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def sort_issues(issues: List[Issue]) -> List[Issue]:
    return sorted(issues, key=lambda item: SEVERITY_ORDER.get(item.severity, 99))


def _md_cell(val: str) -> str:
    return val.replace("|", "\\|").replace("\r\n", " ").replace("\n", " ").strip()


def format_report(
    title: str,
    target: str,
    issues: List[Issue],
    summary: Optional[Dict[str, Any]] = None,
    fmt: str = "markdown",
) -> str:
    """Serialize findings to Markdown table or JSON."""
    ordered = sort_issues(issues)
    counts = {k: 0 for k in SEVERITY_ORDER}
    for item in ordered:
        counts[item.severity] = counts.get(item.severity, 0) + 1

    payload = {
        "title": title,
        "target": target,
        "summary": summary or {},
        "severity_counts": counts,
        "issues": [i.to_dict() for i in ordered],
    }
    if fmt == "json":
        return json.dumps(payload, indent=2, ensure_ascii=False)

    lines = [f"# {title}", "", f"**Target:** `{target}`"]
    if summary:
        for k, v in summary.items():
            lines.append(f"**{k}:** {v}")
    lines.extend(
        [
            "",
            (
                f"**Counts:** Critical={counts['Critical']} | High={counts['High']} | "
                f"Medium={counts['Medium']} | Low={counts['Low']} | Informational={counts['Informational']}"
            ),
            "",
            "| Issue | Severity | Location | Evidence | Recommended Fix |",
            "|---|---|---|---|---|",
        ]
    )
    if not ordered:
        lines.append("| All checks passed | Informational | N/A | No defects detected in scanned scope | Proceed to human preview/verification |")
    else:
        for item in ordered:
            lines.append(
                f"| {_md_cell(item.issue)} | {_md_cell(item.severity)} | {_md_cell(item.location)} "
                f"| {_md_cell(item.evidence)} | {_md_cell(item.fix)} |"
            )
    return "\n".join(lines)


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class HttpResponse:
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


def is_http_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def fetch_url(url: str, timeout: float = 10.0, method: str = "GET", max_redirects: int = 5) -> HttpResponse:
    """Fetch an HTTP/HTTPS URL safely while tracking redirects."""
    if not is_http_url(url):
        return HttpResponse(url, url, None, {}, b"", [], f"Invalid HTTP/HTTPS URL: {url}")

    chain: List[Tuple[int, str]] = []
    current = url
    opener = urllib.request.build_opener(_NoRedirectHandler())

    for _ in range(max_redirects + 1):
        req = urllib.request.Request(
            current,
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
                body = b"" if method == "HEAD" else resp.read(5_000_000)
                return HttpResponse(url, current, status, headers, body, chain, None)
        except urllib.error.HTTPError as exc:
            headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
            if exc.code in {301, 302, 303, 307, 308} and "location" in headers:
                nxt = urllib.parse.urljoin(current, headers["location"])
                chain.append((exc.code, nxt))
                current = nxt
                continue
            body = exc.read(5_000_000) if method != "HEAD" else b""
            return HttpResponse(url, current, exc.code, headers, body, chain, None)
        except (urllib.error.URLError, TimeoutError, ssl.SSLError, ValueError, OSError) as exc:
            return HttpResponse(url, current, None, {}, b"", chain, str(exc))

    return HttpResponse(url, current, None, {}, b"", chain, f"Exceeded {max_redirects} redirects")


def read_text_safe(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_repo_files(root: Path, extensions: Iterable[str]) -> List[Path]:
    ext_set = {e.lower() for e in extensions}
    out: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in filenames:
            p = Path(dirpath) / fname
            if p.suffix.lower() in ext_set:
                out.append(p)
    return sorted(out)


def parse_frontmatter_and_body(text: str) -> Tuple[Dict[str, str], str]:
    """Parse simple YAML frontmatter from Markdown/MDX documents."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.DOTALL)
    if not match:
        return {}, text
    raw_fm = match.group(1)
    body = text[match.end():]
    fields: Dict[str, str] = {}
    for line in raw_fm.splitlines():
        kv = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip().strip('"').strip("'")
            fields[key] = val
    return fields, body


class HTMLDocParser(HTMLParser):
    """Extract headings, metadata, links, images, IDs, and JSON-LD blocks from HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: Optional[str] = None
        self.title: Optional[str] = None
        self.meta_description: Optional[str] = None
        self.meta_robots: Optional[str] = None
        self.canonical: Optional[str] = None
        self.open_graph: Dict[str, str] = {}
        self.headings: List[Tuple[str, str]] = []
        self.links: List[Dict[str, str]] = []
        self.images: List[Dict[str, Optional[str]]] = []
        self.jsonld_blocks: List[str] = []
        self.ids: Set[str] = set()

        self._in_title = False
        self._title_buf: List[str] = []
        self._active_h: Optional[str] = None
        self._h_buf: List[str] = []
        self._in_a = False
        self._a_attrs: Dict[str, str] = {}
        self._a_buf: List[str] = []
        self._in_jsonld = False
        self._jsonld_buf: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        amap = {k.lower(): (v or "") for k, v in attrs}
        if amap.get("id"):
            self.ids.add(amap["id"])
        if t == "html":
            self.lang = amap.get("lang")
        elif t == "title":
            self._in_title = True
            self._title_buf = []
        elif t == "meta":
            name = amap.get("name", "").lower()
            prop = amap.get("property", "").lower()
            content = amap.get("content", "")
            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.meta_robots = content
            if prop.startswith("og:"):
                self.open_graph[prop] = content
        elif t == "link":
            rels = {r.lower() for r in amap.get("rel", "").split()}
            if "canonical" in rels and amap.get("href"):
                self.canonical = amap["href"]
        elif t in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._active_h = t
            self._h_buf = []
        elif t == "img":
            self.images.append(
                {
                    "src": amap.get("src"),
                    "alt": amap.get("alt") if "alt" in amap else None,
                    "width": amap.get("width"),
                    "height": amap.get("height"),
                    "loading": amap.get("loading"),
                }
            )
        elif t == "a":
            self._in_a = True
            self._a_attrs = amap
            self._a_buf = []
        elif t == "script" and amap.get("type", "").lower().split(";")[0].strip() == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "title" and self._in_title:
            self._in_title = False
            self.title = "".join(self._title_buf).strip()
        elif t == self._active_h:
            txt = re.sub(r"\s+", " ", "".join(self._h_buf)).strip()
            self.headings.append((t, txt))
            self._active_h = None
        elif t == "a" and self._in_a:
            self._in_a = False
            if "href" in self._a_attrs:
                self.links.append(
                    {
                        "href": self._a_attrs["href"],
                        "text": re.sub(r"\s+", " ", "".join(self._a_buf)).strip(),
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
        if self._active_h:
            self._h_buf.append(data)
        if self._in_a:
            self._a_buf.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)


def parse_html(html_text: str) -> HTMLDocParser:
    parser = HTMLDocParser()
    parser.feed(html_text)
    parser.close()
    return parser


def detect_publishing_architecture(root: Path) -> Dict[str, Any]:
    """Detect static frameworks, content directories, and database/CMS integrations."""
    arch: Dict[str, Any] = {
        "framework": "Unknown / Static",
        "version": None,
        "publishing_mode": "Static / Source-Controlled",
        "db_orm_or_cms": [],
        "prisma_models": [],
        "content_dirs": [],
        "image_dirs": [],
        "sitemap_files": [],
        "robots_files": [],
    }
    deps: Dict[str, str] = {}
    pkg_path = root / "package.json"
    if pkg_path.is_file():
        try:
            pkg = json.loads(read_text_safe(pkg_path))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        except json.JSONDecodeError:
            pass

    for dep, label in [
        ("next", "Next.js"),
        ("astro", "Astro"),
        ("gatsby", "Gatsby"),
        ("nuxt", "Nuxt"),
        ("@sveltejs/kit", "SvelteKit"),
        ("react", "React"),
    ]:
        if dep in deps:
            arch["framework"] = label
            arch["version"] = deps[dep]
            break

    if (root / "wp-config.php").is_file() or (root / "wp-content").is_dir():
        arch["framework"] = "WordPress"
        arch["publishing_mode"] = "Database / CMS"
        arch["db_orm_or_cms"].append("WordPress")

    cms_markers = [
        ("@prisma/client", "Prisma"),
        ("prisma", "Prisma"),
        ("drizzle-orm", "Drizzle"),
        ("mongoose", "Mongoose"),
        ("pg", "PostgreSQL"),
        ("mongodb", "MongoDB"),
        ("@sanity/client", "Sanity"),
        ("next-sanity", "Sanity"),
        ("@strapi/strapi", "Strapi"),
        ("@directus/sdk", "Directus"),
        ("payload", "Payload CMS"),
        ("contentful", "Contentful"),
    ]
    for dep, label in cms_markers:
        if dep in deps and label not in arch["db_orm_or_cms"]:
            arch["db_orm_or_cms"].append(label)

    prisma_schema = root / "prisma" / "schema.prisma"
    if prisma_schema.is_file():
        if "Prisma" not in arch["db_orm_or_cms"]:
            arch["db_orm_or_cms"].append("Prisma")
        schema_txt = read_text_safe(prisma_schema)
        arch["prisma_models"] = re.findall(r"^\s*model\s+([A-Za-z0-9_]+)\s*\{", schema_txt, re.MULTILINE)

    if arch["db_orm_or_cms"]:
        arch["publishing_mode"] = "Database / CMS"

    for cdir in ("content", "src/content", "posts", "blog", "content/blog", "data"):
        if (root / cdir).is_dir():
            arch["content_dirs"].append(cdir)

    for idir in ("public/images", "public", "src/assets", "assets"):
        if (root / idir).is_dir():
            arch["image_dirs"].append(idir)

    for pat in ("robots.txt", "public/robots.txt", "app/robots.*", "src/app/robots.*"):
        arch["robots_files"].extend(str(p.relative_to(root)) for p in root.glob(pat) if p.is_file())
    for pat in ("sitemap*.xml", "public/sitemap*.xml", "app/sitemap.*", "src/app/sitemap.*"):
        arch["sitemap_files"].extend(str(p.relative_to(root)) for p in root.glob(pat) if p.is_file())

    return arch


def discover_known_internal_routes(root: Path) -> Set[str]:
    """Collect real routes and content URLs present in a local repository."""
    routes: Set[str] = {"/"}

    for app_rel in ("app", "src/app"):
        app_dir = root / app_rel
        if app_dir.is_dir():
            for page_file in iter_repo_files(app_dir, {".tsx", ".ts", ".jsx", ".js", ".mdx"}):
                if page_file.stem in {"page", "index"}:
                    rel_parent = page_file.parent.relative_to(app_dir)
                    parts = [p for p in rel_parent.parts if not (p.startswith("(") and p.endswith(")"))]
                    route = "/" + "/".join(parts)
                    routes.add(route if route != "" else "/")

    for pages_rel in ("pages", "src/pages"):
        pages_dir = root / pages_rel
        if pages_dir.is_dir():
            for pf in iter_repo_files(pages_dir, {".tsx", ".ts", ".jsx", ".js", ".mdx", ".md"}):
                rel = pf.relative_to(pages_dir)
                if rel.parts[0] == "api" or rel.stem.startswith("_"):
                    continue
                route_path = "/" + "/".join(rel.with_suffix("").parts)
                route_path = re.sub(r"/index$", "", route_path) or "/"
                routes.add(route_path)

    for cdir_rel in ("content", "src/content", "posts", "blog"):
        cdir = root / cdir_rel
        if cdir.is_dir():
            for cf in iter_repo_files(cdir, {".md", ".mdx"}):
                rel = cf.relative_to(cdir).with_suffix("")
                fm, _ = parse_frontmatter_and_body(read_text_safe(cf))
                slug = fm.get("slug") or rel.name
                routes.add("/" + "/".join((*rel.parts[:-1], slug)))
                routes.add("/blog/" + slug)

    for hf in iter_repo_files(root, {".html", ".htm"}):
        rel = hf.relative_to(root)
        routes.add("/" + str(rel).replace("\\", "/"))
        if rel.name == "index.html":
            parent_route = "/" + str(rel.parent).replace("\\", "/")
            routes.add("/" if parent_route == "/." else parent_route)

    return routes
