# SEO Content Research, Writing & Refresh Workflow

Deliver genuinely useful, human-edited content tailored to buyer intent and verified sources—never keyword-stuffed filler or generic AI boilerplate.

## Integration with `content-research-writer`

If the sibling **`content-research-writer`** skill (`content-writer-skill/content-research-writer/` or installed in the active agent's skill directory) is available, hand off deep drafting, image-license checks, full human preview, approval gates, and CMS/static publishing via [../integrations/provider-adapters/content-research-writer-bridge.md](../integrations/provider-adapters/content-research-writer-bridge.md).

---

## Built-In 9-Step Content Creation Workflow

1. Identify target keyword cluster and confirm primary + secondary search intents.
2. Research primary, authoritative sources and record citations with access dates.
3. Analyze competing SERP pages to spot information gaps (never copy or spin).
4. Confirm target buyer segment, technical level, and primary conversion goal.
5. Choose optimal content format and draft an outline via [../templates/content-brief.md](../templates/content-brief.md).
6. Write humanized, natural prose answering the reader's core question first.
7. Include complete deliverable package where appropriate:
   - SEO title, meta description, clean URL slug, single `H1`, logical `H2`/`H3` hierarchy
   - Introduction, main content, relevant real examples, evidence & external citations
   - Verified internal links, FAQs (only when genuinely helpful), contextual CTA
   - Image recommendations + descriptive `alt` text + eligible Schema.org recommendations
8. **Mandatory Preview & Explicit Approval Gate:** Present the full preview before publishing unless the user explicitly authorized automated publishing. Support revision requests for tone, structure, additional research, different keywords, positioning, expansion, reduction, or rewriting.
9. Publish only the approved version and record baseline/changes if optimizing an existing page.

---

## Humanized Writing Guardrails

- **Do:** Write clear active sentences, use concrete trade-offs/checklists/tables, cite verifiable docs/standards, and optimize for the human reader first.
- **Avoid:** Keyword stuffing, unnatural keyword repetition, repetitive `"In today's fast-paced digital landscape..."` AI openings, empty filler paragraphs, unnecessary headings, unsupported claims, fabricated statistics, invented case studies, or padding article length to chase arbitrary word counts or exact keyword densities.

---

## Content Refresh Workflow (Mode I)

When refreshing declining or outdated URLs:
1. Check GSC query trends for **intent drift**, CTR drop vs. position drop, or newly emerging subtopics.
2. Audit outdated years, deprecated specs/APIs, broken links, missing internal links, and thin sections.
3. Preserve the canonical URL when intent matches; log baseline + exact edits in [../templates/ranking-experiment.md](../templates/ranking-experiment.md).
