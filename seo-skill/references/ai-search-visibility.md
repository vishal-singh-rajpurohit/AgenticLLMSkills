# AI Search Visibility & Answer Engine Optimization (AEO / GEO)

Design content and technical foundations so sites can be accurately discovered, grounded, and cited by **Google AI Overviews, Google AI Mode, Bing Copilot / AI search, and conversational answer engines**—without falling for hype or spam tactics.

## How AI Search Systems Ground Answers (Evidence-Based Reality)

Per current Google Search Central and Bing Webmaster guidance:
1. **Core Search Foundations Drive AI Grounding:** Google AI Overviews and AI Mode—as well as Bing AI search—retrieve candidate sources from the **core web search index** via Retrieval-Augmented Generation (RAG) and **query fan-out** (issuing multiple related sub-queries for complex multi-part questions).
2. **No Separate Magic Index or Secret Optimization:** Pages must first be crawlable, indexable, renderable, and helpful under standard search systems to be cited.
3. **Real-Time Freshness Matters:** Keeping XML sitemaps clean (with accurate `<lastmod>`) and supporting **IndexNow** (for Bing and participating engines) reduces indexing latency when product specs, pricing, or docs change.

---

## Practical Optimization Levers That Actually Help

### 1. Crawlability & Rendering Access
- Confirm critical text, pricing, specifications, and comparison tables render cleanly in initial HTML (SSR/SSG) rather than hiding behind client-side tabs or JS-only hydration barriers.
- Verify crawler controls deliberately:
  - Blocking `Googlebot` / `Bingbot` removes pages from Search *and* AI search features inside Search.
  - Note the distinction of **`Google-Extended`** (which controls broader Gemini model training/grounding controls outside core Search indexing) and standard snippet controls (`nosnippet`, `max-snippet`, `data-nosnippet`) if a business wants to restrict excerpting. Never apply `nosnippet` accidentally without explaining the Search visibility trade-off.

### 2. Extractable, Unambiguous Information Architecture
- **Lead sections with clear, direct factual answers** before nuance and background.
- **Structure complex facts cleanly:** Use semantic HTML headings (`H2`/`H3` matching real sub-questions), `<table>` elements for spec/pricing/feature comparisons, and concise bulleted checklists.
- **Keep entity naming consistent:** Clearly define brand name, product name, service locations, pricing units, dates, and author/reviewer credentials across the page and `Organization`/`Article`/`Product`/`LocalBusiness` JSON-LD.

### 3. Originality & Citation Worthiness
- Query fan-out favors pages offering **specific, differentiated substance**: original benchmarks, troubleshooting edge cases, exact compatibility matrices, regional pricing realities, real implementation steps, and first-hand experience.
- Attribute data, regulations, and technical claims to verifiable primary sources with clear publication/update dates.

---

## Myths & Anti-Patterns to Reject

Do **not** recommend or promise results from:
- Guaranteed "AI Overview placement" or "ChatGPT #1 ranking" claims.
- Artificial keyword-chunking or robotic Q&A padding that degrades human readability.
- Unproven claims that adding an `llms.txt` file or proprietary AI meta tags automatically improves Google AI Overviews or AI search rankings (only evaluate `llms.txt` if a developer explicitly wants clean markdown doc indexes for coding assistants, and clearly state it is **not** a verified Google/Bing ranking factor).
- Stuffing fake brand mentions or self-serving "best in the world" claims—grounded models and evaluators cross-check independent third-party consensus, reviews, and authoritative citations.
