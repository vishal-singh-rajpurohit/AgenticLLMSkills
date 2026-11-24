# Database & CMS Publishing Architecture

Use the website's **existing** database schema, ORM, CMS API, authentication model, media adapter, and caching hooks—never build a rogue schema or bypass application safeguards.

## Step 1 — Repository & CMS Investigation

Before proposing how content will be stored or published, inspect:
1. **ORM / Database / Headless CMS:** Check `package.json`, `prisma/schema.prisma`, Drizzle schema files, Mongoose models, SQL migrations, or CMS SDKs (`@sanity/client`, `@strapi`, `@directus/sdk`, WordPress REST/WP-CLI, Payload, Contentful).
2. **Existing Content Models:** Inspect actual table/collection names and columns. Never assume a table is named `Post`, `Article`, or `Blog`—discover the real field names (`slug`, `status`, `publishedAt`, `seoTitle`, `metaDescription`, `authorId`, `categoryId`, `body`/`contentJson`).
3. **Publishing Workflow & Draft States:** Check how drafts vs. published records work (e.g., `status: "DRAFT" | "PUBLISHED"`, Sanity draft IDs, Strapi `publishedAt`, WordPress `post_status`).
4. **Media Storage Adapter:** Check how images upload and bind (S3/R2/Cloudinary/Vercel Blob/CMS upload endpoint + media table relations).
5. **Auth, API Contracts & Admin Flows:** Check existing server actions, REST/GraphQL endpoints, input validation (`zod`, etc.), and auth checks. Never use hardcoded production DB credentials or bypass auth checks.
6. **Caching & On-Demand Revalidation:** Inspect ISR/caching (`revalidatePath`, `revalidateTag`, `cacheTag`, CDN purge webhooks).

---

## Step 2 — Publishing & Data Safeguards

- **Wait for explicit user approval** on the exact previewed version before running any insert, update, or publish mutation.
- **Validate before saving:** Enforce unique `slug`, required foreign keys (`authorId`, `categoryId`), clean content serialization (Markdown/HTML/Portable Text/Lexical), and valid image URLs/asset IDs.
- **Prevent silent overwrites:** Query by `slug` / `id` first. When updating an existing record, show a before-and-after diff and preserve prior revisions/history where supported.
- **Use transactions** when creating multi-table records (e.g., post + tag joins + SEO metadata + media relation).
- **Schema migrations require explicit separate approval:** If an existing model lacks needed SEO fields or no content model exists yet, explain the exact proposed migration and get sign-off before altering database schemas.

### Representative Field Mapping (Adapt to Existing Schema Only)
Typical fields to map onto the target system's actual columns:
`id`, `title`, `slug`, `excerpt`, `content` / `content_format`, `featured_image`, `seo_title`, `meta_description`, `canonical_url`, `open_graph_data`, `structured_data`, `references`, `category_id`, `author_id`, `status` (`research` -> `draft` -> `review` -> `approved` -> `published` -> `archived`), `content_version`, `published_at`, `updated_at`.

---

## Step 3 — Cache Revalidation & Post-Publish Verification

Only **after** a successful database/CMS write:
1. Trigger existing revalidation hooks where used by the framework:
   - Next.js App Router: `revalidatePath('/blog/[slug]', 'page')`, `revalidatePath('/blog')`, or `revalidateTag('posts')` via the authorized route/action.
   - CMS webhooks / CDN purge if configured.
2. Fetch and verify the persisted record and live rendered route:
   - Confirm title, slug, status (`published`), author, categories, body formatting, images, SEO metadata, structured data, and public `200 OK` response.
3. Log exact record ID, status, public URL, and verification results in [../templates/publication-report.md](../templates/publication-report.md).
