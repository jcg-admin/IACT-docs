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

- **P-15 (CERRADA — 2026-05-02):** El maestro ahora usa `QUARTER(CURDATE())` y
  trimestres calendario estándar (Q1=ene-mar, Q2=abr-jun, Q3=jul-sep, Q4=oct-dic).
  La discrepancia en el AS-IS era el punto de inicio del sistema en 2025, no la
  definición del trimestre. G-32 cerrado.

## ETL dinámico y carga histórica (2026-05-02)

- discover/etl-job-flow-design.md — **v2.2.0**: `sp_etl_maestro` reescrito sin
  ELSEIF hardcodeado por año. Ahora usa `YEAR(CURDATE())` y `QUARTER(CURDATE())`
  para calcular dinámicamente: `v_quarter` ('Q02_26'), `v_table`
  ('tbl_historico_t2_2026'), `v_inicio`/`v_fin`. Funciona para cualquier año.

- `sp_etl_base_detalle` actualizado con 4to parámetro `p_table VARCHAR(50)`.
  Implementa PREPARE/EXECUTE para nombre de tabla dinámico (CNST-ETL-008).
  Eliminado el comentario "tabla dinámica en implementación real" — ahora es real.

- Nuevo SP `sp_etl_historico(p_year INT, p_quarter_num TINYINT)` para carga de
  quarters históricos bajo demanda. Event Scheduler solo toca el quarter actual.
  Ejemplo de uso para cargar Q1-Q4 2025 documentado en el SP.

- **G-32 (CERRADO):** El sistema usa trimestres calendario estándar.
  `QUARTER(CURDATE())` devuelve 1 para ene-mar, 2 para abr-jun, etc. La discrepancia
  Feb-Mar en el AS-IS refleja el inicio de operaciones en 2025, no la definición
  del trimestre.

## Decisiones nuevas

- **D-20:** Quarter y año se calculan dinámicamente con `YEAR(CURDATE())` y
  `QUARTER(CURDATE())`. Ningún SP tiene años o fechas hardcodeadas.
- **D-21:** El nombre de tabla `tbl_historico_tN_YYYY` se construye en
  `sp_etl_maestro` con CONCAT y se pasa como parámetro `p_table` a los SPs ETL.
- **D-22:** El Event Scheduler diario procesa **solo el quarter actual**. Los
  quarters históricos se cargan con `sp_etl_historico(year, quarter_num)` —
  ejecución manual, una sola vez por quarter ya cerrado.

## Nuevas restricciones de arquitectura

- **CNST-ETL-007:** MariaDB 10.1.48 (versión de producción, fuera de scope
  actualizar). Sin window functions (`OVER`, `PARTITION BY`, `ROW_NUMBER`, etc.).
  Todos los SPs usan subconsultas correlacionadas o JOINs a subconsultas como
  alternativa. Esta restricción es permanente.

- **CNST-ETL-008:** MariaDB 10.1 no permite usar una variable como identificador
  de tabla. Los SPs ETL que reciben `p_table` como parámetro usan PREPARE/EXECUTE
  con SQL dinámico construido via CONCAT. Los valores `p_quarter`, `p_inicio`,
  `p_fin` se incrustan literalmente (no son input de usuario — no hay riesgo
  de inyección SQL).

## Correcciones E05 v6.0 documentadas (2026-05-02)

- discover/e05-extract-corrected.md — documento nuevo: E05 v6.0 corregido
  con las 7 correcciones aplicadas (C-01..C-07). Mantiene la estructura
  de secciones del original pero con arquitectura, SQL y restricciones
  alineados al WP.

  Correcciones aplicadas:
  - C-01 (FATAL): Eliminada asunción de índices en `tbl_historico_*` — CNST-ETL-005
  - C-02 (FATAL): Arquitectura diaria row-level → trimestral agregada.
    `tbl_llamadas_limpias` eliminada. `base_ivr_detalle` + `base_ivr_clientes`
    reemplazan toda la capa de destino.
  - C-03 (FATAL): Columnas inexistentes eliminadas: `nidRegistro`,
    `nTiempoEsperaSeg`, `id_CTransferencia` (esta última está en `llamadas_QN`,
    no en `tbl_historico_*`).
  - C-04 (IMPORTANTE): `LAG(...) OVER (...)` en Anexo B reemplazado por
    `TIMESTAMPDIFF(MINUTE, start_time, end_time)` — compatible MariaDB 10.1.
  - C-05 (IMPORTANTE): UNION ALL hardcodeado (3 tablas 2025) → PREPARE/EXECUTE
    con tabla dinámica (`p_table` construido por sp_etl_maestro).
  - C-06 (IMPORTANTE): `WHERE DATE(dFecha) = p_fecha` → `WHERE dFecha BETWEEN
    p_inicio AND p_fin`. La forma original inhabilita índices incluso si existieran.
  - C-07 (IMPORTANTE): `fn_corregir_timestamps`, `fn_determinar_estado`,
    `fn_calcular_duracion` eliminadas — innecesarias en diseño agregado.
    Solo `fn_extraer_codigo_centro` se conserva como lógica inline.

- discover/etl-job-flow-design.md — **v2.2.0 (diagrama corregido)**: PASO 2
  del diagrama de flujo corregido de ELSEIF hardcodeado a cálculo dinámico
  con YEAR()/QUARTER().

## Reglas de negocio IVR documentadas (2026-05-02)

- discover/business-rules-ivr.md — documento nuevo con 4 BRs confirmadas
  por el equipo:

  - **BR-CLIENT-001:** Identificación del cliente por teléfono. Tres casos
    mutuamente excluyentes: `cTelefono_Origen = cTelefono_Digitado` → misma
    línea; `!=` → línea diferente; `cTelefono_Digitado IS NULL` → no digitó.
    Confirma la implementación actual de `misma_linea`, `linea_diferente`,
    `no_digito_telefono` en `base_ivr_detalle`.

  - **BR-ROUTING-001:** NK90 → IPVR: cuando `LENGTH(cDID_Centro_Transferencia) > 10`,
    los últimos 10 dígitos son `cTelefono_Digitado` concatenado por NK90.
    El VDN real es `LEFT(..., LENGTH - 10)`. Explica la causa raíz de la
    normalización ya implementada en `sp_etl_base_detalle`. La migración a IPVR
    cambiará este comportamiento para nuevas tablas (P-18).

  - **BR-MENU-001:** Múltiples menu+opcion pueden redirigir al mismo centro.
    `GROUP_CONCAT(DISTINCT CONCAT(cMenu, ':', cOpcion))` por VDN muestra el
    mapeo. Ejemplo: VDN `15070013` recibe de 6 combinaciones distintas. Este es
    el comportamiento esperado — no una anomalía en `base_ivr_detalle`.

  - **BR-ROUTING-002:** `cMenu = 'Desborde_Cabecera'` indica enrutamiento por
    `cEtiquetacliente`, no por navegación del menú IVR. NO es un sentinel de
    datos malos — es un valor semánticamente válido. No se normaliza en el ETL.
    Impacto en `sp_rpt_llamadas_abandonadas` y `sp_rpt_menu_redirigidos`
    pendiente de confirmar (P-16, P-17).

- discover/real-db-schema-analysis.md — nueva sección 5.1: causa raíz del
  `LENGTH > 10` en la normalización de centro. Documenta el comportamiento
  NK90 con ejemplo real de concatenación (BR-ROUTING-001).

- discover/etl-job-flow-design.md — tabla de sentinels ampliada:
  - `Desborde_Cabecera` agregado como valor especial (no sentinel): no se
    normaliza, requiere `cEtiquetacliente` para contexto completo.
  - Nota NK90 agregada bajo la tabla explicando el LENGTH > 10.

## Preguntas abiertas nuevas

- **P-16 (ABIERTA):** `Desborde_Cabecera` en `sp_rpt_llamadas_abandonadas`:
  ¿se excluye, se cuenta como abandono o se trata como categoría propia?
- **P-17 (ABIERTA):** `Desborde_Cabecera` en `sp_rpt_menu_redirigidos`:
  ¿se incluye o se filtra?
- **P-18 (ABIERTA):** ¿Cuándo se espera que NK90 complete la migración a IPVR?
  La normalización `LENGTH > 10` tendrá fecha de revisión post-migración.

## Análisis del script de producción "Análisis LLamadas Menu" (2026-05-02)

El equipo compartió el script SQL real que generó los datasets Q01-Q03 2025.
Hallazgos críticos que corrigen y completan la documentación:

### Bugs en el script (NO reproducir en SPs de producción)

| Variable | Valor en script | Correcto | Consecuencia |
|---|---|---|---|
| `@ONacional02` | `1902001` (7 dígitos) | `19020001` | DID 19020001 NUNCA incluido en WHERE |
| `@OPuebla` | `19020084` | `19020084` | Correcto |
| `@ONacionalA` | `19028031` | `19028031` | Correcto |

**Impacto directo:** El dataset Q01-Q03 compartido por el equipo **solo contiene
nacional_A** (DID 19028031). `nacional_B` (DID 19020001) fue excluido por el
bug `@ONacional02 = 1902001`. Las filas de nacional_B en BR-MENU-002 son datos
de un query diferente y están marcadas como UNCERTAIN.

### Lógica del script (base para documentación)

**Sentinel VACIO:** La lógica de mapeo del script:
```sql
WHEN cMenu = ''    THEN 'VACIO'   -- vacío literal
WHEN cMenu IS NULL THEN 'VACIO'   -- NULL
```
Confirma: `VACIO` es GENERADO por el análisis/ETL, no almacenado por el IVR.
Nuestro ETL usa `SIN_MENU` para la misma lógica → ver P-24.

**Normalización UPPER(TRIM):** `ELSE UPPER(TRIM(cMenu))` — todos los valores
de menú en el dataset histórico están en MAYÚSCULAS. `cliente_colgo` → `CLIENTE_COLGO`.

**Detección telefono_cMenu:**
```sql
WHEN cTelefono_Digitado = cMenu AND cTelefono_Origen = cMenu THEN 'telefono_cMenu'
```
Ambos campos deben ser iguales al cMenu. No solo uno.

**DIDs por segmento:**
- Puebla: `@OPuebla = 19020084`
- Nacional A: `@ONacionalA = 19028031`
- Nacional B: `@ONacionalB = 19020001` (DID correcto; `@ONacional02` es bug separado)

### Decisiones confirmadas / actualizadas

- **D-23 (NUEVO):** "Total Nacional" en SPs de reporte = `WHERE segmento IN
  ('nacional_A','nacional_B')`. Nunca filtrar solo por `= 'nacional_A'`.

- **D-24 (NUEVO — VACIO sentinel):** `VACIO` y `SIN_MENU` son equivalentes
  semánticos. El script de análisis histórico usa `VACIO`. El ETL actual usa
  `SIN_MENU`. El SP `sp_rpt_llamadas_abandonadas` maneja `IN ('SIN_MENU','VACIO')`.
  P-24 abierta para alinear naming definitivamente.

### Nuevas reglas de negocio documentadas

- **BR-ROUTING-003 (CONFIRMADA):** `Desborde_Promocional` = enrutamiento a
  cola promocional. Mismo patrón que `Desborde_Cabecera`. No es abandono.

- **BR-MENU-002 (ACTUALIZADA) — v1.2.0:** Tabla de volúmenes Q01-Q03 2025
  agregada. Catálogo ampliado con menús nuevos: `SaldoCabecera`, `Saldos1_Pagar`,
  `Saldos3_Otra`, `MASI_RepiteBoleta`, `NoTMX_SinOp`, `KIPSOLCOM`,
  `RES_FALLA_STOP`, `ANI`, `MenuSaldosCabecera`. Nota de evolución del catálogo
  por trimestre documentada.

- **BR-DATA-001 (NUEVA):** Anomalía `telefono_cMenu`. Dos formas:
  - Forma A: `Numero Telmex` — menú válido en Puebla (desde Q02). Almacenar tal cual.
  - Forma B: número de teléfono literal como cMenu (Nacional Q03). Detectado por
    `cTelefono_Digitado = cMenu AND cTelefono_Origen = cMenu`. `sp_rpt_cMENU_ERROR`
    captura via `REGEXP '^[0-9]+'`. Volumen: < 500 registros/trimestre.

### Decisiones resueltas por análisis de datos (P-16, P-17, P-19, P-20, P-21 cerradas)

Estas preguntas se resolvieron sin necesidad de confirmación del equipo:

- **D-16/P-16 CERRADA:** `Desborde_Cabecera` en `sp_rpt_llamadas_abandonadas`
  → **EXCLUIR**. Es una llamada enrutada, no abandonada.
- **D-17/P-17 CERRADA:** `Desborde_Cabecera` en `sp_rpt_menu_redirigidos`
  → **INCLUIR**. Es exactamente un evento de redirección.
- **D-19/P-19 CERRADA:** `Desborde_Promocional` en `sp_rpt_llamadas_abandonadas`
  → **EXCLUIR**. Misma lógica que P-16.
- **D-20/P-20 CERRADA:** `Desborde_Promocional` en `sp_rpt_menu_redirigidos`
  → **INCLUIR**. Misma lógica que P-17.
- **D-21/P-21 CERRADA:** Definición de llamada abandonada — incluye `cliente_colgo`
  y `SinOpcion_Cabecera` además de `SIN_MENU`/`VACIO`. El SP actual solo captura
  ~8-9%; con definición correcta sube a ~27-28%. Reescritura del SP requerida.

### Preguntas abiertas nuevas de esta sesión

- **P-22 (ABIERTA):** ¿Causa raíz de `CASO_ERROR_CEROS` en Puebla? ~20K-30K/mes
  en Q02-Q03. Posible error de configuración IVR donde `cDID_Centro_Transferencia`
  no se captura.
- **P-23 (ABIERTA):** VDN `2309004` y `230806646350495` con prefijo "2" vs "1"
  en versiones antiguas. ¿DIDs nuevos o error de captura?
- **P-24 (ABIERTA):** Alinear naming `VACIO` vs `SIN_MENU`. Compatibilidad
  histórica vs legibilidad del ETL.

### Archivos modificados

- discover/business-rules-ivr.md — **v1.3.0**: D-16..D-21 documentadas,
  VACIO corregido en tabla de catálogo, P-24 agregada, sección "Decisiones
  derivadas resueltas" nueva.
- discover/etl-job-flow-design.md — **v2.3.0**: D-23 documentada, VACIO
  sentinel corregido con nota de convención histórica y referencia a P-24.

## Cierre de preguntas y decisión D-24 VACIO (2026-05-02)

- **P-18 CERRADA:** No relevante — normalización `LENGTH > 10` cubre todos los
  casos sin depender del estado de migración NK90→IPVR.
- **P-22 CERRADA:** No relevante — `CASO_ERROR_CEROS` es un sentinel;
  el reporte muestra el dato sin filtrar ni inferir causa raíz.
- **P-23 CERRADA:** No relevante — VDNs con prefijo `2...` se almacenan y
  muestran como vienen; no requieren tratamiento especial.
- **D-24/P-24 CERRADA — VACIO:** Convención unificada definitiva para cMenu
  vacío/NULL → `'VACIO'`. Eliminación completa de `'SIN_MENU'` del ETL.
  Justificación: compatibilidad con el script de análisis histórico y con los
  datos reales Q01-Q03 en producción. El SP ya no necesita `IN ('SIN_MENU','VACIO')`.

### Archivos modificados

- discover/etl-job-flow-design.md — **v2.4.0:**
  - Sentinel `SIN_MENU` eliminado de la tabla. Solo `VACIO`.
  - CASE cMenu: `THEN 'SIN_MENU'` → `THEN 'VACIO'` en todos los bloques
    (flujo ASCII, código PREPARE/EXECUTE del SP completo).
  - `sp_rpt_llamadas_abandonadas`: condición actualizada a
    `IN ('VACIO','cliente_colgo','SinOpcion_Cabecera')` (D-21 + D-24).
  - `sp_rpt_menu_redirigidos`: `SIN_MENU` eliminado del IN list.
  - Comentario de columna `menu` actualizado.

- discover/business-rules-ivr.md — **v1.4.0:**
  - P-18, P-22, P-23, P-24 cerradas con resolución definitiva.
  - Tabla de preguntas abiertas reemplazada por tabla de decisiones cerradas.
  - Todas las referencias a `SIN_MENU` en textos y SQL actualizadas a `VACIO`.
  - BR-ROUTING-002/003: P-16/P-17/P-19/P-20 reemplazadas por D-16..D-20.
  - BR-MENU-003: SQL de abandono actualizado con definición D-21 + D-24.

## Status de promoción a CHANGELOG.md raíz
Pendiente — el WP está en Phase 1 DISCOVER.
