# Search Intent Analysis & Page-Type Selection

Search engines rank pages that satisfy **what the searcher actually wants to accomplish next**—not pages that merely repeat the keyword string.

## Intent Classification Taxonomy

| Intent Type | What the User Wants | Typical Modifiers | Typical SERP Signals |
|---|---|---|---|
| **Informational** | Understand a concept, solve a problem, learn steps | `how to`, `what is`, `why`, `guide`, `requirements`, `tips` | Guides, tutorials, definitions, AI Overviews, video results, PAA |
| **Navigational** | Reach a specific brand, login, or documentation portal | Brand name, `login`, `pricing`, `docs`, `support` | Sitelinks, brand homepage, app login, official social/GBP |
| **Commercial Investigation** | Compare options, evaluate cost, verify quality before buying | `best`, `top`, `vs`, `alternative`, `review`, `cost`, `comparison` | Comparison articles, category pages, listicles, review threads (Reddit/G2) |
| **Transactional** | Purchase, book, request quote, sign up, download tool | `buy`, `price`, `order`, `book`, `quote`, `free trial`, `demo`, `hire` | Product pages, service landing pages, shopping grids, pricing pages |
| **Local Intent** | Find a nearby provider, storefront, or service in a city/area | `near me`, city/district name, `in <city>`, `installation`, `repair` | Map Pack / Local Pack, Google Business Profiles, local service pages, directories |
| **Mixed / Ambiguous** | Broad head term where users split between learning and buying | Broad nouns (`"crm software"`, `"cctv camera"`, `"wireless earbuds"`) | Mixed SERP: e-commerce/product pages alongside guides and comparisons |

---

## Live SERP Reverse-Engineering Protocol

Never guess the required page format from keyword wording alone. Inspect the top 10 live results (and note country/device):

1. **Dominant Page Format:** Are 7+ of the top 10 results blog guides, product category pages, single PDPs, service landing pages, comparison tables, or interactive tools? Match the dominant satisfying format unless you have clear evidence of an unmet format gap.
2. **SERP Features Present:** Local Pack, Shopping / Product snippets, Video carousels, Image packs, AI Overviews, Discussions/Forums, Sitelinks. These reveal what Google believes helps the user fastest.
3. **Content Angle & Depth:** Notice whether top pages emphasize pricing breakdowns, technical specs, troubleshooting steps, visual proof, regional compliance, or checklists.
4. **Freshness Expectations:** Do top results show current-year benchmarks, recent pricing, or live inventory?
5. **Incumbent Type:** Are the top positions dominated by local businesses, national marketplaces (Amazon, IndiaMART, Justdial), SaaS vendors, or publishers? This determines ranking feasibility.

---

## Keyword-to-Page-Type Mapping Matrix

| Optimal Page Type | Best-Fit Search Intent | When to Choose This Format |
|---|---|---|
| **Service Landing Page** | Transactional / Local | Buyer wants to hire a provider, request a quote, or book an appointment |
| **Product Detail Page (PDP)** | Transactional (specific SKU/model) | Searcher wants a specific product model, price, stock status, specs, and checkout |
| **Category / Collection Page** | Commercial / Transactional (browse) | Searcher wants to compare multiple models/SKUs within a category (`"4k security cameras"`) |
| **Location Landing Page** | Local | Business genuinely serves/operates in that distinct city/region with unique local proof |
| **Comparison / Alternatives Page** | Commercial Investigation | Searcher explicitly evaluates vendors (`"A vs B"`, `"B alternatives"`) |
| **Buying Guide / Listicle** | Commercial Investigation | Searcher needs help choosing among criteria, tiers, or use cases |
| **Blog Article / Explainer** | Informational | Searcher needs concepts, causes, pros/cons, or strategic guidance |
| **Tutorial / Documentation** | Informational (task execution) | Searcher wants step-by-step setup, API reference, troubleshooting, or configuration |
| **Interactive Tool / Calculator** | Commercial / Informational utility | Searcher wants personalized output (ROI, camera count/storage, pricing estimator) |
| **FAQ Section (embedded)** | Narrow sub-questions | Questions too small for standalone URLs that strengthen a parent service/product page |

---

## Handling Split or Mixed-Intent Keywords

When a broad term shows mixed intent (e.g., `"cctv camera"` returns Amazon categories, local installers, and buying guides):
- Identify which sub-intent aligns with your business model and realistic ranking power.
- Target the actionable long-tail sub-intents on dedicated pages (category page for shopping, service page for installation, guide for selection) and link them cleanly together with descriptive internal anchors.
- Do **not** build two near-identical pages trying to force one exact head phrase.
