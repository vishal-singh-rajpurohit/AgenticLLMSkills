# Token Efficiency Quality Evaluation Scenarios (Scenarios A–E)

All scenarios require holding **model, model version, reasoning settings, repo state, and tool permissions constant** across baseline and optimized runs. Any quality/security regression triggers the rollback gate.

---

## Scenario A — Simple UI Change (Button Label Edit)
- **Task:** Change a single CTA button label in a React/Next.js component.
- **Optimized Workflow:** Locate button component via single `rg -n "<old-label>" src/` -> read only that component file -> apply minimal single-line patch -> run targeted unit/type check covering that component.
- **Pass Gate:** Zero full-repo scans, zero unrelated file reads, exact label updated, relevant check passes.

## Scenario B — Complex Authentication Modification
- **Task:** Modify auth spanning Express/Next middleware, HttpOnly cookies, access/refresh token rotation, and frontend session refresh interceptor.
- **Optimized Workflow:** Inspect **all** related backend middleware, token issuer, cookie config, and frontend interceptor modules (batched parallel reads of exact symbol ranges) -> verify security invariants -> run full auth integration tests.
- **Pass Gate:** Zero skipped security checks or uninspected layers; all integration tests pass. (Quality overrides token reduction.)

## Scenario C — Monorepo Documentation
- **Task:** Document a monorepo (`frontend/`, `admin/`, `backend/`, `worker/`, `shared/`, `docker-compose.yml`).
- **Optimized Workflow:** Run `inspect_repo.py` (excludes `node_modules`/`.next`/`dist`/`.venv`) -> write compact root `README.md` + separated `docs/projects/<app>/README.md` + single `docs/architecture.md` -> validate links (`validate_links.py`) and audit (`audit_docs.py`).
- **Pass Gate:** Clear app boundaries, zero duplicated architecture blocks, zero broken links, zero unverified commands.

## Scenario D — Long-Running Multi-Module Feature
- **Task:** Implement a multi-phase billing/webhook feature across DB schema, backend service, queue worker, and frontend status page.
- **Optimized Workflow:** Track milestone state in `.agent/TASK_STATE.md` (`Objective`, `Constraints`, `Completed`, `Decisions`, `Changed Files`, `Validation`, `Remaining`) -> compact context at phase transitions preserving unresolved issues and changed files -> re-read only active next-phase files -> run Stage 1 -> Stage 4 tests.
- **Pass Gate:** Decisions and constraints preserved across compaction without repeating early discovery; full validation passes.

## Scenario E — Large Framework API Research
- **Task:** Verify a specific framework feature (e.g., Next.js 15 async `params` in `generateMetadata` and `revalidateTag`).
- **Optimized Workflow:** Step 1 targeted search snippet with exact framework version and API name -> Step 2 fetch full official page **only** if snippet omits required types/caveats; never crawl or dump unrelated docs.
- **Pass Gate:** Exact version-accurate signature verified from official source; zero unrelated doc noise loaded.
