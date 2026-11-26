# Structured Data & Search Appearance

Implement Schema.org JSON-LD accurately to clarify entity identity and establish rich-result **eligibility**—never fabricate properties or promise SERP features.

## Supported Schema.org Types

Use only types describing **real, visible content** on that exact URL, preferring the most specific accurate type and linking entities via stable `@id` values (e.g., `https://example.com/#organization`):

- **`Organization`:** `name`, canonical `url`, crawlable `logo`, stable `@id`, verified `sameAs` profiles.
- **`LocalBusiness`** (or specific subtype like `ProfessionalService`, `HomeAndConstructionBusiness`): `name`, visible `address` or `areaServed`, `telephone`, `openingHoursSpecification`, unique `@id` per distinct physical location.
- **`Product`:** `name`, `image`, `description`, `sku`/`brand`, `offers` (`price`, `priceCurrency`, `availability`, `url`). Add `aggregateRating`/`review` **only** when genuine, visible product reviews exist on that exact page (respect Google self-serving review restrictions).
- **`Article` / `BlogPosting` / `NewsArticle`:** `headline`, `image`, truthful `datePublished` and `dateModified` (never fake fresh dates without substantive edits), real `author` (`Person`/`Organization`), and `publisher` linked to `@id`.
- **`BreadcrumbList`:** `itemListElement` matching visible page breadcrumb hierarchy.
- **`Service` / `SoftwareApplication`:** Visible service scope/provider/areaServed or app `operatingSystem`, `applicationCategory`, and accurate `offers`.
- **`VideoObject`:** `name`, `description`, crawlable `thumbnailUrl`, `uploadDate`, `contentUrl`/`embedUrl` when video is primary watchable content.

---

## Current Eligibility & Honesty Guardrails

- **Discontinued/Deprecated Rich Results:** Do **not** pitch `HowTo` (deprecated) or `FAQPage` (discontinued for rich SERP accordions across all sites in May 2026) as rich-result growth tactics. Clean visible Q&A UX remains fine for users.
- **Zero Fabrication:** Never invent star ratings, review counts, prices, stock levels, fake authors, or fictitious physical addresses.
- **Validation Workflow:** Escape `<` as `\u003c` inside React/Next.js inline JSON-LD scripts, validate syntax/rules via `scripts/structured-data-validation/validate_structured_data.py`, and confirm rendered DOM output in Google's Rich Results Test and Schema Markup Validator.
