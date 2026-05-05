#!/usr/bin/env bash
# build-with-log.sh — wrapper para registrar builds con timestamp ISO en el WP activo
#
# Uso:
#   bash scripts/build-with-log.sh <nombre-corto> -- <comando-make-o-sphinx>
#
# Ejemplos:
#   bash scripts/build-with-log.sh build-full-cached -- make html
#   bash scripts/build-with-log.sh build-strict -- .venv/bin/sphinx-build -W -j auto -b html -d build/doctrees source build/html
#
# Lee el WP activo desde .thyrox/context/now.md (campo current_work).

set -euo pipefail

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <nombre-corto> -- <comando...>" >&2
    exit 2
fi

NOMBRE="$1"
shift
if [[ "$1" != "--" ]]; then
    echo "Falta '--' antes del comando" >&2
    exit 2
fi
shift

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Resolver WP activo
WP_PATH=$(grep -E '^current_work:' .thyrox/context/now.md | head -1 | sed 's|^current_work: *||' | tr -d '"')
if [[ -z "$WP_PATH" || ! -d "$WP_PATH" ]]; then
    echo "WARN: WP activo no resuelto, usando .thyrox/context/build-logs" >&2
    WP_PATH=".thyrox/context"
fi

LOG_DIR="$WP_PATH/build-logs"
mkdir -p "$LOG_DIR"

ISO_TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
LOG_FILE="$LOG_DIR/${ISO_TS}-${NOMBRE}.log"

# Metadata
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
HEAD="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
SPHINX_VER="$(.venv/bin/sphinx-build --version 2>/dev/null | head -1 || echo 'sphinx not found')"

START_EPOCH=$(date +%s)
START_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
    echo "=== BUILD LOG — ${NOMBRE} ==="
    echo "Timestamp ISO:  ${START_ISO}"
    echo "Comando:        $*"
    echo "Working dir:    ${REPO_ROOT}"
    echo "Sphinx:         ${SPHINX_VER}"
    echo "Branch:         ${BRANCH}"
    echo "HEAD:           ${HEAD}"
    echo
    echo "--- COMBINED OUTPUT (stdout + stderr) ---"
} > "$LOG_FILE"

set +e
"$@" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?
set -e

END_EPOCH=$(date +%s)
END_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
WALL=$(( END_EPOCH - START_EPOCH ))

WARN_COUNT=$(grep -cE "WARNING|warning" "$LOG_FILE" 2>/dev/null || echo 0)
ERR_COUNT=$(grep -cE "ERROR|FATAL" "$LOG_FILE" 2>/dev/null || echo 0)

{
    echo
    echo "--- RESULTADO ---"
    echo "End ISO:        ${END_ISO}"
    echo "Exit code:      ${EXIT_CODE}"
    echo "Wall clock:     ${WALL}s ($((WALL / 60))m $((WALL % 60))s)"
    echo "Warnings count: ${WARN_COUNT}"
    echo "Errors count:   ${ERR_COUNT}"
} >> "$LOG_FILE"

echo "Log saved: $LOG_FILE"
echo "Exit: $EXIT_CODE  Wall: ${WALL}s  Warns: $WARN_COUNT  Errs: $ERR_COUNT"

exit $EXIT_CODE
