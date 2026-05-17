#!/bin/bash
# find-uc-stubs.sh
#
# Detecta los `diagrama-de-caso-de-uso.rst` creados como STUB en
# Nivel B (D-07) que aún esperan completarse en Nivel A.
#
# Patrón: contienen el marcador TODO específico del WP rebuild.
#
# Uso:
#   bash .thyrox/context/work/2026-05-05-14-49-16-use-case-view-uml07-rebuild/discover/find-uc-stubs.sh
#   bash ... | wc -l                 # contar stubs pendientes
#   bash ... | xargs ls -la          # listar con tamaños

cd "$(git rev-parse --show-toplevel)" 2>/dev/null || cd /home/user/IACT-docs

grep -l "TODO (use-case-view-uml07-rebuild Nivel A)" \
  source/requisitos/casos-uso/*/uc-*/diagramas-uml/diagrama-de-caso-de-uso.rst \
  2>/dev/null | sort
