```yml
created_at: 2026-05-06 08:25:00
project: IACT-docs
work_package: 2026-05-06-08-10-51-uc-rpt-sp-flujo-principal-rewrite
phase: Phase 10 — EXECUTE (B-1..B-5 done)
author: NestorMonroy
status: En progreso
version: 0.5.0
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

## B-2 — UC_RPT_13 (sp_rpt_llamadas_abandonadas)

### Changed

- `flujo-principal.rst`: PASOs 7-8 reescritos a un solo
  `ReportingService.callproc('sp_rpt_llamadas_abandonadas',
  [period, segments])`. Renumerados 9..11 → 8..10. Nota
  CNST-007.
- `actores-precondiciones.rst`: AnalyticsRepo →
  ReportingService (callproc); precondicion BD_IVR + SP;
  postcondicion read-only.
- `implementacion-tecnica.rst`: ReportingService agregado a
  componentes; pseudocodigo usa callproc + parser
  AbandonReportOutput.from_rows; restricciones cross-cutting.
- `datos-involucrados.rst`: Base Analitica IVR → BD_IVR via
  callproc al SP.
- `excepciones.rst`, `criterios-aceptacion.rst`,
  `testing.rst`: BD timeout → callproc BD_IVR timeout;
  UT-01..03 testean parser de filas del SP, no calculos
  derivados en backend.
- `diagramas-uml/diagrama-de-caso-de-uso.rst`: actores
  KpiCalculator/Bucket/BaseReportService removidos; reemplazados
  por ReportingService (SP) → BD_IVR.

### Verification

- Strict build OK: `execute/build-logs/sphinx-strict-b2-uc-rpt-13-
  2026-05-06T08-27-48.log` (EXIT=0).

## B-3 — UC_RPT_15 (DOBLE: sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento)

### Changed

- `flujo-principal.rst`: PASO 7 dividido en PASO 7a + 7b
  (un callproc por SP); PASO 8 = combinar result sets sin
  recalculo; nota CNST-007 + DOBLE SP.
- `actores-precondiciones.rst`: AnalyticsRepo →
  ReportingService con dos callprocs.
- `implementacion-tecnica.rst`: ReportingService como
  componente principal con DOBLE SP; pseudocodigo invoca
  los dos SPs y compone TransferReportOutput.from_rows;
  restricciones cross-cutting.
- `datos-involucrados.rst`: Base Analitica IVR → BD_IVR
  via DOS SPs.
- `excepciones.rst`, `criterios-aceptacion.rst`,
  `testing.rst`: BD timeout → callproc BD_IVR timeout
  (cualquiera de los 2 SPs); UT-01..03 testean parsers
  contra filas de cada SP.
- `diagramas-uml/diagrama-de-caso-de-uso.rst`: actores
  TransferReportService/Call/TimingCalculator removidos;
  reemplazados por ReportingService (2 SPs) → BD_IVR.

### Verification

- Strict build OK: `execute/build-logs/sphinx-strict-b3-uc-rpt-15-
  2026-05-06T08-31-22.log` (EXIT=0).

## B-4 — UC_RPT_16 (TRIPLE: sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR)

### Changed

- `flujo-principal.rst`: PASOs 7-8 reescritos en sub-vistas
  (PASO 7a/7b/7c) — un callproc por SP segun la `vista`
  solicitada; PASO 8 = combinar / parsear sin recalculo;
  nota CNST-007 + TRIPLE SP. Las sub-vistas son ALTERNAS
  (un panel UI por vista), no flujos paralelos.
- `actores-precondiciones.rst`: AnalyticsRepo →
  ReportingService con tres callprocs.
- `implementacion-tecnica.rst`: ReportingService como
  componente principal con TRIPLE SP; pseudocodigo con
  diccionario `SP_BY_VISTA` que dispatcha vista→SP;
  parser MenuReportOutput.from_rows; restricciones
  cross-cutting.
- `datos-involucrados.rst`: Base Analitica IVR → BD_IVR
  via TRES SPs (uno por sub-vista).
- `excepciones.rst`, `criterios-aceptacion.rst`,
  `testing.rst`: BD timeout → callproc BD_IVR timeout
  (cualquiera de los 3 SPs); UT-01..03 testean parsers
  de las filas de cada SP, no PathMiner.
- `patrones-diseno.rst`: P-74 reformulado como "Triple SP
  por sub-vista" (no "Path mining bounded"); explica el
  trade-off.
- `diagramas-uml/diagrama-de-caso-de-uso.rst`: actores
  IvrNavigationReportService/Bucket/Call removidos;
  reemplazados por ReportingService (3 SPs) → BdIvrLegacy
  con un usecase por vista (Vista: redirigidos /
  menu_centro / errores). Aliases STD-011 compliant.

### Verification

- Strict build OK: `execute/build-logs/sphinx-strict-b4-aliases-fix-
  2026-05-06T08-37-17.log` (EXIT=0). Build previo
  `sphinx-strict-b4-uc-rpt-16-2026-05-06T08-35-15.log` tambien EXIT=0.
- STD-011 alias compliance verificada en B-1..B-4 (commit
  separado: aliases SP/BDIVR/INVOKER → ReportingService/
  BdIvrLegacy/view_reports).

## B-5 — UC_RPT_17 (sp_rpt_clientes + ETL anonimizacion)

### Changed

- `flujo-principal.rst`: PASOs 7-10 reescritos como un solo
  callproc a `sp_rpt_clientes`; el SP entrega distinct count
  (exact o HLL), recurrence distribution, new vs returning
  y Top N por hash anonimizado. Nota explicita del orden
  canonico: ETL anonymize → SP (lee hash) → backend.
  Renumerados a 10 PASOs. CNST-007 + CNST-026.
- `actores-precondiciones.rst`: AnalyticsRepo →
  ReportingService (callproc) + actor ETL upstream
  (sp_etl_base_clientes) como precondicion de los datos.
  Postcondicion: backend NUNCA ve telefono raw.
- `implementacion-tecnica.rst`: ReportingService como
  componente principal; pseudocodigo callproc + parser
  ClientReportOutput.from_rows; restricciones cross-cutting
  (CNST-007, CNST-026, Top N solo prefix).
- `datos-involucrados.rst`: Base Analitica IVR → BD_IVR
  con base_ivr_clientes ya anonimizada por el ETL upstream.
- `excepciones.rst`, `criterios-aceptacion.rst`,
  `testing.rst`: BD timeout → callproc BD_IVR timeout;
  UT-01..05 testean parsers de filas del SP en lugar de
  DistinctCounter / RecurrenceCalculator / Comparative
  Calculator / TopN locales.
- `diagramas-uml/diagrama-de-caso-de-uso.rst`: actores
  CallerReportService/Sanitizer/Call/KpiCalculator
  removidos; reemplazados por ReportingService (1 SP) +
  EtlAnonimizador (upstream) → BdIvrLegacy. Aliases
  STD-011 compliant. La nota CNST-026 anclada al ETL
  (donde realmente ocurre el hash), no al backend.

### Verification

- Strict build OK: `execute/build-logs/sphinx-strict-b5-uc-rpt-17-
  2026-05-06T08-42-04.log` (EXIT=0).

## Resumen del WP

| Batch | UC | SPs | Status |
|---|---|---|---|
| B-1 | UC_RPT_01 | sp_rpt_centros_xsegmento | ✅ |
| B-2 | UC_RPT_13 | sp_rpt_llamadas_abandonadas | ✅ |
| B-3 | UC_RPT_15 | sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento | ✅ DOBLE |
| B-4 | UC_RPT_16 | sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR | ✅ TRIPLE |
| B-5 | UC_RPT_17 | sp_rpt_clientes + ETL anonimizacion | ✅ |

5 UCs × 12 partes (incluyendo diagramas-uml) auditadas y
alineadas con el patron canonico cursor.callproc('sp_rpt_*')
sobre BD_IVR. STD-011 compliance en aliases UML.

Strict build (`-W`) OK tras cada batch — 6 logs en
`execute/build-logs/`.

Pendiente: cierre Phase 11 cuando el ejecutor lo ordene
(I-011: solo el ejecutor cierra el WP). (sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento)
- B-4 UC_RPT_16 (sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR)
- B-5 UC_RPT_17 (sp_rpt_clientes + ETL anonimizacion)
- Cierre WP en Phase 11.
