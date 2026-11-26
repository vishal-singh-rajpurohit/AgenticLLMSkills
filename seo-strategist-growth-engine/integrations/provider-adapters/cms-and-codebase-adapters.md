# CMS & Codebase Implementation Adapters

Inspect repository architecture and CMS workflows before implementing any SEO changes. Preserve existing frameworks, routing, plugins, and URLs.

---

## 1. Stack Detection Matrix

| Detected Stack | Key Files Inspected | SEO Implementation Mechanism |
|---|---|---|
| **Next.js App Router** | `package.json`, `app/layout.tsx`, `app/**/page.tsx`, `app/sitemap.ts`, `app/robots.ts` | `metadataBase`, `Metadata` / `async generateMetadata({ params })` (`await params` in Next.js 15+), `MetadataRoute.Sitemap`, `MetadataRoute.Robots`, `<Image>`, escaped JSON-LD (`\u003c`). |
| **Next.js Pages Router** | `pages/_app.tsx`, `pages/**/*.tsx`, `next.config.*` | `next/head` or shared SEO component, `getStaticProps`/`getServerSideProps` metadata, dynamic `sitemap.xml` route or `next-sitemap`. |
| **React SPA (Vite / CRA)** | `index.html`, `src/App.*`, `package.json` | Recommend pre-rendering/SSG/SSR migration for SEO pages; verify static HTML shell, meta/canonical injection risks, and crawlable `<a href>` links. |
| **Astro / Nuxt / SvelteKit** | `astro.config.*`, `nuxt.config.*`, `src/routes/**` | Framework head/SEO composables (`@astrojs/sitemap`, `useSeoMeta`, `<svelte:head>`), SSR output verification. |
| **Static HTML** | `*.html`, `robots.txt`, `sitemap.xml` | Direct `<title>`, `<meta name="description">`, `<link rel="canonical">`, headings, Open Graph, JSON-LD, `alt`, `sitemap.xml`. |
| **WordPress** | `wp-config.php`, theme files, Yoast / Rank Math / WP REST API | Edit via existing SEO plugin fields/REST endpoints—never inject duplicate `<title>`, canonical, or schema tags from theme templates alongside active SEO plugins. |
| **Shopify** | `layout/theme.liquid`, `templates/*.json`, Shopify Admin API | Use native metafields, `canonical_url`, `page_title`, `page_description`, and theme JSON-LD carefully without duplicating built-in Shopify schema. |

---

## 2. Pre- and Post-Edit Verification

1. Run `python scripts/technical-seo-audit/run_technical_audit.py <repo-path>` before editing to establish technical baseline.
2. Obtain explicit user approval before changing live URLs, configuring `301`/`308` redirect maps, or writing production CMS entries.
3. Run production build (`npm run build` or equivalent) and re-run `scripts/` validators (`audit_metadata.py`, `audit_sitemap.py`, `audit_links.py`, `validate_structured_data.py`).
