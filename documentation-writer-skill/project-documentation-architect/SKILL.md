---
name: project-documentation-architect
description: >-
  Universal Project Documentation Architect Agent Skill. Use when asked to
  inspect a codebase and generate, organize, audit, or maintain compact,
  developer-friendly Markdown documentation across single applications,
  monorepos, microservices, or multiple unrelated projects. Covers repository
  discovery, compact root READMEs, separated per-project docs, Mermaid system
  architecture, API/database/env/deployment guides, developer onboarding,
  change-aware doc updates, and broken-link/accuracy audits.
license: MIT
compatibility: >-
  Compatible with Claude Code, OpenAI Codex, Google Antigravity, Cursor, and
  Agent Skills-compliant runners. Python 3.9+ scripts use standard library only.
metadata:
  author: AgenticLLMSkills
  version: "1.0.0"
  standard: agentskills.io
---

# Project Documentation Architect

Inspect actual codebases and produce **compact, accurate, maintainable Markdown documentation** so a new developer can quickly understand the system, find the right files, run services locally, and ship changes safely. Never write documentation books or invent undocumented behavior.

---

## Core Operating Principles

1. **Fact-checked against real code.** Inspect manifests, entry points, routes, schemas, Dockerfiles, `.env.example`, and scripts before documenting. Never guess commands, ports, env vars, models, or endpoints. Mark unverifiable details explicitly as `Unknown (requires developer confirmation)`.
2. **Minimum useful documentation.** Keep files short, scannable, and high-signal. Link to source files instead of copying code implementations verbatim.
3. **Strict multi-project separation.** Keep the root `README.md` as a compact landing page. Never merge backend, frontend, worker, or unrelated-project details into one giant file.
4. **Never expose secrets.** Document environment variables with safe placeholders only—never real credentials, keys, or tokens.
5. **Preserve accurate docs; update incrementally.** Before writing, inspect existing Markdown files. When code changes, update only affected docs.
6. **Never edit application source code to satisfy doc checks.** Treat documentation audits strictly as read-only inspection of source files and edits to Markdown docs.

---

## Automatic Mode Router (Modes A–G)

Select the workflow automatically from the user's request and load **only** the required references and templates:

| Mode | Trigger / User Request | References to Load | Templates / Scripts |
|---|---|---|---|
| **A. Document New Project** | Undocumented single app or repository | [repository-discovery.md](references/repository-discovery.md), [documentation-standards.md](references/documentation-standards.md), [developer-onboarding.md](references/developer-onboarding.md) | [root-readme.md](templates/root-readme.md), [environment.md](templates/environment.md), `scripts/inspect-repository/` |
| **B. Document Multiple Projects** | Monorepo, microservices, or multiple independent apps in one directory | [repository-discovery.md](references/repository-discovery.md), [multi-project-documentation.md](references/multi-project-documentation.md) | [root-readme.md](templates/root-readme.md), [project-readme.md](templates/project-readme.md), [architecture.md](templates/architecture.md) |
| **C. Document Specific Module** | Request to document an API, database, auth flow, deployment, or service | [api-documentation.md](references/api-documentation.md), [database-documentation.md](references/database-documentation.md), [architecture-documentation.md](references/architecture-documentation.md) | [api.md](templates/api.md), [database.md](templates/database.md), [deployment.md](templates/deployment.md) |
| **D. Update Documentation** | Code/routes/models/env changed; keep docs in sync incrementally | [documentation-maintenance.md](references/documentation-maintenance.md), [documentation-standards.md](references/documentation-standards.md) | Inspect diff first, then `scripts/documentation-audit/` |
| **E. Documentation Audit** | Review existing docs for broken links, duplication, stale commands, missing env | [documentation-maintenance.md](references/documentation-maintenance.md), [documentation-standards.md](references/documentation-standards.md) | `scripts/documentation-audit/audit_docs.py`, `scripts/validate-markdown-links/validate_links.py` |
| **F. Developer Onboarding** | Create or streamline fast new-hire setup path | [developer-onboarding.md](references/developer-onboarding.md) | [root-readme.md](templates/root-readme.md), [environment.md](templates/environment.md), [troubleshooting.md](templates/troubleshooting.md) |
| **G. Architecture Documentation** | Document service boundaries, communication, data/request flows | [architecture-documentation.md](references/architecture-documentation.md), [multi-project-documentation.md](references/multi-project-documentation.md) | [architecture.md](templates/architecture.md) |

---

## Standard Execution Sequence

1. **Discover Topology First:** Run `python scripts/inspect-repository/inspect_repo.py <repo-path>` (or inspect manifests directly) to classify whether the repository is a **single project**, **monorepo / multi-service system**, or **collection of unrelated projects**.
2. **Audit Existing Docs:** Read existing `README.md` and `docs/` files so accurate content is preserved and nothing is duplicated.
3. **Plan Compact Doc Tree:** Decide the smallest helpful set of Markdown files (see [multi-project-documentation.md](references/multi-project-documentation.md)). Create specialized docs (`api.md`, `database.md`, `authentication.md`, `deployment.md`, `troubleshooting.md`) only when complexity warrants them.
4. **Write / Update Incrementally:** Populate only verified commands, relative paths, real directory layouts, safe env placeholders, and purposeful Mermaid diagrams.
5. **Validate Before Finishing:** Run `scripts/validate-markdown-links/validate_links.py` and `scripts/documentation-audit/audit_docs.py` on the repository and present the Quality Report table (`| Check | Status | Details |`).

See [examples/](examples/) for single-app, monorepo, and multi-project worked outputs.

## Token Efficiency

Follow the repository's shared token-efficiency policy.

- Inspect only relevant context.
- Load detailed references on demand.
- Avoid duplicate file reads.
- Minimize unnecessary tool output.
- Preserve critical implementation evidence.
- Never reduce reasoning, accuracy, or verification quality.

Reference: agent-token-efficiency/references/default-policy.md
