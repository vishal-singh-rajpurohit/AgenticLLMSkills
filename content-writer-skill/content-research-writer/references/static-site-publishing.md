# Static & Source-Code Website Publishing

When content lives in source control (Markdown, MDX, TypeScript/JSON collections, HTML, or static site generators), follow the repository's existing templates, routing, and build conventions cleanly.

## Supported Stacks & Inspection Checklist

Inspect the codebase before drafting the implementation plan:
- **Frameworks:** Next.js (App Router & Pages Router), Astro, Gatsby, Nuxt/Vue, SvelteKit, React, Hugo/Eleventy/Jekyll, or standard HTML.
- **Files & Conventions to Inspect:**
  1. `package.json` (framework version & MDX/content libraries like `@next/mdx`, `contentlayer`, `velite`, `astro:content`, `gray-matter`).
  2. Content directory & frontmatter schema (e.g., `content/blog/*.mdx`, `src/content/blog/*.md`, `data/posts.ts`, `pages/blog/*.html`).
  3. Shared article/service layout templates and MDX custom components.
  4. Metadata generation (`export const metadata`, `generateMetadata`, `<BaseHead.astro>`, `useSeoMeta`, `<svelte:head>`).
  5. Listing/index pages, category/tag archives, pagination, navigation menus, and RSS/Atom feeds.
  6. `sitemap.ts`/`sitemap.xml` and `robots.ts`/`robots.txt`.
  7. Image directory (`public/images/`, `src/assets/`) and image component conventions (`next/image`, `astro:assets`).

---

## Implementation Rules

1. **Wait for explicit user approval** on the exact final preview before writing or editing files.
2. **Use the existing content mechanism.** Never install a heavy CMS or rewrite routing just to add an article or service page.
3. **Reuse existing page templates** instead of duplicating layout JSX/HTML across articles.
4. **Never redesign unrelated pages** or overwrite existing articles without reviewing `git log` / file diff and obtaining approval.
5. **Keep assets local and permanent:** Save approved images inside the existing `public/` or `assets/` structure with descriptive filenames, proper dimensions, and alt text—never temporary external links.

---

## Step-by-Step Static Publication Sequence

After explicit approval:
1. Place approved visual assets into the project's image folder (`public/images/...` or `src/assets/...`).
2. Create (or update) the content file (`.mdx`, `.md`, `.ts`, `.json`, `.html`) following the repository's exact frontmatter schema.
3. Populate complete SEO metadata, canonical URL, Open Graph metadata, author, and accurate dates.
4. Add approved internal links from relevant existing pages (inspecting git/file state before editing) and update listing/category/RSS integrations if manual rather than filesystem-driven.
5. Verify sitemap generation includes the new canonical URL (update `sitemap.ts` / static `sitemap.xml` if needed).
6. Run the project's **typecheck, lint, and production build** (`npm run build` / `astro check` / etc.) plus `scripts/` validators (`validate_content.py`, `validate_metadata.py`, `validate_links.py`, `validate_images.py`, `validate_sitemap.py`).
7. Report exact modified/created files and verification output in [../templates/publication-report.md](../templates/publication-report.md).
