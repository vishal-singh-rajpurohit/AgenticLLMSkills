# Developer Onboarding Guide

Design documentation around the **exact sequence a newly hired or first-time contributor follows** to go from `git clone` to running tests and shipping a small feature.

## Standard 10-Step Onboarding Path

Ensure the documentation set lets a developer move smoothly through every step without guessing:

1. **Read the root `README.md`** to understand what the system does and locate the target application.
2. **Inspect system architecture** (`docs/architecture.md`, if multi-service/monorepo) to see service boundaries and dependencies.
3. **Open the target app's README** (`docs/projects/<app>/README.md` or `<app>/README.md`).
4. **Install prerequisites and dependencies** using verified runtime versions and lockfile/package-manager commands.
5. **Configure environment variables** from `.env.example` using safe placeholder explanations in `environment.md`.
6. **Start required local dependencies** (PostgreSQL, Redis, Docker Compose services, local mocks).
7. **Run the application** via the verified development command and confirm the health endpoint/page responds.
8. **Review important modules and entry points** to see where routes, services, models, and components live.
9. **Follow feature implementation conventions** (linting, typing, folder conventions, API/DB migration patterns in `development.md`).
10. **Run tests and checks** before opening a pull request.

---

## Onboarding Checklist Template Snippet

Include a brief actionable checklist in the root or development guide:
- [ ] Installed verified runtime (`Node >= ...` / `Python >= ...`) and dependencies
- [ ] Copied `.env.example` to `.env` and filled required local keys
- [ ] Started local services (`docker compose up -d` or local DB)
- [ ] Applied migrations / seed data (if applicable)
- [ ] Started dev server cleanly
- [ ] Verified test suite passes locally
