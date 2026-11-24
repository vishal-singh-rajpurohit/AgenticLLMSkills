# Worked Example: E-Commerce Electronics & CCTV Store (Test 2 — Database Publishing)

*(Demonstrates verified specification writing, original product imagery, internal category cross-linking, and database-backed CMS publishing.)*

---

## 1. Repository & Database Discovery

Inspected project architecture (`package.json`, `prisma/schema.prisma`, `src/lib/media.ts`):
- **ORM:** Prisma (`Product`, `Category`, `MediaAsset`, `PublishStatus` enum: `DRAFT | REVIEW | PUBLISHED`).
- **Media Storage:** Existing S3 upload service (`uploadProductMedia()`), storing `url`, `altText`, `width`, `height`, and `attribution`.
- **Cache Layer:** Next.js App Router `revalidatePath('/products/[slug]', 'page')` and `revalidateTag('products')`.

---

## 2. Verified Product & Category Copy Principles

- **Specs verified against official datasheet only:** Camera sensor resolution (`4MP 2560x1440`), PoE standard (`802.3af`), ingress rating (`IP67`), storage compression (`H.265+`). Never invent night-vision distance or warranty years absent from official documentation.
- **Buyer Questions Answered:**
  - Will this work with an existing 8-channel ONVIF NVR?
  - Outdoor weather durability during monsoon heat/rain.
  - Clear comparison table vs. standard 2MP analog cameras.
- **Internal Cross-Links (Verified DB Slugs):**
  - Category: `/categories/poe-ip-cameras` (*"explore all 4MP PoE IP cameras"*)
  - Complementary product: `/products/8-channel-poe-nvr-recorder` (*"compatible 8-channel PoE NVR"*)
- **Image Assets:** Original vendor product images uploaded via `uploadProductMedia()` (never hotlinked from external supplier domains).

---

## 3. Database Publication Sequence (Post-Approval Only)

1. User confirms **"Approve and publish"** after viewing full product description, metadata, specs, image manifest, and JSON-LD preview.
2. Run existing Prisma transaction creating/updating the `Product` record (`status: "PUBLISHED"`), connecting existing `Category` and `MediaAsset` IDs, validating unique `slug`.
3. Trigger `revalidatePath('/products/<slug>')` and `revalidateTag('products')`.
4. Fetch persisted record and verify public URL HTTP `200`, `Product` + `Offer` JSON-LD, and XML sitemap inclusion.
