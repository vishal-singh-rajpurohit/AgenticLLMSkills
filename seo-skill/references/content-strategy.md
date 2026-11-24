# Content Strategy, Creation & Optimization

Create **people-first, genuinely useful content** aligned with Google's helpful content guidance and E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)—never filler written just to hit a word count or repeat keywords.

## Content Portfolio Planning

Match content formats to the business model, audience stages, and real editorial capacity:
- **Commercial Hubs:** Service pages, product/category pages, feature/use-case/industry pages, location pages (only where real local value exists).
- **Decision-Stage Assets:** Honest comparisons (`X vs Y`), alternatives guides, transparent pricing/cost breakdowns, case studies with measurable outcomes, ROI calculators.
- **Informational & Trust-Building Clusters:** Deep tutorials, compliance/specification explainers, troubleshooting checklists, original benchmarks or field lessons.

### Editorial Calendar Discipline
- Sequence high-intent commercial gaps and quick-win refreshes **before** broad top-of-funnel blog posts.
- Size publishing cadence realistically to the team's capacity to include real SME input, photography, or original examples. Publishing 2 deeply original pieces per month beats 20 generic AI summaries (which risk Google's **Scaled Content Abuse** policy if mass-produced without unique value).

---

## Content Brief Standard

Every planned article or landing page needs a structured brief using [../templates/content-brief.md](../templates/content-brief.md) covering all 17 fields:
1. Proposed title (`<title>` & H1 direction)
2. Target URL slug
3. Primary keyword
4. Secondary keyword group (intent-aligned variants, not stuffed synonyms)
5. Search intent & expected SERP format
6. Target customer segment
7. Specific user problem / trigger
8. Desired reader outcome (what they can decide or do afterward)
9. Content format & depth target (driven by utility, never arbitrary word counts)
10. Suggested heading outline (`H1` / `H2` / `H3`)
11. Competitor research findings (what top results cover—and what they miss)
12. Original insights / first-hand proof required from the business (photos, pricing examples, real client cases, product screenshots, test results)
13. Internal linking opportunities (inbound links to add from existing pages + outbound links to hubs/spokes)
14. Authoritative external references to cite accurately
15. Relevant conversion CTA aligned with intent stage
16. Subject-matter expert (SME) / author review requirements (mandatory for medical, legal, financial, safety, or high-stakes YMYL topics)
17. Content freshness & review cadence

---

## Writing & Quality Standards

- **Answer fast, then go deep.** Put the direct answer or takeaway early before unpacking edge cases, trade-offs, and implementation steps.
- **Demonstrate real Experience & Expertise.** Show screenshots, installation specifics, exact error conditions, real numbers/pricing contexts, or decision criteria—not vague platitudes like *"In today's fast-paced digital landscape..."*.
- **Natural language.** Never force awkward exact-match grammar (*"best cctv installation jodhpur best price"*). Write for an intelligent human reader.
- **Cite primary evidence.** Attribute statistics, regulations, specs, and tool benchmarks to named, verifiable sources; never invent customer quotes or statistics.
- **Avoid duplicate/doorway scaling.** Never spin 50 city pages or 100 near-identical "X vs Y" pages by swapping one noun.

---

## Existing Content Audit & Action Framework

Before creating new pages, inspect existing pages using GSC/GA4/crawl evidence (when available) and page inspection:

| Diagnosis | Action | Criteria & Safeguards |
|---|---|---|
| High impressions, positions 4–20, weak CTR or partial coverage | **Improve** | Sharpen title/meta, align above-the-fold answer with intent, add missing subtopics, strengthen internal links |
| Thin or outdated page covering a core topic with good URL equity | **Expand** | Add current facts, SME examples, visual proof, clear comparison tables, and conversion path |
| 2+ URLs targeting the exact same intent (cannibalization) | **Consolidate** | Merge strongest elements into the higher-performing/cleaner canonical URL and `301` redirect the weaker URL(s); update all internal links |
| Legacy URL replaced by a new canonical asset | **Redirect (301/308)** | Only when destination closely satisfies the old page's intent and after verifying backlinks/traffic |
| Necessary utility/filtered/internal search/thin archive page | **Noindex** | Keep accessible to users if needed, add `noindex, follow` (never block via `robots.txt` if already indexed and needing removal) |
| Accurate, converting, well-ranked page | **Retain** | Monitor periodically for freshness and competitor encroachment |
| Zero traffic, zero backlinks, zero conversions, obsolete topic with no valid redirect target | **Remove (404/410)** | **Never** delete or redirect without checking GSC traffic, GA4 conversions, internal links, and external backlinks first, and obtain user approval |
