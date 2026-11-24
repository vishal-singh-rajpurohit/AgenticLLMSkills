# Worked Example: AI Email Automation SaaS (Test 3 — CMS Publishing)

*(Demonstrates B2B pain-point research, educational article connected to product features, and headless CMS publication.)*

---

## 1. Research & Editorial Framing

- **Target Segment:** B2B RevOps and outbound growth leads seeing falling cold-email reply rates and domain spam placement.
- **Primary Sources Cited:** Google Bulk Sender Guidelines & Yahoo Sender Best Practices (SPF, DKIM, DMARC alignment, one-click unsubscribe, spam complaint threshold `< 0.3%`).
- **Editorial Angle:** Step-by-step deliverability checklist before scaling AI personalization—explaining why AI personalization fails if DNS authentication and sending cadence fail first.
- **Verified Internal Links (Existing SaaS Pages):**
  - `/features/inbox-deliverability-monitor` (*"automated SPF/DKIM/DMARC monitoring"*)
  - `/features/ai-sequence-personalization` (*"conditional AI follow-up workflows"*)
  - `/pricing` (*"compare sending tier limits"*)

---

## 2. CMS Workflow & Metadata

- **Detected CMS:** Directus / Sanity headless CMS with `article` collection (`draft` -> `published` workflow + webhook revalidation).
- **Metadata Preview:**
  - Title: `Email Deliverability Checklist Before Scaling AI Outbound Sequences`
  - Schema.org: `Article` + `BreadcrumbList` using verified real author profile and `Organization` publisher.
- **Approval & Publish:** Previewed in full with primary citation URLs and diagram manifest; published via authorized CMS draft->publish endpoint only upon explicit user sign-off.
