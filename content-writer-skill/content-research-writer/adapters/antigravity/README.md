# Google Antigravity Adapter

## Option A: Install as a Skill (Recommended)

### Workspace-scoped (`.agents/skills/`)
```powershell
New-Item -ItemType Directory -Force ".agents/skills" | Out-Null
Copy-Item -Recurse -Force "path/to/content-research-writer" ".agents/skills/content-research-writer"
```

### Global (`~/.gemini/config/skills/`)
```powershell
New-Item -ItemType Directory -Force "$HOME/.gemini/config/skills" | Out-Null
Copy-Item -Recurse -Force "path/to/content-research-writer" "$HOME/.gemini/config/skills/content-research-writer"
```

Or run `./adapters/install.ps1 -Target antigravity -Scope workspace`.

## Option B: Package as an Antigravity Plugin

Create `~/.gemini/config/plugins/content-research-writer/` (or `.agents/plugins/content-research-writer/`):
1. Copy [plugin.json](plugin.json) into the plugin root.
2. Copy [AGENTS.md](AGENTS.md) into `rules/AGENTS.md`.
3. Copy `content-research-writer/` into `skills/content-research-writer/`.
