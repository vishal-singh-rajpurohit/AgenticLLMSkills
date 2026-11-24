# Database Guide (Single Project Example)

- **Engine & ORM:** PostgreSQL + Prisma (`prisma/schema.prisma` in the application repo)
- **Core Entities:** `User` (1:N `Session`), `Workspace` (M:N via `Membership`), `Project` (belongs to `Workspace`)

## Verified Commands

```bash
# Apply local migrations
npx prisma migrate dev

# Regenerate Prisma Client after schema edits
npx prisma generate
```
