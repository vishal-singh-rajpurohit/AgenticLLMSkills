#!/usr/bin/env bash
set -euo pipefail

TARGET=""
SCOPE="project"
PROJECT_DIR="$(pwd)"
POLICY_ONLY=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --policy-only) POLICY_ONLY=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Usage: $0 --target <claude|codex|antigravity|cursor> [--scope <project|global>] [--project-dir <path>] [--policy-only] [--dry-run]" >&2; exit 1 ;;
  esac
done

[[ -n "$TARGET" ]] || { echo "Error: --target is required." >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$(cd "$SCRIPT_DIR/.." && pwd)"

case "$TARGET:$SCOPE" in
  claude:project)      DEST_BASE="$PROJECT_DIR/.claude/skills" ;;
  claude:global)       DEST_BASE="$HOME/.claude/skills" ;;
  codex:project)       DEST_BASE="$PROJECT_DIR/.agents/skills" ;;
  codex:global)        DEST_BASE="$HOME/.codex/skills" ;;
  antigravity:project) DEST_BASE="$PROJECT_DIR/.agents/skills" ;;
  antigravity:global)  DEST_BASE="$HOME/.gemini/config/skills" ;;
  cursor:project)      DEST_BASE="$PROJECT_DIR/.cursor/skills" ;;
  cursor:global)       DEST_BASE="$HOME/.cursor/skills" ;;
  *) echo "Invalid target/scope: $TARGET:$SCOPE" >&2; exit 1 ;;
esac

DEST="$DEST_BASE/agent-token-efficiency"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "[Dry Run] Would install to $DEST (policy_only=$POLICY_ONLY)"
  exit 0
fi

if [[ "$POLICY_ONLY" == "true" ]]; then
  mkdir -p "$DEST/references"
  cp "$SKILL_SRC/references/default-policy.md" "$DEST/references/default-policy.md"
else
  mkdir -p "$DEST"
  for item in SKILL.md README.md references templates scripts examples; do
    if [[ -e "$SKILL_SRC/$item" ]]; then
      rm -rf "$DEST/$item"
      cp -R "$SKILL_SRC/$item" "$DEST/$item"
    fi
  done
  if [[ "$TARGET" == "codex" && -f "$SKILL_SRC/adapters/codex/agents/openai.yaml" ]]; then
    mkdir -p "$DEST/agents"
    cp "$SKILL_SRC/adapters/codex/agents/openai.yaml" "$DEST/agents/openai.yaml"
  fi
fi
echo "Installed agent-token-efficiency to $DEST"
