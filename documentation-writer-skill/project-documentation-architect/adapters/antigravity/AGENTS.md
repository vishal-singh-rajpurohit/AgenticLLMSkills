# Documentation Architect Guardrails

When using `project-documentation-architect`:

1. Inspect manifests, entry points, routes, schemas, and `.env.example` before documenting. Never invent CLI commands, ports, APIs, or models.
2. Keep the root `README.md` compact; separate independent or multi-service projects cleanly.
3. Never expose real secrets, credentials, or tokens—document environment variables with safe placeholders only.
4. Preserve accurate existing documentation and update only affected files when code changes.
5. Never modify application source code merely to satisfy documentation checks.
