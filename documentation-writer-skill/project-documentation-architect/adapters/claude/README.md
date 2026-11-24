# Claude Code Adapter

## Installation

### Project-scoped
```bash
mkdir -p .claude/skills
cp -R path/to/project-documentation-architect .claude/skills/project-documentation-architect
```

### Personal / Global
```bash
mkdir -p ~/.claude/skills
cp -R path/to/project-documentation-architect ~/.claude/skills/project-documentation-architect
```

Or run `./adapters/install.sh --target claude --scope project`.

## Invocation
- Ask naturally (e.g., *"Document this monorepo cleanly"* or *"Audit our docs after adding the billing service"*).
- Or invoke `/project-documentation-architect` directly (or copy [command-docs.md](command-docs.md) to `.claude/commands/docs.md`).
