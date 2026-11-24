"""Shared stdlib utilities for agent-token-efficiency auditing scripts."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "out",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "target",
    "coverage",
    "vendor",
}

INSTRUCTION_FILENAMES = {"CLAUDE.md", "AGENTS.md", "GEMINI.md", ".cursorrules"}
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass
class AuditFinding:
    category: str
    severity: str
    path: str
    observation: str
    recommendation: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def read_text_safe(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_repo_files(root: Path, extensions: Optional[Iterable[str]] = None) -> List[Path]:
    ext_set = {e.lower() for e in extensions} if extensions else None
    out: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for fname in sorted(filenames):
            p = Path(dirpath) / fname
            if ext_set is None or p.suffix.lower() in ext_set:
                out.append(p)
    return out


def estimate_tokens(text: str) -> Dict[str, Any]:
    """Return byte/line/word metrics and clearly labeled heuristic token approximation.

    Uses ~4 chars/token heuristic unless an external tokenizer is explicitly wired.
    Never claims heuristic output is an exact model token count.
    """
    chars = len(text)
    raw_bytes = len(text.encode("utf-8", errors="replace"))
    lines = len(text.splitlines())
    words = len(re.findall(r"\S+", text))
    approx_tokens = max(1, round(chars / 4)) if chars else 0
    return {
        "bytes": raw_bytes,
        "chars": chars,
        "lines": lines,
        "words": words,
        "approx_tokens": approx_tokens,
        "exact_tokens": None,
        "estimation_method": "heuristic_chars_div_4 (approximation, not exact tokenizer count)",
    }


def parse_skill_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.DOTALL)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end():]
    fields: Dict[str, str] = {}
    key: Optional[str] = None
    buf: List[str] = []
    for line in raw.splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km and not line.startswith((" ", "\t")):
            if key is not None:
                fields[key] = " ".join(buf).strip().strip('"').strip("'")
            key = km.group(1)
            val = km.group(2).strip()
            buf = [] if val in {">-", ">", "|", "|-"} else [val]
        elif key is not None and line.startswith((" ", "\t")):
            buf.append(line.strip())
    if key is not None:
        fields[key] = " ".join(buf).strip().strip('"').strip("'")
    return fields, body


def discover_instruction_files(root: Path, include_global: bool = False) -> Dict[str, List[Path]]:
    """Collect workspace rules, nested instructions, SKILL.md files, and optional global configs."""
    found: Dict[str, List[Path]] = {
        "root_instructions": [],
        "nested_instructions": [],
        "skills": [],
        "mcp_configs": [],
        "global_instructions": [],
    }

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        cur = Path(dirpath)
        for fname in sorted(filenames):
            p = cur / fname
            rel_parts = cur.relative_to(root).parts
            if fname in INSTRUCTION_FILENAMES or (".cursor" in rel_parts and "rules" in rel_parts) or (
                ".agents" in rel_parts and "rules" in rel_parts
            ):
                if cur == root:
                    found["root_instructions"].append(p)
                else:
                    found["nested_instructions"].append(p)
            elif fname == "SKILL.md":
                found["skills"].append(p)
            elif fname in {"mcp_config.json", ".mcp.json"}:
                found["mcp_configs"].append(p)

    if include_global:
        home = Path.home()
        for cand in (
            home / ".claude" / "CLAUDE.md",
            home / ".codex" / "AGENTS.md",
            home / ".gemini" / "config" / "GEMINI.md",
            home / ".gemini" / "GEMINI.md",
        ):
            if cand.is_file():
                found["global_instructions"].append(cand)

    return found


def format_report(title: str, summary: Dict[str, Any], findings: List[AuditFinding], fmt: str = "markdown") -> str:
    payload = {
        "title": title,
        "summary": summary,
        "findings": [f.to_dict() for f in findings],
    }
    if fmt == "json":
        return json.dumps(payload, indent=2, ensure_ascii=False)

    lines = [f"# {title}", ""]
    for k, v in summary.items():
        lines.append(f"- **{k}:** {v}")
    lines.extend(["", "| Category | Severity | File / Scope | Observation | Recommended Action |", "|---|---|---|---|---|"])
    if not findings:
        lines.append("| Clean | Informational | N/A | No context or instruction issues flagged | Maintain current density standards |")
    else:
        for f in findings:
            obs = f.observation.replace("|", "\\|").replace("\n", " ")
            rec = f.recommendation.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {f.category} | {f.severity} | `{f.path}` | {obs} | {rec} |")
    return "\n".join(lines)
