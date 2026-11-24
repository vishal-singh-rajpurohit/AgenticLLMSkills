# Session, Compaction & Project Knowledge Management

Prevent context bloat across long-running tasks and new unrelated workstreams without losing critical decisions or code truth.

## 1. Unrelated Tasks (Session Isolation)

When switching to an unrelated task on platforms that support resetting context (e.g., `/clear` in Claude Code or starting a fresh thread in Codex/Antigravity/Cursor), reset cleanly rather than dragging stale debugging traces into the new task.

---

## 2. Long-Running Tasks & `.agent/TASK_STATE.md`

For multi-phase implementations, maintain a concise external state file using [../templates/task-state.md](../templates/task-state.md) (`Objective`, `Constraints`, `Completed`, `Decisions`, `Changed Files`, `Validation`, `Remaining`).
- Update `.agent/TASK_STATE.md` only at meaningful milestones—never treat it as a verbose step-by-step chat transcript.

---

## 3. Safe Context Compaction

Trigger compaction only when context pressure builds or at major phase transitions—never compact small short tasks.
**Before compacting, explicitly preserve:**
- Original user requirements & hard constraints.
- Key architectural decisions.
- Exact files modified and why.
- Unresolved bugs/errors and current test pass/fail status.
- Key evidence and exact next action.

**After compacting:** Re-read **only** the specific source files needed for the next step.

---

## 4. Compact Project Knowledge (`.agent/PROJECT_MAP.md`)

Optionally maintain `.agent/PROJECT_MAP.md` ([../templates/project-map.md](../templates/project-map.md)) + `.agent/decisions/architecture-decisions.md` summarizing applications, key directories, entry points, versions, build/test commands, and doc links.
- **Anti-staleness rule:** Treat `PROJECT_MAP.md` as a navigation index, never as higher authority than actual code. Always verify signatures/scripts directly against live files before editing, and keep root `README.md` compact per `project-documentation-architect`.
