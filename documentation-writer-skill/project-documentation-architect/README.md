# Project Documentation Architect (`project-documentation-architect`)

A modular, cross-agent skill built to the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`). Compatible with **Claude Code**, **OpenAI Codex**, **Google Antigravity**, **Cursor**, and any Agent Skills-compatible coding environment.

---

## What It Does

1. **Selective Repository Discovery:** Detects whether a repository holds a single application, a coupled monorepo/multi-service architecture, or multiple completely unrelated projects—capturing languages, frameworks, entry points, databases, `.env.example` keys, Docker/CI files, and verified scripts.
2. **Compact Root README + Strict Multi-Project Separation:** Generates a concise root landing page and keeps frontend, admin, backend, worker, shared package, and standalone project docs cleanly isolated.
3. **Technical Modules & Onboarding:** Creates `architecture.md` (with Mermaid diagrams), `api.md`, `database.md`, `authentication.md`, `environment.md`, `deployment.md`, `development.md`, and `troubleshooting.md` only when warranted—never copying source code verbatim or exposing secrets.
4. **Change-Aware Maintenance & Quality Audits:** Inspects recent code modifications to update only impacted docs, flags unverified commands or missing `.env.example` variables, and validates relative Markdown links and heading anchors.

---

## Repository Structure

```text
project-documentation-architect/
├── SKILL.md                           # Core progressive-disclosure skill entrypoint
├── README.md                          # Documentation, installation, and tests
├── references/                        # 8 modular documentation & maintenance guides
├── templates/                         # 8 reusable Markdown templates
├── scripts/                           # Zero-dependency Python 3.9+ CLI tools
│   ├── _shared.py
│   ├── inspect-repository/inspect_repo.py
│   ├── validate-markdown-links/validate_links.py
│   └── documentation-audit/audit_docs.py
├── examples/                          # Single-project, monorepo, and multi-project examples
├── adapters/                          # Claude Code, Codex, Antigravity, Cursor installers
└── tests/                             # Automated tests across Scenarios 1–5
```

---

## Installation

**PowerShell (Windows):**
```powershell
./documentation-writer-skill/project-documentation-architect/adapters/install.ps1 -Target antigravity -Scope project
```

**Bash (macOS / Linux):**
```bash
./documentation-writer-skill/project-documentation-architect/adapters/install.sh --target claude --scope project
```

See agent-specific guides in:
- [adapters/claude/README.md](adapters/claude/README.md)
- [adapters/codex/README.md](adapters/codex/README.md)
- [adapters/antigravity/README.md](adapters/antigravity/README.md)
- [adapters/cursor/README.md](adapters/cursor/README.md)

---

## Usage & CLI Scripts

- **Inspect any repository:**
  `python documentation-writer-skill/project-documentation-architect/scripts/inspect-repository/inspect_repo.py <repo-path>`
- **Validate Markdown links & anchors:**
  `python documentation-writer-skill/project-documentation-architect/scripts/validate-markdown-links/validate_links.py <repo-path>`
- **Run full documentation quality audit:**
  `python documentation-writer-skill/project-documentation-architect/scripts/documentation-audit/audit_docs.py <repo-path>`

---

## Running Tests

```bash
python documentation-writer-skill/project-documentation-architect/tests/run_tests.py -v
```
