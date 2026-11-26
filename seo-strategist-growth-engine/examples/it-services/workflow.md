# Scenario 1 — Local IT Services Agency (Worked Example)

> *Illustrative demonstration scenario showing conversational discovery, tool discovery, local + national keyword mapping, and phased roadmap without fabricating live metrics.*

## 1. Tool Discovery & Baseline Check
- Command: `python scripts/technical-seo-audit/run_technical_audit.py --discover-tools`
- Connected session state: Semrush MCP `Not Signed In` -> Independent Research Engine (`search_web` + codebase audit scripts); GSC/GA4 `Pending User CSV/OAuth`.

## 2. Progressive Interview (One Question at a Time)
1. **Offer & Margin:** *"Which of your four core offerings—web development, mobile apps, custom software, or AI integrations—drives your highest margin and best client fit?"* -> Custom enterprise software and AI workflow integrations.
2. **Buyers & Objections:** *"What stops mid-market CTOs or operations leads from booking a technical scoping call?"* -> Fear of agency scope creep, vague fixed-price quotes, and post-launch handover gaps.
3. **Geography Trade-off:** *"Should we prioritize city-level local SEO first or target national/remote B2B buyers?"* -> Recommended dual-track: city-level trust in Pune & Mumbai (real office + local proof) paired with national B2B solution pages.
4. **Confirmed Business SEO Profile:**
```yaml
business:
  name: Illustrative Horizon Tech Studio
  type: B2B IT Services Agency
  industry: Software Development & AI Integration
  website_url: https://illustrative-horizon.example
  platform: Next.js App Router
  products:
    - Custom software development
    - AI workflow integrations
    - Web application development
    - Mobile app development
audience:
  primary: Operations directors & mid-market CTOs
  objections:
    - Unpredictable engineering cost & timeline drift
    - Security & legacy ERP integration risk
geography:
  scope: Local + National
  countries: [India]
  regions: [Pune, Mumbai]
  languages: [English]
conversions:
  primary: Technical discovery call bookings
```

## 3. Commercial Keyword & Intent Map

| Keyword | Intent | Volume | Difficulty | Business Relevance | Recommended Action |
|---|---|---:|---:|---|---|
| `custom software development company in pune` | Local / Commercial | Unavailable (No API) | Unavailable | High | Dedicated Pune Service Page (`/services/custom-software-pune`) |
| `enterprise ai integration services` | Commercial | Unavailable | Unavailable | High | Dedicated Service Page (`/services/ai-integrations`) |
| `web application development services` | Commercial | Unavailable | Unavailable | High | Core Service Page (`/services/web-development`) |
| `custom software vs off the shelf erp cost` | Commercial Investigation | Unavailable | Unavailable | High | Comparison Guide (`/insights/custom-software-vs-erp`) linking to scoping CTA |

## 4. Local SEO & Strategy Highlights
- **P0 (Foundation):** Fix Next.js `metadataBase`, canonical URLs, and XML sitemap; add `Organization` + `LocalBusiness` (`ProfessionalService`) + `Service` JSON-LD using verified office details; align Google Business Profile primary category (`Software Company`).
- **P1 (Commercial Pages):** Build dedicated pages for Custom Software, AI Integrations, Web Apps, and Mobile Apps, plus genuinely unique Pune/Mumbai regional case context (zero doorway city clones).
- **P2 (Content & Authority):** Publish architecture trade-off guides, integration security checklists, and original engineering benchmarks linking internally to `/book-discovery-call`.
