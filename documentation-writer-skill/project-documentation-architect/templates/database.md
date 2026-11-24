# Database & Schema Guide

- **Database Engine:** `<PostgreSQL / MySQL / MongoDB / SQLite>`
- **ORM / Query Layer:** `<Prisma / Drizzle / SQLAlchemy / Mongoose>`
- **Schema Source of Truth:** `<Relative link to prisma/schema.prisma or models/>`

---

## Core Entities & Relationships

| Entity | Responsibility | Key Relationships |
|---|---|---|
| `<User>` | `<Accounts and roles>` | `<1:N with Order>` |
| `<Order>` | `<Transactions>` | `<Belongs to User>` |

*(Keep only key entities; link to the schema file for full columns.)*

## Local Setup & Migrations (Verified)

```bash
# Start local DB (if configured in docker-compose)
<verified command>

# Apply schema migrations
<verified migration command>

# Seed development data (if seed script exists)
<verified seed command>
```
