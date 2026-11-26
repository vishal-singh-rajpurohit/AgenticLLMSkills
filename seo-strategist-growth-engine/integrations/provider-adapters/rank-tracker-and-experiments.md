# Rank Tracker & Controlled Experiment Adapter

Use authorized rank trackers (Semrush Position Tracking, DataForSEO SERP API, AccuRanker, Ahrefs Rank Tracker, or agency CSV exports) plus GSC to measure real post-optimization outcomes honestly.

---

## 1. Measurement Hygiene Contract

Every rank-tracking comparison must preserve identical measurement context:
- **Provider & Snapshot Date** (e.g., `Semrush Position Tracking`, `DataForSEO`, `GSC Export`)
- **Location** (`Country`, and `State/City` for local queries)
- **Language** (e.g., `en-IN`, `en-US`)
- **Device** (`mobile` vs. `desktop`)
- **Organic vs. SERP Feature Position** (do not conflate a Local Pack #1 or Featured Snippet with organic #1 unless labeled separately)

> **Never equate Search Console `Average Position` with a clean geo-pinned rank tracker.** GSC blends impressions across locations, devices, and personalization.

---

## 2. Experiment Logging & Evaluation Protocol

When shipping any on-page, technical, or content refresh change:
1. Instantiate [../../templates/ranking-experiment.md](../../templates/ranking-experiment.md) **before** deploying edits.
2. Record real pre-change baseline (28-day GSC clicks, impressions, CTR, average position, conversions, and geo-pinned tracker position where available; mark missing inputs `unavailable`).
3. Record exact deploy date and file/copy changes.
4. Wait an adequate observation window (**minimum 14–28 days post-recrawl** for stable pages, longer for low-impression B2B/new pages).
5. Evaluate with `scripts/technical-seo-audit/experiment_evaluator.py` (or manual equal-period comparison) using honest statuses:
   - `awaiting-data`: insufficient elapsed window or missing post-edit metrics
   - `inconclusive`: missing baseline, low sample volume, or confounding SERP/seasonality shifts
   - `improved` / `declined`: clear directional shift across equal windows with recorded confounding checks
