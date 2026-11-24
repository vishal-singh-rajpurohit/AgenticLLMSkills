# Tool Output, Terminal & MCP Optimization

Every line printed to stdout/stderr or returned by an MCP server consumes working context. Keep outputs tight without ever hiding failures or warnings.

## 1. Quiet & Summary Terminal Modes (Verified Flags Only)

Prefer built-in compact flags **only when supported by the installed tool** (never guess or invent flags):
- `git status --short` / `git diff --stat` / `git diff --name-only`
- `pytest -q` or `--tb=short` (expand with `-vv` only when debugging a failing assertion)
- `vitest run --reporter=dot` (switch to default/verbose only on failure)
- `npm run lint -- --quiet` (suppresses warnings when only errors block; verify linter supports `--quiet`)
- `rg -n --max-count 5` or path-scoped `rg -n "<pattern>" src/`

---

## 2. Large Command Output Protocol

When running builds, migrations, or test suites:
1. **Preserve exit status** cleanly—never ignore non-zero return codes.
2. **Success path:** Report concise pass counts and scope (`Ran 24 tests in 1.8s — OK`).
3. **Failure path:** Extract error summary, failing file/line locations, exact assertion/type/compiler mismatch, and relevant stack trace lines—never silently drop security warnings or failing tests, and expand full logs when root-cause debugging demands it.

### Compact Error Reporting Format
- **Summary:** What failed and exit code.
- **Location:** `path/to/file:line`.
- **Evidence:** Exact error message / relevant trace slice.
- **Fix / Next check:** Proposed patch or targeted diagnostic command.

---

## 3. MCP & Tool Definition Hygiene

- Enable only MCP servers relevant to the project/task (avoid attaching 5 duplicate web/DB servers simultaneously).
- Prefer focused discovery/search MCP tools (`search_documents`, filtered `jq`/projection queries) over raw `dump_all` endpoints.
- Load lazy tool schemas or full MCP resources only when needed for the active call.
- Never sacrifice required verification/security tools merely to trim schema tokens.
