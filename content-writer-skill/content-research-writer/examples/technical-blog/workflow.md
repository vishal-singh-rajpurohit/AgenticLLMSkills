# Worked Example: Static Next.js MDX Blog Implementation (Test 4)

*(Demonstrates repo inspection, version detection, MDX file creation, local WebP image integration, listing/sitemap updates, and build validation.)*

---

## 1. Repository Inspection Output

- **Framework:** Next.js `15.x` App Router (`package.json`) using local MDX files under `content/blog/*.mdx`.
- **Existing Route:** `app/blog/[slug]/page.tsx` reads MDX frontmatter (`title`, `description`, `publishedAt`, `author`, `coverImage`, `category`) and exports `generateMetadata`.
- **Listing & Sitemap:** `app/blog/page.tsx` dynamically reads `content/blog/`, and `app/sitemap.ts` iterates all blog slugs automatically.

## 2. Preview & Approval Gate

- Presented full MDX article, verified external references, `public/images/nextjs-app-router-caching-flow.webp` asset manifest (`1200x630`, original diagram), `generateMetadata` compatibility check, and internal links to existing `/docs/deployment` and `/blog/server-actions-guide`.
- Held file creation until user explicitly typed: **"Approve and publish"**.

## 3. Static Implementation & Verification

1. Wrote `public/images/nextjs-app-router-caching-flow.webp`.
2. Created `content/blog/on-demand-revalidation-nextjs-app-router.mdx` matching the exact repository frontmatter schema.
3. Added 1 contextual internal link from existing `content/blog/server-actions-guide.mdx` (preserving git history and existing text).
4. Executed:
   - `python scripts/validate-content/validate_content.py content/blog/on-demand-revalidation-nextjs-app-router.mdx`
   - `python scripts/validate-links/validate_links.py content/blog/on-demand-revalidation-nextjs-app-router.mdx --repo .`
   - `python scripts/validate-images/validate_images.py content/blog/on-demand-revalidation-nextjs-app-router.mdx --repo .`
   - `npm run build` (confirming clean static/SSR build and `/sitemap.xml` output).
