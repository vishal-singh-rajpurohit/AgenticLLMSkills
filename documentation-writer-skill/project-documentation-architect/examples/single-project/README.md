# Example: Single Next.js Application (Scenario 1)

*Worked documentation output for a single Next.js App Router + PostgreSQL/Prisma web app.*

## 1. Compact Root `README.md` Pattern

- **Overview:** Customer portal and API built with Next.js App Router, TypeScript, and Prisma.
- **Tech Stack:** Next.js `15.x` | TypeScript | PostgreSQL + Prisma | Tailwind CSS
- **Getting Started:**
  ```bash
  npm install
  cp .env.example .env
  npx prisma migrate dev
  npm run dev
  ```
- **Architecture & Modules:**
  - `src/app/` — App Router pages, layouts, and API route handlers
  - `src/components/` — Reusable UI components
  - `src/lib/` — Prisma client, auth helpers, and API utilities
  - `prisma/schema.prisma` — Database models and relations
- **Detailed Guides:**
  - [Environment Setup](docs/environment.md)
  - [Database & Migrations](docs/database.md)

## 2. Onboarding Checklist Included
- [ ] Node.js >= 20 and PostgreSQL running locally
- [ ] `.env` populated from `.env.example`
- [ ] `npx prisma migrate dev` applied cleanly
- [ ] `npm run dev` serving `http://localhost:3000`
- [ ] `npm test` passing
