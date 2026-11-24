# OpenAI Codex Adapter

## Installation

### Project-scoped (`.agents/skills/`)
```bash
mkdir -p .agents/skills
cp -R path/to/project-documentation-architect .agents/skills/project-documentation-architect
mkdir -p .agents/skills/project-documentation-architect/agents
cp path/to/project-documentation-architect/adapters/codex/agents/openai.yaml .agents/skills/project-documentation-architect/agents/openai.yaml
```

### Global (`~/.codex/skills/`)
```bash
mkdir -p ~/.codex/skills
cp -R path/to/project-documentation-architect ~/.codex/skills/project-documentation-architect
mkdir -p ~/.codex/skills/project-documentation-architect/agents
cp path/to/project-documentation-architect/adapters/codex/agents/openai.yaml ~/.codex/skills/project-documentation-architect/agents/openai.yaml
```

Or run `./adapters/install.sh --target codex --scope project` (or `install.ps1 -Target codex`).
