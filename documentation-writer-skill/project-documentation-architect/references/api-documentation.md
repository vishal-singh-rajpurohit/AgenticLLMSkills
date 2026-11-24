# API & Authentication Documentation Guide

Document APIs cleanly so frontend/mobile/integration engineers know how to call endpoints and debug auth—without cloning massive OpenAPI specs manually into Markdown.

## What `api.md` Should Contain

Inspect actual router/controller files, middleware, and OpenAPI/Swagger specs (if present) first:
1. **Base URL & Versioning:** Local dev base URL (verified from port config) and version prefix (`/api/v1`).
2. **Authentication Overview:** Header/cookie scheme (`Authorization: Bearer <token>`, session cookie, API key header) and link to `authentication.md` when auth is nontrivial.
3. **Important Endpoint Groups Table:** Method, Path, Auth/Role Required, Purpose, Source Controller Link.
4. **Concise Request/Response Examples:** Show 1–2 representative JSON payloads and the project's standard error envelope (`{ error, code, message }` or actual observed shape).
5. **Generated / Spec Docs:** Link directly to Swagger/OpenAPI YAML/JSON or GraphQL schema files rather than manually maintaining duplicate field lists across 50 endpoints.
   - If the API is very large, split by domain module (`api/users.md`, `api/orders.md`) only if developers actually benefit.

---

## When to Create `authentication.md`

Create a dedicated `authentication.md` when the project implements custom sessions, JWT refresh rotation, OAuth callbacks, multi-role RBAC, or multi-tenant guards:
- Login / registration / verification flow.
- Session or access + refresh token lifecycle and storage (HttpOnly cookie vs header).
- Authorization roles, middleware guards, and protected route patterns (link to actual guard middleware files).
- **Security Rule:** Never include real API keys, sample production JWTs, passwords, or private secrets—use clearly synthetic placeholders (`<JWT_ACCESS_TOKEN>`).
