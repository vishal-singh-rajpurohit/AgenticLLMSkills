# Search Appearance & Index Discoverability

Publishing is incomplete until search engines can cleanly crawl, render, interpret, and discover the new or updated URL.

## Search Appearance Optimization

Ensure every published piece exposes coherent on-page and machine-readable signals:
- Clear `<title>`, `<meta name="description">`, single `<h1>`, logical `<h2>`/`<h3>` hierarchy, descriptive slug, and Open Graph tags.
- **Relevant Schema.org JSON-LD** reflecting **only** real, visible page content:
  - Editorial content: `Article` or `BlogPosting` (`headline`, `description`, `image`, `datePublished`, `dateModified`, real `author` `Person`/`Organization`, `publisher`).
  - Navigation hierarchy: `BreadcrumbList`.
  - Brand identity: `Organization`.
  - Product/commerce pages: `Product` + `Offer` (verified price/currency/availability; `aggregateRating` only when genuine on-page SKU reviews exist).
- **No deprecated rich-result promises:** Do not implement `HowTo` or `FAQPage` markup expecting Search SERP rich cards (Google deprecated HowTo rich results and retired FAQ rich results across all sites in 2026).

---

## Post-Publication Index Discoverability Checklist

Verify every item after publishing (using `scripts/validate-sitemap/`, `scripts/validate-metadata/`, `scripts/validate-links/`, and `scripts/validate-structured-data/`):
1. Target URL returns `200 OK` (no unexpected redirect chains or 404/500 errors) and primary text renders in HTML.
2. No accidental `<meta name="robots" content="noindex">` or `X-Robots-Tag: noindex`.
3. `robots.txt` does **not** disallow the new URL path or required CSS/JS/image assets, and cleanly references the XML sitemap.
4. `rel="canonical"` points to the exact preferred HTTPS canonical URL.
5. XML sitemap lists the new URL and updates `<lastmod>` accurately (staying within Google's 50,000 URL / 50 MB limits).
6. At least 1–3 relevant existing pages on the site link internally to the new URL with crawlable `<a href>` anchors.

---

## Google Search Console & Indexing API Boundaries

- **If authorized GSC access is connected:** Run URL Inspection, inspect live crawlability/canonical selection, verify sitemap processing, and optionally request indexing via Search Console URL Inspection UI/tools when appropriate.
- **Google Indexing API strict policy:** Google's Indexing API is **only** permitted for pages containing `JobPosting` or `BroadcastEvent` embedded in `VideoObject`. **Never** recommend or call the Google Indexing API for ordinary blog posts, guides, category pages, or service pages.
- **No guarantees:** Never claim a page *"is indexed"* without inspecting live search/GSC evidence, and never promise specific rankings, traffic levels, or indexing timelines.
