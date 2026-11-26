# Independent SEO Research Engine (Fallback Adapter)

When paid SEO plugins/APIs (Semrush, Ahrefs, DataForSEO) or GSC/GA4 are unavailable or only partially connected, use this **Terms-compliant independent research workflow**. Never scrape Google/Bing HTML pages with automated bots or fabricate quantitative metrics.

---

## 1. Authorized Research Channels

| Task | Compliant Method | Output Integrity Label |
|---|---|---|
| **Live SERP & Intent Inspection** | Agent's built-in `search_web` / Search API / browser view + `country` & `language` context | `[SERP-Observed <YYYY-MM-DD>]` |
| **Keyword Discovery & Modifiers** | Customer discovery interviews, support tickets, `search_web` related topics, Google Ads Keyword Planner CSVs, Google Trends | `[Qualitative]` or `[GKP / Trends]` |
| **Competitor Page Analysis** | Direct HTTP fetch (`urllib` / browser / `scripts/`) of public competitor landing pages, sitemaps, headings, and visible schema | `[Page-Observed <URL> <YYYY-MM-DD>]` |
| **Technical & On-Page Audit** | Zero-dependency Python CLIs in `scripts/` (`run_technical_audit.py`, `audit_sitemap.py`, `audit_metadata.py`, `audit_links.py`, `validate_structured_data.py`) | `[Script-Verified]` |
| **Search Volume / KD / Backlinks** | Mark strictly as `Unavailable` unless supplied by an authorized provider or CSV export | `Unavailable (No Volume Provider)` |

---

## 2. Keyword Discovery Without Volume APIs

1. Expand seed concepts from buyer jobs-to-be-done, industry terminology, integrations, pricing qualifiers, comparison triggers (`vs`, `alternatives`), and local modifiers.
2. Validate every candidate cluster via live search (`search_web` or authorized search API) to observe:
   - Which page types actually rank (service page vs. category vs. article vs. directory).
   - What recurring buyer questions and subtopics appear across top results.
   - Where incumbents leave gaps (unclear pricing drivers, missing implementation edge cases, outdated specs).
3. Score opportunity transparently using business relevance, buyer intent fit, qualitative SERP competition strength (incumbent authority/depth), and content gap—leaving search volume explicitly `Unavailable`.
