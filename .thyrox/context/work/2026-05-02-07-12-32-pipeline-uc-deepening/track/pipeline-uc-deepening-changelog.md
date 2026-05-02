```yml
created_at: 2026-05-02 07:12:32
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
author: NestorMonroy
```

# WP Changelog — pipeline-uc-deepening

## Added
- discover/pipeline-uc-deepening-analysis.md — análisis completo
  del estado actual del módulo pipeline: inventario, arquitectura ETL,
  modelos de datos, RBAC, restricciones, inconsistencias, gap analysis
  y orden de trabajo recomendado

- discover/ivr-schema-analysis.md — análisis del schema IVR extraído
  del material pedagógico (PARTE_0/PARTE_6). Confirmó: tabla `ivr_calls`
  con columnas `quarter`, `year`, `segment`, `status`, `duration_seconds`.
  NOTA: este schema corresponde al material pedagógico, no al schema real.
  Ver real-db-schema-analysis.md para la corrección.

- discover/canonical-findings.md — hallazgos completos de PARTE_0 y
  PARTE_6: módulos del sistema, CNST completas, actores RBAC (AGR-001..005),
  segmentos (OP/FI/VT/SP), BRs principales (BR-028, BR-031, BR-046, BR-053,
  BR-087, BR-104, BR-105), UC-RPT-01 completo con 12 pasos y 10 FRs,
  queries SQL de analytics_calls y ivr_calls, matriz RTM, 15 gaps documentales.

- discover/real-db-schema-analysis.md — HALLAZGO DISRUPTIVO: el schema
  real del MySQL IVR usa tablas `tbl_historico_tN_YYYY` (una por trimestre),
  NO una tabla `ivr_calls` con columna `quarter`. Columnas reales: `dFecha`,
  `cDID_800Transfer`, `cDID_Centro_Transferencia`, `cMenu`, `cOpcion`,
  `cTelefono_Origen`, `cTelefono_Digitado`. Vista normalizada `llamadas_QN`
  con 13+ columnas incluyendo `id_CTransferencia`, `id_8T`, `division`,
  `area`, `nidMQ`, `etiquetas`. 7 nuevos gaps documentales (G-16..G-22).

- discover/etl-architecture-correction.md — HALLAZGO CRÍTICO: la
  arquitectura ETL documentada en source/ (Python ETL + PostgreSQL
  Analytics) es incorrecta. La arquitectura real usa ETL MySQL-interno
  (Stored Procedures + Functions + Events/Jobs + Triggers) que limpia
  `tbl_historico_tN_YYYY` y escribe en tablas limpias (una por reporte).
  Django consume SOLO las tablas limpias MySQL. Identifica 5 archivos
  en source/ con BREAKING CHANGES, propone 4 nuevas CNST (CNST-ETL-001..004)
  y 8 preguntas abiertas (P-01..P-08) pendientes de confirmación del equipo.

## Status de promoción a CHANGELOG.md raíz
Pendiente — el WP está en Phase 1 DISCOVER.
