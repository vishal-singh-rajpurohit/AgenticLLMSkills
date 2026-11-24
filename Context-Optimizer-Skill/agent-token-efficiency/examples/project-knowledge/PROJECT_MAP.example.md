# Project Map (Example — AgenticLLMSkills)

*(Compact navigation index; verify details directly against source files before editing.)*

## Skill Packages
| Skill | Path | Primary Role | Scripts | Docs |
|---|---|---|---|---|
| `seo-skill` | `seo-skill/` | End-to-end SEO strategy, technical audits, Next.js/HTML fixes | `seo-skill/scripts/` | `seo-skill/README.md` |
| `content-research-writer` | `content-writer-skill/content-research-writer/` | Research-first humanized writing, approval gate, CMS/static publishing | `content-writer-skill/content-research-writer/scripts/` | `content-writer-skill/content-research-writer/README.md` |
| `project-documentation-architect` | `documentation-writer-skill/project-documentation-architect/` | Repo topology discovery, compact multi-project docs & audits | `documentation-writer-skill/project-documentation-architect/scripts/` | `documentation-writer-skill/project-documentation-architect/README.md` |
| `agent-token-efficiency` | `Context-Optimizer-Skill/agent-token-efficiency/` | Universal context density, caching, subagent & audit engineering | `Context-Optimizer-Skill/agent-token-efficiency/scripts/` | `Context-Optimizer-Skill/agent-token-efficiency/README.md` |

## Test Commands
- `python seo-skill/tests/run_tests.py -v`
- `python documentation-writer-skill/project-documentation-architect/tests/run_tests.py -v`
- `python Context-Optimizer-Skill/agent-token-efficiency/tests/run_tests.py -v`
