# Backend Service

Core REST API handling authentication, orders, inventory, and job enqueueing.

- **Stack:** Node.js, Express, PostgreSQL + Prisma, Redis
- **Commands:** `pnpm --filter backend dev` | `pnpm --filter backend test`
- **Modules:** `src/routes/` (API endpoints), `src/services/` (business logic), `prisma/schema.prisma` (DB schema)
- **Related:** [System Architecture](../../architecture.md)
