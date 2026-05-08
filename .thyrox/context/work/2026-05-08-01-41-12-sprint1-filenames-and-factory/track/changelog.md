```yml
created_at: 2026-05-08 02:30:00
project: IACT-docs
work_package: 2026-05-08-01-41-12-sprint1-filenames-and-factory
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — Sprint 1 (filenames sod + ReportFactory)

## [1.0.0] — 2026-05-08

### Renamed (WP-H — 1 archivo)

`source/requisitos/_metodologia-aplicacion/patrones-diseno/factory-reportefactory.rst`
→ `factory-method-reportes.rst`.

Clase ejemplificada renombrada:

- `ReportFactory` → `ReportTypeRegistry` (registry/dispatcher
  polimórfico de subclases de `IReport`, NO Assembler/Generator).
- `SoDComplianceReport` → `SeparationComplianceReport`
  (consistencia con regla "no Sod en identificadores").
- Nota historica documentando el rename.
- Cross-refs actualizados (`index.rst` toctree +
  `tpl-uc-larman-contratos.rst`).

### Renamed (WP-A — 10 archivos)

| # | Filename antiguo | Nuevo | Cross-refs |
|---|---|---|---|
| 1 | `reglas-negocio/br-007-separacion-funciones-sod.rst` | `br-007-separacion-de-funciones.rst` | 9 |
| 2 | `reglas-negocio/rbac/sod.rst` | `rbac/separacion-de-deberes.rst` | 3 + toctree |
| 3 | `arquitectura-tecnica/design-view/act-sod-check.rst` | `act-validacion-separacion.rst` | 1 + toctree |
| 4 | `normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod.rst` | `cnst-030-reglas-de-separacion-de-funciones.rst` | 18 |
| 5 | `requisitos-funcionales/access/uc-010.../fr-010-02-validar-sod-antes-asignar.rst` | `fr-010-02-validar-separacion-antes-asignar.rst` | 1 toctree |
| 6 | `normativa/gobernanza/raci-rbac/raci-sod.rst` | `raci-separacion-de-deberes.rst` | 1 toctree |
| 7 | `arquitectura-tecnica/modulos/rbac-core/diagramas/evaluacion-conflicto-sod.rst` | `evaluacion-conflicto-separacion.rst` | 1 toctree |
| 8 | `casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst` | `diagrama-de-estados-separation-rule.rst` | 1 toctree |
| 9 | `casos-uso/access/uc-acc-01/diagramas-uml/diagrama-de-sod-validation.rst` | `diagrama-de-validacion-separacion.rst` | 1 toctree |
| 10 | `casos-uso/access/uc-acc-05/diagramas-uml/diagrama-de-estados-sodrule.rst` | `diagrama-de-estados-separation-rule.rst` | 1 toctree |

**Total cross-refs actualizadas:** ~37 + 9 toctrees.

### Restriccion respetada

NO se modifico contenido **interno** de los archivos
renombrados (excepto el de WP-H que requeria explicacion del
rename). La narrativa interna SoD/sod queda para Sprint 2
(WP-B y WP-C).

### Verification

```bash
# Cero filenames con sod
$ find source/ -name "*sod*.rst"
(vacio)

# Cero cross-refs huerfanos
for old in br-007-...-sod rbac/sod act-sod-check cnst-030-...-sod \
           fr-010-02-validar-sod-... raci-sod evaluacion-conflicto-sod \
           diagrama-de-estados-sod-rule diagrama-de-sod-validation \
           diagrama-de-estados-sodrule; do
  grep -rln "$old" source/
done
(vacio)
```

## Commits del WP

12 commits totales:

1. WP setup.
2. WP-H — ReportFactory rename.
3-12. WP-A — 10 renames de filenames sod.
13. (este commit) — TR cierre.

## Sprint 1 cerrado

Roadmap del audit clean-code-naming:

| WP | Estado |
|---|---|
| WP-A | ✅ 10/10 |
| WP-D | ✅ Resuelto en WP previo (naming-rules-resolution) |
| WP-H | ✅ |

Sprint 2 disponible (WP-B, WP-C, WP-E).
Sprint 3 disponible (WP-F, WP-G).

## Refs

- WP `naming-rules-resolution` (cerrado, predecesor).
- WP `clean-code-naming-audit` (cerrado, audit-only).
- CLEAN_CODE_NAMING_PRINCIPLES §1.4, §5, §8.2.
