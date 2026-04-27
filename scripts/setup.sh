#!/usr/bin/env bash
# Bootstrap del entorno de desarrollo IACT-docs.
# Crea .venv via uv, instala dependencias del sistema requeridas, instala
# deps Python y activa git hooks. Idempotente — seguro de re-ejecutar.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "==> 1/5 Verificando 'uv'"
if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: 'uv' no está instalado. Instala con: pip install uv" >&2
  exit 1
fi

echo "==> 2/5 Verificando libsystem 'enchant' (requerido por sphinxcontrib-spelling)"
# enchant es una libsystem C, no un paquete Python. Detectar y advertir
# si falta. Solo intenta apt en sistemas Debian/Ubuntu.
need_enchant=false
if ! ldconfig -p 2>/dev/null | grep -qi enchant; then
  if [ -z "$(find /usr/lib /usr/local/lib /opt/homebrew/lib -name 'libenchant*' 2>/dev/null | head -1)" ]; then
    need_enchant=true
  fi
fi

if [ "$need_enchant" = true ]; then
  if command -v apt-get >/dev/null 2>&1; then
    echo "  -> instalando libenchant-2-2 via apt-get (puede pedir sudo)"
    if [ "$(id -u)" -eq 0 ]; then
      apt-get install -y libenchant-2-2
    else
      sudo apt-get install -y libenchant-2-2 || {
        echo "WARN: no se pudo instalar libenchant-2-2. Instalalo manualmente:" >&2
        echo "      sudo apt-get install libenchant-2-2  # Debian/Ubuntu" >&2
        echo "      brew install enchant                 # macOS" >&2
      }
    fi
  elif command -v brew >/dev/null 2>&1; then
    echo "  -> instalando enchant via Homebrew"
    brew install enchant
  else
    echo "WARN: enchant no encontrado y no se detectó apt-get ni brew." >&2
    echo "      Instalalo manualmente para que sphinx-spelling funcione." >&2
  fi
else
  echo "  -> enchant ya disponible"
fi

echo "==> 3/5 Verificando 'plantuml' (requerido por sphinxcontrib-plantuml)"
# plantuml es un binario Java, no paquete Python. sphinxcontrib-plantuml
# (en pyproject) solo lo invoca; sin él los .. uml:: producen warnings y
# diagramas vacíos en el HTML.
if ! command -v plantuml >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    echo "  -> instalando plantuml (jala openjdk como dependencia)"
    if [ "$(id -u)" -eq 0 ]; then
      apt-get install -y plantuml
    else
      sudo apt-get install -y plantuml || {
        echo "WARN: no se pudo instalar plantuml. Instalalo manualmente:" >&2
        echo "      sudo apt-get install plantuml  # Debian/Ubuntu" >&2
        echo "      brew install plantuml          # macOS" >&2
      }
    fi
  elif command -v brew >/dev/null 2>&1; then
    echo "  -> instalando plantuml via Homebrew"
    brew install plantuml
  else
    echo "WARN: plantuml no encontrado y no se detectó apt-get ni brew." >&2
    echo "      Los diagramas .. uml:: no se renderizarán hasta instalarlo." >&2
  fi
else
  echo "  -> plantuml ya disponible ($(plantuml -version 2>&1 | head -1))"
fi

echo "==> 4/5 Sincronizando dependencias (uv sync)"
uv sync

echo "==> 5/5 Activando git hooks"
bash "$REPO_ROOT/scripts/install-hooks.sh"

echo
echo "OK: Entorno listo. Para construir docs:"
echo "  source .venv/bin/activate   # Linux/macOS"
echo "  source .venv/Scripts/activate   # Windows Git Bash"
echo "  make html"
