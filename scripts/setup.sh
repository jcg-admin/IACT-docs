#!/usr/bin/env bash
# Bootstrap del entorno de desarrollo IACT-docs.
# Crea .venv via uv, instala dependencias y activa git hooks.
# Idempotente — seguro de re-ejecutar.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "==> 1/3 Verificando 'uv'"
if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: 'uv' no está instalado. Instala con: pip install uv" >&2
  exit 1
fi

echo "==> 2/3 Sincronizando dependencias (uv sync)"
uv sync

echo "==> 3/3 Activando git hooks"
bash "$REPO_ROOT/scripts/install-hooks.sh"

echo
echo "OK: Entorno listo. Para construir docs:"
echo "  source .venv/bin/activate   # Linux/macOS"
echo "  source .venv/Scripts/activate   # Windows Git Bash"
echo "  make html"
