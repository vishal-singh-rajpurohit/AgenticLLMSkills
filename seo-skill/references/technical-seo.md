# Technical SEO Audit Handbook

Inspect actual live pages, server responses, and repository source code before reporting defects. Ground every severity rating in real crawlability, indexability, rendering, performance, or user-experience evidence.

## Authoritative Baseline References

Verify changing engine policies against primary sources when in doubt:
- **Google Search Essentials & Spam Policies:** `https://developers.google.com/search/docs/essentials`
- **Google Crawling & Indexing:** `https://developers.google.com/search/docs/crawling-indexing`
- **Google Structured Data Search Gallery:** `https://developers.google.com/search/docs/appearance/structured-data/search-gallery`
- **Core Web Vitals (web.dev):** `https://web.dev/articles/vitals`
- **Bing Webmaster Guidelines:** `https://www.bing.com/webmasters/help/webmasters-guidelines`

---

## Audit Modules

### 1. Crawlability & Indexing
- **`robots.txt`:** Verify HTTP 200 (or intentional absence), valid directives, and confirm critical JS, CSS, image assets, and money pages are **not** accidentally disallowed. Remember: `robots.txt` blocks crawling, not guaranteed deindexing if external links exist—use `noindex` (while leaving the URL crawlable) to deindex.
- **XML Sitemaps:** Check validity, `<urlset>`/`<sitemapindex>` schema, max 50,000 URLs and 50 MB uncompressed per sitemap file, absolute canonical HTTPS URLs only (no 3xx/4xx/5xx or `noindex` URLs), accurate `<lastmod>` dates (only update when content meaningfully changes), and discovery in `robots.txt` / Search Console.
- **Indexability & Directives:** Inspect `<meta name="robots">` and `X-Robots-Tag` HTTP headers across templates and staging/preview deployments (prevent staging sites from indexing; ensure production money pages do not carry accidental `noindex`).
- **Canonicalization:** Verify self-referencing `rel="canonical"` on indexable pages, consistent host (`www` vs apex) and trailing slash convention, HTTP->HTTPS redirection, and no canonical pointing to 4xx/3xx or wrong pages. Prefer HTML `<link rel="canonical">` in initial server HTML rather than injecting canonicals via client-side JavaScript.
- **HTTP Status & Redirects:** Check for redirect chains (>1 hop), redirect loops, internal links hitting 301/302s instead of final canonical URLs, accidental 302s on permanent moves (use 301/308 for permanent, 302/307 for genuine temporary moves), and 4xx/5xx errors on linked pages. Intentional 404/410 is valid for permanently removed content with no replacement.
- **Orphan Pages & Crawl Depth:** Important commercial/content pages should be reachable via crawlable `<a href="...">` links (not only JS `onClick` handlers) within 3–4 clicks of the homepage.
- **JavaScript Rendering:** Google crawls raw HTML first, queues JS rendering in Chromium, then indexes rendered DOM. Verify titles, meta descriptions, canonicals, primary copy, and internal links exist in server-rendered/static HTML (SSR/SSG/ISR) rather than client-only rendering where possible. Never depend on click/scroll events to load primary indexable content.
- **Pagination:** Ensure paginated series use clean, crawlable URLs (`?page=2` or `/page/2`) with self-referencing canonicals (do **not** canonicalize page 2+ back to page 1; note Google deprecated `rel="prev"/"next"` as an indexing signal).

### 2. Website Architecture & URL Hygiene
- Clean, descriptive, lowercase hyphenated URL slugs; avoid session IDs, redundant uppercase variants, or uncontrolled query parameters creating infinite duplicate crawl traps.
- Clear hierarchical navigation and `<nav aria-label="Breadcrumb">` matching `BreadcrumbList` schema.
- Check for duplicate or near-duplicate landing pages competing for the same intent.

### 3. Core Web Vitals & Performance
Use real-user **CrUX / PageSpeed Insights field data** (75th percentile) first, and clearly distinguish it from synthetic **Lighthouse lab runs**:

| Metric | Good | Needs Improvement | Poor | What It Measures |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | <= 2.5 s | > 2.5 s to 4.0 s | > 4.0 s | Loading speed of primary viewport content |
| **INP** (Interaction to Next Paint) | <= 200 ms | > 200 ms to 500 ms | > 500 ms | Overall responsiveness (replaced FID as stable CWV) |
| **CLS** (Cumulative Layout Shift) | <= 0.1 | > 0.1 to 0.25 | > 0.25 | Visual layout stability |

Audit causes from real diagnostics—never guess from scores alone:
- Image sizing, modern formats (WebP/AVIF), `fetchpriority="high"` on hero LCP image (and **never** `loading="lazy"` on the LCP image!).
- Explicit `width`/`height` or aspect-ratio CSS on images/ads/embeds to prevent CLS.
- Render-blocking CSS/JS, third-party tag bloat, unoptimized web fonts (`font-display: swap`), and long main-thread tasks hurting INP.
- Valid HTTPS everywhere, zero mixed content, strong mobile viewport (`<meta name="viewport" content="width=device-width, initial-scale=1">`).
- Note: A 100/100 Lighthouse score does **not** guarantee higher search rankings.

### 4. Mobile-First Parity & HTML Metadata
Because Google uses mobile-first indexing, verify mobile and desktop expose equivalent:
- Primary content, headings (`<h1>` once per page, logical `<h2>`–`<h3>`), and internal links.
- `<title>`, `<meta name="description">`, `robots`, `rel="canonical"`, `hreflang` (when multilingual/multiregional, always reciprocal + `x-default`), `<html lang="...">`.
- Open Graph (`og:title`, `og:description`, `og:url`, `og:image`) and descriptive `alt` attributes on meaningful images.

### 5. Structured Data & Current Rich-Result Eligibility
Validate JSON-LD syntax, required/recommended properties, and policy compliance:
- **Core active types:** `Organization`, `LocalBusiness`, `Product` (Product Snippets & Merchant Listings), `Article` / `NewsArticle` / `BlogPosting`, `BreadcrumbList`, `Event`, `ProfilePage`, `DiscussionForumPosting`.
- **Deprecated rich results (do not promise SERP cards):**
  - `HowTo` rich results were deprecated by Google.
  - `FAQPage` rich results were discontinued in Google Search across all sites in 2026 (documentation and Search Console reporting retired; only retain clean Q&A HTML/schema if genuinely helpful for structured entity clarity, never to chase FAQ accordions).
- **Strict honesty rule:** Markup must accurately reflect visible page content. Never add fabricated ratings, reviews, authors, prices, stock statuses, or local addresses. Valid schema enables eligibility; it never guarantees rich results.

---

## Severity Grading & Output Format

| Severity | Definition & Examples |
|---|---|
| **Critical** | Blocks indexing/crawling or breaks site revenue/access (production `noindex`, `robots.txt` blocking site, 5xx on core templates, broken canonical pointing all pages to homepage) |
| **High** | Major ranking, crawl-budget, or UX damage across templates (CSR-only missing metadata, broken XML sitemap, high-traffic 404s, severe CWV failure on key landing pages, duplicate titles across all dynamic routes) |
| **Medium** | Significant single-page or secondary optimization gap (redirect chains in nav, missing `BreadcrumbList` or `Product` schema, unoptimized images, suboptimal H1 hierarchy) |
| **Low** | Minor hygiene issue with modest impact (missing OG image on blog archive, minor meta description length tweaks, non-critical external 404s) |
| **Informational** | Verified healthy state, architecture observation, or non-defect note (intentional `noindex` on `/cart` or `/search`) |

Write audit deliverables using [../templates/technical-audit.md](../templates/technical-audit.md) with the exact columns:

`| Issue | Severity | Affected URLs | Evidence | Recommended Fix |`
