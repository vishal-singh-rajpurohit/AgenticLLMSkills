# Quality Assurance Scenarios & Acceptance Rubrics

Use these 5 end-to-end scenarios to evaluate the `seo-skill` behavior across Claude Code, OpenAI Codex, Google Antigravity, and Cursor.

---

## Test 1 — Local Service Business (CCTV Installation, Jodhpur, Rajasthan)

- **User Prompt:** *"I run a CCTV camera installation business in Jodhpur, Rajasthan and want more business from Google. Where should we start?"*
- **Required Behaviors:**
  - Opens with a natural, conversational discovery question (Stage A)—does **not** dump 15–20 form questions or jump immediately into a generic keyword table.
  - Uncovers distinct customer segments (homeowners, retail shops/offices, schools/warehouses/factories, AMC/repair).
  - Identifies local + service keywords (`cctv camera installation jodhpur`, `commercial cctv installation jodhpur`, `cctv amc jodhpur`) and classifies intent accurately.
  - Marks unavailable SV/KD metrics transparently instead of fabricating numbers.
  - Recommends focused segment/service pages and GBP optimization without recommending mass doorway neighborhood pages.
  - Produces a phased local SEO roadmap (`templates/seo-roadmap.md`).

## Test 2 — E-Commerce Store (Pan-India Electronics Retail)

- **User Prompt:** *"We run an online electronics store shipping across India and our category and product pages barely rank. Help us audit and improve our SEO."*
- **Required Behaviors:**
  - Discovers priority product categories, margins, and buyer segments (consumer vs. B2B/bulk).
  - Separates commercial browse intent (category/sub-category) from transactional SKU intent (PDP).
  - Audits faceted navigation / filter parameter duplication, product variants, pagination canonicals, and out-of-stock lifecycle (`OutOfStock` vs `301` vs `404`/`410`).
  - Validates `Product` & `Offer` JSON-LD without fabricating `aggregateRating` or store reviews.

## Test 3 — SaaS Company (AI-Powered Email Automation)

- **User Prompt:** *"We built an AI-powered email automation SaaS. Build an SEO strategy to acquire qualified signups and demos."*
- **Required Behaviors:**
  - Clarifies target ICP, buyer roles (RevOps, outbound teams, founders, agencies), and conversion events (trial vs. demo vs. PQL/SQL).
  - Covers problem-oriented queries, software comparison/alternative queries, integration terms, and free micro-tools.
  - Maps features, use cases, verticals, and integrations to dedicated landing pages while warning against thin programmatic page cloning.
  - Plans educational content clusters linked internally to commercial landing pages and aligns KPIs with pipeline conversions.

## Test 4 — Existing Next.js Website Technical Audit & Implementation

- **User Prompt:** *"Audit this Next.js repository for technical SEO issues (metadata, canonicals, sitemap, robots) and fix the critical gaps once I approve."*
- **Required Behaviors:**
  - Fast-tracks directly to codebase inspection without forcing a full 6-stage business interview.
  - Detects exact Next.js version and router (`App Router` vs `Pages Router`), inspects routes, metadata exports, `robots`, `sitemap`, and JSON-LD (using `scripts/seo-audit/seo_audit.py`).
  - Outputs the prioritized 5-column Technical Audit Table (`Issue | Severity | Affected URLs | Evidence | Recommended Fix`).
  - Uses Next.js App Router Metadata API (`generateMetadata`, `MetadataRoute.Sitemap`, `MetadataRoute.Robots`) cleanly without overwriting existing functionality or fabricating metadata.
  - Obtains user approval before URL/destructive changes and validates changes with builds/tests and `scripts/` before claiming completion.

## Test 5 — Existing Website with 3-Month Ranking & Traffic Decline

- **User Prompt:** *"Our organic traffic has been falling steadily for the past three months. Help us figure out why and fix it."*
- **Required Behaviors:**
  - Requests Google Search Console and GA4 exports/access (or explicitly states data limitations if unavailable) rather than guessing the cause.
  - Compares equal/YoY periods, isolates branded vs. non-branded queries, affected URL groups, countries, and devices.
  - Walks through tracking regressions, indexing/canonical/technical changes, seasonality/impression demand, SERP shifts, cannibalization, and competitor improvements before attributing causes to an algorithm update.
  - Clearly distinguishes confirmed technical/data facts from working hypotheses and recommends evidence-backed corrective actions.
