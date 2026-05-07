#!/bin/bash
# scripts/check-dependency-branch-alert.sh
# Detect dependency lock changes in PRs targeting main and emit branch sync alerts.

set -euo pipefail

EVENT_PATH="${GITHUB_EVENT_PATH:-}"

if [ -z "$EVENT_PATH" ] || [ ! -f "$EVENT_PATH" ]; then
  echo "::error::GITHUB_EVENT_PATH is not available."
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
  echo "::error::Unable to resolve BASE_SHA and HEAD_SHA from event payload."
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
  ALERT_MESSAGE="⚠️ **Branch synchronization alert**\n\n"
  ALERT_MESSAGE+="This PR modifies locked dependencies (**pyproject.toml**/**uv.lock**).\n"
  ALERT_MESSAGE+="Other active branches should **merge/rebase with main** to avoid dependency drift and future lockfile conflicts.\n"

  if [ "$CHANGED_PYPROJECT" = true ] && [ "$CHANGED_UV_LOCK" = false ]; then
    ALERT_MESSAGE+="\n❗ **pyproject.toml** changed without **uv.lock**. Recommendation: regenerate the lockfile before merge.\n"
  fi

  if [ "$CHANGED_PYPROJECT" = false ] && [ "$CHANGED_UV_LOCK" = true ]; then
    ALERT_MESSAGE+="\nℹ️ Only **uv.lock** changed. Verify this matches an intentional dependency resolution update.\n"
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
