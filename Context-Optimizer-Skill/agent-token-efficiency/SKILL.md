---
name: agent-token-efficiency
description: >-
  Universal AI Agent Token Efficiency and Context Engineering Skill. Use to
  optimize context density, progressive disclosure, targeted repository
  discovery, quiet tool/MCP output, instruction deduplication, prompt caching,
  selective subagent delegation, session compaction, and automated instruction
  audits across Claude Code, OpenAI Codex, Google Antigravity, and Cursor—while
  strictly preserving reasoning quality, research depth, security checks, and
  verification accuracy.
license: MIT
compatibility: >-
  Compatible with Claude Code, OpenAI Codex, Google Antigravity, Cursor, and
  Agent Skills-compliant runners. Python 3.9+ audit scripts use standard library
  only.
metadata:
  author: AgenticLLMSkills
  version: "1.0.0"
  standard: agentskills.io
---

# Universal AI Agent Token Efficiency Engineer

**Core Principle:** Optimize **information density, not intelligence**. Remove irrelevant context, duplicated rules, bloated tool outputs, and redundant turns while preserving every piece of evidence, reasoning, security check, and test verification needed for a correct result. Quality always overrides token savings.

---

## Non-Negotiable Safeguards

Never save tokens by:
- Downgrading to a weaker model by default or disabling reasoning.
- Skipping source-code inspection, research, edge cases, security checks, or tests.
- Replacing verified evidence with guesses or lossy summaries of critical signatures/types.
- Claiming exact token counts from character heuristics or unexposed platform telemetry.

---

## On-Demand Reference Router (Load Only What Applies)

| Area | When to Load | Reference |
|---|---|---|
| **Shared Default Policy** | Referenced as baseline by all workspace skills | [default-policy.md](references/default-policy.md) |
| **Context & File Reading** | Repo discovery, `rg`/`git` filtering, selective reads, batching | [context-management.md](references/context-management.md) |
| **Tool & MCP Output** | Quiet CLI flags, error summaries, scoped MCP discovery | [tool-output-optimization.md](references/tool-output-optimization.md) |
| **Search & Docs Retrieval** | Two-step snippet-first retrieval, versioned primary docs | [search-and-retrieval.md](references/search-and-retrieval.md) |
| **Rules & Instructions** | Auditing `CLAUDE.md`/`AGENTS.md`/`GEMINI.md`/Skills overlap | [instructions-and-rules.md](references/instructions-and-rules.md) |
| **Prompt Caching** | Prefix ordering, breakpoints, API usage accounting | [prompt-caching.md](references/prompt-caching.md) |
| **Subagent Delegation** | When to fan out vs stay sequential, 6-part compact reports | [subagent-optimization.md](references/subagent-optimization.md) |
| **Long Tasks & Compaction** | `.agent/TASK_STATE.md`, `.agent/PROJECT_MAP.md`, resets | [session-and-long-tasks.md](references/session-and-long-tasks.md) |
| **Coding, Testing & Output** | Minimal diffs, 4-stage risk testing, concise final replies | [coding-and-testing-efficiency.md](references/coding-and-testing-efficiency.md) |
| **Quality & A/B Evals** | Baseline vs optimized evaluation, regression rollback gate | [quality-evaluation.md](references/quality-evaluation.md) |
| **Platform Adapters** | Claude Code / Codex / Antigravity / Cursor specifics | [references/adapters/](references/adapters/) |

---

## Automated Audit Scripts (Read-Only by Default)

Run zero-dependency stdlib tools in `scripts/` (all support `--dry-run` / non-mutating reporting):
- `python scripts/audit-instructions.py <repo-path>` — Inspect instruction files, size budgets, and progressive-disclosure gaps.
- `python scripts/estimate-text-tokens.py <path-or-text>` — Report byte/char/word counts and clearly labeled approximate tokens (`--usage-json` for actual API telemetry).
- `python scripts/find-duplicate-docs.py <repo-path>` — Detect repeated paragraphs and duplicated architecture docs across Markdown files.
- `python scripts/audit-skill-references.py <repo-path>` — Validate skill compactness, `references/` separation, and shared policy adoption.
- `python scripts/validate-optimization-config.py <repo-path>` — Verify `.agent/` indexes, frontmatter limits, and cross-skill policy integrity.
