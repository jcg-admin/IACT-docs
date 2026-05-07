#!/bin/bash
# scripts/check-dependency-branch-alert.sh
# Detect dependency lock changes in PRs targeting main and emit branch sync alerts.

set -euo pipefail

EVENT_PATH="${GITHUB_EVENT_PATH:-}"

if [ -z "$EVENT_PATH" ] || [ ! -f "$EVENT_PATH" ]; then
  echo "::error::GITHUB_EVENT_PATH no está disponible."
  exit 1
fi

BASE_SHA="${GITHUB_BASE_SHA:-}"
HEAD_SHA="${GITHUB_HEAD_SHA:-}"

if [ -z "$BASE_SHA" ]; then
  BASE_SHA="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["pull_request"]["base"]["sha"])' "$EVENT_PATH")"
fi

if [ -z "$HEAD_SHA" ]; then
  HEAD_SHA="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["pull_request"]["head"]["sha"])' "$EVENT_PATH")"
fi

if [ -z "$BASE_SHA" ] || [ -z "$HEAD_SHA" ]; then
  echo "::error::No se pudieron resolver BASE_SHA y HEAD_SHA del evento."
  exit 1
fi

CHANGED_FILES="$(git diff --name-only "$BASE_SHA" "$HEAD_SHA")"

CHANGED_PYPROJECT=false
CHANGED_UV_LOCK=false

if echo "$CHANGED_FILES" | grep -qx 'pyproject.toml'; then
  CHANGED_PYPROJECT=true
fi

if echo "$CHANGED_FILES" | grep -qx 'uv.lock'; then
  CHANGED_UV_LOCK=true
fi

ALERT_REQUIRED=false
if [ "$CHANGED_PYPROJECT" = true ] || [ "$CHANGED_UV_LOCK" = true ]; then
  ALERT_REQUIRED=true
fi

ALERT_MESSAGE=""
if [ "$ALERT_REQUIRED" = true ]; then
  ALERT_MESSAGE="⚠️ **Alerta de sincronización de ramas**\n\n"
  ALERT_MESSAGE+="Este PR modifica dependencias bloqueadas (**pyproject.toml**/**uv.lock**).\n"
  ALERT_MESSAGE+="Las demás ramas activas deberían hacer **merge/rebase con main** para evitar conflictos y desalineación de dependencias.\n"

  if [ "$CHANGED_PYPROJECT" = true ] && [ "$CHANGED_UV_LOCK" = false ]; then
    ALERT_MESSAGE+="\n❗ Se cambió **pyproject.toml** sin cambios en **uv.lock**. Recomendación: regenerar lockfile antes del merge.\n"
  fi

  if [ "$CHANGED_PYPROJECT" = false ] && [ "$CHANGED_UV_LOCK" = true ]; then
    ALERT_MESSAGE+="\nℹ️ Se cambió solo **uv.lock**. Verifica que corresponda a cambios intencionales de resolución.\n"
  fi

  echo "::warning::$ALERT_MESSAGE"
fi

{
  echo "alert_required=$ALERT_REQUIRED"
  echo "changed_pyproject=$CHANGED_PYPROJECT"
  echo "changed_uv_lock=$CHANGED_UV_LOCK"
  echo "message<<EOF"
  echo -e "$ALERT_MESSAGE"
  echo "EOF"
} >> "$GITHUB_OUTPUT"
