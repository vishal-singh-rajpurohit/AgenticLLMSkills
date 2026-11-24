"""Detect duplicated instruction blocks and repeated architecture paragraphs across Markdown files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPTS_ROOT = Path(__file__).resolve().parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import AuditFinding, format_report, iter_repo_files, read_text_safe  # noqa: E402


def _normalize_paragraph(para: str) -> str:
    return re.sub(r"\s+", " ", para.strip().lower())


def find_duplicate_blocks(target: str, min_chars: int = 160) -> Dict[str, Any]:
    root = Path(target).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Repository directory does not exist: {target}")

    md_files = iter_repo_files(root, {".md"})
    seen: Dict[str, List[Dict[str, str]]] = {}

    for f in md_files:
        rel = str(f.relative_to(root)).replace("\\", "/")
        txt = re.sub(r"```.*?```", "", read_text_safe(f), flags=re.DOTALL)
        # Split on blank lines, headings, or single-line bullet transitions to catch adjacent repeated prose
        chunks = re.split(r"\r?\n\s*\r?\n|(?=\r?\n#{1,6}\s+)|(?=\r?\n[-*]\s+)", txt)
        for raw_para in chunks:
            cleaned = re.sub(r"^#{1,6}\s+.*\r?\n?", "", raw_para.strip())
            norm = _normalize_paragraph(cleaned)
            if len(norm) < min_chars:
                continue
            digest = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]
            seen.setdefault(digest, []).append({"file": rel, "preview": cleaned.strip()[:100]})

        # Also check exact single non-empty lines >= min_chars (catches long pasted paragraphs inside dense blocks)
        for line in txt.splitlines():
            s = line.strip()
            if not s or s.startswith(("#", "-", "*", "|")):
                continue
            norm_line = _normalize_paragraph(s)
            if len(norm_line) >= min_chars:
                digest = hashlib.sha256(norm_line.encode("utf-8")).hexdigest()[:16]
                if not any(h["file"] == rel for h in seen.get(digest, [])):
                    seen.setdefault(digest, []).append({"file": rel, "preview": s[:100]})

    findings: List[AuditFinding] = []
    duplicates: List[Dict[str, Any]] = []
    for digest, hits in seen.items():
        distinct_files = sorted({h["file"] for h in hits})
        if len(distinct_files) > 1:
            duplicates.append({"hash": digest, "files": distinct_files, "preview": hits[0]["preview"]})
            findings.append(
                AuditFinding(
                    "Duplicate Documentation Block",
                    "Medium",
                    ", ".join(distinct_files[:4]),
                    f'Repeated text across {len(distinct_files)} files: "{hits[0]["preview"]}..."',
                    "Keep one canonical document/reference and link to it from other files.",
                )
            )

    summary = {
        "Target": str(root),
        "Markdown Files Scanned": len(md_files),
        "Duplicate Multi-File Blocks": len(duplicates),
    }
    return {"summary": summary, "duplicates": duplicates, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Find duplicated Markdown paragraphs across instruction and doc files.")
    parser.add_argument("target", nargs="?", default=".", help="Repository directory path")
    parser.add_argument("--min-chars", type=int, default=160, help="Minimum normalized paragraph length to compare")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        res = find_duplicate_blocks(args.target, min_chars=args.min_chars)
    except Exception as exc:
        print(f"Error scanning duplicate docs: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(
            json.dumps(
                {
                    "summary": res["summary"],
                    "duplicates": res["duplicates"],
                    "findings": [f.to_dict() for f in res["findings"]],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(format_report("Duplicate Documentation & Rule Audit", res["summary"], res["findings"], "markdown"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
