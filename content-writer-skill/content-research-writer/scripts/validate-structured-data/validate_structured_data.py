"""JSON-LD structured data validator for editorial, product, organization, and breadcrumb schemas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    fetch_url,
    format_report,
    is_http_url,
    iter_repo_files,
    parse_html,
    read_text_safe,
)

REQUIRED_PROPS: Dict[str, List[str]] = {
    "Article": ["headline", "author", "datePublished"],
    "BlogPosting": ["headline", "author", "datePublished"],
    "NewsArticle": ["headline", "author", "datePublished"],
    "Organization": ["name", "url"],
    "Person": ["name"],
    "Product": ["name"],
    "BreadcrumbList": ["itemListElement"],
}

DEPRECATED_TYPES = {
    "HowTo": "Google deprecated HowTo rich results; do not promise HowTo cards.",
    "FAQPage": "Google retired FAQ rich results across all sites in 2026; do not promise FAQ SERP accordions.",
}


def _extract_nodes(obj: Any) -> List[Dict[str, Any]]:
    nodes: List[Dict[str, Any]] = []
    if isinstance(obj, list):
        for item in obj:
            nodes.extend(_extract_nodes(item))
    elif isinstance(obj, dict):
        if isinstance(obj.get("@graph"), list):
            for item in obj["@graph"]:
                nodes.extend(_extract_nodes(item))
        if "@type" in obj:
            nodes.append(obj)
    return nodes


def validate_jsonld_text(source: str, raw: str) -> Tuple[List[Issue], List[str]]:
    issues: List[Issue] = []
    types_found: List[str] = []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [Issue("Invalid JSON-LD syntax", "High", source, str(exc), "Fix JSON syntax errors.")], types_found

    if any(tok in raw.lower() for tok in ("example.com", "lorem ipsum", "john doe", "todo")):
        issues.append(Issue("Placeholder data inside JSON-LD", "High", source, "Contains placeholder domain/author/text", "Replace with verified live data."))

    if isinstance(data, dict) and "@context" not in data:
        issues.append(Issue("Missing @context in JSON-LD", "Medium", source, "Top-level @context omitted", 'Add "@context": "https://schema.org".'))

    for node in _extract_nodes(data):
        raw_t = node.get("@type")
        tlist = raw_t if isinstance(raw_t, list) else [raw_t]
        for t in tlist:
            if not isinstance(t, str):
                continue
            types_found.append(t)
            if t in DEPRECATED_TYPES:
                issues.append(Issue(f"Deprecated rich result type ({t})", "Informational", source, DEPRECATED_TYPES[t], "Focus on active Schema.org types."))
            missing = [p for p in REQUIRED_PROPS.get(t, []) if not node.get(p)]
            if missing:
                issues.append(Issue(f"{t} missing recommended properties", "Medium", source, ", ".join(missing), "Populate missing fields from visible content."))
            if t == "Product" and not any(k in node for k in ("offers", "review", "aggregateRating")):
                issues.append(Issue("Product schema lacks offers/reviews", "Medium", source, "Requires visible Offer or real product review", "Add accurate Offer price, currency, and availability."))

    return issues, types_found


def run_structured_data_validation(target: str) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []
    types: List[str] = []

    if is_http_url(target):
        resp = fetch_url(target)
        if resp.error or (resp.status and resp.status >= 400):
            return [Issue("Failed to fetch URL", "Critical", target, resp.error or f"HTTP {resp.status}", "Confirm URL resolves.")], {"Mode": "Live URL"}
        parsed = parse_html(resp.text)
        for idx, block in enumerate(parsed.jsonld_blocks, start=1):
            b_issues, b_types = validate_jsonld_text(f"{resp.final_url}#jsonld-{idx}", block)
            issues.extend(b_issues)
            types.extend(b_types)
        return issues, {"Mode": "Live URL", "Types Found": ", ".join(sorted(set(types))) or "None"}

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    files = [path] if path.is_file() else iter_repo_files(path, {".html", ".htm", ".jsonld"})
    for f in files:
        rel = f.name if path.is_file() else str(f.relative_to(path))
        if f.suffix.lower() in {".json", ".jsonld"}:
            b_issues, b_types = validate_jsonld_text(rel, read_text_safe(f))
            issues.extend(b_issues)
            types.extend(b_types)
        else:
            parsed = parse_html(read_text_safe(f))
            for idx, block in enumerate(parsed.jsonld_blocks, start=1):
                b_issues, b_types = validate_jsonld_text(f"{rel}#jsonld-{idx}", block)
                issues.extend(b_issues)
                types.extend(b_types)
    return issues, {"Mode": "Local Files", "Types Found": ", ".join(sorted(set(types))) or "None"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate JSON-LD structured data.")
    parser.add_argument("target", help="Live URL, HTML/JSON-LD file, or directory")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_structured_data_validation(args.target)
    except Exception as exc:
        print(f"Error validating structured data: {exc}", file=sys.stderr)
        return 1

    print(format_report("Structured Data Validation", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
