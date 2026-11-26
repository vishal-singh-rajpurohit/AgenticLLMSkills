# Business & Audience Discovery

Build a **verified Business SEO Profile** grounded in real offerings, buyer economics, and customer language—never invented personas or assumed demographics.

## Pre-Interview Inspection Checklist

Before asking the user anything about an existing site or repository:
- Fetch or inspect homepage, pricing, service/product pages, about/contact pages, `robots.txt`, and `sitemap.xml`.
- Detect tech stack (`package.json`, CMS files, `wp-content`, Shopify Liquid, Astro/Next.js routes).
- Extract stated value propositions, cities/countries mentioned, customer logos/proof, and conversion CTAs.

---

## Information to Uncover Across Existing vs. New Sites

| Dimension | Existing Websites | New Websites |
|---|---|---|
| **Business Identity** | Core offerings, highest-margin services/products, real differentiators, B2B/B2C/SaaS/local/ecom model | Positioning, planned core offerings, initial revenue wedge, differentiation |
| **Target Audience** | Verified buyer segments, B2B roles/titles, technical fluency, objections, questions sales/support hear | Target customer segments, urgent pain points, buying triggers, awareness stage |
| **Geography & Languages** | Countries, priority cities/regions, local vs. national vs. international reach, languages | Launch market, city/regional vs. national rollout sequence, language requirements |
| **Customer Acquisition** | Primary conversion (demos, quotes, calls, signups, purchases) + multi-step buyer journey | Target conversion actions + realistic funnel milestones |
| **Website & Data Access** | URL, platform/CMS, main landing pages, traffic sources, current SEO/rankings, GSC & GA4 access | Planned URL hierarchy, core landing pages to launch first, known rivals |

---

## Verified Business SEO Profile Contract

Compile answers into [../templates/business-profile.md](../templates/business-profile.md) using structured YAML containing **only verified or user-confirmed data** (mark missing/unverified fields explicitly as `unavailable` or `pending-confirmation`):

```yaml
business:
  name: Example Business
  type: B2B SaaS
  industry: Software
  website_url: https://example.com # or new-website
  platform: Next.js
  products:
    - Project management software

audience:
  primary: Small businesses
  secondary: Freelancers
  technical_level: Non-technical operations leads
  objections:
    - Migration effort from spreadsheets

geography:
  scope: National
  countries:
    - India
  languages:
    - English

objectives:
  - Organic traffic
  - Qualified leads
  - Product signups

conversions:
  primary: Demo bookings
  secondary:
    - Registrations
```

Never lock strategy until the user confirms or corrects this profile.
