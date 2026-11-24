"""JSON-LD structured data validator aligned with Schema.org & Google Search Central.

Supports:
  - Live URLs
  - Local HTML files / directories
  - Standalone .json / .jsonld files
  - Deprecated Google rich-result alerts (HowTo, FAQPage rich results)
  - Placeholder / fabricated review & domain sanity warnings
"""

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

REQUIRED_PROPERTIES: Dict[str, List[str]] = {
    "Organization": ["name", "url"],
    "LocalBusiness": ["name"],
    "Product": ["name"],
    "Article": ["headline"],
    "BlogPosting": ["headline"],
    "NewsArticle": ["headline"],
    "BreadcrumbList": ["itemListElement"],
    "Event": ["name", "startDate", "location"],
}

DEPRECATED_RICH_RESULTS = {
    "HowTo": "Google deprecated HowTo rich results. Do not promise HowTo rich snippets.",
    "FAQPage": "Google retired FAQ rich results across all sites in 2026. Keep clean Q&A UX only if useful for users; do not expect FAQ SERP accordions.",
}

PLACEHOLDER_TOKENS = ("example.com", "lorem ipsum", "123 main st", "todo", "your company name")


def _flatten_nodes(data: Any) -> List[Dict[str, Any]]:
    nodes: List[Dict[str, Any]] = []
    if isinstance(data, list):
        for item in data:
            nodes.extend(_flatten_nodes(item))
    elif isinstance(data, dict):
        if "@graph" in data and isinstance(data["@graph"], list):
            for item in data["@graph"]:
                nodes.extend(_flatten_nodes(item))
        if "@type" in data:
            nodes.append(data)
    return nodes


def validate_jsonld_block(source_label: str, raw_json: str) -> Tuple[List[Issue], List[str]]:
    """Parse and validate a single JSON-LD payload."""
    issues: List[Issue] = []
    found_types: List[str] = []

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        issues.append(
            Issue(
                "Invalid JSON-LD syntax",
                "High",
                source_label,
                f"JSON parse error: {exc}",
                "Fix JSON syntax inside <script type=\"application/ld+json\"> and verify with Schema Markup Validator.",
            )
        )
        return issues, found_types

    lower_raw = raw_json.lower()
    for token in PLACEHOLDER_TOKENS:
        if token in lower_raw:
            issues.append(
                Issue(
                    "Placeholder or template text inside structured data",
                    "High",
                    source_label,
                    f'JSON-LD contains placeholder token "{token}"',
                    "Replace placeholders with verified, visible business/product facts.",
                )
            )
            break

    if isinstance(data, dict) and "@context" not in data:
        issues.append(
            Issue(
                "JSON-LD missing @context",
                "Medium",
                source_label,
                "Top-level JSON-LD object omits @context",
                'Set "@context": "https://schema.org".',
            )
        )

    nodes = _flatten_nodes(data)
    if not nodes:
        issues.append(
            Issue(
                "JSON-LD block contains no typed Schema.org entity",
                "Medium",
                source_label,
                "No @type node found in JSON-LD",
                "Specify a valid Schema.org @type (e.g., Organization, Product, Article, LocalBusiness).",
            )
        )
        return issues, found_types

    for node in nodes:
        raw_type = node.get("@type")
        types = raw_type if isinstance(raw_type, list) else [raw_type]
        for schema_type in types:
            if not isinstance(schema_type, str):
                continue
            found_types.append(schema_type)

            if schema_type in DEPRECATED_RICH_RESULTS:
                issues.append(
                    Issue(
                        f"Deprecated Google rich result schema type ({schema_type})",
                        "Informational",
                        source_label,
                        DEPRECATED_RICH_RESULTS[schema_type],
                        "Focus on active eligible Schema.org types aligned with visible page content.",
                    )
                )

            req_fields = REQUIRED_PROPERTIES.get(schema_type, [])
            missing = [f for f in req_fields if not node.get(f)]
            if missing:
                issues.append(
                    Issue(
                        f"{schema_type} JSON-LD missing core properties",
                        "Medium",
                        source_label,
                        f"Missing {', '.join(missing)}",
                        f"Populate {', '.join(missing)} accurately from visible page content.",
                    )
                )

            if schema_type == "Product":
                if not any(k in node for k in ("offers", "review", "aggregateRating")):
                    issues.append(
                        Issue(
                            "Product JSON-LD lacks offers, review, or aggregateRating",
                            "Medium",
                            source_label,
                            "Google Product structured data requires at least one of offers, review, or aggregateRating",
                            "Add accurate Offer pricing/availability (and only real on-page product reviews if present).",
                        )
                    )
                offers = node.get("offers")
                offer_list = offers if isinstance(offers, list) else ([offers] if isinstance(offers, dict) else [])
                for offer in offer_list:
                    if isinstance(offer, dict):
                        missing_offer = [k for k in ("price", "priceCurrency", "availability") if offer.get(k) in (None, "")]
                        if missing_offer:
                            issues.append(
                                Issue(
                                    "Product Offer missing pricing or availability fields",
                                    "Medium",
                                    source_label,
                                    f"Offer missing: {', '.join(missing_offer)}",
                                    "Include accurate visible price, ISO-4217 priceCurrency, and schema.org availability URL.",
                                )
                            )

            if schema_type == "LocalBusiness" and not node.get("address") and not node.get("areaServed"):
                issues.append(
                    Issue(
                        "LocalBusiness JSON-LD missing address and areaServed",
                        "Medium",
                        source_label,
                        "Neither address nor areaServed is specified",
                        "Include verified storefront address (or areaServed for service-area businesses) matching visible page details.",
                    )
                )

    return issues, found_types


def run_structured_data_validation(target: str) -> Tuple[List[Issue], Dict[str, str]]:
    """Validate JSON-LD on a live URL, local HTML/JSON file, or directory."""
    issues: List[Issue] = []
    all_types: List[str] = []

    if is_http_url(target):
        resp = fetch_url(target)
        if resp.error or (resp.status and resp.status >= 400):
            issues.append(
                Issue(
                    "Failed to fetch target URL",
                    "Critical",
                    target,
                    resp.error or f"HTTP {resp.status}",
                    "Ensure target URL responds 200 OK before validating structured data.",
                )
            )
            return issues, {"Mode": "Live URL"}

        parsed = parse_html(resp.text)
        if not parsed.jsonld_blocks:
            issues.append(
                Issue(
                    "No JSON-LD structured data found",
                    "Informational",
                    resp.final_url,
                    "0 <script type=\"application/ld+json\"> blocks found",
                    "Add relevant Schema.org JSON-LD (e.g., Organization, LocalBusiness, Product, Article, BreadcrumbList) if applicable.",
                )
            )
        for idx, block in enumerate(parsed.jsonld_blocks, start=1):
            b_issues, b_types = validate_jsonld_block(f"{resp.final_url}#jsonld-{idx}", block)
            issues.extend(b_issues)
            all_types.extend(b_types)
        return issues, {"Mode": "Live URL", "Types Found": ", ".join(sorted(set(all_types))) or "None"}

    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    if path.is_file():
        if path.suffix.lower() in {".json", ".jsonld"}:
            b_issues, b_types = validate_jsonld_block(path.name, read_text_safe(path))
            issues.extend(b_issues)
            all_types.extend(b_types)
        else:
            parsed = parse_html(read_text_safe(path))
            for idx, block in enumerate(parsed.jsonld_blocks, start=1):
                b_issues, b_types = validate_jsonld_block(f"{path.name}#jsonld-{idx}", block)
                issues.extend(b_issues)
                all_types.extend(b_types)
        return issues, {"Mode": "Single File", "Types Found": ", ".join(sorted(set(all_types))) or "None"}

    files = iter_repo_files(path, {".html", ".htm", ".jsonld"})
    for fpath in files:
        rel = str(fpath.relative_to(path))
        if fpath.suffix.lower() == ".jsonld":
            b_issues, b_types = validate_jsonld_block(rel, read_text_safe(fpath))
            issues.extend(b_issues)
            all_types.extend(b_types)
        else:
            parsed = parse_html(read_text_safe(fpath))
            for idx, block in enumerate(parsed.jsonld_blocks, start=1):
                b_issues, b_types = validate_jsonld_block(f"{rel}#jsonld-{idx}", block)
                issues.extend(b_issues)
                all_types.extend(b_types)

    return issues, {
        "Mode": "Local Directory",
        "Files Scanned": str(len(files)),
        "Types Found": ", ".join(sorted(set(all_types))) or "None",
    }


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

    print(format_report("Structured Data (JSON-LD) Validation", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
