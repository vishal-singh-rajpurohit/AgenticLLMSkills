---
description: Run Universal SEO Strategist workflows (discovery, keyword research, technical audit, content strategy, codebase implementation, or reporting)
argument-hint: "<task or target URL/path>"
---

Load and follow the `seo-skill` instructions in `.claude/skills/seo-skill/SKILL.md` (or `~/.claude/skills/seo-skill/SKILL.md`).

User request: $ARGUMENTS

Remember:
- If this is a full strategy, keyword research, or content request, research any supplied URL/codebase first, then conduct the humanized one-question-at-a-time discovery interview from `references/business-discovery.md`.
- If this is a scoped technical audit or implementation task, inspect the codebase/URL directly and run `scripts/` validation tools without blocking on a full business interview.
- Never fabricate metrics, rankings, or connected tool access.
