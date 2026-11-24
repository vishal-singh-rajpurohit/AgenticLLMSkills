# Cursor Adapter

Cursor natively supports the `agentskills.io` open standard (`SKILL.md`).

## Installation

### Project-scoped
Place `seo-skill/` in either `.cursor/skills/seo-skill/` or `.agents/skills/seo-skill/`:

```bash
mkdir -p .cursor/skills
cp -R path/to/seo-skill .cursor/skills/seo-skill
```

### Global (All workspaces)
```bash
mkdir -p ~/.cursor/skills
cp -R path/to/seo-skill ~/.cursor/skills/seo-skill
```

Or run `./adapters/install.sh --target cursor --scope project` (or `install.ps1 -Target cursor`).
