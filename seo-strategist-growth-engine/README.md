# Universal SEO Strategist & Content Growth Engine (`seo-strategist-growth-engine`)

A portable, research-driven, end-to-end SEO Agent Skill built to the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`). Designed for **Claude Code**, **OpenAI Codex**, **Google Antigravity**, **Cursor**, and any compatible Agent Skills runner.

---

## Core Lifecycle & Architecture

1. **Tool & Plugin Discovery (`integrations/`):** Inspects active SEO MCP servers (e.g., Semrush), Search Console, GA4, PageSpeed Insights, sibling `content-research-writer`, and local scripts first—producing a Capability Matrix without duplicating existing tools.
2. **Conversational Discovery (`Mode A`):** Inspects supplied URLs/repos first, then conducts a progressive one-question-at-a-time interview to build a confirmed YAML Business SEO Profile (works for both existing and new websites).
3. **Research & Strategy (`Modes C–E`):** Runs independent SERP/competitor research or provider adapters, classifies search intent, clusters keywords without cannibalization, scores opportunities transparently, and creates a phased P0–P2 roadmap.
4. **Humanized Content & Codebase Implementation (`Modes F–G`):** Delegates to sibling `content-research-writer` when available or runs a built-in 9-step preview-approved workflow; implements Next.js, static, or CMS SEO changes safely with production-build checks.
5. **Technical Audits & Controlled Ranking Experiments (`Modes B, H–J`):** Zero-dependency Python 3.9+ audit CLIs verify sitemaps, metadata, broken links/orphans, and JSON-LD; ranking experiments separate GSC average position from geo-pinned trackers and report `inconclusive` honestly when windows or baselines are insufficient.

---

## Directory Layout

```text
seo-strategist-growth-engine/
├── SKILL.md                          # Compact progressive-disclosure router
├── README.md                         # Installation & usage documentation
├── references/                       # 13 on-demand SEO domain guides
├── templates/                        # 7 structured YAML/Markdown deliverable templates
├── scripts/                          # Zero-dependency Python 3.9+ audit & evaluation CLIs
│   ├── _shared.py
│   ├── sitemap-audit/audit_sitemap.py
│   ├── metadata-audit/audit_metadata.py
│   ├── broken-link-audit/audit_links.py
│   ├── structured-data-validation/validate_structured_data.py
│   └── technical-seo-audit/
│       ├── run_technical_audit.py
│       └── seo_metrics.py
├── integrations/                     # Tool discovery engine & provider adapters
├── examples/                         # Scenarios 1–6 (IT agency, e-com, SaaS, local/new/experiment)
├── adapters/                         # Claude Code, Codex, Antigravity, Cursor installers
└── tests/                            # Automated verification suites
```

---

## Installation

**Windows (PowerShell):**
```powershell
# Target: claude | codex | antigravity | cursor
# Scope:  project | global
./seo-strategist-growth-engine/adapters/install.ps1 -Target antigravity -Scope project
```

**macOS / Linux (Bash):**
```bash
./seo-strategist-growth-engine/adapters/install.sh --target claude --scope project
```

Platform-specific instructions:
- [Claude Code](adapters/claude/README.md)
- [OpenAI Codex](adapters/codex/README.md)
- [Google Antigravity](adapters/antigravity/README.md)
- [Cursor](adapters/cursor/README.md)

---

## CLI Quick Checks & Tests

```bash
# Discover connected SEO tools & build capability matrix
python seo-strategist-growth-engine/scripts/technical-seo-audit/run_technical_audit.py --discover-tools

# Run full technical audit on a local repository or live URL
python seo-strategist-growth-engine/scripts/technical-seo-audit/run_technical_audit.py <repo-or-url>

# Run automated verification suites (Python 3.9+ stdlib only)
python seo-strategist-growth-engine/tests/run_tests.py -v
```
