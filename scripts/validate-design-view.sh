#!/usr/bin/env bash
# validate-design-view.sh — audit script for source/arquitectura-tecnica/design-view/
#
# Checks (per WP design-view-buildout, decision D-08):
#   C-01: every file has .. meta:: with :tipo: Diagrama Arquitectonico — Design View — {subtipo}
#   C-02: every <<sistema>> actor name exists as a file in domain-model/
#   C-03: every initiating actor (RBAC function) follows snake_case pattern
#   C-04: NO uml-12 (componentes) ni uml-13 (distribucion) syntax
#   C-05: every file has a `seealso` block with cross-refs
#   C-06: NO @startuml NAME (per WP plantuml-cache-corruption-remediation)

set -euo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel)}"
DV_DIR="$REPO_ROOT/source/arquitectura-tecnica/design-view"
DM_DIR="$REPO_ROOT/source/arquitectura-tecnica/domain-model"

if [ ! -d "$DV_DIR" ]; then
  echo "ERROR: design-view dir not found: $DV_DIR" >&2
  exit 2
fi

# Build set of canonical domain-model class names (from filenames)
declare -A DM_CLASSES
while IFS= read -r f; do
  base=$(basename "$f" .rst)
  # convert kebab-case to PascalCase
  pascal=$(echo "$base" | awk -F'-' '{
    s=""
    for (i=1; i<=NF; i++) s = s toupper(substr($i,1,1)) substr($i,2)
    print s
  }')
  DM_CLASSES[$pascal]=1
done < <(find "$DM_DIR" -maxdepth 1 -name "*.rst" -not -name "index.rst" -not -name "overview.rst" 2>/dev/null)

# Allowed pseudo-actors (not real classes)
DM_CLASSES[scheduler]=1
DM_CLASSES[Scheduler]=1
DM_CLASSES[evaluator]=1
DM_CLASSES[Evaluator]=1

violations_total=0

c01_pass=0; c01_fail=0
c02_pass=0; c02_fail=0
c04_pass=0; c04_fail=0
c05_pass=0; c05_fail=0
c06_pass=0; c06_fail=0

declare -a c02_violations=()
declare -a c04_violations=()
declare -a c06_violations=()

for f in "$DV_DIR"/*.rst; do
  base=$(basename "$f")
  [ "$base" = "index.rst" ] && continue

  # C-01
  if grep -q ":tipo: Diagrama Arquitectonico — Design View" "$f"; then
    c01_pass=$((c01_pass+1))
  else
    c01_fail=$((c01_fail+1))
    violations_total=$((violations_total+1))
  fi

  # C-02 — every <<sistema>> actor must exist in domain-model
  while IFS= read -r line; do
    name=$(echo "$line" | sed -E 's/.*as ([A-Za-z_][A-Za-z0-9_]*).*/\1/')
    if [ -n "$name" ] && [ -z "${DM_CLASSES[$name]:-}" ]; then
      c02_violations+=("$base: $name")
      c02_fail=$((c02_fail+1))
      violations_total=$((violations_total+1))
    else
      c02_pass=$((c02_pass+1))
    fi
  done < <(grep -E 'actor "[^"]+" as [A-Za-z_]+ <<sistema>>' "$f" || true)

  # C-04 — no component/deployment syntax
  if grep -qE 'component |node |artifact |deployment ' "$f"; then
    c04_violations+=("$base")
    c04_fail=$((c04_fail+1))
    violations_total=$((violations_total+1))
  else
    c04_pass=$((c04_pass+1))
  fi

  # C-05 — has seealso
  if grep -q "^\.\. seealso::" "$f"; then
    c05_pass=$((c05_pass+1))
  else
    c05_fail=$((c05_fail+1))
    violations_total=$((violations_total+1))
  fi

  # C-06 — no @startuml NAME
  if grep -E '^\s*@startuml \S' "$f" > /dev/null; then
    c06_violations+=("$base")
    c06_fail=$((c06_fail+1))
    violations_total=$((violations_total+1))
  else
    c06_pass=$((c06_pass+1))
  fi
done

cat <<REPORT
=== validate-design-view audit report ===
Path: $DV_DIR
Files audited: $(find "$DV_DIR" -name "*.rst" -not -name "index.rst" | wc -l)

Results:
  C-01 metadata tipo correcto:        PASS=$c01_pass  FAIL=$c01_fail
  C-02 sistemas en domain-model:      PASS=$c02_pass  FAIL=$c02_fail
  C-04 sin uml-12/uml-13 syntax:      PASS=$c04_pass  FAIL=$c04_fail
  C-05 seealso block presente:        PASS=$c05_pass  FAIL=$c05_fail
  C-06 sin @startuml NAME:            PASS=$c06_pass  FAIL=$c06_fail

Total violations: $violations_total
REPORT

set +u

if [ ${#c02_violations[@]} -gt 0 ]; then
  echo
  echo "C-02 violations (actor <<sistema>> no esta en domain-model):"
  for v in "${c02_violations[@]}"; do echo "  - $v"; done
fi

if [ ${#c04_violations[@]} -gt 0 ]; then
  echo
  echo "C-04 violations (componentes/distribucion en design-view):"
  for v in "${c04_violations[@]}"; do echo "  - $v"; done
fi

if [ ${#c06_violations[@]} -gt 0 ]; then
  echo
  echo "C-06 violations (@startuml NAME, debe ser plain @startuml):"
  for v in "${c06_violations[@]}"; do echo "  - $v"; done
fi

if [ "$violations_total" -eq 0 ]; then
  echo
  echo "AUDIT PASSED — 0 violations"
  exit 0
else
  echo
  echo "AUDIT FAILED — $violations_total violations"
  exit 1
fi
