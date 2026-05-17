```yml
created_at: 2026-05-04 19:58:53
project: THYROX
work_package: 2026-05-04-19-53-57-list-table-errors-fix
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# R-09 — List-table Column Mismatch ERRORs

## Origen

Build log `b75ert8rr` (pre-fixes concurrent build): 7 ERRORs across 2 files:
`uniform two-level bullet list expected, but row N does not contain the same
number of items as row 1 (7 vs 8)` and `(4 vs 2)`.

## Causa raíz

Sphinx `list-table` directive requires that every data row has exactly the
same number of cells as declared by `:widths:` (or as established by the
first/header row). Two distinct root causes across the two files:

### Causa A — raci-modulo.rst (PROVEN)

`:widths: 8 30 12 10 10 10 10 10` declares 8 columns.
Header row: `ID | Funcion | AdmNT | AdmT | Op | TLB | Aud | Comp` = 8 cols.
All 8 data rows had 7 cells each — the "Funcion" description column was
structurally declared but never populated in any data row.

Root cause: a "Funcion" column was added to the header/widths but data rows
were never updated to include it.

### Causa B — concerns-principles-decisions.rst (PROVEN)

2-column table (`:widths: 30 70`). Row 4 ("Decisiones pendientes") had 4
items instead of 2: `H-14` text, `H-15` text, and `Operational viewpoint`
text as three separate bullet items plus the row-header cell. Sphinx
counted 4 cells in a row where 2 were expected.

Root cause: three related decision items were listed as separate bullet cells
instead of being combined into the single second column.

## Inventario — 7 ERRORs en 2 archivos

| Archivo | Líneas | Tipo | ERRORs |
|---------|--------|------|--------|
| `normativa/gobernanza/raci-rbac/raci-modulo.rst` | 136, 236, 280, 373, 459, 503 | Causa A | 6 |
| `base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/concerns-principles-decisions.rst` | 640 | Causa B | 1 |
| **Total** | | | **7** |

## Fix aplicado

### raci-modulo.rst — dos pasos

1. **`:widths:`** — `8 30 12 10 10 10 10 10` → `8 12 10 10 10 10 10`
   (eliminar columna Funcion de las widths, 8→7 columnas). 8 ocurrencias.

2. **Header "Funcion"** — patrón ` * - ID\n   - Funcion\n` → ` * - ID\n`
   (eliminar línea de cabecera Funcion en el header row). 8 ocurrencias.

Verificación post-fix (PROVEN): script Python confirmó 8 tablas × 7 cols
uniformes en todas las filas.

### concerns-principles-decisions.rst — merge de celdas

Row 4 col 2: los tres items separados (H-14, H-15, Operational viewpoint)
fueron unificados en una sola celda usando párrafos separados por línea en
blanco (forma RST para múltiples párrafos dentro de una celda de tabla).

## Build logs

- `logs/build-after-fix-2026-05-04T195839.txt` — build post-fix: 0 ERRORs,
  `build succeeded.` sin warnings en los archivos modificados.
