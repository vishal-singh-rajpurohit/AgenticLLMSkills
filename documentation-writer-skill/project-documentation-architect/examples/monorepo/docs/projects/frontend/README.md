# Frontend Application

Customer-facing storefront consuming the backend REST API and shared validation types.

- **Stack:** Next.js, TypeScript, `@repo/shared`
- **Dev Command:** `pnpm --filter frontend dev`
- **Build / Test:** `pnpm --filter frontend build` | `pnpm --filter frontend test`
- **Important Directories:** `src/app/` (routes), `src/components/` (UI), `src/services/` (API client)
- **Depends On:** Backend API (`NEXT_PUBLIC_API_URL`) and `shared/`
