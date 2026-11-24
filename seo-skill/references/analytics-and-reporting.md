# Analytics, Diagnostics, CRO & Reporting

Measure search performance rigorously, diagnose drops using multi-source evidence instead of guesswork, connect rankings to conversions, and communicate progress plainly.

## Data-Source Discipline

- **Never fabricate** historical rankings, impressions, CTR, conversions, or projected ROI.
- **Never claim access** to Search Console, GA4, or rank trackers unless files/APIs are genuinely supplied in the conversation.
- **Always separate correlation from causation** (e.g., a ranking shift coinciding with a Google update does not prove an update caused it if a release also deployed `noindex` or changed canonicals the same week).

---

## 1. Google Search Console (GSC) Analysis

Segment data before drawing conclusions—sitewide averages hide real changes:
- **Performance Report:** Inspect Clicks, Impressions, CTR, Average Position split by:
  - Branded vs. Non-branded queries (`query` filter).
  - Specific landing pages and templates (e.g., `/blog/` vs `/products/` vs `/services/`).
  - Country and Device (Desktop vs. Mobile—critical for mobile-first indexing and Local Pack CTR differences).
  - Search Appearance (Product snippets, Merchant listings, Video, Web light, etc.).
- **High-Potential Opportunity Filters:**
  - *Quick-win rankings:* Non-branded queries averaging position **4–15** with strong impressions.
  - *CTR gaps:* Top-5 positions with noticeably weak CTR -> inspect live SERP features (ads, AI Overviews, local packs) and title/meta clarity before blaming the title alone.
- **Indexing, Sitemaps & CWV Reports:** Monitor `"Crawled - currently not indexed"`, `"Discovered - currently not indexed"`, `"Duplicate without user-selected canonical"`, `404`/`5xx` spikes, sitemap submission errors, and CrUX Core Web Vitals status groups.

---

## 2. Google Analytics 4 (GA4) & Conversion Optimization (CRO)

Filter to `Session default channel group = Organic Search` and inspect by **Landing Page + Query String**:
- Track **Engaged sessions**, **Engagement rate**, **Key Events** (lead forms, quote requests, demo bookings, phone/WhatsApp clicks, `purchase`), and **Revenue / Lead Quality** (when CRM feedback is available).
- **CRO Audit on Top Organic Entry Pages:**
  - *High organic traffic + low key-event conversion rate:* Check intent mismatch (informational visitors landing on hard-sell pages or vice versa), unclear above-the-fold value prop, buried/broken CTA, slow mobile checkout/form friction, missing trust signals (pricing expectations, warranty, local proof, security compliance), or un-tracked phone/WhatsApp clicks inflating "zero conversion" reports.

---

## 3. Rank Tracking Discipline

When third-party rank tracking or GSC query-page pairs are monitored:
- Record **Keyword, Target URL, Target Country/City, Device, Current Position, Previous Position, Change, SERP Features, Measurement Date, Source**.
- Keep **country, city/location emulation, and device type constant** across periods.
- Never treat a single day's rank fluctuation as a confirmed trend; check 14–28 day rolling baselines alongside clicks/conversions.

---

## 4. Traffic & Ranking Decline Diagnostic Tree

When organic traffic or rankings drop (e.g., over the past 1–3+ months), work top-down through evidence before blaming an algorithm update:

1. **Measurement & Tracking Integrity Check:** Did GA4 tags, cookie consent banners, server-side GTM, or domain changes break analytics tracking while GSC clicks stayed steady? (Compare GSC clicks vs. GA4 organic sessions first!)
2. **Indexing & Technical Regressions:** Check GSC Page Indexing, `robots.txt` history, accidental `noindex`, canonical shifts, SSL/DNS/CDN outages, 4xx/5xx spikes, broken redirects, or JS rendering failures from recent deployments.
3. **Scope Isolation (GSC):** Did traffic drop across *all* queries, specific page folders, specific countries/devices, or branded vs. non-branded terms?
4. **Seasonality & Market Demand:** Compare year-over-year (YoY) rather than just month-over-month (MoM), and check Google Trends / impression drops (if impressions fell while average position held steady, demand shifted—not rankings!).
5. **SERP Layout Shifts & Competitor Gains:** Did new ads, Local Pack, Shopping units, or AI Overviews push organic blue links lower? Did competitors launch stronger category/comparison/local pages?
6. **Cannibalization & Content Changes:** Did a new post/page split clicks from an existing winner? Did a recent redesign strip headings, internal links, copy, or URLs?
7. **Core / Spam Update Correlation:** Only after inspecting dates against documented Google Search Status Dashboard updates *and* reviewing affected pages against Helpful Content / E-E-A-T / Spam policies, hypothesize an algorithmic revaluation—clearly labeled as a hypothesis backed by timing and page-quality evidence.

---

## 5. Monthly Reporting Standard

Deliver plain-language, decision-oriented monthly reports using [../templates/monthly-report.md](../templates/monthly-report.md) covering all 12 required sections, separating confirmed data from hypotheses and next-month actions.
