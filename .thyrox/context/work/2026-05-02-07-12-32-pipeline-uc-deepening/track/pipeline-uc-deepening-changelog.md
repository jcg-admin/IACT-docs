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

- discover/reports-uc-analysis.md — análisis de UCs de MOD_Reports en la
  referencia vs los reportes reales del IVR. HALLAZGO CRÍTICO: los 14
  UC_RPT de temp-holding usan conceptos genéricos (Agentes/Colas/Campañas)
  incompatibles con IACT real. Documenta los 7 reportes IVR reales con
  columnas conocidas de scripts SQL, naming de scripts de producción
  (q_cMENU_ERROR.sql, q_menu_centro_transferecia_*.sql), y 5 nuevos gaps
  documentales (G-23..G-27). Agrega preguntas P-09..P-11 sobre naming
  definitivo de tablas limpias.

## Decisiones (confirmadas por el equipo, 2026-05-02)

- **D-01:** Prefijo `rpt_` para todas las tablas limpias MySQL.
- **D-02:** Scope 1 = 7 reportes. Reportes futuros quedan en open clause.
  Tablas: `rpt_menu_centro`, `rpt_clientes_unicos`, `rpt_llamadas_abandonadas`,
  `rpt_centros_transferencia`, `rpt_colgadas`, `rpt_cMENU_ERROR`,
  `rpt_menu_redirigidos`.
- **D-03:** `rpt_menu_redirigidos` es tabla separada de `rpt_menu_centro`.
- **D-04:** No existe tabla de tracking del ETL aún. Se diseñará junto con los SPs.
- **D-05:** Los 14 UC_RPT de la referencia (Agentes/Colas/Campañas) deben
  reescribirse desde cero. Los reportes reales son IVR-específicos.
- **D-06:** Triggers y Jobs se crearán en MySQL para mantener integridad
  de las tablas limpias una vez que sean pobladas. Todo el ETL ocurre
  exclusivamente en MySQL — sin componente Python ni proceso externo.
- **D-07:** ETL diario usa TRUNCATE+INSERT dentro de transacción. Si el
  SP falla, ROLLBACK automático conserva los datos del run anterior.
- **D-08:** Events/Jobs MySQL se disparan diariamente.
- **D-09:** Django es solo monitoreo — no puede disparar ni reiniciar el
  ETL manualmente. UC_PIP_04 queda como notificación, no acción técnica.
- **D-10:** Misma instancia MySQL para tablas IVR y tablas limpias `rpt_*`.
  La única BD separada es PostgreSQL para datos de la aplicación Django
  (usuarios, sesiones, permisos).
- **D-11:** Todas las tablas limpias `rpt_*` incluyen columna `quarter_name`
  ('Q01_25', 'Q02_25', 'Q03_25') para filtrado por trimestre.
- **D-12:** Tabla `c_dias_festivos (fecha DATE, activo CHAR(1))` existe en
  MySQL como soporte para `fn_es_dia_habil` y `fn_agregar_dias_habiles`.
- **D-13:** Campo `etiquetas` en `llamadas_QN` es CSV separado por comas
  (máx 6 posiciones observadas en Q3 2025). Función `fn_extraer_etiqueta`
  lo parsea por posición.

## Schemas confirmados desde datos reales (2026-05-02)

- discover/reports-uc-analysis.md — nueva sección 11 con schemas confirmados
  desde reportes reales (Excel/tabular) compartidos por el equipo:
  `rpt_centros_transferencia` (11 columnas), `rpt_clientes_unicos` (3 columnas),
  reporte `llamadas_cmenu` (4 columnas, tabla destino pendiente de mapeo).
  Volumen total confirmado: 34,101,981 llamadas Q01-Q03 2025.

- discover/etl-architecture-correction.md — nueva sección 11 con volumen de
  datos brutos (~34.1M registros en tbl_historico_*) vs datos limpios (cientos
  de filas en rpt_*). Confirmación definitiva de D-07 (TRUNCATE+INSERT correcto
  porque las tablas limpias son agregados, no registros individuales).

## Decisiones nuevas (confirmadas por datos reales, 2026-05-02)

- **D-14:** `rpt_centros_transferencia` tiene 11 columnas: `trimestre`, `fecha`,
  `800_transfer`, `centro_transferencia`, `menu`, `opcion`, `total_llamadas`,
  `porcentaje`, `misma_linea`, `linea_diferente`, `no_digito_telefono`.
- **D-15:** La columna `fecha` en las tablas limpias almacena formato YYYYMM
  (e.g. `202501`, `202502`), NO es tipo DATE de MySQL.
- **D-16:** Las tablas limpias `rpt_*` almacenan datos AGREGADOS (decenas a
  cientos de filas por quarter), no registros brutos. TRUNCATE+INSERT sobre
  ellas es trivialmente rápido. D-07 CONFIRMADO definitivamente.
- **D-17:** El segmento Nacional tiene dos sub-grupos físicamente distintos:
  `nacional_A` (DID 19028031) y `nacional_B` (DID 19020001). En `rpt_clientes_unicos`
  aparecen como dos filas separadas. En otros reportes pueden aparecer sumados
  bajo `'Nacional'`.

## Gaps nuevos identificados

- **G-28:** El reporte `llamadas_cmenu` (cDID_800Transfer, trimestre, cMenu,
  total_llamadas) no mapea claramente a ninguna tabla del catálogo D-02. ¿Es
  el origen de `rpt_menu_centro` en forma simplificada, o es una tabla nueva?
  Pendiente confirmar con el equipo.
- **G-29:** La causa exacta del problema en `dFecha` de `tbl_historico_t2/t3_2025`
  no está documentada formalmente. Evidencia indirecta: `CASO_ERROR_CEROS` aparece
  en Q02/Q03 pero no en Q01, sugiriendo degradación de datos desde Q2 2025.

## Status de promoción a CHANGELOG.md raíz
Pendiente — el WP está en Phase 1 DISCOVER.
