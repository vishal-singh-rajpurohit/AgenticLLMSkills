# Universal SEO Strategist Agent Skill (`seo-skill`)

A modular, research-driven, cross-platform SEO Agent Skill built to the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`). Compatible with **Claude Code**, **OpenAI Codex**, **Google Antigravity**, **Cursor**, and other Agent Skills-compatible coding agents.

> **Naming note:** The root directory and `SKILL.md` `name` field are both `seo-skill` to satisfy the Agent Skills specification rule that `name` must match its parent folder name.

---

## Capabilities Across the Full SEO Lifecycle

1. **Humanized Business Discovery:** Conversational one-question-at-a-time discovery interview (Stages A–F) preceded by automated pre-research of any supplied website or codebase, plus fast-track execution for scoped technical tasks.
2. **Real Buyer Segmentation & Search Journeys:** Evidence-grounded segmentation replacing fictional personas.
3. **Competitor & Live SERP Analysis:** Direct, search, content, local, and benchmark competitor auditing with citation logs.
4. **Keyword Research, Intent Classification & Clustering:** Anti-cannibalization intent mapping with strict data-integrity rules (zero fabricated volumes or rankings).
5. **Technical & On-Page SEO Audits:** Crawlability, indexing, JS rendering, Core Web Vitals (`LCP`, `INP`, `CLS`), mobile parity, metadata, internal linking, and Schema.org validation aligned with current Google Search Central & Bing Webmaster Guidelines.
6. **Specialized Playbooks:** Local SEO (anti-doorway rules, GBP, `LocalBusiness`), E-Commerce SEO (facets, variants, pagination, OOS lifecycle, `Product` schema), SaaS/B2B SEO (use-case, integration, comparison, free tools, pipeline metrics), Ethical Off-Page/PR, and AI Search Visibility (AI Overviews, AI Mode, Bing Copilot grounding).
7. **Codebase Implementation:** Framework-aware implementation patterns (Next.js App & Pages Router, React, Astro, Nuxt, SvelteKit, Angular, WordPress, static HTML) with safety and approval gates.
8. **Analytics, Drop Diagnostics & Reporting:** Search Console, GA4, CRO audits, structured traffic-drop isolation, and executive monthly reporting.
9. **Zero-Dependency Python Audit Tools:** Standard-library Python 3.9+ scripts for metadata, XML sitemaps, broken links/redirects, JSON-LD structured data, and full repo/URL technical audits.

---

## Repository Structure

```text
seo-skill/
├── SKILL.md                          # Core progressive-disclosure skill entrypoint
├── README.md                         # Setup, usage, and architecture documentation
├── references/                       # 15 domain-specific SEO manuals (loaded on demand)
├── templates/                        # 8 reusable Markdown and CSV deliverable templates
├── scripts/                          # Zero-dependency Python 3.9+ verification tools
│   ├── _shared.py
│   ├── seo-audit/seo_audit.py
│   ├── metadata-check/check_metadata.py
│   ├── sitemap-validation/validate_sitemap.py
│   ├── broken-link-check/check_links.py
│   └── structured-data-validation/validate_jsonld.py
├── examples/                         # Worked local, e-commerce, and SaaS case studies
├── adapters/                         # Claude Code, Codex, Antigravity, and Cursor setup
└── tests/                            # Structure, script workflow, and QA scenario suites
```

---

## Quick Installation

Use the bundled cross-platform installer or copy `seo-skill/` directly into your agent's skill directory:

**Windows (PowerShell):**
```powershell
# Choose: claude | codex | antigravity | cursor
# Scope:  project | global
./seo-skill/adapters/install.ps1 -Target antigravity -Scope project
```

**macOS / Linux (Bash):**
```bash
./seo-skill/adapters/install.sh --target claude --scope project
```

See detailed platform notes in:
- [adapters/claude/README.md](adapters/claude/README.md)
- [adapters/codex/README.md](adapters/codex/README.md)
- [adapters/antigravity/README.md](adapters/antigravity/README.md)
- [adapters/cursor/README.md](adapters/cursor/README.md)

---

## Usage & Example Prompts

- **Full Business SEO Strategy:** *"I run a residential and commercial solar installation company in Pune. Help me build an SEO strategy from scratch."* (Triggers pre-research + humanized Stage A discovery.)
- **Technical & Codebase Audit:** *"Audit this Next.js repository for metadata, canonicals, robots, sitemap, and JSON-LD issues, then show me proposed fixes."* (Fast-tracks codebase inspection + `scripts/seo-audit/seo_audit.py`.)
- **Traffic Drop Diagnosis:** *"Our organic clicks dropped 35% over the last 3 months. Help diagnose why using these Search Console and GA4 exports."* (Triggers `references/analytics-and-reporting.md` diagnostic tree.)
- **Content Brief & Cluster Plan:** *"Build an intent-mapped keyword cluster and content brief for our SaaS HubSpot integration page."*

---

## Validation & Tests

Run all automated tests (zero third-party test packages required):

```bash
python seo-skill/tests/run_tests.py -v
```
