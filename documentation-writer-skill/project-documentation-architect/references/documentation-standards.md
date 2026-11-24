# Documentation Writing Standards

Good engineering documentation minimizes time-to-first-working-change. Write concisely, verify every fact, and organize for rapid scanning.

## Writing Principles

- **Plain, direct language:** Short sentences and short paragraphs (2–4 lines max). Cut empty intros (*"Welcome to the future of..."*).
- **Clear visual hierarchy:** Logical `H1` -> `H2` -> `H3` structure; never bury key setup commands deep inside prose.
- **Compact Markdown:** Use tables for structured comparisons (env vars, apps table, endpoints summary, troubleshooting matrix)—not for padding single-sentence facts.
- **Purposeful Mermaid diagrams:** Use `flowchart` / `sequenceDiagram` only when relationships or multi-hop flows are genuinely clearer visually than a 3-bullet list. Quote labels containing parentheses, slashes, or brackets (`svc["API Gateway (Node.js)"]`).
- **Source links over code dumps:** Point developers to `[schema.prisma](../../backend/prisma/schema.prisma)` or `[routes.ts](src/routes.ts)` rather than pasting 150 lines of code that immediately go stale.
- **Zero duplication:** Explain a system flow, env table, or command sequence in **one** canonical doc and link to it from everywhere else.

---

## Anti-Patterns to Reject

- Writing a 600-line root `README.md` covering every folder, endpoint, and table.
- Documenting every single `.ts`/`.py` helper file when a concise folder-level tree explains responsibilities cleanly.
- Listing guessed commands (`npm run lint` when `package.json` has no `lint` script) or unverified ports.
- Repeating the exact same project overview paragraph in `README.md`, `architecture.md`, and `development.md`.
- Including actual API keys, database URLs with passwords, JWT secrets, or real production credentials instead of placeholders (`postgres://user:password@localhost:5432/app_db`).

---

## Per-Project README Essentials (Include Only What Applies)

1. **Project overview:** Purpose, responsibilities, core stack, dependencies on sibling projects.
2. **Getting started:** Exact prerequisites, install, dev, build, and test commands verified from repo manifests.
3. **Directory structure:** Important top-level source directories and what each owns.
4. **Application workflow:** 3–6 bullet trace from entry point to core execution path.
5. **Important modules & related docs:** Relative links to `api.md`, `database.md`, `environment.md`, or sibling services.
