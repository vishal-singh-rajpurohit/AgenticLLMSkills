# OpenAI Codex Token & Context Adapter

Follow OpenAI Codex native conventions cleanly:

- **`AGENTS.md` & Directory Overrides:** Keep root `AGENTS.md` minimal (build, test, invariants) and place package/service-specific rules inside nested `<app>/AGENTS.md` files rather than repeating all instructions at root and nested levels.
- **Prompt Caching Prefix Stability:** Keep `AGENTS.md` and static system/tool setups invariant across turns so Codex KV prefix caching (`usage.input_tokens_details.cached_tokens` / `prompt_tokens_details.cached_tokens`) hits consistently; avoid inserting dynamic timestamps or shifting preamble text at the start of prompts.
- **Skills Discovery (`.agents/skills/` & `~/.codex/skills/`):** Codex indexes only skill paths, names, and descriptions initially (~8,000 char / 2% context budget heuristic)—keep `SKILL.md` descriptions crisp and move large manuals into `references/`.
- **Parallel Tool Calls:** Batch independent read/search calls in one turn where supported; keep search scopes narrow with `rg`.
- **Compact Terminal Outputs & Session Compaction:** Prefer summary flags (`git diff --stat`, `pytest -q`). When long sessions compact, persist key task invariants and active file lists in `.agent/TASK_STATE.md` so critical checklists survive compaction cleanly.
- **Tool Discovery:** Enable only relevant MCP servers in Codex config to limit idle tool schema overhead.
