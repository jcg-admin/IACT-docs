#!/usr/bin/env bash
# validate-naming-arquitectura-tecnica.sh — STD-008 §3.5.2 enforcement.
#
# Check C-07: detecta identificadores en español en zonas productivas:
#   - source/arquitectura-tecnica/**/*.rst (excepto _metodologia y _uml subpaths)
#   - source/databases/**/*.rst
#
# Las zonas pedagógicas declaradas en STD-008 §3.5.1 se excluyen:
#   - source/requisitos/_metodologia-aplicacion/**
#   - source/base-cognitiva/_uml/**
#   - source/normativa/estandares/metodologia-*-ucs.rst

set -euo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel)}"

# Vocabulario español prohibido en clases/entities (PascalCase compounds)
SPANISH_PATTERNS=(
  'class +(Usuario|Sesion|Llamada|Operador|Reporte|Permiso|Funcion|Grupo|Asignacion|Auditoria|Evento|Cliente|Cuenta|Empleado|Mensaje|Producto|Pedido|Carro|Pago|Direccion)\b'
  'entity +(Usuario|Sesion|Llamada|Operador|Reporte|Permiso|Funcion|Grupo|Asignacion|Auditoria|Evento|Cliente)\b'
  'class +[A-Z][a-z]*[A-Z][a-z]*(Llamadas|Llamada|Reporte|Reportes|Auditoria|Permiso|Permisos|Cliente|Clientes|Usuario|Usuarios|Sesion|Funcion|Funciones|Grupo|Grupos|Asignacion|Asignaciones|Disparador|Reintento|Cancelacion|Ejecucion)\b'
)

# Productive zones (in-scope for this audit)
PRODUCTIVE_PATHS=(
  "source/arquitectura-tecnica"
  "source/databases"
)

violations_total=0
declare -a violations=()

for productive in "${PRODUCTIVE_PATHS[@]}"; do
  full_path="$REPO_ROOT/$productive"
  [ ! -d "$full_path" ] && continue

  while IFS= read -r f; do
    # check for any spanish pattern
    for pattern in "${SPANISH_PATTERNS[@]}"; do
      while IFS= read -r line; do
        rel=${f#$REPO_ROOT/}
        violations+=("$rel: $line")
        violations_total=$((violations_total+1))
      done < <(grep -nE "$pattern" "$f" 2>/dev/null || true)
    done
  done < <(find "$full_path" -name "*.rst" -type f)
done

cat <<REPORT
=== validate-naming-arquitectura-tecnica audit (STD-008 §3.5.2 / C-07) ===
Zonas productivas auditadas:
$(for p in "${PRODUCTIVE_PATHS[@]}"; do echo "  - $p"; done)

Zonas pedagógicas excluidas (STD-008 §3.5.1):
  - source/requisitos/_metodologia-aplicacion/
  - source/base-cognitiva/_uml/
  - source/normativa/estandares/metodologia-*-ucs.rst

Total violations: $violations_total
REPORT

set +u
if [ ${#violations[@]} -gt 0 ]; then
  echo
  echo "Violations:"
  for v in "${violations[@]}"; do echo "  - $v"; done
  echo
  echo "AUDIT FAILED — $violations_total identificadores en español en zona productiva."
  echo "Per STD-008 §3.5.2: traducir a inglés (vocabulario canónico del domain-model)."
  exit 1
fi

echo
echo "AUDIT PASSED — 0 violations"
exit 0
