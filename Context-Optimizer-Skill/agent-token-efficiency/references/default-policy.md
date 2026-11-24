# Default Token Efficiency Policy (Shared Standard)

All skills and agent workflows in this repository inherit these baseline rules. Load specialized references only when a task requires deeper optimization mechanics.

## 1. Quality First (Non-Negotiable)
- **Optimize information density, not intelligence.** Never skip source-code reading, primary research, security verification, edge-case checks, or tests just to reduce token volume.
- Never downgrade model capability or disable reasoning by default.
- Retrieve additional context immediately whenever missing information threatens correctness.

## 2. Progressive Disclosure & Context Discipline
- Keep `SKILL.md` compact (< 150 lines where practical) and frontmatter descriptions short and trigger-focused.
- Load `references/`, `templates/`, and `examples/` **only** for the active workflow step.
- Before reading a file, ask: *Is it relevant? Can `rg` locate the exact function/lines first? Has it already been read unchanged?*
- Skip generated directories (`node_modules`, `.git`, `dist`, `build`, `.next`, `coverage`, `vendor`, lockfiles) during broad searches unless the task specifically inspects build/dependency artifacts.
- Batch independent file reads and searches in parallel where the agent runtime supports it.

## 3. Tool Output, Search & Retrieval Control
- Use supported quiet/summary CLI flags (`git status --short`, `git diff --stat`, `pytest -q`, `vitest run --reporter=dot`, `npm run lint -- --quiet`—only when actually supported by the tool; never invent flags).
- Always preserve exit codes, relevant warnings, and diagnostic stack traces on failures—never hide test or security errors.
- Use two-step retrieval for docs/web: targeted snippets first; load full documentation only when snippets are insufficient.
- Scope MCP servers and tool discovery to relevant tools only.

## 4. Coding, Subagents, Sessions & Output
- Prefer minimal diffs reusing existing patterns; never regenerate entire large files for a small patch.
- Run risk-based staged tests (affected unit -> relevant integration -> broader regression -> full suite when warranted).
- Delegate to subagents only when parallel investigation or isolation beats coordination cost; pass tight file scopes and require compact structured reports (Findings, Files/Lines, Decisions, Evidence, Risks, Unknowns).
- Reset unrelated sessions where supported; use `.agent/TASK_STATE.md` and `.agent/PROJECT_MAP.md` (verified against real code) for long multi-phase tasks.
- Keep final user replies concise and structured (changes, decisions, files, exact validation results, remaining issues)—do not echo prompts or full files unless requested.
