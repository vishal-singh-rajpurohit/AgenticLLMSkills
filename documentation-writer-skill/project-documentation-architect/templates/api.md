# API Reference

- **Local Base URL:** `http://localhost:<verified-port>/<prefix>`
- **Authentication:** `<Bearer JWT / Session Cookie / API Key — see authentication.md if complex>`
- **Spec / Source Root:** `<Link to openapi.yaml, Swagger endpoint, or router directory>`

---

## Core Endpoints

| Method | Path | Auth | Purpose | Source |
|---|---|---|---|---|
| `GET` | `/health` | Public | Health check | `<src/routes/health.ts>` |
| `POST` | `/<resource>` | Required | `<Create resource>` | `<src/routes/...>` |

## Request & Response Example

```json
// POST /api/<resource>
{
  "field": "value"
}
```

```json
// 200 OK
{
  "id": "example-id",
  "status": "ok"
}
```

## Error Format

```json
{
  "error": "ValidationError",
  "message": "<Observed error structure from middleware>"
}
```
