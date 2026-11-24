# Coding, Testing & Final Output Efficiency

Keep edits surgical, test proportionally to risk, and deliver crisp, verifiable final summaries.

## 1. Coding Efficiency Rules
- **Inspect before editing**—read the target symbol and callers first.
- **Prefer minimal diffs:** Use targeted section replacements (`edit_file` / patch tools) instead of regenerating entire files for small changes.
- **Reuse existing project patterns:** Follow current utilities, types, error handlers, and formatting—avoid unnecessary refactoring, unused files, or extra dependencies.
- **Quality over brevity:** Never collapse readable code into cryptic one-liners or drop validation just to save output tokens.

---

## 2. Four-Stage Risk-Based Testing
Run tests proportional to blast radius; never re-run identical passing suites repeatedly with zero edits in between:
1. **Stage 1 (Targeted Unit):** Run tests directly covering modified files/functions.
2. **Stage 2 (Integration):** Run integration/contract tests touching API, DB, auth, or cross-module edges.
3. **Stage 3 (Broader Regression):** Run affected package/app test suites when shared utilities, types, or architecture changed.
4. **Stage 4 (Full Validation):** Run full repo test + build + lint when shipping high-risk changes, release checks, or explicitly requested.

Never skip security, data-integrity, or regression tests to save tokens, and never claim tests passed without running them after the final edit.

---

## 3. Output Optimization (User Replies)
Lead with concrete results in concise Markdown:
- Summary of changes & important decisions.
- Exact modified files (clickable links where supported).
- Actual validation scope and results (including full error details if any check failed or was skipped).
- Remaining issues or explicit limitations.

**Avoid:** Repeating the user's entire prompt, dumping full rewritten files after small patches, narrating every routine tool call, re-explaining documented architecture, or requesting verbose private chain-of-thought traces.
