"""Editorial, structural, AI-filler, and repository publishing-architecture validator."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    detect_publishing_architecture,
    format_report,
    iter_repo_files,
    parse_frontmatter_and_body,
    parse_html,
    read_text_safe,
)

AI_CLICHE_PATTERNS = [
    r"in today'?s fast-paced digital (?:world|landscape|era)",
    r"in an ever-evolving (?:world|landscape)",
    r"\bunlock the full potential\b",
    r"\bgame-chang(?:ing|er)\b",
    r"\bseamless synergy\b",
    r"\belevate your .* to new heights\b",
    r"\bdelve into\b",
    r"\bin conclusion,\s+by leveraging\b",
]

PLACEHOLDER_PATTERNS = [
    (r"\[NEEDS SME VERIFICATION\]", "Unresolved [NEEDS SME VERIFICATION] marker"),
    (r"\blorem ipsum\b", "Placeholder Lorem ipsum text"),
    (r"\b(?:TODO|TBD|FIXME)\b", "Unresolved TODO/TBD marker"),
]


def _extract_markdown_headings(body: str) -> List[Tuple[int, str]]:
    stripped = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    headings: List[Tuple[int, str]] = []
    for line in stripped.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+?)\s*#*$", line)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip()))
    return headings


def analyze_content_file(path: Path, rel_label: str) -> List[Issue]:
    """Check one Markdown, MDX, or HTML content piece for editorial and verification gaps."""
    issues: List[Issue] = []
    raw = read_text_safe(path)
    is_html = path.suffix.lower() in {".html", ".htm"}

    if is_html:
        parsed = parse_html(raw)
        body_text = re.sub(r"<[^>]+>", " ", raw)
        headings = [(int(tag[1]), txt) for tag, txt in parsed.headings]
        has_external_link = any(lnk["href"].startswith(("http://", "https://")) for lnk in parsed.links)
    else:
        _, body = parse_frontmatter_and_body(raw)
        body_text = body
        headings = _extract_markdown_headings(body)
        has_external_link = bool(re.search(r"\[[^\]]+\]\(https?://", body))

    word_count = len(re.findall(r"\b\w+\b", body_text))
    if word_count < 80:
        issues.append(
            Issue(
                "Very thin content draft",
                "Medium",
                rel_label,
                f"Only {word_count} words detected",
                "Verify whether this page needs deeper practical detail, examples, and answers.",
            )
        )

    for pattern, label in PLACEHOLDER_PATTERNS:
        if re.search(pattern, body_text, re.IGNORECASE):
            issues.append(
                Issue(
                    label,
                    "High",
                    rel_label,
                    f"Matched pattern `{pattern}` in draft content",
                    "Confirm with subject-matter expert or replace placeholder before approval.",
                )
            )

    cliches = [pat for pat in AI_CLICHE_PATTERNS if re.search(pat, body_text, re.IGNORECASE)]
    if cliches:
        issues.append(
            Issue(
                "Generic AI-filler phrasing detected",
                "Medium",
                rel_label,
                f"Matched {len(cliches)} cliché pattern(s)",
                "Rewrite openings/transitions using specific facts, concrete examples, and natural human phrasing.",
            )
        )

    h1_count = sum(1 for lvl, _ in headings if lvl == 1)
    if h1_count == 0:
        issues.append(
            Issue(
                "Missing H1 heading in content",
                "Medium",
                rel_label,
                "No level-1 heading found",
                "Ensure the article or layout template renders one clear primary H1.",
            )
        )
    elif h1_count > 1:
        issues.append(
            Issue(
                "Multiple H1 headings",
                "Low",
                rel_label,
                f"Found {h1_count} level-1 headings",
                "Use one H1 for the main title and H2/H3 for subsections.",
            )
        )

    prev = 0
    for lvl, txt in headings:
        if prev and lvl > prev + 1:
            issues.append(
                Issue(
                    "Skipped heading hierarchy level",
                    "Low",
                    rel_label,
                    f"Jumped from H{prev} to H{lvl} ({txt[:45]})",
                    "Maintain sequential heading levels (H1 -> H2 -> H3).",
                )
            )
            break
        prev = lvl

    if word_count >= 500 and not has_external_link:
        issues.append(
            Issue(
                "Long draft has no external primary citations",
                "Low",
                rel_label,
                f"{word_count}-word piece contains 0 outbound http(s) references",
                "Verify and link primary documentation or authoritative sources supporting factual claims.",
            )
        )

    return issues


def run_content_validation(target: str, inspect_repo: bool = False) -> Tuple[List[Issue], Dict[str, str]]:
    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    issues: List[Issue] = []
    summary: Dict[str, str] = {}

    if path.is_file():
        issues.extend(analyze_content_file(path, path.name))
        summary["Mode"] = "Single Content File"
        return issues, summary

    if inspect_repo or (path / "package.json").is_file() or (path / "prisma").is_dir():
        arch = detect_publishing_architecture(path)
        summary["Framework"] = f"{arch['framework']} ({arch['version'] or 'unknown'})"
        summary["Publishing Mode"] = arch["publishing_mode"]
        if arch["db_orm_or_cms"]:
            summary["DB / CMS Detected"] = ", ".join(arch["db_orm_or_cms"])
        if arch["prisma_models"]:
            summary["Prisma Models"] = ", ".join(arch["prisma_models"])
        if arch["content_dirs"]:
            summary["Content Directories"] = ", ".join(arch["content_dirs"])

    files = iter_repo_files(path, {".md", ".mdx", ".html", ".htm"})
    summary["Files Scanned"] = str(len(files))
    for f in files:
        issues.extend(analyze_content_file(f, str(f.relative_to(path))))
    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate content quality, citations, headings, and repo publishing stack.")
    parser.add_argument("target", help="Content file (.md/.mdx/.html) or repository directory")
    parser.add_argument("--inspect-repo", action="store_true", help="Include framework and DB/CMS detection summary")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_content_validation(args.target, inspect_repo=args.inspect_repo)
    except Exception as exc:
        print(f"Error validating content: {exc}", file=sys.stderr)
        return 1

    print(format_report("Content Quality & Architecture Check", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
