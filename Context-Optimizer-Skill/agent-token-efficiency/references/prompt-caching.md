# Prompt Caching & Token Telemetry

**Critical Distinction:** Prompt caching reduces repeated input **processing cost and latency (TTFT)**—it does **not** reduce the context window size or prevent context-rot when irrelevant data fills the prompt.

## Prefix-Caching Engineering Rules (API & Runtime Agents)

Prompt caches rely on exact prefix matching from token 0:
1. **Static first, dynamic last:** Place unchanging system prompts, tool definitions, `AGENTS.md`/`CLAUDE.md` rules, and stable reference schemas at the very start of the prompt. Place dynamic timestamps, user queries, and volatile diffs at the end.
2. **Keep tool definitions deterministic:** Never dynamically reorder, inject, or mutate tool schemas mid-session unless required—any edit at the tool layer invalidates the entire downstream KV cache.
3. **Append-only history:** Append new tool results and turns rather than mutating earlier messages mid-task.
4. **Use supported cache breakpoints thoughtfully:** Where an API uses explicit breakpoints (e.g., Anthropic `cache_control: {"type": "ephemeral"}`), place them at stable boundaries (end of system prompt/tools, end of stable repo prefix).
5. **Evaluate compaction vs. cache breaks:** Compaction resets the prefix (causing a one-time uncached write/miss) in exchange for reclaiming context room on long tasks—never rewrite prefixes unnecessarily on short tasks.
6. **IDE boundary:** Coding IDEs (Cursor, Antigravity desktop, Claude Code CLI, Codex CLI) manage their own harness prefixes internally. Only configure cache parameters when building or running API-based agent harnesses that expose them.

---

## Official Provider Usage Fields (API Accounting)

When measuring actual API usage (never fabricate telemetry when unexposed by an IDE):
- **Anthropic:** `usage.input_tokens`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens`, `usage.output_tokens`.
- **OpenAI:** `usage.prompt_tokens` (or `input_tokens`), `usage.prompt_tokens_details.cached_tokens` (`input_tokens_details.cached_tokens`), `usage.completion_tokens`.
- **Google Gemini:** `usage_metadata.prompt_token_count`, `usage_metadata.cached_content_token_count`, `usage_metadata.candidates_token_count`, `usage_metadata.total_token_count` (and `thoughts_token_count` when reasoning tokens are exposed).

Use `python scripts/estimate-text-tokens.py --usage-json <response.json>` to summarize real API usage cleanly, and label character-based file estimates explicitly as approximations.
