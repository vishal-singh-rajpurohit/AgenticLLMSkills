# Technical SEO Audit & Codebase Implementation

Inspect live URLs, server responses, and repository source before proposing or editing code. Preserve existing architecture and URLs unless a migration is justified and approved.

## 1. Technical SEO Audit Pillars

### Crawlability & Indexability
- **`robots.txt`:** Must never return `5xx`; do not block CSS, JS, or public pages needed for rendering (`robots.txt` prevents crawling, not guaranteed deindexing of linked URLs). Review AI bots (`OAI-SearchBot`, `GPTBot`, `Google-Extended`) intentionally per business policy.
- **XML Sitemaps:** Valid UTF-8 XML (`sitemaps.org/schemas/sitemap/0.9`), <= 50,000 URLs and <= 50 MB uncompressed per file, listing only `200 OK` canonical HTTPS URLs (no `noindex`, redirects, or 4xx/5xx).
- **Canonicals & Index Directives:** Inspect server-rendered `<link rel="canonical">`, `<meta name="robots">`, and `X-Robots-Tag`. Verify canonicals point cleanly to final HTTPS URLs without conflicting with redirects or sitemaps.
- **HTTP, Redirects & Architecture:** Eliminate redirect chains (>1 hop) and loops; use `301`/`308` for permanent moves and `302`/`307` for temporary moves. Surface orphan pages, non-crawlable JS-only navigation (prefer `<a href>`), broken links, and duplicate URL/faceted parameter traps.

### Performance, Rendering & Core Web Vitals (75th Percentile)
- **Thresholds:** **LCP** <= 2.5 s | **INP** <= 200 ms (replaced FID) | **CLS** <= 0.1.
- Separate real-user **CrUX / PageSpeed Insights** field metrics from synthetic **Lighthouse** lab runs.
- Verify **mobile usability & parity** and **JavaScript rendering**: critical content, titles, meta descriptions, canonicals, and internal links should be present in initial SSR/SSG HTML. Optimize images (`width`/`height`, WebP/AVIF, `fetchpriority="high"` on LCP hero).

---

## 2. Framework Implementation Rules

Detect stack (`package.json`, `wp-config.php`, Shopify Liquid, HTML) before touching files:

### Next.js (App Router & Pages Router)
- **App Router:** Configure `metadataBase` in root `app/layout.tsx`. Use static `export const metadata: Metadata` or `export async function generateMetadata({ params })` (`await params` in Next.js 15+)—never export both in the same route file.
- Set `alternates.canonical`, `openGraph`, and `twitter` metadata cleanly per route; avoid duplicate `<title>` across routes or deprecated `next/head` inside `app/`.
- Implement `app/sitemap.ts` (`MetadataRoute.Sitemap`) using real production base URLs (never hardcoded `localhost` or fake `new Date()` for every page) and `app/robots.ts` (`MetadataRoute.Robots`).
- Embed JSON-LD via `<script type="application/ld+json">` escaping `<` as `\u003c`.
- Leverage SSG, ISR (`revalidate`), `next/image` (descriptive `alt` + dimensions), and crawlable `<Link href>` internal navigation.

### Static Websites & SPAs
- Maintain unique `<title>`, `<meta name="description">`, absolute `<link rel="canonical">`, `<html lang>`, `<meta name="viewport">`, Open Graph, JSON-LD, `sitemap.xml`, `robots.txt`, descriptive `alt` text, and logical heading hierarchy (`H1`–`H3`).
- For client-side React SPAs serving public SEO routes, recommend SSR/SSG/prerendering so crawlers receive full HTML without brittle JS execution delays.

### WordPress / Shopify / Headless CMS
- Respect existing themes, SEO plugins (Yoast/Rank Math/Shopify metafields), and publishing APIs—never inject duplicate `<meta>` or conflicting JSON-LD blocks alongside active SEO plugins.

---

## 3. Codebase Validation Safeguards

- Never change live URL slugs silently; require user approval and wire `301`/`308` redirects when URLs must move.
- Preserve accessibility (landmarks, contrast, alt attributes, semantic headings).
- Run production build (`npm run build` / framework equivalent) **and** `scripts/` validators (`run_technical_audit.py`, `audit_sitemap.py`, `audit_metadata.py`, `audit_links.py`, `validate_structured_data.py`) after edits.
