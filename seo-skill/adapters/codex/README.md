# OpenAI Codex Adapter

## Installation

### Project-scoped (`.agents/skills/` standard)
```bash
mkdir -p .agents/skills
cp -R path/to/seo-skill .agents/skills/seo-skill
mkdir -p .agents/skills/seo-skill/agents
cp path/to/seo-skill/adapters/codex/agents/openai.yaml .agents/skills/seo-skill/agents/openai.yaml
```

### User-scoped (`~/.codex/skills/`)
```bash
mkdir -p ~/.codex/skills
cp -R path/to/seo-skill ~/.codex/skills/seo-skill
mkdir -p ~/.codex/skills/seo-skill/agents
cp path/to/seo-skill/adapters/codex/agents/openai.yaml ~/.codex/skills/seo-skill/agents/openai.yaml
```

Or run the automated installer:
```bash
./adapters/install.sh --target codex --scope project
```

## Notes for Codex
- Codex reads `SKILL.md` frontmatter (`name: seo-skill` matching directory `seo-skill/`) and uses [agents/openai.yaml](agents/openai.yaml) for UI metadata and invocation policy.
- Python scripts in `scripts/` use Python 3.9+ standard library only, so they run cleanly in Codex sandboxes without needing `pip install`.
