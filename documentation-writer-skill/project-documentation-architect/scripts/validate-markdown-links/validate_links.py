"""Relative Markdown link, anchor fragment, and local-path validator."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    MD_LINK_RE,
    extract_markdown_anchors,
    iter_repo_files,
    read_text_safe,
    strip_markdown_code,
)

LOCAL_ABS_PATH_RE = re.compile(r"^(?:[A-Za-z]:[/\\]|/Users/|/home/)")


def validate_markdown_links(target: str) -> Tuple[List[Dict[str, str]], int]:
    """Validate all relative Markdown links and heading fragments in a file or repository."""
    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    md_files = [path] if path.is_file() else iter_repo_files(path, {".md"})
    base_root = path.parent if path.is_file() else path
    anchor_cache: Dict[Path, Set[str]] = {}
    findings: List[Dict[str, str]] = []

    def get_anchors(md_path: Path) -> Set[str]:
        if md_path not in anchor_cache:
            anchor_cache[md_path] = extract_markdown_anchors(read_text_safe(md_path))
        return anchor_cache[md_path]

    for md_file in md_files:
        rel_src = md_file.name if path.is_file() else str(md_file.relative_to(base_root)).replace("\\", "/")
        raw = read_text_safe(md_file)
        stripped = strip_markdown_code(raw)
        for match in MD_LINK_RE.finditer(stripped):
            raw_target = match.group(1).strip().split(" ", 1)[0]
            if not raw_target or raw_target.startswith(("http://", "https://", "mailto:", "tel:", "<")):
                continue
            if LOCAL_ABS_PATH_RE.match(raw_target):
                findings.append(
                    {
                        "file": rel_src,
                        "link": raw_target,
                        "issue": "Machine-local absolute filesystem path in Markdown link",
                    }
                )
                continue

            path_part, _, frag = raw_target.partition("#")
            path_part = urllib.parse.unquote(path_part.split("?", 1)[0]).strip()
            if not path_part:
                if frag and frag.lower() not in get_anchors(md_file):
                    findings.append(
                        {
                            "file": rel_src,
                            "link": raw_target,
                            "issue": f"Broken same-file heading anchor #{frag}",
                        }
                    )
                continue

            resolved = (md_file.parent / path_part).resolve()
            if not resolved.exists():
                findings.append(
                    {
                        "file": rel_src,
                        "link": raw_target,
                        "issue": "Broken relative path (target does not exist)",
                    }
                )
            elif frag and resolved.is_file() and resolved.suffix.lower() == ".md":
                if frag.lower() not in get_anchors(resolved):
                    findings.append(
                        {
                            "file": rel_src,
                            "link": raw_target,
                            "issue": f"Target heading anchor #{frag} not found in {path_part}",
                        }
                    )

    return findings, len(md_files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate relative Markdown links and heading anchors.")
    parser.add_argument("target", nargs="?", default=".", help="Markdown file or repository directory")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        findings, files_scanned = validate_markdown_links(args.target)
    except Exception as exc:
        print(f"Error validating Markdown links: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps({"files_scanned": files_scanned, "broken_count": len(findings), "findings": findings}, indent=2))
    else:
        print(f"# Markdown Link Validation\n\n**Files Scanned:** {files_scanned}\n**Issues Found:** {len(findings)}\n")
        if findings:
            print("| File | Link | Issue |\n|---|---|---|")
            for f in findings:
                print(f"| `{f['file']}` | `{f['link']}` | {f['issue']} |")
        else:
            print("All relative Markdown links and anchors resolved cleanly.")
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
