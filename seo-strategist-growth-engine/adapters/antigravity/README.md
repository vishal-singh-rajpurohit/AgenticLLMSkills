# Google Antigravity Adapter

## Option A: Install as a Skill (Recommended)

### Project/Workspace-scoped (`.agents/skills/`)
```powershell
./seo-strategist-growth-engine/adapters/install.ps1 -Target antigravity -Scope project
```

### Global (`~/.gemini/config/skills/`)
```powershell
./seo-strategist-growth-engine/adapters/install.ps1 -Target antigravity -Scope global
```

## Option B: Package as an Antigravity Plugin (Skill + Rule Bundle)

To bundle `seo-strategist-growth-engine` with its always-on data-integrity & approval rules:
1. Create `~/.gemini/config/plugins/seo-strategist-growth-engine/` (or `.agents/plugins/seo-strategist-growth-engine/`).
2. Copy [plugin.json](plugin.json) into the plugin root.
3. Place [AGENTS.md](AGENTS.md) inside `rules/AGENTS.md`.
4. Place `seo-strategist-growth-engine/` inside `skills/seo-strategist-growth-engine/`.
