# Universal AI Agent Token Efficiency Engineer (`agent-token-efficiency`)

A universal, quality-first context engineering and token efficiency Agent Skill compliant with the [Agent Skills open standard](https://agentskills.io). Works across **Claude Code**, **OpenAI Codex**, **Google Antigravity**, and **Cursor**.

**Core Principle:** Optimize information density, not intelligence. Never skip required code inspection, primary research, security verification, or tests to reduce token usage.

---

## Structure

```text
agent-token-efficiency/
├── SKILL.md                           # Compact progressive-disclosure entrypoint
├── README.md                          # Overview, installation, usage, and validation
├── references/                        # On-demand engineering guides + default-policy.md
│   └── adapters/                      # Claude Code, Codex, Antigravity, Cursor guides
├── templates/                         # .agent/TASK_STATE.md, PROJECT_MAP.md, subagent & audit templates
├── scripts/                           # 5 zero-dependency Python 3.9+ stdlib auditing CLIs
│   ├── audit-instructions.py
│   ├── estimate-text-tokens.py
│   ├── find-duplicate-docs.py
│   ├── audit-skill-references.py
│   └── validate-optimization-config.py
├── examples/                          # Baseline vs optimized comparison & .agent index samples
├── adapters/                          # Cross-agent installation scripts & manifests
└── tests/                             # Automated tests + Scenarios A-E evaluation suite
```

---

## Installation

**PowerShell (Windows):**
```powershell
./Context-Optimizer-Skill/agent-token-efficiency/adapters/install.ps1 -Target antigravity -Scope project
```

**Bash (macOS / Linux):**
```bash
./Context-Optimizer-Skill/agent-token-efficiency/adapters/install.sh --target claude --scope project
```

To sync only the shared policy referenced by sibling skills (`agent-token-efficiency/references/default-policy.md`):
```powershell
./Context-Optimizer-Skill/agent-token-efficiency/adapters/install.ps1 -Target claude -Scope project -PolicyOnly
```

---

## Auditing Usage

```bash
python Context-Optimizer-Skill/agent-token-efficiency/scripts/audit-instructions.py .
python Context-Optimizer-Skill/agent-token-efficiency/scripts/audit-skill-references.py .
python Context-Optimizer-Skill/agent-token-efficiency/scripts/find-duplicate-docs.py .
python Context-Optimizer-Skill/agent-token-efficiency/scripts/validate-optimization-config.py .
python Context-Optimizer-Skill/agent-token-efficiency/scripts/estimate-text-tokens.py Context-Optimizer-Skill/agent-token-efficiency/SKILL.md
```

---

## Tests

```bash
python Context-Optimizer-Skill/agent-token-efficiency/tests/run_tests.py -v
```
