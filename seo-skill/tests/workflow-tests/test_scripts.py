"""End-to-end workflow tests for all Python SEO audit and validation scripts."""

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
    script_path = SCRIPTS_DIR / script_rel
    return subprocess.run(
        [sys.executable, str(script_path), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


class _MockSeoHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/robots.txt":
            body = b"User-agent: *\nAllow: /\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/sitemap.xml":
            host = self.headers.get("Host")
            xml = (
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f"  <url><loc>http://{host}/</loc><lastmod>2026-11-01</lastmod></url>\n"
                f"  <url><loc>http://{host}/old-page</loc></url>\n"
                f"  <url><loc>http://{host}/hidden</loc></url>\n"
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
  <title>Acme Industrial CCTV Systems Jodhpur</title>
  <meta name="description" content="Trusted residential and warehouse CCTV camera installation in Jodhpur with warranty and AMC support." />
  <link rel="canonical" href="http://{host}/" />
  <meta property="og:title" content="Acme CCTV" />
  <meta property="og:description" content="Trusted CCTV installation." />
  <meta property="og:image" content="http://{host}/hero.webp" />
</head>
<body>
  <h1>CCTV Installation in Jodhpur</h1>
  <a href="/products">Products</a>
  <a href="/old-page">Old Page</a>
  <a href="/missing-404">Broken Link</a>
  <img src="/cam.webp" alt="4MP warehouse camera" />
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/products":
            html = """<!DOCTYPE html>
<html lang="en">
<head><title>4MP PoE Security Camera Kit | Acme</title></head>
<body>
  <h1>4MP PoE Camera Kit</h1>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "4MP PoE Security Camera Kit",
    "offers": {
      "@type": "Offer",
      "price": "18500",
      "priceCurrency": "INR",
      "availability": "https://schema.org/InStock"
    }
  }
  </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/old-page":
            self.send_response(301)
            self.send_header("Location", "/products")
            self.end_headers()
        elif self.path == "/hidden":
            html = '<html><head><title>Hidden</title><meta name="robots" content="noindex" /></head><body><h1>Hidden</h1></body></html>'
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class TestWorkflowScripts(unittest.TestCase):
    """Test local repo audits, static HTML fixtures, error handling, and live HTTP server audits."""

    def test_nextjs_app_router_fixture_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text(
                json.dumps({"name": "demo-next", "dependencies": {"next": "15.2.0", "react": "19.0.0"}}),
                encoding="utf-8",
            )
            (repo / "app" / "products" / "[slug]").mkdir(parents=True)
            (repo / "app" / "about").mkdir(parents=True)

            # Root layout missing metadataBase
            (repo / "app" / "layout.tsx").write_text(
                'export const metadata = { title: "Demo Site" };\nexport default function RootLayout({ children }: any) { return <html><body>{children}</body></html>; }\n',
                encoding="utf-8",
            )
            # Duplicate title on two routes + dynamic route missing generateMetadata
            (repo / "app" / "page.tsx").write_text(
                'export const metadata = { title: "Same Title" };\nexport default function Home() { return <main>Home</main>; }\n',
                encoding="utf-8",
            )
            (repo / "app" / "about" / "page.tsx").write_text(
                'export const metadata = { title: "Same Title" };\nexport default function About() { return <main>About</main>; }\n',
                encoding="utf-8",
            )
            (repo / "app" / "products" / "[slug]" / "page.tsx").write_text(
                "export default async function ProductPage() { return <main>Product</main>; }\n",
                encoding="utf-8",
            )
            (repo / "app" / "sitemap.ts").write_text(
                'export default function sitemap() { return [{ url: "http://localhost:3000/" }]; }\n',
                encoding="utf-8",
            )

            proc = _run_cli("seo-audit/seo_audit.py", str(repo), "--format", "json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)

            self.assertIn("Next.js", report["summary"]["Framework"])
            self.assertEqual(report["summary"]["Router"], "App Router")
            issue_titles = {item["issue"] for item in report["issues"]}
            self.assertIn("Next.js root layout missing metadataBase", issue_titles)
            self.assertIn("Dynamic route lacks generateMetadata", issue_titles)
            self.assertIn("Duplicate hardcoded page title across App Router routes", issue_titles)
            self.assertIn("Hardcoded localhost URL in dynamic sitemap source", issue_titles)
            self.assertIn("No robots configuration found in repository", issue_titles)

    def test_static_html_broken_links_metadata_and_jsonld(self) -> None:
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
  <h1 id="top">Welcome</h1>
  <h3>Skipped H2</h3>
  <img src="banner.jpg" />
  <a href="/does-not-exist.html">Missing Page</a>
  <a href="#missing-anchor">Missing Anchor</a>
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

            meta_proc = _run_cli("metadata-check/check_metadata.py", str(site), "--format", "json")
            self.assertEqual(meta_proc.returncode, 0, meta_proc.stderr)
            meta_issues = {i["issue"] for i in json.loads(meta_proc.stdout)["issues"]}
            self.assertIn("Missing html lang attribute", meta_issues)
            self.assertIn("Relative canonical URL", meta_issues)
            self.assertIn("Skipped heading hierarchy level", meta_issues)
            self.assertIn("Images missing alt attribute", meta_issues)

            link_proc = _run_cli("broken-link-check/check_links.py", str(site), "--format", "json")
            self.assertEqual(link_proc.returncode, 0, link_proc.stderr)
            link_issues = {i["issue"] for i in json.loads(link_proc.stdout)["issues"]}
            self.assertIn("Broken internal link", link_issues)
            self.assertIn("Broken in-page anchor link", link_issues)

            schema_proc = _run_cli("structured-data-validation/validate_jsonld.py", str(site), "--format", "json")
            self.assertEqual(schema_proc.returncode, 0, schema_proc.stderr)
            schema_issues = {i["issue"] for i in json.loads(schema_proc.stdout)["issues"]}
            self.assertIn("Deprecated Google rich result schema type (FAQPage)", schema_issues)

    def test_sitemap_validation_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_xml = Path(tmp) / "sitemap.xml"
            bad_xml.write_text(
                '<?xml version="1.0"?><urlset><url><loc>/relative-only</loc></url></urlset>',
                encoding="utf-8",
            )
            proc = _run_cli("sitemap-validation/validate_sitemap.py", str(bad_xml), "--format", "json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            issues = {i["issue"] for i in json.loads(proc.stdout)["issues"]}
            self.assertIn("Missing standard sitemaps.org XML namespace", issues)
            self.assertIn("Non-absolute URLs in XML sitemap", issues)

            malformed = Path(tmp) / "broken.xml"
            malformed.write_text("<urlset><url></urlset>", encoding="utf-8")
            proc2 = _run_cli("sitemap-validation/validate_sitemap.py", str(malformed), "--format", "json")
            self.assertEqual(proc2.returncode, 0, proc2.stderr)
            issues2 = {i["issue"] for i in json.loads(proc2.stdout)["issues"]}
            self.assertIn("Malformed XML sitemap", issues2)

    def test_live_http_server_audit_and_redirect_detection(self) -> None:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _MockSeoHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{port}"
            proc = _run_cli("seo-audit/seo_audit.py", base, "--check-status", "--max-pages", "5", "--format", "json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            issue_titles = {i["issue"] for i in report["issues"]}
            self.assertIn("robots.txt does not declare a Sitemap directive", issue_titles)
            self.assertIn("Sitemap lists redirecting URLs instead of final canonical URLs", issue_titles)
            self.assertIn("Sitemap includes noindex URLs", issue_titles)
            self.assertIn("Broken outbound/internal link (4xx/5xx or unreachable)", issue_titles)
            self.assertIn("Internal link hits a redirect instead of canonical URL", issue_titles)

            md_proc = _run_cli("seo-audit/seo_audit.py", base, "--format", "markdown")
            self.assertEqual(md_proc.returncode, 0)
            self.assertIn("| Issue | Severity | Affected URLs | Evidence | Recommended Fix |", md_proc.stdout)
        finally:
            server.shutdown()
            server.server_close()

    def test_error_handling_for_missing_path(self) -> None:
        for script_rel in (
            "seo-audit/seo_audit.py",
            "metadata-check/check_metadata.py",
            "sitemap-validation/validate_sitemap.py",
            "broken-link-check/check_links.py",
            "structured-data-validation/validate_jsonld.py",
        ):
            proc = _run_cli(script_rel, "/definitely/nonexistent/seo_skill_path_12345")
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
