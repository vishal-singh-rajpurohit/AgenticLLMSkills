"""Estimate file/text token size (labeled approximation) or summarize official API usage JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPTS_ROOT = Path(__file__).resolve().parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import estimate_tokens, iter_repo_files, read_text_safe  # noqa: E402


def summarize_api_usage(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extract actual provider token telemetry from Anthropic, OpenAI, or Gemini responses."""
    usage = payload.get("usage") or payload.get("usage_metadata") or payload
    if not isinstance(usage, dict):
        raise ValueError("Usage JSON must contain an object under `usage`, `usage_metadata`, or root.")

    if "cache_read_input_tokens" in usage or "cache_creation_input_tokens" in usage:
        return {
            "provider_format": "Anthropic",
            "input_tokens": usage.get("input_tokens"),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
            "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "measurement_type": "actual_api_telemetry",
        }
    if "cached_content_token_count" in usage or "prompt_token_count" in usage:
        return {
            "provider_format": "Google Gemini",
            "input_tokens": usage.get("prompt_token_count"),
            "cached_input_tokens": usage.get("cached_content_token_count"),
            "output_tokens": usage.get("candidates_token_count"),
            "reasoning_tokens": usage.get("thoughts_token_count"),
            "total_tokens": usage.get("total_token_count"),
            "measurement_type": "actual_api_telemetry",
        }
    details = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
    return {
        "provider_format": "OpenAI / Generic",
        "input_tokens": usage.get("prompt_tokens", usage.get("input_tokens")),
        "cached_input_tokens": details.get("cached_tokens"),
        "output_tokens": usage.get("completion_tokens", usage.get("output_tokens")),
        "total_tokens": usage.get("total_tokens"),
        "measurement_type": "actual_api_telemetry",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate text/file tokens (approx) or summarize API usage JSON.")
    parser.add_argument("target", nargs="?", help="File or directory path to estimate")
    parser.add_argument("--text", help="Inline text string to estimate")
    parser.add_argument("--usage-json", help="Path to saved LLM API response JSON to extract actual token metrics")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        if args.usage_json:
            upath = Path(args.usage_json).resolve()
            if not upath.is_file():
                raise FileNotFoundError(f"Usage JSON file not found: {args.usage_json}")
            telemetry = summarize_api_usage(json.loads(read_text_safe(upath)))
            print(json.dumps(telemetry, indent=2) if args.format == "json" else "\n".join(f"- **{k}:** {v}" for k, v in telemetry.items()))
            return 0

        if args.text is not None:
            res = estimate_tokens(args.text)
            print(json.dumps(res, indent=2) if args.format == "json" else f"Approx tokens: ~{res['approx_tokens']} ({res['estimation_method']})")
            return 0

        if not args.target:
            raise ValueError("Provide a target file/directory path, --text, or --usage-json.")

        tpath = Path(args.target).resolve()
        if not tpath.exists():
            raise FileNotFoundError(f"Target path does not exist: {args.target}")

        files = [tpath] if tpath.is_file() else iter_repo_files(tpath, {".md", ".txt", ".py", ".ts", ".tsx", ".js", ".json"})
        rows: List[Dict[str, Any]] = []
        total_approx = 0
        total_bytes = 0
        for f in files:
            stats = estimate_tokens(read_text_safe(f))
            total_approx += stats["approx_tokens"]
            total_bytes += stats["bytes"]
            rel = f.name if tpath.is_file() else str(f.relative_to(tpath)).replace("\\", "/")
            rows.append({"path": rel, **stats})

        rows.sort(key=lambda r: r["approx_tokens"], reverse=True)
        payload = {
            "estimation_method": "heuristic_chars_div_4 (approximation, not exact model tokenizer count)",
            "files_scanned": len(rows),
            "total_bytes": total_bytes,
            "total_approx_tokens": total_approx,
            "files": rows[:25],
        }
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(f"# Token Estimation Report\n\n- **Method:** {payload['estimation_method']}\n- **Files Scanned:** {len(rows)}\n- **Total Approx Tokens:** ~{total_approx:,} ({total_bytes:,} bytes)\n")
            print("| File | Lines | Bytes | Approx Tokens |\n|---|---:|---:|---:|")
            for r in rows[:20]:
                print(f"| `{r['path']}` | {r['lines']} | {r['bytes']:,} | ~{r['approx_tokens']:,} |")
    except Exception as exc:
        print(f"Error estimating tokens: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
