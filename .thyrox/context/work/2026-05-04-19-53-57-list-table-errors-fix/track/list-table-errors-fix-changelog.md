```yml
created_at: 2026-05-04 19:58:53
updated_at: 2026-05-04 19:58:53
project: THYROX
work_package: 2026-05-04-19-53-57-list-table-errors-fix
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# Changelog — list-table-errors-fix (R-09)

## Added

- `discover/list-table-errors-fix-analysis.md` — análisis de 7 ERRORs en 2
  archivos: causa A (columna declarada pero sin datos) y causa B (demasiadas
  celdas en una fila de tabla de 2 columnas).
- `logs/build-after-fix-2026-05-04T195839.txt` — log del build post-fix.

## Fixed

- **`normativa/gobernanza/raci-rbac/raci-modulo.rst`** — 6 ERRORs corregidos:
  - `:widths:` reducido de 8 a 7 columnas (eliminada columna "Funcion" vacía
    en las 8 tablas del archivo).
  - Línea de cabecera `Funcion` eliminada del header row de las 8 tablas.
  - Verificación: 8 tablas × 7 columnas uniformes (script Python).

- **`base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/concerns-principles-decisions.rst`**
  — 1 ERROR corregido: fila 4 de tabla 2-columnas tenía 4 celdas; los tres
  items (H-14, H-15, Operational viewpoint) unificados en un solo párrafo
  multi-entrada en la segunda columna.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main`. Entrada sugerida bajo `### Fixed`:

```
- Corregir 7 ERRORs de list-table column mismatch en 2 archivos RST (R-09):
  raci-modulo.rst (6 tablas con columna Funcion declarada pero vacía) y
  concerns-principles-decisions.rst (fila con demasiadas celdas).
```
