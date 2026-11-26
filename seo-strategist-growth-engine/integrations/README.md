# SEO Tool Discovery, Capability Matrix & Integration Architecture

Before implementing custom crawlers or promising keyword/ranking metrics, inspect the active agent environment for connected integrations. **Never duplicate a reliable connected tool**, **never invent unsupported provider APIs**, and **never scrape search engines in violation of their Terms of Service**.

---

## 1. Environment Discovery Sequence

Run `python scripts/technical-seo-audit/run_technical_audit.py --discover-tools <optional-repo-or-dir>` and also inspect the active agent's loaded tools/plugins:

1. **SEO Plugins & MCP Servers:** Check for connected Semrush MCP (`semrush_mcp`), Ahrefs MCP, DataForSEO MCP, or project `.mcp.json` configurations.
2. **First-Party Analytics & Performance:** Check Google Search Console access (OAuth/Service Account or CSV exports), GA4, and Google PageSpeed Insights / Lighthouse.
3. **Authorized Rank Trackers & Crawlers:** Check configured rank-tracking exports/APIs or Screaming Frog / Sitebulb exports alongside local Python `scripts/`.
4. **Web Search & Fetch:** Check native agent web search / browser / HTTP fetch tools for live SERP and competitor inspection.
5. **Content & Publishing Integrations:** Check sibling `content-research-writer` skill and repo CMS/ORM clients (WordPress, Shopify, Sanity, Strapi, Directus, Prisma, Drizzle, Next.js).

---

## 2. Tool Selection Criteria

Evaluate each candidate tool across:
- **Accuracy & Data Freshness** (first-party GSC/GA4 vs. third-party index estimates vs. live SERP fetch)
- **Metric Availability** (Search Volume, KD, CPC, Search Intent, SERP Features, Backlinks, CrUX CWV)
- **Competitor & Geographic Coverage** (regional databases, city-level vs. national rank precision)
- **Cost, Rate Limits & API Units** (disclose unit usage before running third-party MCP queries)
- **Integration Complexity & Auth State** (signed-in plugin vs. OAuth approval needed vs. zero-setup fallback)

---

## 3. Capability Matrix Template

Populate this matrix at the start of an engagement based on live discovery:

| SEO Capability | Existing Tool | Available | Alternative / Adapter |
|---|---|---|---|
| **Keyword Research** | Semrush MCP (`keyword_research`) / Keyword Planner | Check session | [semrush-mcp.md](provider-adapters/semrush-mcp.md) or [independent-research-engine.md](provider-adapters/independent-research-engine.md) |
| **Search Intent & SERP** | Semrush (`phrase_organic`) / Web Search | Check session | Live SERP observation + [search-intent-analysis.md](../references/search-intent-analysis.md) |
| **Competitor Research** | Semrush (`competitors_research`) | Check session | Live SERP & page fetch ([independent-research-engine.md](provider-adapters/independent-research-engine.md)) |
| **Search Performance** | Google Search Console | Check auth/CSV | [search-console-ga4-psi.md](provider-adapters/search-console-ga4-psi.md) or manual inspection |
| **Conversions & Behavior** | Google Analytics 4 (GA4) | Check auth/CSV | Server/CRM conversion logs or unavailable |
| **Rank Tracking** | Authorized Rank Tracker / Semrush / GSC | Check auth/CSV | [rank-tracker-and-experiments.md](provider-adapters/rank-tracker-and-experiments.md) |
| **Technical SEO Audit** | Semrush Site Audit / Screaming Frog | Check auth/CSV | Local `scripts/technical-seo-audit/run_technical_audit.py` |
| **CWV & PageSpeed** | PageSpeed Insights API / CrUX / Lighthouse | Check key/CLI | Browser DevTools / Lighthouse local run |
| **Content Drafting & Publishing** | Sibling `content-research-writer` | Check repo/skills | [content-research-writer-bridge.md](provider-adapters/content-research-writer-bridge.md) or built-in Mode F |
| **Codebase / CMS SEO Edits** | Direct Repo / CMS API | Check workspace | [cms-and-codebase-adapters.md](provider-adapters/cms-and-codebase-adapters.md) |
