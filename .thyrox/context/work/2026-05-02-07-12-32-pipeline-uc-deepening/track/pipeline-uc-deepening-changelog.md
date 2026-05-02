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

## Análisis de scripts SQL de producción (2026-05-02)

- discover/real-db-schema-analysis.md — análisis de dos scripts SQL:
  `q_menu_centro_transferecia_010925.sql` y `REPTRIM001-WS.sql`. Hallazgos:
  columnas `dHoraInicio`/`dHoraFin` (DATETIME) confirmadas en schema real;
  bug en `@ONacionalB = 19028031` (debería ser `19020001`) en script de análisis;
  `cEtiquetacliente` es el campo raw que `llamadas_QN` normaliza a `etiquetas`;
  el problema reportado en "campo de fecha" es `dHoraInicio`/`dHoraFin`
  (registros con inicio > fin), NO `dFecha`.

- discover/etl-architecture-correction.md — sección 12 nueva: anti-patrón
  documentado de REPTRIM001-WS.sql que tardó 1 día completo. El script materializa
  ~34M filas en tabla temporal y luego indexa — patrón prohibido para SPs de ETL.
  Corrección: agregar directamente en SELECT y escribir solo el resultado (~centenas
  de filas) en la tabla rpt_*.

## Bugs documentados en scripts de análisis (NO reproducir en SPs de producción)

| Bug | Script | Valor incorrecto | Correcto |
|---|---|---|---|
| `@ONacionalB` mismo DID que A | `q_menu_centro_transferecia_010925.sql` | `19028031` | `19020001` |
| `@ONacional02` dígito faltante | `REPTRIM001-WS.sql` | `1902001` | `19020001` |
| `@ONacional02` ausente en Q2/Q3 | `REPTRIM001-WS.sql` | IN solo 2 DIDs | 3 DIDs en todos los quarters |
| Q1 empieza en febrero | `REPTRIM001-WS.sql` | `2025-02-01` | `2025-01-01` |
| Q3 termina en julio | `REPTRIM001-WS.sql` | `2025-07-31` | `2025-09-30` |

## Gaps y decisiones adicionales

- **G-29 (actualizado):** El problema de "campo de fecha" es en realidad
  `dHoraInicio`/`dHoraFin` — registros donde `dHoraInicio > dHoraFin`. `dFecha`
  funciona correctamente. El workaround ABS() en scripts produce duraciones incorrectas
  para llamadas que cruzan medianoche.
- **G-30:** Bug en `@ONacionalB = 19028031` en `q_menu_centro_transferecia_010925.sql`.
  Nacional B nunca se consulta con este script.
- **G-31 (CERRADO — confirmado 2026-05-02):** `tbl_historico_*` NO tienen índices.
  Full table scans de ~11-14M filas/quarter en cada run del ETL. → CNST-ETL-005.
- **P-12 (CERRADA — confirmado 2026-05-02):** No es posible. IACT solo tiene acceso
  de lectura a `tbl_historico_*`. No puede agregar índices al sistema IVR del cliente.

## Nuevas restricciones de arquitectura

- **CNST-ETL-005:** Las tablas `tbl_historico_tN_YYYY` no tienen índices y IACT no
  puede crearlos. Todo acceso del ETL es full table scan. Los SPs deben: (a) una sola
  pasada por tabla por run, (b) todos los DIDs en un solo `WHERE IN`, (c) nunca
  materializar datos brutos en tablas temporales intermedias.

- **CNST-ETL-006:** Las tablas `rpt_*`, creadas y controladas por IACT, DEBEN tener
  índices definidos en el `CREATE TABLE`. Mínimo: `INDEX(trimestre)` y
  `INDEX(trimestre, <columna_segmento>)` en cada tabla. `TRUNCATE+INSERT` conserva
  la definición de índices — no se necesita DROP/CREATE INDEX durante el ETL.

## Arquitectura ETL rediseñada — 2 tablas base (2026-05-02)

- discover/etl-job-flow-design.md — **v2.0.0** (reescritura completa): nueva
  arquitectura de 2 tablas base en lugar de 7 tablas `rpt_*`. Motivo: con
  `tbl_historico_*` sin índices, 7 SPs ETL = 7 full table scans (~14M filas c/u).
  2 tablas base = 2 scans totales. Tablas: `base_ivr_detalle` (grain:
  quarter+fecha+segmento+centro+menu+opcion, 5 métricas) y `base_ivr_clientes`
  (COUNT DISTINCT no aditivo, separado por diseño). 7 SPs de reporte READ-ONLY
  llamados por Django bajo demanda.

- **D-18:** `base_ivr_detalle` y `base_ivr_clientes` son las únicas tablas de
  destino del ETL. Los 7 reportes se derivan de estas bases mediante SPs de lectura.
- **D-19:** Los SPs `sp_rpt_*` son exclusivamente READ-ONLY y pueden ser llamados
  por Django bajo demanda. Django NO puede llamar `sp_etl_*` (D-09 se mantiene).

## Hallazgos del AS-IS COMPLETO (2026-05-02)

- **CNST-ETL-007 (NUEVO):** El motor es **MariaDB 10.1.48** — versión legacy que
  NO incluye window functions (`OVER`, `PARTITION BY`, `ROW_NUMBER`, `LAG`, etc.).
  Window functions llegaron en MariaDB 10.2. Todos los SPs deben usar subconsultas
  correlacionadas o JOINs a subconsultas en lugar de funciones de ventana.

- discover/etl-job-flow-design.md — **v2.1.0**: dos SPs corregidos para MariaDB 10.1:
  - `sp_rpt_centros_transferencia`: `OVER(PARTITION BY fecha, segmento)` reemplazado
    por subconsulta correlacionada con alias `t`.
  - `sp_rpt_menu_centro`: `OVER(PARTITION BY centro_transferencia)` reemplazado
    por JOIN a subconsulta de totales por centro.
  - Fila agregada en tabla de información: "MariaDB 10.1 no tiene window functions".

- **G-32 (ABIERTO):** Conflicto en rango de Q1 2025. AS-IS COMPLETO define
  Q1=01-Feb-2025→31-Mar-2025 (59 días). El WP y `sp_etl_maestro` usan
  Q1=01-Jan-2025→31-Mar-2025 (90 días). El script REPTRIM001-WS.sql también
  arrancaba en Feb (bug documentado en G-29). Pendiente confirmar con el equipo
  cuál es el rango real de Q1 2025 en el sistema.

- **Confirmación de G-29:** El AS-IS COMPLETO cuantifica la inversión
  `dHoraInicio > dHoraFin` en **38.8% de los ~34.1M registros** (~13.2M afectados).
  Confirma que `dFecha` (DATE) está correcto. El campo problemático es exclusivamente
  el par de DATETIMEs de hora.

- **Nuevas métricas del sistema (PROVEN desde AS-IS):**
  - 96 centros de transferencia activos en Q3 2025
  - 25 menús distintos activos
  - `cTelefono_Digitado` NULL: 75.3% de registros (baseline para `no_digito_telefono`)
  - Volumen total Q01-Q03 2025: 34,101,981 llamadas (ya documentado en D-16)

## Preguntas abiertas nuevas

- **P-15 (ABIERTA):** ¿El rango real de Q1 2025 es enero-marzo (01-Jan → 31-Mar)
  o febrero-marzo (01-Feb → 31-Mar)? Determina `v_inicio` en `sp_etl_maestro`
  para el branch ELSEIF Q01_25. Ver G-32.

## Status de promoción a CHANGELOG.md raíz
Pendiente — el WP está en Phase 1 DISCOVER.
