# Project Map — AgenticLLMSkills

*(Compact navigation index for coding agents; verify exact details against live files before editing.)*

## Skill Packages

| Skill Name | Directory | Scope | Entry Point |
|---|---|---|---|
| `agent-token-efficiency` | `Context-Optimizer-Skill/agent-token-efficiency/` | Context density, caching, subagents, instruction audits | `Context-Optimizer-Skill/agent-token-efficiency/SKILL.md` |
| `project-documentation-architect` | `documentation-writer-skill/project-documentation-architect/` | Codebase discovery, multi-project docs, onboarding, audits | `documentation-writer-skill/project-documentation-architect/SKILL.md` |
| `seo-skill` | `seo-skill/` | SEO strategy, discovery, technical/on-page/local/ecom/SaaS audits | `seo-skill/SKILL.md` |
| `content-research-writer` | `content-writer-skill/content-research-writer/` | Research-first writing, approval preview, CMS/static publishing | `content-writer-skill/content-research-writer/SKILL.md` |

## Shared Policy
- Canonical policy: `Context-Optimizer-Skill/agent-token-efficiency/references/default-policy.md`

## Verified Test Suites
- `python Context-Optimizer-Skill/agent-token-efficiency/tests/run_tests.py -v`
- `python documentation-writer-skill/project-documentation-architect/tests/run_tests.py -v`
- `python seo-skill/tests/run_tests.py -v`
