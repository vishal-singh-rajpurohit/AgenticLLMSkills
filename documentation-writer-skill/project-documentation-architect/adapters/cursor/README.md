# Cursor Adapter

Cursor supports the open `agentskills.io` `SKILL.md` standard natively.

## Installation

### Project-scoped
```bash
mkdir -p .cursor/skills
cp -R path/to/project-documentation-architect .cursor/skills/project-documentation-architect
```

### Global
```bash
mkdir -p ~/.cursor/skills
cp -R path/to/project-documentation-architect ~/.cursor/skills/project-documentation-architect
```

Or run `./adapters/install.sh --target cursor --scope project` (or `install.ps1 -Target cursor`).
