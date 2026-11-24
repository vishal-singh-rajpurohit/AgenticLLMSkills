# Google Antigravity Adapter

## Option A: Install as a Skill (Recommended)

### Workspace-scoped (`.agents/skills/`)
```powershell
New-Item -ItemType Directory -Force ".agents/skills" | Out-Null
Copy-Item -Recurse -Force "path/to/seo-skill" ".agents/skills/seo-skill"
```

### Machine-global (`~/.gemini/config/skills/`)
```powershell
New-Item -ItemType Directory -Force "$HOME/.gemini/config/skills" | Out-Null
Copy-Item -Recurse -Force "path/to/seo-skill" "$HOME/.gemini/config/skills/seo-skill"
```

Or run:
```powershell
./adapters/install.ps1 -Target antigravity -Scope workspace
```

## Option B: Package as an Antigravity Plugin (Skill + Rule Bundle)

If you want `seo-skill` bundled with its always-on data-integrity & approval guardrails:
1. Create `~/.gemini/config/plugins/seo-skill/` (or `.agents/plugins/seo-skill/`).
2. Copy [plugin.json](plugin.json) into the plugin root.
3. Place [AGENTS.md](AGENTS.md) inside `rules/AGENTS.md`.
4. Place the `seo-skill/` directory inside `skills/seo-skill/`.
