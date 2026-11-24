#!/usr/bin/env bash
set -euo pipefail

TARGET=""
SCOPE="project"
PROJECT_DIR="$(pwd)"
DRY_RUN=false

usage() {
  cat <<EOF
Install project-documentation-architect for Claude Code, OpenAI Codex, Google Antigravity, or Cursor.

Usage:
  $0 --target <claude|codex|antigravity|cursor> [--scope <project|global>] [--project-dir <path>] [--dry-run]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "Error: --target is required." >&2
  usage
  exit 1
fi

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

DEST="$DEST_BASE/project-documentation-architect"
echo "Source:      $SKILL_SRC"
echo "Destination: $DEST"

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[Dry Run] Would install project-documentation-architect into $DEST"
  exit 0
fi

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

SHARED_POLICY="$SKILL_SRC/../../Context-Optimizer-Skill/agent-token-efficiency/references/default-policy.md"
if [[ -f "$SHARED_POLICY" ]]; then
  mkdir -p "$DEST_BASE/agent-token-efficiency/references"
  cp "$SHARED_POLICY" "$DEST_BASE/agent-token-efficiency/references/default-policy.md"
fi

echo "Installed project-documentation-architect to $DEST"
