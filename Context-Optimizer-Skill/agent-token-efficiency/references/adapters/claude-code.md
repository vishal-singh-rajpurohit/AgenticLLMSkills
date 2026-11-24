# Claude Code Token & Context Adapter

Follow these Claude Code-native practices without mixing other platforms' configuration syntax:

- **`CLAUDE.md` Hygiene:** Keep project-root `CLAUDE.md` concise (~150–250 lines) containing build/test commands, invariants, and `# Compact instructions` guiding what `/compact` must keep. Put subdir rules in subdir `CLAUDE.md` files and multi-step workflows in `.claude/skills/<name>/SKILL.md`.
- **Context Inspection (`/context`):** Run `/context` when responses degrade or sessions grow long to inspect system prompt, memory, file reads, and conversation usage.
- **Session Isolation (`/clear`):** Run `/clear` (aliases `/reset`, `/new`) when switching to an unrelated task so old logs do not pollute new work (`CLAUDE.md` reloads cleanly from disk).
- **Focused Compaction (`/compact`):** Run `/compact <focus>` mid-task to compress history while retaining critical constraints, changed files, and open failures (e.g., `/compact Keep auth middleware changes and failing integration tests`).
- **Skills & Subagents:** Keep `SKILL.md` descriptions tight (loaded at startup); use dedicated `.claude/agents/` subagents only for parallel/isolated investigations returning structured findings.
- **Quiet CLI Usage:** Use `git status --short`, `git diff --stat`, `pytest -q`, or supported quiet flags; expand full logs on failures.
