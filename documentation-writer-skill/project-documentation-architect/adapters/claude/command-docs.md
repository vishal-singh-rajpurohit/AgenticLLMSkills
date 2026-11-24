---
description: Inspect a repository and create, update, or audit compact Markdown documentation using project-documentation-architect
argument-hint: "<document|update|audit|onboard> [target-path]"
---

Load and follow `project-documentation-architect` from `.claude/skills/project-documentation-architect/SKILL.md` (or `~/.claude/skills/project-documentation-architect/SKILL.md`).

User request: $ARGUMENTS

Mandatory rules:
1. Run repository discovery before writing docs; verify all commands against manifests.
2. Keep the root README compact; separate independent projects cleanly.
3. Never expose real secrets or invent undocumented commands/endpoints.
4. Validate Markdown links and doc accuracy before finishing.
