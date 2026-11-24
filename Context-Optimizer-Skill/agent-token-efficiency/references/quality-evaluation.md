# Quality Preservation & A/B Evaluation Framework

Token efficiency succeeds **only** when correctness, completeness, security, and test verification stay equal or improve. Never optimize tokens at the expense of task quality.

## Controlled Baseline vs. Optimized Evaluation Rules

Hold constant across baseline and optimized runs:
- Exact model & model version
- Reasoning / thinking effort setting
- Identical task prompt & acceptance criteria
- Identical starting git commit / repository state
- Identical tool permissions & test environment

### Comparison Scorecard

| Metric | Optimization Target | Measurement Rule |
|---|---|---|
| **Input tokens** | Reduce redundant/irrelevant context | Report actual API usage when exposed; otherwise label char/byte approximation |
| **Cached input tokens** | Increase stable prefix reuse | Measure `cache_read_input_tokens` / `cached_tokens` / `cached_content_token_count` if API exposed |
| **Output tokens** | Cut filler without hiding errors/caveats | Measure actual output tokens when exposed |
| **Tool calls** | Eliminate duplicate reads & noisy full scans | Count tool invocations per task |
| **Task success & completeness** | 100% requirements met (no regressions) | Pass/fail rubric |
| **Test results** | Zero broken or skipped verification checks | Exact test command exit status & counts |
| **Security & correctness** | Zero missed auth/validation/edge-case risks | Code review & security assertions |

---

## Regression Rollback Gate (Mandatory)

If any optimization rule causes a missed requirement, uninspected dependency, skipped edge case, or failed test:
1. Identify which missing context or skipped tool check caused the regression.
2. Restore the required context/inspection step immediately.
3. Tighten the optimization heuristic so quality-critical context is always fetched.
4. Re-run the full evaluation before adopting the rule.
