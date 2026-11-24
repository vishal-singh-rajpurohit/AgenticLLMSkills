# Claude Code Adapter

## Installation

### Project-scoped (Recommended for teams)
Copy or symlink the `seo-skill/` directory into `.claude/skills/seo-skill/` at the root of your project repository:

```bash
mkdir -p .claude/skills
cp -R path/to/seo-skill .claude/skills/seo-skill
```

### User-scoped (All repositories)
```bash
mkdir -p ~/.claude/skills
cp -R path/to/seo-skill ~/.claude/skills/seo-skill
```

Or run the cross-platform installer from `seo-skill/`:
```bash
./adapters/install.sh --target claude --scope project
```

## Invocation in Claude Code

1. **Automatic discovery:** Ask naturally (e.g., *"Help me plan SEO for my local CCTV business"* or *"Audit this Next.js app's technical SEO"*). Claude matches the `SKILL.md` description and loads references progressively.
2. **Direct slash command:** Invoke `/seo-skill` directly, or copy [command-seo.md](command-seo.md) to `.claude/commands/seo.md` if you prefer `/seo <task>`.
3. **Plugin packaging (optional):** Use [plugin.json](plugin.json) inside `.claude-plugin/plugin.json` if bundling into a Claude Code plugin distribution.
