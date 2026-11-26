# Search Console, GA4 & Performance Reporting

Integrate authorized first-party measurement tools cleanly. **Never** claim to have checked Google Search Console, GA4, or PageSpeed Insights unless live API data or user-supplied exports were actually inspected. Request explicit user permission before initiating OAuth or external API connections.

## Supported Diagnostic Workflows

### Google Search Console (API or CSV Export)
- **Performance Analysis:** Compare equal date windows (e.g., 28d vs. previous 28d, or YoY for seasonal businesses) segmented by branded vs. non-branded queries, landing pages, country, device, and search appearance.
  - *Quick wins:* High-impression queries at average position `4–20` where targeted content depth or internal links can improve visibility.
  - *CTR outliers:* Strong average position (`1–5`) with weak CTR relative to SERP layout (check SERP features, ads, or title/meta clarity).
- **Indexing & Sitemaps:** Inspect URL index status, `user-declared canonical` vs. `Google-selected canonical`, `Crawled - currently not indexed` (quality/duplication signal), `Discovered - currently not indexed` (crawl budget/internal linking), 4xx/5xx server errors, and sitemap processing counts.
- **Indexing API Restriction:** Strictly refuse requests to submit ordinary blogs, product pages, or service pages via Google's Indexing API—it is officially restricted to `JobPosting` and `BroadcastEvent` embedded in `VideoObject`.

### GA4 & PageSpeed Insights
- **GA4:** Segment `Session default channel group = Organic Search` by landing page to track engaged sessions, key events (leads, demos, trial signups, checkout revenue), and conversion rate so SEO prioritizes revenue over low-intent sessions.
- **PageSpeed Insights / CrUX:** Separate 28-day field CWV (`LCP`, `INP`, `CLS`) from synthetic Lighthouse lab scores and diagnose root causes before proposing code changes.

---

## Reporting Standard

Summarize verified performance transparently using [../templates/seo-report.md](../templates/seo-report.md), explicitly naming data sources, date ranges, and unavailable metrics.
