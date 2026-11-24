# System Architecture (Monorepo Example)

## Boundaries & Communication

```mermaid
flowchart LR
  Customer["Customer UI (Next.js)"] -->|REST JSON| API["Backend API (Express)"]
  Admin["Admin Dashboard (React)"] -->|REST JSON| API
  API -->|SQL| DB[("PostgreSQL")]
  API -->|Enqueue Task| Redis[("Redis")]
  Redis --> Worker["Background Worker (Python)"]
  Worker -->|SQL / SMTP| DB
```

- **Frontend & Admin** never connect directly to PostgreSQL; all mutations flow through `backend/`.
- **Shared DTOs** live in `shared/` and are imported by `frontend/`, `admin/`, and `backend/`.
- **Worker** consumes jobs queued by `backend/` via Redis (defined in `docker-compose.yml`).
