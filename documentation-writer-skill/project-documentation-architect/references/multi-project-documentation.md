# Multi-Project & Monorepo Documentation Architecture

Prevent giant, unreadable catch-all READMEs when a repository holds multiple apps, services, packages, or completely unrelated projects.

## Core Separation Rules

1. **Root `README.md` stays compact.** It functions strictly as a map and landing page (overview, app inventory table, high-level stack, quick pointer to architecture/apps, onboarding path). Keep detailed API routes, DB schemas, and directory trees out of the root README.
2. **Every independent project gets its own docs.** Place either `<app>/README.md` or `docs/projects/<app>/README.md` (with optional `api.md`, `database.md`, `workflows.md` only if complex enough to need them).
3. **Never mix frontend, backend, admin, or worker implementation details** in one file.
4. **Keep shared packages & shared infrastructure separate** (e.g., `docs/projects/shared/` or `packages/shared/README.md`, and `docs/deployment.md` for shared `docker-compose.yml`/CI).
5. **Document cross-app communication at the system level** inside `docs/architecture.md` (avoid repeating the same architecture diagram inside every sub-project README).
6. **Use relative Markdown links** everywhere and create sub-files only when they provide concrete value.

---

## Pattern A — Coupled Full-Stack Monorepo (`frontend/`, `backend/`, `admin/`, `worker/`, `packages/shared/`)

```text
repo-root/
├── README.md                              # Compact index + app table + quick start links
└── docs/
    ├── architecture.md                    # System boundaries, communication & Mermaid diagram
    ├── deployment.md                      # Shared docker-compose, build & CI pipeline
    └── projects/
        ├── frontend/
        │   ├── README.md                  # Customer UI overview, install, dev, structure
        │   └── development.md             # UI conventions & state/API patterns (only if needed)
        ├── admin/
        │   └── README.md
        ├── backend/
        │   ├── README.md
        │   ├── api.md
        │   ├── database.md
        │   └── authentication.md
        └── workers/
            ├── README.md
            └── workflows.md
```
*(Or keep `<app>/README.md` alongside each app folder when the repository already follows colocation—adapt to repo conventions rather than forcing one rigid tree!)*

---

## Pattern B — Multiple Unrelated Projects in One Workspace (`ecommerce/`, `portfolio/`, `chatbot/`)

When directories share zero runtime coupling, package dependencies, or deployment pipeline:
- Treat each folder as an **autonomous project** with its own `<project>/README.md` (and optional `<project>/docs/`).
- Keep the root `README.md` strictly as a **workspace directory index** table linking to each independent project—do **not** invent a fake unified system architecture diagram connecting unrelated apps!
- Keep installation, environment variables, and run commands 100% isolated inside each project's own documentation.
