# Cursor Token & Context Adapter

Follow Cursor's native Skills and Rules architecture cleanly:

- **Skills (`.cursor/skills/` & `.agents/skills/`):** Place `SKILL.md` workflows inside `.cursor/skills/<name>/` or `.agents/skills/<name>/` so instructions load dynamically on demand rather than permanently sitting in always-on context.
- **Scoped Rules (`.cursor/rules/*.mdc`):** Use `globs` (e.g., `frontend/**/*.tsx` or `backend/prisma/*`) instead of `alwaysApply: true` for domain-specific rules so backend rules never inflate frontend edits.
- **Avoid Rule/Skill Duplication:** Do not mirror the same guidance across `.cursorrules`, `.cursor/rules/`, `AGENTS.md`, and `SKILL.md`. Keep one canonical source per rule.
- **Targeted Indexing & Context:** Exclude generated build directories cleanly via `.cursorignore` alongside `.gitignore`, and reference exact files/symbols (`@file` / targeted line reads) rather than dumping entire directories.
