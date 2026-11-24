# Context Management & Selective File Reading

Control what enters the context window before calling tools so high-signal code and requirements occupy the working budget.

## 1. Progressive Disclosure Structure

Keep every skill lightweight at discovery time:
- **`SKILL.md`:** Short trigger description (1–3 crisp sentences) + mode/workflow routing table + critical invariants.
- **`references/`:** Deep procedures loaded **only** when that specific workflow is invoked.
- **`templates/` & `examples/`:** Loaded only when formatting outputs or onboarding to an edge pattern.
- **Avoid duplication:** Never paste handbook rules into global `CLAUDE.md`/`AGENTS.md` when a skill reference owns them.

---

## 2. Six-Question Context Relevance Gate

Before calling `read_file` (or `cat`/viewer tools):
1. Is this file directly relevant to the current task?
2. What exact symbol, schema, or behavior do I need from it?
3. Can `rg -n` locate the exact line range first?
4. Do I need the whole file, or just lines `N..M` around the target symbol?
5. Was this exact file already read and unchanged in this session?
6. Is there a more authoritative source (e.g., actual `prisma/schema.prisma` vs an older doc)?

Never repeat architecture explanations already established in the active session.

---

## 3. Targeted Repository Discovery

Start with compact orientation commands rather than recursive tree dumps:
- Check CWD, `git status --short`, `git diff --stat`, `git diff --name-only`, `git log -n 5 --oneline`.
- Inspect project manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`) and root index/instruction files (`README.md`, `CLAUDE.md`, `AGENTS.md`, `.agent/PROJECT_MAP.md`).
- Use targeted searches (`rg --files`, `rg -n "<symbol>"`).

### Default Search Exclusions
Exclude noisy generated directories during broad discovery:
`node_modules`, `.git`, `dist`, `build`, `.next`, `out`, `coverage`, `vendor`, `__pycache__`, `.venv`, binary assets, and multi-megabyte lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) when manifest dependencies suffice.

**Safety override:** Never assume an excluded file is irrelevant if the user specifically asks to debug lockfile resolution, compiled output, or build artifacts—inspect it directly when required.

---

## 4. Targeted Reading & Parallel Batching

- Read specific functions, classes, types, interfaces, and route handlers in bounded line ranges. Preserve exact signatures, types, and error paths.
- When multiple independent reads or searches are predictable, plan them together and execute in **parallel** using the host agent's supported multi-tool call mechanism—avoid massive 25-file dumps that blow out context, and avoid slow one-by-one sequential reads when paths are already known.
