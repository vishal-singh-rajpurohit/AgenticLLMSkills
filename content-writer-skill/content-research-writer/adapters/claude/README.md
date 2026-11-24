# Claude Code Adapter

## Installation

### Project-scoped
```bash
mkdir -p .claude/skills
cp -R path/to/content-research-writer .claude/skills/content-research-writer
```

### Personal / Global
```bash
mkdir -p ~/.claude/skills
cp -R path/to/content-research-writer ~/.claude/skills/content-research-writer
```

Or run the cross-platform installer from `content-research-writer/`:
```bash
./adapters/install.sh --target claude --scope project
```

## Invocation

- **Automatic skill matching:** Describe your content or publishing request naturally.
- **Explicit slash invocation:** `/content-research-writer` (or copy [command-write.md](command-write.md) to `.claude/commands/write-content.md`).
- **Plugin manifest:** [plugin.json](plugin.json) provides `.claude-plugin/plugin.json` metadata for bundle distribution.
