# Google Antigravity Token & Context Adapter

Follow Google Antigravity's customization loading and context budgeting model:

- **Rules Scoping (`.agents/rules/*.md`, `AGENTS.md`, `GEMINI.md`, `~/.gemini/config/`):**
  - Keep `always_on` global and workspace rules minimal (strict invariants only), because `always_on` rules consume context on every single turn.
  - Prefer `trigger: model_decision` rules or on-demand Skills (`.agents/skills/<name>/SKILL.md`) for specialized multi-step procedures.
  - Deduplicate shared rules across global `~/.gemini/config/` and workspace `.agents/`.
- **Skills Progressive Disclosure:** Antigravity injects only `name` and `description` at startup and loads `SKILL.md` and `references/` only on activation. Keep `SKILL.md` lean and avoid duplicating `references/` text inside `SKILL.md`.
- **MCP Retrieval:** Antigravity uses lazy schemas (`<appDataDir>/mcp/<serverName>/<toolName>.json`) for lazy MCP tools—inspect only the specific tool JSON needed instead of bulk-reading all schemas.
- **Subagents (`invoke_subagent` / `research`):** Delegate broad multi-file codebase surveys to `research` (or isolated subagents) only when parallelization/isolation reduces main-context clutter; require compact file+line reports rather than full file dumps.
- **Compaction & Parallel Tool Calls:** Call `update_focus` / `update_steps` in parallel alongside tool calls (zero extra turn latency), batch independent `read_file` ranges (`StartLine`/`EndLine` < 150 lines) in parallel, and use `/compact` when sessions grow long.
