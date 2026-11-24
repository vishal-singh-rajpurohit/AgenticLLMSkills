# OpenAI Codex Adapter

## Installation

### Project-scoped (`.agents/skills/`)
```bash
mkdir -p .agents/skills
cp -R path/to/content-research-writer .agents/skills/content-research-writer
mkdir -p .agents/skills/content-research-writer/agents
cp path/to/content-research-writer/adapters/codex/agents/openai.yaml .agents/skills/content-research-writer/agents/openai.yaml
```

### User-scoped (`~/.codex/skills/`)
```bash
mkdir -p ~/.codex/skills
cp -R path/to/content-research-writer ~/.codex/skills/content-research-writer
mkdir -p ~/.codex/skills/content-research-writer/agents
cp path/to/content-research-writer/adapters/codex/agents/openai.yaml ~/.codex/skills/content-research-writer/agents/openai.yaml
```

Or run `./adapters/install.sh --target codex --scope project` (or `install.ps1 -Target codex`).

## Codex Notes
- [agents/openai.yaml](agents/openai.yaml) configures Codex display name, default prompt, and automatic selection policy.
- All scripts in `scripts/` use Python 3.9+ stdlib only and work inside restricted sandboxes without `pip install`.
