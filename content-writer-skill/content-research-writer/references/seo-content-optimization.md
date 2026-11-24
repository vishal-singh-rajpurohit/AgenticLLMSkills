# SEO Content Optimization & Metadata Standards

Integrate search discoverability cleanly into genuinely useful content—never at the cost of readability or honesty.

## Search Intent Verification

Match the piece to what searchers actually want next:
- **Informational:** Learn concept or solve problem cleanly.
- **Navigational:** Reach official brand resource or docs.
- **Commercial Investigation:** Evaluate options, trade-offs, pricing, or reviews.
- **Transactional:** Purchase, request quote, book demo, or sign up.
- **Local Service:** Find qualified provider in a specific city/area.
- **Support / Troubleshooting:** Diagnose and fix a concrete error or issue.

---

## Metadata Generation Standards

Prepare complete metadata in every content package:
- **SEO Title (`<title>`):** Clear, unique, descriptive of actual page content; place the core topic naturally near the front. Do not enforce rigid arbitrary character cutoffs—prioritize clarity and scannability.
- **Meta Description:** Accurate, compelling summary of what the reader gets and why it helps.
- **Page `<h1>`:** Clear primary headline matching the user's expectation (aligned with `<title>`, not stuffed).
- **URL Slug:** Short, lowercase, hyphenated, evergreen (avoid embedding brittle years inside URLs for evergreen guides).
- **Primary Topic & Supporting Terms:** Reflect natural buyer vocabulary rather than mechanical density targets.
- **Canonical URL:** Self-referencing canonical (or explicit cross-canonical if syndicating/consolidating).
- **Open Graph (`og:title`, `og:description`, `og:image`, `og:type`):** Accurate share metadata matching page visuals.
- **Robots Directives:** Default indexable (`index, follow`) for public pages; never publish accidental `noindex`.
- **Structured Data Recommendation:** Match visible page reality (`Article` / `BlogPosting`, `BreadcrumbList`, `Product`, `Organization`, `Person`).
- **Author & Dates:** Real verified author/organization and accurate `publishedAt` / `updatedAt` timestamps.

### Google Display Reality Disclosure
Google automatically generates and may rewrite search **title links** (drawing from `<title>`, `<h1>`, prominent headings, or anchor context) and **snippets** (primarily dynamically extracted from page content matching the query, using meta description when helpful). Present metadata as **strong signals**, never as guaranteed SERP appearance.

---

## Structural Optimization

- Use one `<h1>` per page and valid sequential `<h2>` -> `<h3>` hierarchy without skipping levels.
- Lead with clear answers, scannable lists, comparison `<table>`s where decision criteria span multiple options, concise FAQs when genuinely helpful (without assuming retired `FAQPage` SERP accordions), next-step CTAs, and cited references.
- Use descriptive, natural phrasing in headings—never cram the target keyword into every `<h2>`.
