# Claude Code Adapter

## Installation

### Project-scoped (`.claude/skills/`)
```bash
./seo-strategist-growth-engine/adapters/install.sh --target claude --scope project
```

### User-scoped (`~/.claude/skills/`)
```bash
./seo-strategist-growth-engine/adapters/install.sh --target claude --scope global
```

## Invocation
1. **Automatic discovery:** Ask naturally (e.g., *"Help me build an SEO growth strategy for our SaaS"* or *"Audit this Next.js codebase for SEO issues"*).
2. **Optional slash command:** Copy [command-seo-growth.md](command-seo-growth.md) to `.claude/commands/seo-growth.md` to invoke `/seo-growth <goal>`.
3. **Plugin packaging:** Bundle with [plugin.json](plugin.json) inside `.claude-plugin/plugin.json` if distributing as a Claude Code plugin.
