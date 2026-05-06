```yml
created_at: 2026-05-06 08:15:00
project: IACT-docs
work_package: 2026-05-06-08-04-31-uc-rpt-stored-procedures-alignment
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — UC_RPT Stored Procedures Alignment (DISCOVER-only)

## Naturaleza del WP

WP de **diagnóstico**. Phase 1 DISCOVER completada con
identificación del gap, mapeo SP→UC, hallazgo causa raíz, y
propuesta de 3 opciones de remediación.

La ejecución (opción B aprobada por el ejecutor) se deriva
a un **WP sucesor dedicado** para mantener separación clara
entre análisis y ejecución masiva.

## Hallazgo principal

5 UC_RPT (`UC_RPT_01, 13, 15, 16, 17`) describen agregación
ORM en su `flujo-principal.rst` cuando el backend realmente
ejecuta `cursor.callproc('sp_rpt_*')` contra el IVR legacy.

7 stored procedures legacy mapeados a los 5 UCs:

- sp_rpt_llamadas_abandonadas → UC_RPT_13
- sp_rpt_centros_transferencia → UC_RPT_15
- sp_rpt_centros_xsegmento → UC_RPT_15, UC_RPT_01
- sp_rpt_menu_redirigidos → UC_RPT_16
- sp_rpt_menu_centro → UC_RPT_16
- sp_rpt_cMENU_ERROR → UC_RPT_16
- sp_rpt_clientes → UC_RPT_17

## Added

- `discover/uc-rpt-stored-procedures-alignment-analysis.md` —
  Phase 1 con cobertura por zona, mapeo SP↔UC, gap por UC,
  causa raíz, opciones de remediación (A/B/C).
- Este changelog.

## Decisión del ejecutor (SP-01)

**Opción B aprobada** — audit completo de todas las 12 partes
de los 5 UCs. Ejecución se delega a WP sucesor.

## WP sucesor derivado

`{TS}-uc-rpt-sp-flujo-principal-rewrite` — bootstrap inminente
con plan de batches por UC (B-1..B-5) y por parte del UC
(informacion-general, actores-precondiciones, flujo-principal,
flujos-alternos, excepciones, datos-involucrados,
implementacion-tecnica, criterios-aceptacion, requisitos-no-
funcionales, patrones-diseno, testing, diagramas-uml).

## Refs

- Predecesor: `2026-05-05-20-28-12-use-case-view-uml07-
  standalone-pass`.
- Patrón canónico: `arquitectura-tecnica/modulos/vis-reports/
  diagramas/secuencia-sp-rpt-flujo-completo.rst`.
- Identificación del gap por el ejecutor.
