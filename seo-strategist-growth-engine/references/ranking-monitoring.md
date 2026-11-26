# Ranking Monitoring & Controlled SEO Experiments

Never edit pages and declare them SEO-optimized without measuring real outcomes. Establish a verifiable baseline, log every major change as a structured experiment, and evaluate performance honestly.

## 8-Step Experiment Lifecycle

For every important content or on-page optimization, track using [../templates/ranking-experiment.md](../templates/ranking-experiment.md):
1. Record the original URL and snapshot existing title/H1/structure.
2. Record exact target keyword cluster.
3. Capture verifiable baseline (`date`, `position`, `clicks`, `impressions`, `CTR`, `conversions`, `indexed_status`—mark `unavailable` if no GSC/rank tracker is connected; never fabricate).
4. Record exact deploy/change date.
5. Document every specific edit shipped (title, H1, content depth, internal links, schema, CTA).
6. Monitor subsequent Search Console, GA4, and authorized rank-tracker metrics.
7. Compare equal pre/post periods once recrawl and sample size are sufficient.
8. Decide next step (`keep`, `iterate`, `revert`, or `continue-observing`).

---

## Measurement Integrity Rules

1. **Separate GSC Average Position from Rank-Tracker Position:** GSC `Average Position` aggregates all impressions across geographies, devices, personalization, and SERP features—it is **not** a universal rank. When using an authorized rank tracker, keep **country/city, language, device (`mobile`/`desktop`), search features, and provider** constant across comparisons.
2. **Account for Confounding Variables:** Algorithm updates, SERP layout shifts (Ads, Local Pack, AI Overviews), seasonality, and competitor edits alter clicks and CTR independently of your edit.
3. **Require Sufficient Observation Windows:** Avoid calling winners or losers from 1–7 days of crawl flux. Wait for Google recrawl/reindexing and meaningful impression volume (typically 14–28+ days post-recrawl).
4. **Report `inconclusive` Honestly:** When baseline metrics are missing, impressions are too low for confidence, or observation time is under 14 days, mark `evaluation.status: inconclusive` or `awaiting-data` instead of claiming success.
