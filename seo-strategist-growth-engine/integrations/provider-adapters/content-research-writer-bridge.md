# Content Research Writer Integration Bridge

Use this bridge whenever the sibling **`content-research-writer`** skill (`content-writer-skill/content-research-writer/` in this repository, or installed in `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, `.codex/skills/`) is available. Do not duplicate its drafting, image-licensing, and CMS publishing machinery inside `seo-strategist-growth-engine`.

---

## 1. Detection Check

Verify availability before Mode F (`SEO Content Writer`) or Mode I (`Content Refresh`):
- Check workspace path `content-writer-skill/content-research-writer/SKILL.md` or active skill directories for `content-research-writer`.
- If absent, execute the built-in 9-step workflow in [../../references/content-strategy.md](../../references/content-strategy.md).

---

## 2. Handoff Contract (`seo-strategist-growth-engine` -> `content-research-writer`)

Pass a compact structured brief (via [../../templates/content-brief.md](../../templates/content-brief.md)) containing only verified context so `content-research-writer` skips redundant discovery questions:
1. **Verified Business Profile:** Brand, offer, buyer segment, technical level, geography, conversion CTA.
2. **Keyword Cluster & Intent:** Primary keyword, supporting terms, dominant SERP intent, target URL slug (new or existing refresh).
3. **Competitor Gap Evidence:** Inspected competing URLs + concrete differentiation angles.
4. **Technical & Internal Linking Constraints:** Verified real target URLs to link to, eligible Schema.org types, and whether the site is Next.js/Astro/WordPress/CMS/static.
5. **Approval Rule:** Require `content-research-writer` Mode G (`Preview`) and explicit user sign-off before any write/publish action.

---

## 3. Return Loop (`content-research-writer` -> `seo-strategist-growth-engine`)

Once `content-research-writer` completes Mode H/I (Publish & Verify):
1. Re-run `scripts/technical-seo-audit/run_technical_audit.py` on affected routes/sitemaps.
2. Capture pre/post details inside [../../templates/ranking-experiment.md](../../templates/ranking-experiment.md) to monitor indexing, impressions, clicks, and conversions via Mode H.
