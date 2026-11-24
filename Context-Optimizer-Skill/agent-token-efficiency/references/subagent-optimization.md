# Subagent & Multi-Agent Optimization

Subagents isolate noisy exploration from the main orchestrator's working context—**when used selectively**. Spawning subagents for trivial single-file tasks wastes context and latency on duplicated instructions and handoff overhead.

## When to Delegate vs. Keep Local

| Delegate to Subagent(s) | Keep in Main Agent |
|---|---|
| Parallel inspection of independent modules (e.g., frontend vs backend) | Single-file edit or 1–2 targeted grep lookups |
| Independent security audit or broad codebase research | Tight sequential edits sharing intermediate state |
| Investigating unrelated test failures in parallel | Tasks where brief + coordination exceeds local work |

---

## Tight Delegation Brief Requirements

Never hand a subagent the entire conversation history or unbounded repo sweep. Pass only:
1. **Specific objective** (exact question or deliverable).
2. **Exact file/directory scope** (`src/auth/`, `backend/routes/`).
3. **Critical constraints / context** (framework version, security invariants).
4. **Expected output format** (compact structured report below).
5. **Required verification** (exact test/command or evidence check).

---

## Mandatory 6-Part Compact Subagent Report

Require every subagent to return concise structured findings (use [../templates/subagent-brief-and-report.md](../templates/subagent-brief-and-report.md))—never raw terminal logs:
1. **Findings:** Core answer or root cause.
2. **Relevant Files & Lines:** Exact `path/to/file.ext:L10-L45` references.
3. **Decisions / Recommendations:** Proposed options or actions taken.
4. **Evidence:** Observed assertions, command exit codes, or spec citations.
5. **Risks:** Potential regressions, edge cases, or security concerns.
6. **Remaining Unknowns:** Explicitly unverified gaps.
