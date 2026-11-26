# Interview Framework & Conversational Approval Flow

Conduct discovery like a senior SEO strategist—**one meaningful question at a time**, never a 20-question intake form.

## Core Conversational Rules

1. **Research before asking:** If the user provides a URL, repository path, or brand name, inspect the site/repo first (products, platform, target regions, metadata, pages). Never ask what is already visible.
2. **One question per turn:** Ask the single most informative next question, adapt based on the previous answer, and explain briefly *why* it matters when non-obvious.
3. **Handle uncertainty gracefully:** If the user is unsure (e.g., *"Should we target local cities or all of India?"*), present 2–3 concrete options with practical trade-offs (ranking speed vs. addressable demand vs. sales capacity) and a clear recommendation.
4. **Confirm before locking strategy:** Present the compiled YAML Business SEO Profile ([../templates/business-profile.md](../templates/business-profile.md)) and ask for confirmation before generating full keyword maps or roadmaps.
5. **Fast-track scoped technical tasks:** If the user asks specifically for a codebase audit, sitemap check, or JSON-LD fix, skip multi-stage business interviewing and inspect the repo/URL immediately, asking only essential clarifying questions (like canonical domain or URL constraints).

---

## Adaptive Question Sequence (Pick Only Missing Signals)

| Stage | What to Clarify (Skip if Known) | Example Single Question |
|---|---|---|
| **1. Business & Margins** | Core offer, highest-margin services/products, differentiators, model (B2B/SaaS/E-com/Local/Agency) | *"Of your core services, which 1–2 drive the highest margin or best client fit so we prioritize commercial visibility there first?"* |
| **2. Audience & Objections** | Ideal buyers, technical fluency, urgent pain points, pre-purchase objections, real sales questions | *"When prospects hesitate before booking or buying, what is the #1 objection or question your sales team hears?"* |
| **3. Geography & Languages** | Target countries, priority cities/regions, local vs. national vs. international, required languages | *"Do you serve clients anywhere nationally, or do physical/timezone boundaries make specific cities or countries your primary revenue focus?"* |
| **4. Conversion Funnel** | Primary conversion (demos, quotes, calls, trials, checkout) and typical buying journey | *"What single action on the website counts as a real qualified conversion for your team?"* |
| **5. Website & Access** | Existing URL + CMS/repo vs. planned new-site structure, known competitors, GSC/GA4/SEO tool access | *"Do you have Google Search Console or GA4 access (or CSV exports) we can inspect once we establish your strategy, and which 2–3 competitors do you see most often?"* |

---

## End-to-End Progressive Approval Lifecycle

1. Understand the business & margins.
2. Understand target audience segments & objections.
3. Inspect existing website / codebase (or new site positioning & planned IA).
4. Confirm geographic & language targeting.
5. Confirm conversion goals & business objectives.
6. Research real search competitors & live SERPs.
7. Present keyword opportunities & get **strategy approval**.
8. Build content roadmap & outlines.
9. Present full content previews & get **content approval** before publishing (unless automated publishing was explicitly authorized).
10. Implement approved technical/codebase changes.
11. Validate implementation (build, links, metadata, schema, sitemap).
12. Record baseline & monitor ranking experiments via Search Console/analytics.

Always distinguish clearly between **Proposed**, **User-Approved**, **Implemented**, and **Verified** items.
