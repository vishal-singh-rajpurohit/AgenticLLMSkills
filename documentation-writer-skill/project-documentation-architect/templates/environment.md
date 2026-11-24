# Environment Configuration

Copy `.env.example` to `.env` before running locally. **Never commit `.env` or real production credentials.**

## Environment Variables

| Variable | Required | Purpose | Safe Example Placeholder | Where Used |
|---|---|---|---|---|
| `DATABASE_URL` | `Yes` | Primary database connection string | `postgresql://user:password@localhost:5432/app_dev` | `<Backend / Prisma>` |
| `NEXT_PUBLIC_API_URL` | `Yes` | Public backend API base URL | `http://localhost:4000/api` | `<Frontend>` |
| `LOG_LEVEL` | `No` | Application log verbosity (`info` default) | `debug` | `<Backend / Worker>` |

*(List only variables verified in `.env.example` or config loaders; mark uncertain flags as `Unknown (verify with developer)`.)*
