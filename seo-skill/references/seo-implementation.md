# Codebase SEO Implementation Guide

When operating inside a repository, do not stop at prose recommendations—inspect the real stack, propose concrete changes, obtain approval where required, implement cleanly, and validate with tests/scripts.

## Step 1 — Repository Discovery Checklist

Before editing any code, detect and document:
1. **Framework & exact version:** Check `package.json` (`next`, `react`, `astro`, `nuxt`, `@sveltejs/kit`, `@angular/core`), `composer.json` / `wp-config.php`, or static HTML build setup.
2. **Rendering strategy:** SSR, SSG, ISR, hybrid App/Pages Router, or client-only SPA (CSR).
3. **Routing & dynamic routes:** `app/` directory, `pages/` directory, dynamic segments (`[slug]`, `[...slug]`), route groups, middleware, `next.config.*` rewrites/redirects/trailingSlash.
4. **Existing SEO implementation:** Root metadata, per-route `generateMetadata` / `<Head>`, existing `sitemap.*`, `robots.*`, JSON-LD components, OG tags, image components (`next/image`, `@astrojs/image`), analytics scripts, CMS data sources.

---

## Step 2 — Framework-Specific Implementation Patterns

### Next.js App Router (`app/` — Next.js 13.3+ / 14 / 15 / 16+)
- **Do not** hand-inject `<title>` or `<meta>` with `next/head` in App Router. Use the official **Metadata API**:
  - Static routes: `export const metadata: Metadata = { ... }` in `page.tsx` or layout defaults (`metadataBase`, `title.template`).
  - Dynamic routes (`app/products/[slug]/page.tsx`): `export async function generateMetadata({ params }): Promise<Metadata>` fetching actual product/post data! Note: in Next.js 15+, `params` and `searchParams` are Promises (`await params`).
  - Never export both static `metadata` and `generateMetadata` in the same file.
  - Set `metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "https://example.com")` in root `app/layout.tsx` and set route-specific `alternates: { canonical: ... }` cleanly.
- **Sitemaps & Robots:** Use file conventions `app/sitemap.ts` (`MetadataRoute.Sitemap`) and `app/robots.ts` (`MetadataRoute.Robots`), keeping dynamic DB/CMS fetches cleanly handled and listing only canonical, indexable URLs.
- **JSON-LD:** Render sanitized `<script type="application/ld+json">` inside Server Components using `JSON.stringify(schema).replace(/</g, '\\u003c')` to prevent XSS.

### Next.js Pages Router (`pages/`)
- Use `next/head` inside page components (or a shared `<SeoHead />` wrapper receiving page-specific title, description, canonical, robots, OG, and JSON-LD props).
- Implement dynamic `/sitemap.xml` via `pages/sitemap.xml.ts` (`getServerSideProps` writing `application/xml` headers) or `next-sitemap` if already configured—avoid adding redundant packages if simple native generation suffices.

### Client-Side React SPAs (Vite / CRA)
- Flag clearly to the user: client-only rendering delays or weakens metadata/OG previews for crawlers and social scrapers that do not execute JS.
- Short-term improvements: `react-helmet-async` (or React 19 native `<title>`/`<meta>` hoisting), static `robots.txt` + build-time `sitemap.xml` generation.
- Strategic recommendation: migrate public marketing/content routes to SSR/SSG (Next.js, Astro, or pre-rendering) where organic search is a primary channel.

### Astro / Nuxt / SvelteKit / Angular / WordPress / Static HTML
- **Astro:** Shared `<BaseHead.astro>` layout props, `@astrojs/sitemap` (or custom `src/pages/sitemap.xml.ts`), `public/robots.txt`, image optimization via `astro:assets`.
- **Nuxt 3+:** `useSeoMeta()` / `useServerSeoMeta()`, `definePageMeta()`, `useHead()` for canonical & JSON-LD, Nitro server routes or `@nuxtjs/sitemap`.
- **SvelteKit:** Load route SEO data in `+page.ts`/`+page.server.ts`, render inside `<svelte:head>` in `+page.svelte`, generate `/sitemap.xml` via `+server.ts`.
- **Angular:** `Title` & `Meta` services in SSR/hydration (`@angular/ssr`) routes, canonical link injection via `DOCUMENT` token, static/server `sitemap.xml` & `robots.txt`.
- **WordPress:** Inspect active SEO plugin (Yoast SEO, Rank Math, SEOPress) and theme templates **before** adding custom hooks/meta tags—never output duplicate `<title>`, `<meta description>`, canonicals, or conflicting Schema graphs!
- **Static HTML:** Clean semantic `<head>` tags per HTML file, consistent `<html lang="...">`, static `sitemap.xml` & `robots.txt`.

---

## Step 3 — Mandatory Safeguards & Approval Gates

- **Never** ship one static title/description string for every dynamic URL.
- **Reuse** existing data fetching, validation, and layout abstractions—do not invent unnecessary dependencies or overwrite existing features.
- **Never** expose API keys, secrets, internal admin paths, or staging domains in `robots.txt` / sitemaps / public metadata.
- **Obtain explicit user approval BEFORE:**
  - Changing URL structures or route slugs on a live site.
  - Implementing mass `301`/`308` redirects or deleting routes.
  - Changing canonical base domains (`www` vs apex) or `noindex` rules on revenue-generating templates.
  - Modifying hosting, DNS, CDN, or deploying/publishing changes.

---

## Step 4 — Post-Edit Verification

After any codebase change:
1. Run existing project checks/builds/tests (`npm run build`, `npm test`, typecheck, lint) if available.
2. Run local validation scripts (`scripts/metadata-check/check_metadata.py`, `scripts/sitemap-validation/validate_sitemap.py`, `scripts/structured-data-validation/validate_jsonld.py`, `scripts/broken-link-check/check_links.py`) on source or built output.
3. Report **exactly** what was modified, what was tested and passed, and what still requires deployment/live Search Console verification. Never blur "recommended", "proposed", and "completed" changes.
