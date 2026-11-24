# Database Documentation Guide

Give engineers a clear mental model of data ownership, entities, relationships, and safe migration commands—without copying hundreds of lines of schema code.

## What `database.md` Should Cover

Inspect `prisma/schema.prisma`, Drizzle schema files, SQLAlchemy/Django models, Mongoose schemas, `migrations/`, and `docker-compose.yml` first:
1. **Database Technology & ORM:** Engine (PostgreSQL, MySQL, SQLite, MongoDB, Redis) and data-access layer (Prisma, Drizzle, TypeORM, SQLAlchemy, Mongoose).
2. **Source of Truth Link:** Link directly to the real schema path (`[schema.prisma](../../../backend/prisma/schema.prisma)`) so engineers always check exact column types in code.
3. **Core Entities & Relationships:** Concise table or small Mermaid `erDiagram` covering primary domain entities (`User`, `Organization`, `Order`, `Post`) and cardinality (`1:N`, `M:N`).
4. **Local Setup & Seeding:** Exact verified commands to boot the local DB (`docker compose up -d db`), push/apply migrations, and run seed scripts if present.
5. **Migration Workflow:** Verified team workflow for schema changes (e.g., `npx prisma migrate dev --name <change>` vs `alembic revision --autogenerate`). Mark as `Unknown (requires developer confirmation)` if no migration script or convention exists in the repo.

---

## Rules

- Do **not** paste the entire `schema.prisma` or SQL migration log into Markdown.
- Do **not** document invented tables or unverified seed passwords.
- Separate transactional primary DB docs from cache/queue docs unless tightly coupled.
