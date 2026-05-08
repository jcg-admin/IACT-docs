#!/usr/bin/env bash
# Reproducible audit runner.
# All paths are parameters — no hardcoded WP, repo or output locations.
#
# Usage:
#   run-audit.sh <repo-root> <wp-dir> [glob]
#
#   <repo-root>  absolute path to the repository to audit
#   <wp-dir>     absolute path to the work package directory
#   [glob]       optional file glob (default reads from config.yml)
#
# Output:
#   <wp-dir>/track/build-logs/audit-run-<ISO>.log
#   <wp-dir>/track/build-logs/audit-data-<ISO>.json
set -euo pipefail

if [ "$#" -lt 2 ]; then
    echo "usage: $0 <repo-root> <wp-dir> [glob]" >&2
    exit 64
fi

REPO_ROOT="$1"
WP="$2"
GLOB_ARG="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ISO="$(date -u +%Y-%m-%dT%H-%M-%S)"
LOG_DIR="$WP/track/build-logs"
LOG="$LOG_DIR/audit-run-$ISO.log"
OUT="$LOG_DIR/audit-data-$ISO.json"
CONFIG="$SCRIPT_DIR/audit-config.yml"
mkdir -p "$LOG_DIR"

PY_ARGS=(--root "$REPO_ROOT" --out "$OUT" --config "$CONFIG")
if [ -n "$GLOB_ARG" ]; then
    PY_ARGS+=(--glob "$GLOB_ARG")
fi

{
    echo "=== audit run @ $ISO UTC ==="
    echo "repo_root:  $REPO_ROOT"
    echo "wp_dir:     $WP"
    echo "config:     $CONFIG"
    echo "git HEAD:   $(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo n/a)"
    echo "git branch: $(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo n/a)"
    echo "---"
    python3 "$SCRIPT_DIR/audit_functional_decomposition.py" "${PY_ARGS[@]}"
    echo "EXIT=$?"
    echo "---"
    echo "=== aggregated report ==="
    python3 "$SCRIPT_DIR/report_from_audit_data.py" --data "$OUT"
} >"$LOG" 2>&1

echo "audit complete."
echo "  log:  $LOG"
echo "  json: $OUT"
tail -20 "$LOG"
