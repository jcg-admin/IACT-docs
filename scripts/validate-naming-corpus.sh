#!/usr/bin/env bash
# validate-naming-corpus.sh — STD-008 §3.5 enforcement universal.
#
# Check C-07 corpus-wide: detecta identificadores en español
# en declaraciones de clase/entidad en TODO source/, sin
# exclusiones por zona (per STD-008 §3.5.1 — sin excepciones).
#
# Replaces validate-naming-arquitectura-tecnica.sh (que tenía
# whitelist de zonas pedagógicas, ahora invalido per STD-008
# v1.3.0).

set -euo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel)}"

# Patrones de identificadores en español prohibidos
SPANISH_PATTERNS=(
  '^\s*(class|entity) +(Usuario|Sesion|Llamada|Operador|Reporte|Permiso|Funcion|Grupo|Asignacion|Auditoria|Evento|Cliente|Cuenta|Empleado|Mensaje|Producto|Pedido|Carro|Pago|Direccion|Catalogo|Pagina|Tarjeta)\b'
  '^\s*(class|entity) +[A-Z][a-z]*[A-Z][a-z]*(Llamada|Llamadas|Reporte|Reportes|Auditoria|Permiso|Permisos|Cliente|Clientes|Usuario|Usuarios|Sesion|Funcion|Funciones|Grupo|Grupos|Asignacion|Asignaciones|Disparador|Reintento|Cancelacion|Ejecucion|Excepcional|Empleado|Empleados|Producto|Productos|Pedido|Pedidos|Catalogo|Tarjeta|Pagina)\b'
  '^\s*(class|entity) +(Detalle|Tipo|Estado|Modelo|Fabricante|Cargo|Departamento|Unidad|Vendedor|Caja|Comprobante|Saldo|Tarea)[A-Z][a-z]+'
)

# Excluir solo cache de SVGs y zonas no aplicables
EXCLUDE_PATHS=(
  "source/_generated_diagrams"
  "source/_static"
)

violations_total=0
declare -a violations=()

# Build find exclude args
exclude_args=""
for ex in "${EXCLUDE_PATHS[@]}"; do
  exclude_args="$exclude_args -path $REPO_ROOT/$ex -prune -o"
done

while IFS= read -r f; do
  for pattern in "${SPANISH_PATTERNS[@]}"; do
    while IFS= read -r line; do
      rel=${f#$REPO_ROOT/}
      violations+=("$rel: $line")
      violations_total=$((violations_total+1))
    done < <(grep -nE "$pattern" "$f" 2>/dev/null || true)
  done
done < <(find "$REPO_ROOT/source" \( -path "$REPO_ROOT/source/_generated_diagrams" -o -path "$REPO_ROOT/source/_static" \) -prune -o -name "*.rst" -type f -print)

cat <<REPORT
=== validate-naming-corpus audit (STD-008 §3.5 / C-07) ===

Corpus auditado: source/ (excluyendo _generated_diagrams, _static).

Política STD-008 v1.3.0: identifiers SIEMPRE en inglés, sin
excepciones por zona. La narrativa puede ser español; los
identifiers (class, entity, attribute, method) en inglés.

Total violations: $violations_total
REPORT

set +u
if [ ${#violations[@]} -gt 0 ]; then
  echo
  echo "Violations:"
  for v in "${violations[@]}"; do echo "  - $v"; done | head -50
  if [ ${#violations[@]} -gt 50 ]; then
    echo "  ... y $((${#violations[@]} - 50)) más."
  fi
  echo
  echo "AUDIT FAILED — $violations_total identifiers en español detectados."
  echo "Per STD-008 v1.3.0 §3.5: traducir al inglés (vocabulario canónico)."
  exit 1
fi

echo
echo "AUDIT PASSED — 0 violations"
exit 0
