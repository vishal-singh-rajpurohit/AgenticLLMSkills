# Semrush MCP Provider Adapter

Use this adapter when the official **Semrush plugin / MCP server** (`semrush_mcp`) is installed and signed in. If authentication is incomplete, ask the user to sign in rather than faking Semrush metrics or bypassing auth.

---

## 1. Canonical MCP Execution Pattern

Always follow **Discovery -> Schema -> Execution** (never guess report names or parameters from memory):
1. Call the discovery tool (`keyword_research`, `organic_research`, `competitors_research`, `backlinks_research`, `projects`, `site_audit`).
2. Call `get_report_schema` for the exact report identifier returned.
3. Call `execute_report` using validated parameters and minimal row limits (`30–50` exploratory rows before expanding).

> **Cost Guardrail:** Inform the user before the first `execute_report` call that Semrush MCP queries consume API units. Request only required columns.

---

## 2. Verified Report Mapping

| SEO Workflow | Discovery Tool | Report ID | Notes & Constraints |
|---|---|---|---|
| **Single Keyword Metrics** | `keyword_research` | `phrase_this` | Volume, CPC, competition, intent, trend, generic KD (no domain PKD field). |
| **Keyword Expansion** | `keyword_research` | `phrase_related`, `phrase_questions` | Returns raw rows; cluster transparently by intent & SERP overlap. |
| **SERP Ranking URLs** | `keyword_research` | `phrase_organic` | Use `positions_type: organic` for top-10 comparisons; keep feature rows separate. |
| **Existing Domain Rankings** | `organic_research` | `resource_organic` | Index-estimated rankings (may lag GSC first-party data). |
| **Content Gap Pages** | `organic_research` | `resource_organic_unique` | Competitor top organic pages and traffic share. |
| **Organic Competitors** | `competitors_research` | `domain_organic_organic` | Shared-ranking search competitors. |
| **Keyword Gap** | `competitors_research` | `domain_domains` | Up to **5 domains total** (`*` intersection, `+` union, `-` user domain). |
| **Backlink Refdomains / Matrix** | `backlinks_research` / `competitors_research` | `backlinks_refdomains`, `backlinks_matrix`, `backlinks` | Authority Score, referring domains, anchor context. |
| **Site Audit Issues** | `projects` / `site_audit` | `list_projects`, `snapshots`, `info`, `meta_issues`, `issue_details`, `page_list`, `page_info` | Read-only snapshot evidence; join `info.defects` to `meta_issues` dynamically. |

---

## 3. Data Integrity & Intent Decoding

- **Numeric intent codes:** Decode only `0`=Commercial, `1`=Informational, `2`=Navigational, `3`=Transactional (`1,0` = Mixed Intent). Preserve raw codes in the evidence record.
- **Keep raw rows untouched:** Screen out search operators (`inurl:`), broken encodings, and off-topic terms cleanly into a separate analyzed shortlist without mutating raw metrics.
- **Fallback on auth/unit failure:** Stop the MCP branch immediately, report what failed, and switch to [independent-research-engine.md](independent-research-engine.md) or user exports.
