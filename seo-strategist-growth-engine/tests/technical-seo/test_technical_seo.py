"""End-to-end technical SEO tests covering Next.js, static HTML, sitemaps, links, JSON-LD, live HTTP, and tool discovery."""

from __future__ import annotations

import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"


def _run_cli(script_rel: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_rel), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


class _MockSeoSiteHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/robots.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"User-agent: *\nAllow: /\n")
        elif self.path == "/sitemap.xml":
            host = self.headers.get("Host")
            xml = (
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f"  <url><loc>http://{host}/</loc><lastmod>2026-11-20</lastmod></url>\n"
                f"  <url><loc>http://{host}/old-service</loc></url>\n"
                f"  <url><loc>http://{host}/hidden-draft</loc></url>\n"
                "</urlset>\n"
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/xml; charset=utf-8")
            self.end_headers()
            self.wfile.write(xml)
        elif self.path == "/":
            host = self.headers.get("Host")
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Apex Cloud Engineering & Custom Software Studio</title>
  <meta name="description" content="Enterprise software architecture, web platforms, and AI workflow integration." />
  <link rel="canonical" href="http://{host}/" />
  <meta property="og:title" content="Apex Cloud Studio" />
  <meta property="og:description" content="Custom software engineering." />
  <meta property="og:image" content="http://{host}/hero.webp" />
</head>
<body>
  <h1>Custom Software & AI Integrations</h1>
  <a href="/services">Services</a>
  <a href="/old-service">Legacy Service</a>
  <a href="/broken-route">Broken Link</a>
  <img src="/arch.webp" alt="System diagram" width="800" height="450" />
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/services":
            html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Custom Software Services | Apex Cloud</title>
  <meta name="description" content="Dedicated engineering squads for web, mobile, and enterprise AI workflows." />
</head>
<body>
  <h1>Enterprise Software Development Services</h1>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Custom Software Development"
  }
  </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/old-service":
            self.send_response(301)
            self.send_header("Location", "/services")
            self.end_headers()
        elif self.path == "/hidden-draft":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'<html><head><title>Draft</title><meta name="robots" content="noindex" /></head><body><h1>Draft</h1></body></html>')
        else:
            self.send_response(404)
            self.end_headers()


class TestTechnicalSeoScripts(unittest.TestCase):
    """Test tool discovery, codebase audits, static site audits, and live mock crawls."""

    def test_discover_tools_capability_matrix(self) -> None:
        proc = _run_cli("technical-seo-audit/run_technical_audit.py", "--discover-tools", str(SKILL_ROOT), "--format", "json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertTrue(data["sibling_content_research_writer"])
        caps = {row["capability"] for row in data["capability_matrix"]}
        self.assertIn("Keyword Research", caps)
        self.assertIn("Search Performance (GSC)", caps)
        self.assertIn("Technical SEO Audit", caps)

    def test_nextjs_app_router_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                json.dumps({"name": "demo-next", "dependencies": {"next": "15.2.0", "react": "19.0.0"}}),
                encoding="utf-8",
            )
            (repo / "app" / "services" / "[slug]").mkdir(parents=True)
            (repo / "app" / "about").mkdir(parents=True)
            (repo / "app" / "layout.tsx").write_text(
                'export const metadata = { title: "Demo" };\nexport default function Root({ children }: any) { return <html><body>{children}</body></html>; }\n',
                encoding="utf-8",
            )
            (repo / "app" / "page.tsx").write_text(
                'export const metadata = { title: "Same Title" };\n'
                'export default function Home() { return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({ "@type": "Organization" }) }} />; }\n',
                encoding="utf-8",
            )
            (repo / "app" / "about" / "page.tsx").write_text(
                'export const metadata = { title: "Same Title" };\nexport default function About() { return <main>About</main>; }\n',
                encoding="utf-8",
            )
            (repo / "app" / "services" / "[slug]" / "page.tsx").write_text(
                "export default async function ServicePage() { return <main>Service</main>; }\n",
                encoding="utf-8",
            )
            (repo / "app" / "sitemap.ts").write_text(
                'export default function sitemap() { return [{ url: "http://localhost:3000/" }]; }\n',
                encoding="utf-8",
            )

            proc = _run_cli("technical-seo-audit/run_technical_audit.py", str(repo), "--format", "json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            issues = {i["issue"] for i in report["issues"]}
            self.assertIn("Next.js root layout missing metadataBase", issues)
            self.assertIn("Dynamic route lacks generateMetadata", issues)
            self.assertIn("Duplicate hardcoded page title across App Router routes", issues)
            self.assertIn("Hardcoded localhost URL in dynamic sitemap source", issues)
            self.assertIn("Inline React/Next.js JSON-LD omits < escaping", issues)

    def test_static_html_orphans_links_metadata_and_jsonld(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "index.html").write_text(
                """<!DOCTYPE html>
<html>
<head>
  <title>Short</title>
  <link rel="canonical" href="/index.html" />
</head>
<body>
  <h1>Home</h1>
  <h3>Skipped H2</h3>
  <img src="banner.webp" />
  <a href="/missing.html">click here</a>
  <a href="#no-id">Anchor</a>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": []
  }
  </script>
</body>
</html>""",
                encoding="utf-8",
            )
            (site / "orphan.html").write_text(
                '<!DOCTYPE html><html lang="en"><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Orphan Page Title Long Enough</title></head><body><h1>Orphan</h1></body></html>',
                encoding="utf-8",
            )

            meta = json.loads(_run_cli("metadata-audit/audit_metadata.py", str(site), "--format", "json").stdout)
            meta_issues = {i["issue"] for i in meta["issues"]}
            self.assertIn("Missing html lang attribute", meta_issues)
            self.assertIn("Relative canonical URL", meta_issues)
            self.assertIn("Skipped heading hierarchy level", meta_issues)
            self.assertIn("Images missing alt attribute", meta_issues)
            self.assertIn("Images missing explicit width/height attributes", meta_issues)

            links = json.loads(_run_cli("broken-link-audit/audit_links.py", str(site), "--format", "json").stdout)
            link_issues = {i["issue"] for i in links["issues"]}
            self.assertIn("Broken internal link", link_issues)
            self.assertIn("Broken in-page anchor link", link_issues)
            self.assertIn("Generic non-descriptive internal anchor text", link_issues)
            self.assertIn("Orphan HTML pages with zero internal inbound links", link_issues)

            schema = json.loads(_run_cli("structured-data-validation/validate_structured_data.py", str(site), "--format", "json").stdout)
            schema_issues = {i["issue"] for i in schema["issues"]}
            self.assertIn("Deprecated Google rich result schema type (FAQPage)", schema_issues)

    def test_live_http_server_audit(self) -> None:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _MockSeoSiteHandler)
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{port}"
            proc = _run_cli("technical-seo-audit/run_technical_audit.py", base, "--check-status", "--max-pages", "5", "--format", "json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            issues = {i["issue"] for i in json.loads(proc.stdout)["issues"]}
            self.assertIn("robots.txt does not declare a Sitemap directive", issues)
            self.assertIn("Sitemap lists redirecting URLs instead of final canonical URLs", issues)
            self.assertIn("Sitemap includes noindex URLs", issues)
            self.assertIn("Broken outbound/internal link (4xx/5xx or unreachable)", issues)
            self.assertIn("Internal link hits a redirect instead of canonical URL", issues)
        finally:
            server.shutdown()
            server.server_close()

    def test_missing_path_fails_cleanly_without_traceback(self) -> None:
        for script_rel in (
            "technical-seo-audit/run_technical_audit.py",
            "metadata-audit/audit_metadata.py",
            "sitemap-audit/audit_sitemap.py",
            "broken-link-audit/audit_links.py",
            "structured-data-validation/validate_structured_data.py",
        ):
            proc = _run_cli(script_rel, "/definitely/missing/seo_growth_engine_test_path")
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
