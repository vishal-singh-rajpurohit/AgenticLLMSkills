# Google Antigravity Adapter

## Option A: Install as a Skill (Recommended)

### Workspace-scoped (`.agents/skills/`)
```powershell
New-Item -ItemType Directory -Force ".agents/skills" | Out-Null
Copy-Item -Recurse -Force "path/to/project-documentation-architect" ".agents/skills/project-documentation-architect"
```

### Global (`~/.gemini/config/skills/`)
```powershell
New-Item -ItemType Directory -Force "$HOME/.gemini/config/skills" | Out-Null
Copy-Item -Recurse -Force "path/to/project-documentation-architect" "$HOME/.gemini/config/skills/project-documentation-architect"
```

Or run `./adapters/install.ps1 -Target antigravity -Scope project`.

## Option B: Package as an Antigravity Plugin
Create `~/.gemini/config/plugins/project-documentation-architect/` (or `.agents/plugins/project-documentation-architect/`) with [plugin.json](plugin.json), `rules/AGENTS.md` from [AGENTS.md](AGENTS.md), and `skills/project-documentation-architect/`.
