# Universal Content Research, Writing & Publishing Skill (`content-research-writer`)

A production-ready, cross-agent skill built on the [Agent Skills specification](https://agentskills.io) (`SKILL.md`). Compatible with **Claude Code**, **OpenAI Codex**, **Google Antigravity**, **Cursor**, and any Agent Skills-compatible coding environment.

---

## Core Lifecycle Capabilities

1. **Humanized Business & Editorial Discovery:** Inspects supplied websites/codebases first, then conducts a conversational one-question-at-a-time discovery interview (business, audience, objectives, brand voice, first-hand expertise).
2. **Investigative Research & Competitor Analysis:** Maps search intent, audits competing content without copying, logs verified primary sources with dates, and flags unconfirmed claims (`[NEEDS SME VERIFICATION]`).
3. **Editorial Planning & Humanized Writing:** Transparent topic opportunity scoring, natural human prose without AI cliché filler, and dedicated blueprints across educational guides, how-tos, service pages, product copy, case studies, comparisons, and news updates.
4. **Visual Asset Research & Licensing:** Prioritizes user/original assets, verifies Unsplash/Pexels/Wikimedia Commons/official vendor licenses, bans blind hotlinking, enforces descriptive filenames/WebP/alt text, and adapts storage to static folders or existing CMS media adapters.
5. **Mandatory Preview & Explicit Approval Workflow:** Presents full content, metadata, images, internal/external links, and exact code/DB changes via [templates/approval-summary.md](templates/approval-summary.md)—never auto-publishing or silently overwriting existing pages.
6. **Dual Publishing Architecture:**
   - **Database / CMS:** Inspects Prisma, Drizzle, Mongoose, WordPress, Directus, Strapi, Sanity, Payload, or custom APIs; respects existing models, draft/publish states, auth, transactions, and cache revalidation (`revalidatePath` / `revalidateTag`).
   - **Static / Source Code:** Implements into Next.js (MDX/App/Pages), Astro, Gatsby, Nuxt, SvelteKit, Hugo, or HTML reusing existing layouts, updating listings/sitemaps, and running build + validation checks.
7. **Search Discoverability & Performance Loops:** Validates metadata, Schema.org JSON-LD, XML sitemaps, `robots.txt`, internal links, and post-publish live URL resolution.

---

## Repository Structure

```text
content-research-writer/
├── SKILL.md                           # Core progressive-disclosure router & safety rules
├── README.md                          # Documentation & installation guide
├── references/                        # 15 domain references (loaded on demand)
├── templates/                         # 8 reusable briefs, outlines, previews, and reports
├── scripts/                           # Zero-dependency Python 3.9+ validation CLIs
│   ├── _shared.py
│   ├── validate-content/validate_content.py
│   ├── validate-links/validate_links.py
│   ├── validate-metadata/validate_metadata.py
│   ├── validate-images/validate_images.py
│   ├── validate-structured-data/validate_structured_data.py
│   └── validate-sitemap/validate_sitemap.py
├── examples/                          # Worked workflows for Tests 1–6
├── adapters/                          # Claude Code, Codex, Antigravity, and Cursor installers
└── tests/                             # Automated tests across all 6 test categories
```

---

## Installation

**PowerShell (Windows):**
```powershell
./content-writer-skill/content-research-writer/adapters/install.ps1 -Target antigravity -Scope project
```

**Bash (macOS / Linux):**
```bash
./content-writer-skill/content-research-writer/adapters/install.sh --target claude --scope project
```

See detailed guides in:
- [adapters/claude/README.md](adapters/claude/README.md)
- [adapters/codex/README.md](adapters/codex/README.md)
- [adapters/antigravity/README.md](adapters/antigravity/README.md)
- [adapters/cursor/README.md](adapters/cursor/README.md)

---

## Validation & Tests

Run all automated test suites (Python 3.9+ standard library only):

```bash
python content-writer-skill/content-research-writer/tests/run_tests.py -v
```
