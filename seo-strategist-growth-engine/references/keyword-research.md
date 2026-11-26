# Keyword Research & Opportunity Scoring Engine

Discover, classify, cluster, and prioritize keywords around **business conversion value and verified search intent**—never fabricate metrics or spin duplicate pages per phrasing variant.

## 1. Keyword Categories to Cover

- **Core & Long-Tail:** Primary category/service head terms, high-intent modifiers (`for fintech`, `enterprise`, `open source`), and specific long-tail queries.
- **Full Intent Spectrum:**
  - *Informational:* `"what is..."`, `"how to..."`, checklists, benchmarks, architecture guides.
  - *Commercial Investigation:* `"best..."`, `"top..."`, `"X vs Y"`, `"alternatives to..."`, `"pricing"`, `"reviews"`.
  - *Transactional:* `"hire..."`, `"buy..."`, `"get quote"`, `"book demo"`, `"free trial"`.
  - *Navigational:* Brand + login/pricing/docs/support queries.
- **Problem & Question Queries:** Pain-point searches before buyers know your product category exists (`"why does checkout drop on mobile..."`).
- **Local & Branded:** City/region/`"near me"` terms alongside separated branded vs. non-branded demand.

---

## 2. Metrics, Source Integrity & Provider Decoding

Collect where authorized providers (Semrush MCP, Google Search Console, Google Ads Keyword Planner, DataForSEO, Ahrefs) are connected:
`Search Volume | Keyword Difficulty | CPC | Competition | Search Intent | Geography | Trend | SERP Features | Current Position | Ranking URL`

- **Strict separation rule:** Label provider data (`[Semrush]`, `[GSC]`, `[GKP]`) separately from qualitative observations (`[SERP-Observed]`) and missing values (`Unavailable`). Never invent search volumes, KD, CPC, or ranks.
- **Semrush numeric intent codes:** When legacy/API reports return integers, decode only `0`=Commercial, `1`=Informational, `2`=Navigational, `3`=Transactional (comma-separated like `1,0` = Mixed Intent); preserve raw codes in evidence and verify ambiguous terms on the live SERP.
- **Low/Zero-volume rule:** Do not discard high-buying-intent B2B/technical queries purely because third-party tools report `0` or low monthly volume when sales calls or GSC show real demand.

---

## 3. Intent Clustering & Anti-Cannibalization

Group keywords into **one cluster mapped to one canonical target URL** when they share:
1. Same dominant search intent and required page format.
2. Substantial SERP overlap (same or near-identical top-10 ranking URLs across queries).
3. Same buyer stage and primary conversion action.

Do **not** create separate pages for minor singular/plural or word-order variations sharing one intent—consolidate to prevent keyword cannibalization.

---

## 4. Transparent Configurable Opportunity Scoring

Score clusters openly using configurable weights tailored to the business (never present an internal priority score as an official Google ranking metric):

- **Baseline Weights (adjustable per client):**
  - Business Relevance (`0.25`)
  - Search Intent & Conversion Potential (`0.25`)
  - Ranking Feasibility vs. Incumbent Authority (`0.20`)
  - Search Demand / GSC Impressions (`0.15`)
  - Content Gap & Geographic Fit (`0.15`)

Output using [../templates/keyword-research.md](../templates/keyword-research.md):
`| Keyword | Intent | Volume | Difficulty | Business Relevance | Recommended Action |`
