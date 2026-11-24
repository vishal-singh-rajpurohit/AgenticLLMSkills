# Commerce Platform (Monorepo Example — Scenario 2)

Full-stack e-commerce platform separating customer storefront, internal admin UI, core REST API, async background jobs, and shared validation schemas.

## Applications

| Application | Location | Responsibility | Documentation |
|---|---|---|---|
| Frontend | `frontend/` | Customer storefront (Next.js) | [Frontend Docs](docs/projects/frontend/README.md) |
| Admin | `admin/` | Internal admin dashboard (React) | [Admin Docs](docs/projects/admin/README.md) |
| Backend | `backend/` | REST API & Prisma DB (Express) | [Backend Docs](docs/projects/backend/README.md) |
| Worker | `worker/` | Async PDF & email tasks (Python/Celery) | [Worker Docs](docs/projects/worker/README.md) |
| Shared | `shared/` | Shared TypeScript DTOs & schemas | [Shared Package](docs/projects/shared/README.md) |

## Architecture

See [System Architecture](docs/architecture.md) for service boundaries, Redis queueing, and request flows.

## Quick Start

1. Start PostgreSQL and Redis: `docker compose up -d`
2. Follow setup instructions inside the target service README above.
