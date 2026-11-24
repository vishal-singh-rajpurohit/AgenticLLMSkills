# Realistic Test Scenarios (Scenarios 1–5)

## Scenario 1: Single Next.js Application
- **Expected:** Compact root `README.md`, verified install/dev/build/test commands, directory responsibilities, `.env.example` placeholder table (`docs/environment.md`), and database/migration workflow (`docs/database.md`) without copying whole source files.

## Scenario 2: Full-Stack Monorepo (`frontend/`, `backend/`, `admin/`, `worker/`, `shared/`, `docker-compose.yml`)
- **Expected:** Compact root `README.md` inventory table, root-level `docs/architecture.md` with service communication & Mermaid flow, and separated per-project documentation for each app and shared package.

## Scenario 3: Multiple Unrelated Projects (`ecommerce/`, `portfolio/`, `chatbot/`, `README.md`)
- **Expected:** Clean root index table linking independent projects (`ecommerce/README.md`, `portfolio/README.md`, `chatbot/README.md`), zero mixed dependencies or fabricated inter-app architecture.

## Scenario 4: Existing Documentation Audit & Preservation
- **Expected:** Inspect existing docs first, preserve accurate sections, surface broken links / missing env docs / unverified commands via `audit_docs.py`, and avoid regenerating unrelated files.

## Scenario 5: Developer Adds a New Module / Env Var / Route
- **Expected:** Inspect modified files, update only affected docs (e.g., `environment.md`, `api.md`, or `projects/<module>`), validate internal links and script commands, and report exact doc files changed without modifying application source code.
