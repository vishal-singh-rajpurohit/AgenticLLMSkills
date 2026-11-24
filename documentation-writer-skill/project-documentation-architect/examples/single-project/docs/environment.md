# Environment Configuration (Single Project Example)

Copy `.env.example` to `.env` before booting locally. Never commit real keys.

| Variable | Required | Purpose | Safe Placeholder |
|---|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection URI | `postgresql://postgres:postgres@localhost:5432/app_dev` |
| `AUTH_SECRET` | Yes | Session signing key | `replace-with-local-32-char-secret` |
| `NEXT_PUBLIC_APP_URL` | Optional | Base site URL | `http://localhost:3000` |
