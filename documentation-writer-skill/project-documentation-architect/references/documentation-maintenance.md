# Documentation Maintenance & Quality Audit

Keep documentation accurate over time by making **targeted, change-aware updates** instead of regenerating every file from scratch.

## Change-Aware Maintenance Workflow (Mode D)

When source files change (new modules, routes, models, env vars, services, Docker changes, or dependency swaps):
1. **Inspect modified files** (`git status`, `git diff`, or newly added paths).
2. **Understand the operational impact:** Does this add a route, alter an API payload, introduce an env variable, add a background job, change a DB schema, or alter a build/run command?
3. **Identify affected docs only:**
   - New env var -> `environment.md` (or project README env section)
   - New API route/contract -> `api.md`
   - New DB entity/migration -> `database.md`
   - New app/service/worker -> Root `README.md` + `architecture.md` + `<app>` project README
   - Updated npm/Python script -> `<app>` project README / `development.md`
   - Pure internal refactor with no setup, architecture, or contract change -> **no doc edit needed** (state clearly why!).
4. **Update relevant sections cleanly** and remove obsolete commands or references.
5. **Preserve accurate existing docs**—never rewrite accurate prose merely to restyle it.
6. **Run validation** (`scripts/validate-markdown-links/validate_links.py` + `scripts/documentation-audit/audit_docs.py`) and report exact changed Markdown files.

---

## Documentation Quality Audit Checklist (Mode E)

Check existing repositories across:
- Missing or broken internal Markdown links and `#heading` anchors
- Broken relative file paths pointing to moved/deleted code files
- Missing per-project docs in monorepos or multi-app directories
- Duplicated descriptions repeated across root README and sub-docs
- Outdated CLI scripts cited in docs that no longer match `package.json` / `Makefile` / `pyproject.toml`
- Documented directory trees out of sync with actual source folders
- Mixed dependencies or mixed setup instructions across unrelated projects
- `.env.example` keys missing from environment documentation (or leaked secrets!)
- Missing onboarding checklist / run instructions

**Strict Boundary:** Never modify application source code merely to satisfy a documentation check.

### Audit Report Format

```markdown
| Check | Status | Details |
|---|---|---|
| Project discovery | Pass | All applications identified |
| Root README | Pass | Compact entry point |
| Project documentation | Pass | Separated by application |
| Architecture | Pass | System flow documented |
| Broken links | Pass | No broken internal links |
| Environment docs | Review | One optional variable missing |
```
Always distinguish verified checks (`Pass` / `Fail` / `Review`) from checks that could not be verified (`Unknown`).
