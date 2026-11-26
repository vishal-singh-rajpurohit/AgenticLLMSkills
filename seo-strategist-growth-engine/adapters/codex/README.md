# OpenAI Codex Adapter

## Installation

### Project-scoped (`.agents/skills/`)
```bash
./seo-strategist-growth-engine/adapters/install.sh --target codex --scope project
```

### User-scoped (`~/.codex/skills/`)
```bash
./seo-strategist-growth-engine/adapters/install.sh --target codex --scope global
```

## Notes for Codex
- Codex reads `SKILL.md` frontmatter (`name: seo-strategist-growth-engine` matching parent folder name) and uses [agents/openai.yaml](agents/openai.yaml) for metadata and invocation policy.
- Python scripts in `scripts/` use Python 3.9+ standard library only, running without `pip install` inside Codex sandboxes.
