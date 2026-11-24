# Search & Documentation Retrieval (Two-Step Policy)

Fetch only the minimum documentation required to verify exact APIs, versions, and constraints—never load entire documentation sites into context.

## Two-Step Retrieval Protocol

1. **Step 1 — Targeted Snippet Search:** Query using exact library/framework names, version numbers, and function/API identifiers (e.g., `site:nextjs.org/docs/app generateMetadata params Promise 15`). Review search summaries/snippets first.
2. **Step 2 — Selective Full Retrieval:** Fetch the full official page or specific section **only** when the snippet omits required parameter signatures, edge-case behavior, or breaking-change caveats.

---

## Retrieval Discipline

- **Prefer authoritative primary sources:** Official docs, RFCs, language specs, release notes—not multi-page generic blog tutorials.
- **Avoid repeat fetches:** Once an exact API contract or guideline is verified in the active session, summarize or anchor its facts rather than re-fetching the same URL.
- **Preserve version context:** Record exact package/framework version constraints (`Next.js 15 async params`, `Python 3.13`) so solutions do not drift across major versions.
- **Project documentation:** Rely on a compact project index (`README.md` / `.agent/PROJECT_MAP.md`) pointing to specialized `docs/` files rather than loading every doc upfront.
