#!/usr/bin/env bash
# Reproducible audit runner. Persists log per build-logs.md rule (ISO 8601).
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WP="$REPO_ROOT/.thyrox/context/work/2026-05-05-21-56-47-functional-decomposition-antipattern-audit"
ISO="$(date -u +%Y-%m-%dT%H-%M-%S)"
LOG_DIR="$WP/track/build-logs"
LOG="$LOG_DIR/audit-run-$ISO.log"
mkdir -p "$LOG_DIR"

OUT="$WP/track/build-logs/audit-data-$ISO.json"
{
  echo "=== audit-functional-decomposition run @ $ISO UTC ==="
  echo "repo_root: $REPO_ROOT"
  echo "git HEAD: $(git -C "$REPO_ROOT" rev-parse HEAD)"
  echo "git branch: $(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
  echo "---"
  python3 "$WP/scripts/audit_functional_decomposition.py" \
      --root "$REPO_ROOT" --out "$OUT"
  echo "EXIT=$?"
  echo "---"
  echo "=== aggregated report ==="
  python3 "$WP/scripts/report_from_audit_data.py" --data "$OUT"
} >"$LOG" 2>&1

echo "audit complete. log: $LOG"
echo "json:           $OUT"
tail -20 "$LOG"
