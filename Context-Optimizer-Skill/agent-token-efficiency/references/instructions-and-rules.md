# Instructions & Rules Optimization

Global and always-loaded instruction files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md`, `.cursor/rules/*`) run on every turn. Bloated, duplicated, or misplaced instructions silently tax every prompt.

## Rules vs. Skills Separation

| Keep in Permanent Rules (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`) | Move into On-Demand Skills (`skills/*/SKILL.md` + `references/`) |
|---|---|
| Hard security & approval boundaries | Multi-step SEO, content, or audit playbooks |
| Core architectural invariants & build/test commands | Code review, deployment, or PR checklists |
| Directory-scoped coding/API conventions | Framework migration guides & templates |
| Compact pointers to canonical docs | Extensive worked examples & reference manuals |

---

## Instruction Audit Checklist

Inspect existing root, global, and nested instruction files (via `scripts/audit-instructions.py` and `scripts/find-duplicate-docs.py`) to spot:
1. **Duplicate rules** copied across `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and multiple `SKILL.md` files.
2. **Repeated architecture explanations** that belong in one canonical `docs/architecture.md` or `.agent/PROJECT_MAP.md`.
3. **Conflicting directives** between global rules and directory-level rules.
4. **Oversized always-loaded files** (> ~200–250 lines at root or > ~150 lines in `SKILL.md`).
5. **Directory misplacement** (e.g., frontend styling rules loaded inside backend-only directories).

### Optimization Rule
Never delete safety, security, or behavioral constraints blindly to hit a smaller byte target. Audit each directive's purpose first, deduplicate into one canonical location, and keep always-on root rules crisp and minimal.
