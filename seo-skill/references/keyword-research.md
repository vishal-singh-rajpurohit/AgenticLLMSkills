# Keyword Research & Clustering Workflow

Discover, verify, classify, cluster, and prioritize keywords around **real customer demand and business value**—never around empty search-volume sorting.

## Data Integrity Rules

1. **Never invent numbers.** Do not fabricate Monthly Search Volume, Keyword Difficulty (KD), CPC, trend percentages, or projected traffic.
2. **Label every metric's source.** Distinguish:
   - `[GSC]` — Google Search Console first-party impressions/clicks/position
   - `[GKP]` / `[Semrush]` / `[Ahrefs]` / `[DataForSEO]` — Third-party or ad-platform estimate (note country & date)
   - `[SERP-Observed]` — Live autocomplete, PAA, related searches, ranking competitors
   - `[Unavailable]` — Live metric provider not connected in current session
3. **Consistent scope.** Keep country, language, and device assumptions explicit when comparing metrics.

---

## Step 1 — Seed Expansion by Customer Angle

Build seeds from the confirmed Discovery Profile across all relevant modifiers rather than relying on one obvious head term:

- **Core product / service terms:** Exact names of offerings and buyer synonyms.
- **Problem-oriented terms:** Pain points and symptoms before the user knows the solution name.
- **Commercial investigation & comparison:** `"best ..."`, `"... vs ..."`, `"... alternatives"`, `"... reviews"`, `"... pricing"`, `"... cost"`.
- **Transactional & service-ready terms:** `"hire"`, `"buy"`, `"quote"`, `"installation"`, `"service"`, `"agency"`, `"software"`, `"near me"`.
- **Question-based & informational:** `"how to"`, `"what is"`, `"why does"`, `"checklist"`, `"requirements"`, `"guide"`.
- **Local / regional modifiers:** City, district, state, `"near me"`, regional spellings/terms (e.g., `"CCTV AMC"`, `"GST billing"`).
- **Branded vs. non-branded:** Separate brand demand from non-branded discovery so brand traffic never hides non-branded gaps.
- **Segment / use-case / integration modifiers:** `"for schools"`, `"for warehouses"`, `"for Shopify"`, `"HubSpot integration"`.

---

## Step 2 — Discovery Methods (With & Without Paid APIs)

### When Data Providers Are Connected
- Pull query data from **Google Search Console** first (queries already getting impressions at positions 4–30 are often top quick wins).
- Query **Google Ads Keyword Planner**, **Semrush**, **Ahrefs**, or **DataForSEO** scoped to the exact target country/city and language.
- Export Google Trends seasonality where demand fluctuates by season, festival, exam cycle, or fiscal year.

### Fallback When Paid Keyword APIs Are Unavailable
Explicitly tell the user that live search volume / KD / CPC metrics are unavailable, then build high-signal qualitative keyword sets via:
1. Live web search SERP checks, autocomplete patterns, People Also Ask, and related searches.
2. Mining competitor navigation, H1s/H2s, category trees, product titles, FAQs, and sitemaps.
3. Mining customer questions from reviews, forums, and sales objections.
4. Recording `Unavailable (live keyword API not connected)` in numeric metric columns and ranking opportunities using **Qualitative Priority** (business relevance, observable SERP demand, buyer intent, and competitiveness).

---

## Step 3 — Intent Classification & SERP Verification

Classify every keyword using [search-intent-analysis.md](search-intent-analysis.md) before grouping or assigning URLs:
- Informational
- Navigational
- Commercial Investigation
- Transactional
- Local Intent
- Mixed / Ambiguous (requires inspecting live SERP dominant page types)

---

## Step 4 — Intent-Based Clustering & Cannibalization Prevention

**Never cluster keywords by string similarity alone.** Two keywords that look alike (*"email automation software"* vs. *"what is email automation"*) have different intents and belong on different pages. Conversely, *"cctv installation jodhpur"* and *"cctv camera fitting service in jodhpur"* share one intent and belong on one strong page.

### Clustering Criteria
Group keywords into one cluster only when they share:
1. **Same dominant search intent.**
2. **Substantial SERP overlap** (when SERPs are checked, the same URLs rank for both terms).
3. **Same target audience segment & conversion goal.**
4. **Same optimal target page type.**

### Anti-Cannibalization Check
- Assign **one canonical primary URL** per unique search intent cluster.
- Flag any existing pages on the site targeting overlapping intent so they can be consolidated, differentiated by distinct intent/segment, or canonicalized.

---

## Step 5 — Transparent Prioritization Scoring

Prioritize clusters openly without opaque black-box promises. Evaluate each cluster across:

| Factor | High Score Signal |
|---|---|
| **Business Relevance & Margin** | Maps directly to high-margin or strategic core offering |
| **Intent Proximity to Revenue** | Transactional, local service, or high-intent comparison |
| **Search Demand** | Verified high impressions/volume or strong multi-source SERP demand |
| **Ranking Feasibility** | Realistic vs. current site authority and strength of top-10 SERP incumbents |
| **Conversion Potential** | Clear CTA fit without forcing an unnatural pitch |
| **Execution Effort** | Copy tweak / existing page upgrade vs. new engineering/data study |

Bucket clusters into:
- **P1 — Immediate / Quick Wins:** Existing pages ranking 4–20, high-intent service/category gaps, low implementation friction.
- **P2 — Core Commercial & Hub Expansion:** Essential feature, use-case, location, or comparison pages.
- **P3 — Authority & Top-of-Funnel Compounding:** Educational clusters, original data, tools/calculators.

---

## Deliverable Formats

Populate both templates cleanly:
- Raw & classified inventory: [../templates/keyword-research.csv](../templates/keyword-research.csv)
- Intent-grouped page map: [../templates/keyword-mapping.csv](../templates/keyword-mapping.csv)

Document column meanings:
- `keyword-research.csv`: `Keyword, Cluster, Search Intent, Segment, Country/Language, Search Volume, Volume Source, Keyword Difficulty, CPC, Current Position, SERP Features, Recommended Page Type, Business Relevance (1-5), Priority, Notes`
- `keyword-mapping.csv`: `Cluster Name, Primary Keyword, Supporting Keywords, Search Intent, Target Segment, Target URL, Existing vs New, Page Type, Content Angle, Primary CTA, Priority, Cannibalization Risk / Notes`
