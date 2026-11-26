# Google Search Console, GA4 & PageSpeed Insights Adapter

Prioritize first-party Google Search Console (GSC) and Google Analytics 4 (GA4) data for actual website traffic, queries, indexing, and conversions. **Request explicit user authorization before initiating OAuth or API connections**, and never claim data was inspected without real retrieved rows or supplied CSV exports.

---

## 1. Google Search Console (API or CSV Export)

### Supported Ingestion Paths
1. **Connected GSC MCP / API (with user permission):** Query Search Analytics (`searchAnalytics.query`), Sitemaps (`sitemaps.list`), and URL Inspection (`urlInspection.index.inspect`).
2. **User-Supplied CSV Exports:** Accept standard GSC `Queries.csv`, `Pages.csv`, `Countries.csv`, `Devices.csv`, or Index Coverage exports when API access is absent.

### Mandatory Guardrails
- **Separate Branded vs. Non-Branded Queries** before declaring SEO growth.
- **Indexing API Restriction:** Google's Indexing API (`indexing.googleapis.com`) is strictly restricted to `JobPosting` and `BroadcastEvent` inside `VideoObject`. Never submit or automate Indexing API calls for regular blogs, service pages, or product pages.
- **Inspection Rules:** Check `verdict`, `coverageState` (e.g., `Crawled - currently not indexed`), `googleCanonical` vs. `userCanonical`, and `robotsTxtState`.

---

## 2. Google Analytics 4 (GA4)

- Filter `Session default channel group` = `Organic Search` by landing page (`landingPagePlusQueryString`).
- Measure **engaged sessions**, **engagement rate**, **key events** (leads, demo requests, signups, phone clicks, purchases), and **ecommerce revenue**.
- Pair GSC click data with GA4 conversion rates so optimization focuses on pipeline rather than empty top-of-funnel impressions.

---

## 3. PageSpeed Insights (PSI) & Core Web Vitals

- Use the official PageSpeed Insights v5 API (`pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed` with strategy `mobile` and `desktop`) or Chrome DevTools / Lighthouse locally.
- **Field vs. Lab Rule:** Treat `loadingExperience` (28-day CrUX real-user `LCP`, `INP`, `CLS` at p75) as field reality and `lighthouseResult` as synthetic lab diagnostics. Report field metrics as `Unavailable` on low-traffic URLs lacking CrUX coverage.
