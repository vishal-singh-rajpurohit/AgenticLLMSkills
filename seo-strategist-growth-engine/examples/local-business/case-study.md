# Scenarios 4, 5 & 6 — Existing Site Recovery, New Website Launch & Ranking Experiment

> *Illustrative demonstration fixtures showing how the skill handles (A) recovering an underperforming existing site, (B) launching a new website from scratch, and (C) running an honest controlled ranking experiment.*

---

## Scenario 4 — Existing Website with Poor Rankings (Recovery Plan)

- **Context:** Local HVAC & Commercial Cooling Contractor (`example-cooling.example`, WordPress) experiencing stagnant rankings and low leads.
- **Technical Audit Findings (`scripts/technical-seo-audit/run_technical_audit.py`):**
  1. `Critical`: `robots.txt` inadvertently disallowed `/wp-content/uploads/` and CSS assets, hurting mobile rendering parity.
  2. `High`: 14 boilerplate city pages (`/hvac-city-a` through `/hvac-city-n`) had identical 180-word copy with only the city token swapped (Scaled Content Abuse / doorway risk).
  3. `High`: XML sitemap listed `noindex` tag archives and 3 redirected URLs.
  4. `Medium`: Homepage and `/commercial-hvac` targeted the same primary query (`commercial hvac service`), splitting internal link equity.
- **GSC / Competitor Gap Findings (from user CSV export):**
  - High impressions at average positions `9–14` for `chiller maintenance contract` with `0.8%` CTR due to vague title tag (`Services | Acme`).
  - Top local competitors displayed maintenance SLA response times, equipment brands serviced, and transparent inspection checklists.
- **Prioritized Recovery Roadmap:**
  - **P0:** Fix `robots.txt`, clean XML sitemap to canonical `200 OK` URLs only, consolidate duplicate city doorway pages (keep only verified service areas with real project proof and `301` redirect/prune empty clones after explicit user approval).
  - **P1:** Rewrite `/commercial-hvac` title, above-the-fold SLA proof, `LocalBusiness` JSON-LD (real visible address/hours), and internal links from related guides.
  - **P2:** Publish verified maintenance checklist + case documentation.

---

## Scenario 5 — New Website Launch (Zero Historical Authority)

- **Context:** Newly launching boutique dental practice (`new-clinic.example`, Next.js App Router, zero backlinks, zero Search Console history).
- **Discovery & Architecture Plan:**
  1. Confirm core profitable treatments (`dental implants`, `emergency tooth extraction`, `invisalign aligners`) and single-city radius before picking URLs.
  2. Build clean URL taxonomy (`/treatments/dental-implants`, `/treatments/emergency-dentist`, `/about`, `/book`).
  3. Ship Phase-1 technical checklist before launch: `metadataBase`, unique `Metadata`, `app/sitemap.ts` (env-backed domain), `app/robots.ts` (never staging `Disallow: /` leaked to prod!), `Dentist` (`LocalBusiness`) JSON-LD, mobile CWV check.
  4. Target specific low-competition treatment + neighborhood/procedure-question clusters first rather than fighting national directories on `"dentist"` immediately.
  5. Submit sitemap in Google Search Console on launch day and monitor indexing coverage (`Crawled - currently not indexed` checks) without misusing the Indexing API.

---

## Scenario 6 — Controlled Ranking Experiment (`ranking-experiment.md`)

*(Demonstrates strict separation between GSC average position, geo-pinned rank tracker, and honest `inconclusive` vs. `improved` evaluation.)*

```yaml
experiment:
  id: commercial-hvac-001
  url: /services/commercial-hvac
  target_keywords:
    - commercial hvac maintenance contract
    - chiller maintenance service

  measurement_context:
    country: India
    language: en-IN
    device: mobile
    gsc_source: GSC CSV Export (Illustrative)
    rank_tracker_provider: Unavailable

  baseline:
    date: 2026-10-01
    observation_window_days: 28
    gsc_avg_position: 11.4
    tracker_position: unavailable
    clicks: 18
    impressions: 2150
    ctr: 0.84%
    conversions: 1
    indexed_status: Indexed

  changes:
    deploy_date: 2026-10-29
    summary:
      - Rewrote title and H1 to align with commercial AMC intent & SLA turnaround
      - Added preventative maintenance checklist table and verified response-time SLA
      - Added 4 contextual internal links from maintenance guides

  post_change:
    evaluation_date: 2026-11-26
    observation_window_days: 28
    gsc_avg_position: 7.8
    tracker_position: unavailable
    clicks: 41
    impressions: 2480
    ctr: 1.65%
    conversions: 4
    indexed_status: Indexed

  evaluation:
    status: improved
    confounding_factors:
      - Seasonal Q4 cooling contract renewals noted
    conclusion: >-
      Over an equal 28-day post-recrawl window, organic clicks (+127.8%), CTR
      (0.84% -> 1.65%), and qualified quote submissions (1 -> 4) improved on the
      target URL. Localized rank-tracker position remains unavailable; monitor
      another 28 days to isolate Q4 seasonality.
    next_action: keep
```
