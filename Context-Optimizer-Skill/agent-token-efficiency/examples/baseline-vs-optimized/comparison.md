# Baseline vs. Optimized Audit & Workflow Comparison

*(Grounded in actual workspace audit measurements via `scripts/audit-instructions.py`, `scripts/audit-skill-references.py`, `scripts/find-duplicate-docs.py`, and `scripts/estimate-text-tokens.py`.)*

## 1. Repository Instruction & Skill Audit (Before vs. After)

| Measurement | Baseline (Pre-Integration) | Optimized (Post-Integration) | Notes |
|---|---|---|---|
| **Always-loaded root instruction tokens** | `~0` approx | `~0` approx (no bloated root rules; `.agent/PROJECT_MAP.md` is on-demand `~220` approx tokens) | Kept root clean; avoided copying handbooks into `AGENTS.md`/`CLAUDE.md` |
| **Skills audited** | `4` | `4` | `seo-skill`, `content-research-writer`, `project-documentation-architect`, `agent-token-efficiency` |
| **Skills referencing shared `default-policy.md`** | `1 / 4` | `4 / 4` | Added 11-line shared policy pointer (`~55` approx tokens) instead of duplicating `~440`-token handbook per skill (`~1,150+` approx tokens saved if duplicated across 3 sibling skills) |
| **Duplicate multi-file Markdown blocks** | `0` | `0` | Zero repeated architecture/rule blocks across `143` scanned Markdown files |
| **Largest `SKILL.md` size** | `106` lines (`9,334` bytes) | `119` lines (`9,720` bytes) | All 4 `SKILL.md` entrypoints remain compact (`63–119` lines; `agent-token-efficiency/SKILL.md` is `63` lines / `~1,056` approx tokens) |

> **Measurement disclosure:** Token counts above use the script heuristic (`chars / 4`) and are **approximations**, not exact provider tokenizer counts. Actual model API token telemetry requires API response usage objects (`--usage-json`).

## 2. Representative Workflow Efficiency Pattern (Monorepo / Multi-File Tasks)

- **Unoptimized pattern:** Run broad recursive listings across `node_modules`/`.next`, read 6 full reference files + entire large `SKILL.md` upfront, re-read unchanged manifests, run verbose test reporters, and echo full files in final reply.
- **Optimized pattern (`agent-token-efficiency`):** Read `.agent/PROJECT_MAP.md` or run `rg --files` / `inspect_repo.py` once -> batch targeted `read_file` line ranges in parallel -> run quiet summary flags (`git status --short`, `pytest -q`, `--format json` filtered checks) while expanding full traces only on error -> emit concise structured summary with clickable links.
