```yml
created_at: 2026-05-06 08:25:00
project: IACT-docs
work_package: 2026-05-06-08-10-51-uc-rpt-sp-flujo-principal-rewrite
phase: Phase 10 — EXECUTE (B-1 done)
author: NestorMonroy
status: En progreso
version: 0.1.0
```

# WP Changelog — UC_RPT SP Flujo Principal Rewrite

## B-1 — UC_RPT_01 (sp_rpt_centros_xsegmento)

### Changed

- `flujo-principal.rst`: PASO 7 reescrito — `cursor.callproc(
  'sp_rpt_centros_xsegmento', [period, segments])` en lugar de
  AnalyticsRepo + KPICalculator. PASO 8 anterior eliminado (KPIs
  pre-calculados en BD_IVR). PASOs renumerados 8..10. Tabla resumen
  3.2 reducida de 11 a 10 filas.
- `actores-precondiciones.rst`: AnalyticsRepo → ReportingService
  (callproc); precondicion BD_IVR + SP instalado; postcondicion
  read-only BD_IVR + operativa.
- `implementacion-tecnica.rst`: componentes — quitados
  AnalyticsRepo/KPICalculator/TrendBuilder; pseudocodigo usa
  callproc del SP; restricciones cross-cutting actualizadas
  (read-only BD_IVR, KPIs no re-agregados en backend).
- `criterios-aceptacion.rst`: CA-15 cita ETL BD_IVR; CA-16 explicita
  SP read-only sobre BD_IVR.
- `requisitos-no-funcionales.rst`: P50 cache miss = callproc;
  read replicas BD_IVR; mantenibilidad apunta a modificar el SP
  (no extender KPICalculator); cumplimiento cita CNST-007 sobre
  BD_IVR.
- `excepciones.rst`: EX-05 = BD_IVR / callproc timeout (no "Analytics
  timeout").
- `flujos-alternos.rst`: FA-01 = SP retorna 0 rows; FA-05 = ETL BD_IVR
  desfasado; FA-06 = segmentos como parametro al SP.
- `patrones-diseno.rst`: P-25 = read replicas BD_IVR; P-58 = filtro
  por segmento se pasa al SP, no en query directa.
- `datos-involucrados.rst`: entidad principal = BD_IVR consultada via
  `sp_rpt_centros_xsegmento`; KPIs los calcula el SP.
- `informacion-general.rst`: CNST-007 cita SP + BD_IVR.
- `diagramas-uml/diagrama-de-secuencia.rst`: secuencia muestra
  ReportingService → BD_IVR → filas pre-agregadas; KPICalculator
  removido.
- `diagramas-uml/diagrama-de-caso-de-uso.rst`: nota = "Read-only
  BD_IVR via SP".

### Verification

- Strict build OK: `execute/build-logs/sphinx-strict-b1-uc-rpt-01-
  2026-05-06T08-21-51.log` (EXIT=0, build succeeded).
- 0 referencias residuales a `AnalyticsRepo`, `KPICalculator`,
  `TrendBuilder`, `Analytics ` en uc-rpt-01/.

## Pendiente

- B-2 UC_RPT_13 (sp_rpt_llamadas_abandonadas)
- B-3 UC_RPT_15 (sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento)
- B-4 UC_RPT_16 (sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR)
- B-5 UC_RPT_17 (sp_rpt_clientes + ETL anonimizacion)
- Cierre WP en Phase 11.
