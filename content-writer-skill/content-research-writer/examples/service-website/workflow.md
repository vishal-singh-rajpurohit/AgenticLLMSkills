# Worked Example: Existing Article Optimization & Refresh (Test 6)

*(Demonstrates inspecting an existing outdated article, preserving URL & valuable sections, researching current standards, presenting a before-and-after diff, and awaiting approval.)*

---

## 1. Existing Page Audit

- **Inspected File:** `content/blog/google-rich-results-checklist-2023.mdx` (live URL `/blog/google-rich-results-checklist-2023`).
- **What Still Works:** Clear explanation of `Article`, `Product`, and `Organization` JSON-LD plus helpful `next/script` XSS escaping snippet (`replace(/</g, '\\u003c')`). Keep intact!
- **Outdated / Incorrect Claims Found:**
  1. Recommends implementing `HowTo` and `FAQPage` markup to win Google Search accordion rich results (HowTo rich results deprecated; FAQ rich results retired across all sites in 2026).
  2. References FID (`First Input Delay`) instead of `INP` (`Interaction to Next Paint`) for Core Web Vitals.
  3. Points to a broken external link (`404`) and omits `updatedAt` timestamp.

---

## 2. Before-and-After Revision Strategy

- **Preserve URL Slug & Equity:** Keep the exact existing path (`/blog/google-rich-results-checklist-2023`)—**never** break incoming links by renaming the slug silently! Update visible title/H1 (`Google Rich Results & Structured Data Checklist (Updated)`), `updatedAt`, and `<lastmod>` in sitemap.
- **Present Before/After Diff Preview:** Highlight exactly which paragraphs/tables change, cite updated Google Search Central documentation URLs, and wait for explicit approval (`"Approve changes"`) before editing the file.
- **Post-Edit Validation:** Re-run `validate_content.py`, `validate_links.py`, `validate_metadata.py`, and production build checks.
