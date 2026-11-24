# Worked Example: Single Next.js Application (Scenario 1)

Demonstrates compact documentation generated for a single Next.js 15 App Router + Prisma web application (`taskflow-web`).

## Generated Documentation Tree

```text
taskflow-web/
├── README.md              # Compact root landing page (< 70 lines)
├── .env.example
└── docs/
    ├── environment.md     # Verified env vars with safe placeholders
    └── database.md        # Core entities + link to prisma/schema.prisma
```

## Excerpt: Compact Root `README.md`

```markdown
# TaskFlow Web

Team sprint and issue-tracking web application built with Next.js App Router and PostgreSQL.

## Tech Stack
Next.js 15 (App Router) | TypeScript | Prisma ORM | PostgreSQL

## Quick Start

1. Copy `.env.example` to `.env` (see [Environment Guide](docs/environment.md)).
2. Install dependencies: `npm install`
3. Apply local migrations: `npx prisma migrate dev`
4. Start dev server: `npm run dev`

## Directory Structure
- `src/app/` — App Router pages, layouts, and API route handlers
- `src/components/` — Reusable UI primitives
- `src/lib/` — Prisma client, auth session helpers, and validators
- `prisma/` — Database schema ([schema.prisma](prisma/schema.prisma)) and migrations

## Documentation
- [Environment Variables](docs/environment.md)
- [Database & Migrations](docs/database.md)

## Testing
Run `npm test` before opening a pull request.
```
