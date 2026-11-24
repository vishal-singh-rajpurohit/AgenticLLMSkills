# Repository Discovery Protocol

Inspect selectively and systematically before authoring a single line of documentation. Never guess project structure or read every file blindly.

## Step 1 — Topology Classification

Run `python scripts/inspect-repository/inspect_repo.py <repo-root>` or scan top-level and immediate subdirectory manifests to determine which pattern fits:

1. **Single Application:** One main manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.) and one deployable entry point.
2. **Monorepo / Multi-Service System:** Shared workspace config (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`, npm/yarn workspaces, `docker-compose.yml`) or coupled apps sharing packages (`frontend/`, `admin/`, `backend/`, `workers/`, `packages/shared/`).
3. **Multiple Unrelated Projects:** Separate standalone folders inside one workspace (`ecommerce/`, `portfolio/`, `chatbot/`) with no shared architecture or cross-service runtime coupling.

---

## Step 2 — High-Signal Files to Inspect Selectively

Inspect only the files present in the target repository (never assume a file exists):

| Signal Area | Files to Check | What to Extract |
|---|---|---|
| **Runtime & Commands** | `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `Makefile` | Languages, frameworks, package manager (`npm`/`pnpm`/`yarn`/`uv`/`poetry`), exact verified install/dev/build/test/lint scripts |
| **Entry Points & Routing** | `src/index.*`, `src/main.*`, `app/layout.tsx`, `pages/`, `main.py`, `cmd/*/main.go`, API router files | How execution starts and where major features/routes live |
| **Database & Models** | `prisma/schema.prisma`, `drizzle.config.*`, `alembic/`, `models/`, `migrations/` | DB engine, ORM, key entities, schema file location, real migration commands |
| **Auth & Security** | Auth middleware, NextAuth/Clerk/JWT config, RBAC guards | Token/session lifecycle, role checks, protected routes (never record real secrets!) |
| **Environment Config** | `.env.example`, `.env.template`, `config/*.ts`, `settings.py` | Required vs optional env var names, safe placeholder formats, defaults |
| **Infra & Deployment** | `Dockerfile`, `docker-compose.yml`, `.github/workflows/*.yml`, `vercel.json`, `fly.toml` | Services, ports, build steps, CI checks, deployment targets |
| **Testing Setup** | `jest.config.*`, `vitest.config.*`, `pytest.ini`, `tests/`, `__tests__/` | Test framework, test directories, verified test commands |
| **Existing Docs** | `README.md`, `docs/**/*.md`, `*/README.md`, `CONTRIBUTING.md` | Accurate content to keep vs stale commands/broken links to fix |

---

## Honesty & Verification Rules

- **Verify every command** against `package.json` `scripts`, `Makefile` targets, CI workflows, or Python/Go/Rust tool configs.
- **If an env var, deployment target, or startup dependency cannot be confirmed** from source/config files, explicitly mark it `Unknown (requires developer confirmation)` rather than guessing.
- **Do not copy source code files into docs.** Summarize responsibility in 1 line and link cleanly to the file path.
