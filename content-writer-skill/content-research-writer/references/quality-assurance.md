# Content Quality Assurance, Approval Workflow & Optimization

Enforce rigorous editorial, factual, SEO, and engineering gates before any content leaves review, require unambiguous approval before publishing, and monitor live outcomes safely afterward.

## Part 1 — Four-Pillar Quality Assurance Checklist

Evaluate every draft explicitly across all four pillars in [../templates/content-review.md](../templates/content-review.md). **Present concrete defects and fixes directly—never bury issues behind an opaque numeric score.**

1. **Research Quality:** Primary reliable sources cited? Dates verified and current? Conflicting evidence handled honestly? Competitor insights differentiated rather than copied? Unconfirmed claims clearly flagged `[NEEDS SME VERIFICATION]`?
2. **Editorial Quality:** Natural human rhythm and verified brand voice? Strong relevant intro answering the core question? Real examples, concrete insights, and smooth transitions? Zero AI cliché filler, repetition, or unsupported superlatives? Useful conclusion/CTA?
3. **SEO Quality:** Search intent fully satisfied? Clear descriptive title, meta, H1, slug, and heading hierarchy? Real verified internal links and authoritative external sources? Contextual licensed images with descriptive alt text and dimensions? Zero cannibalization with existing URLs?
4. **Implementation Quality (Pre- & Post-Publish):** Renders cleanly in target template/DB? Images, links, canonicals, structured data, and sitemap verified? Indexable (`200 OK`, not `noindex` or blocked)? Zero build, console, or mobile-layout errors?

---

## Part 2 — Mandatory 5-Stage Review & Explicit Approval Gate

**NEVER auto-publish.** Every content item follows all five stages:

1. **Stage 1 — Prepare Complete Package:** Editorial brief + complete draft + SEO metadata + internal/external link plan + licensed image manifest + exact target file/DB destination and proposed URL.
2. **Stage 2 — Human-Readable Preview:** Show the **full text**, images/alt text, links, metadata, references, target URL, and exact code/DB changes via [../templates/approval-summary.md](../templates/approval-summary.md). Never hide major edits behind vague summaries.
3. **Stage 3 — Revision Loop:** Accept natural feedback (*"make it friendlier"*, *"simplify section 3"*, *"swap the featured image"*, *"add a concrete code example"*), regenerate cleanly, and display the updated preview.
4. **Stage 4 — Explicit Approval:** Proceed **only** upon unambiguous authorization for the **exact version** shown (e.g., *"Approve and publish"*, *"Publish this article"*, *"Approve changes"*).
   - Casual praise (*"looks good"*, *"nice job"*, *"makes sense"*) is **not** permission to publish—ask politely for explicit sign-off to publish.
   - Any substantive post-approval revision invalidates prior approval and requires fresh confirmation.
5. **Stage 5 — Publish & Verify:** Execute [database-publishing.md](database-publishing.md) or [static-site-publishing.md](static-site-publishing.md), then verify live rendering and discoverability.

---

## Part 3 — Post-Publication Performance & Refresh Rules

When authorized analytics (GSC, GA4, CMS metrics) are available:
- Track Impressions, Clicks, CTR, Average Position, Organic Sessions, Engagement, Conversions/Leads/Purchases, and Revenue.
- Spot refresh candidates: decaying traffic, stale specs/dates, low CTR despite high impressions, intent mismatch, missing internal links, or newly emerging customer questions.
- **Protect winners:** Never rewrite high-ranking, high-converting content blindly without analytics evidence; preserve URL slugs (`301` only when consolidation/URL change is genuinely required and approved) and preserve version/change history.
