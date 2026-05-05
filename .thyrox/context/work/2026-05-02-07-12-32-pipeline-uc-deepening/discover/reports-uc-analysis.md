```yml
created_at: 2026-05-02 08:02:28
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Análisis de UCs de Reportes — Referencia vs Realidad

> **HALLAZGO CRÍTICO:** Los 14 UCs de reportes en la referencia (`UC_RPT_01..14`)
> están basados en una arquitectura genérica de call center con BD Analytics
> (PostgreSQL). Los reportes reales de IACT son análisis específicos de IVR
> que no tienen nada que ver con "agentes", "colas" ni "campañas".

---

## 1. Inventario de UCs de reportes en la referencia (PROVEN)

Fuente: `temp-holding/GENERACION_DOCUMENTACION/TMP_COMPLETO_IACT_2026-01-13_2/`

| UC ID (referencia) | Nombre | Actor | Función RBAC |
|---|---|---|---|
| UC_RPT_01 | Ver Dashboard | AGR-001 agr_operador_basico | RPT-001: ve_reportes |
| UC_RPT_02 | Ver Métricas Tiempo Real | AGR-001 | RPT-002 |
| UC_RPT_03 | Ver Reportes Históricos | AGR-002 agr_operador_reportes | RPT-003: ve_historicos |
| UC_RPT_04 | Exportar CSV | AGR-002 | RPT-004 |
| UC_RPT_05 | Exportar Excel | AGR-002 | RPT-005 |
| UC_RPT_06 | Exportar PDF | AGR-002 | RPT-006 |
| UC_RPT_07 | Programar Reporte | AGR-002 | RPT-007 |
| UC_RPT_08 | Ver Reportes Programados | AGR-002 | RPT-008 |
| UC_RPT_09 | Configurar Filtros | AGR-002 | RPT-009 |
| UC_RPT_10 | Guardar Vista | AGR-002 | RPT-010 |
| UC_RPT_11 | Compartir Reporte | AGR-003 agr_supervisor | RPT-011 |
| UC_RPT_12 | Ver Reporte Agentes | AGR-003 agr_supervisor | RPT-012: ve_agentes |
| UC_RPT_13 | Ver Reporte Colas | AGR-003 agr_supervisor | RPT-013: ve_colas |
| UC_RPT_14 | Ver Reporte Campañas | AGR-003 agr_supervisor | RPT-014: ve_campanas |

---

## 2. Arquitectura de datos en los UCs de referencia (PROVEN — incorrecta)

### 2.1 Qué asumen los UCs de referencia

Todos los 14 UCs referencian:

```
BD Analytics (PostgreSQL)
├── metricas_diarias           -- tabla principal para históricos
│     columns: segmento_id, fecha, llamadas, tmo, ...
├── vista_agentes              -- vista para UC_RPT_12
│     columns: agente, metricas, segmento_id
├── vista_colas                -- vista para UC_RPT_13
│     columns: cola, metricas, segmento_id
└── vista_campanas             -- vista para UC_RPT_14
      columns: campana, metricas, segmento_id
```

**Queries que aparecen en los diagramas de secuencia:**
```sql
-- UC_RPT_01 Dashboard
SELECT COUNT(*) as total_llamadas,
       SUM(CASE WHEN atendida THEN 1 END) as atendidas,
       AVG(duracion) as tmo
FROM llamadas
WHERE segmento_id = ?
AND fecha = CURRENT_DATE

-- UC_RPT_03 Históricos
SELECT DATE_TRUNC(agregacion, fecha) as periodo,
       SUM(llamadas) as total,
       AVG(tmo) as tmo_prom
FROM metricas_diarias
WHERE segmento_id = ?
AND fecha BETWEEN ? AND ?
GROUP BY periodo ORDER BY periodo

-- UC_RPT_12 Agentes
SELECT agente, metricas FROM vista_agentes WHERE segmento_id = ?

-- UC_RPT_13 Colas
SELECT cola, metricas FROM vista_colas WHERE segmento_id = ?

-- UC_RPT_14 Campañas
SELECT campana, metricas FROM vista_campanas WHERE segmento_id = ?
```

### 2.2 KPIs que muestran los UCs de referencia

**Dashboard (UC_RPT_01):**
- Total llamadas recibidas
- Llamadas atendidas / abandonadas
- TMO (Tiempo Medio de Operación)
- Nivel de Servicio (%)
- Tiempo promedio de espera

**Agentes (UC_RPT_12):**
- Llamadas atendidas, TMO, tiempo en pausa, disponibilidad, tasa resolución

**Colas (UC_RPT_13):**
- Llamadas recibidas/atendidas/abandonadas, tiempo espera, nivel servicio (SLA)

**Campañas (UC_RPT_14):**
- Intentos, contactos, exitosos, tasa conversión, duración

---

## 3. Reportes reales de IACT (PROVEN — de scripts SQL de producción)

Fuente: scripts SQL compartidos por el equipo (sesión anterior).

### 3.1 Análisis Transfer/Menu/Opción
**Origen del script:** "Análisis detallado de Transfer, Menu y Opcion, SEPT/2025"

Columnas resultantes de la vista `llamadas_QN`:
```
fecha, hora_inicio, hora_fin, id_CTransferencia, id_8T,
menu, opcion, division, area, nidMQ, etiquetas,
numero_digitado, cDID_800Transfer
```

Filtros DID aplicados:
- `@OPuebla = 19020084`
- `@ONacionalA = 19028031`
- `@ONacionalB = 19020001`

Tipo de análisis: conteo y % por combinación `(menu, opcion, id_CTransferencia)`

### 3.2 Clientes Únicos por DID y Trimestre
**Origen del script:** "Clientes Únicos por DID y Trimestre, AGOSTO/2025"

Columnas clave:
```
quarter_name ('Q01_25', 'Q02_25', 'Q03_25'),
cDID_800Transfer,
COUNT(DISTINCT cTelefono_Digitado) AS clientes_unicos
```

Rangos de fechas por trimestre (reales de producción):
- Q1 2025: 2025-01-01 a 2025-03-31
- Q2 2025: 2025-04-01 a 2025-06-30
- Q3 2025: 2025-07-01 a 2025-09-30

### 3.3 Llamadas Abandonadas por Menú
**Origen del script:** "Análisis Llamadas Abandonadas, AGOSTO/2025"

Criterio de abandono: `cMenu IS NULL OR TRIM(cMenu) = '' OR cMenu IN ('', 'sin cMenu')`
— NO existe campo `status` en las tablas reales.

Columnas resultantes:
```
cMenu, quarter_name, total_llamadas, llamadas_abandono, pct_abandono
```

### 3.4 Centros de Transferencia con Días Hábiles
**Origen del script:** "Centros de transferencia ID + días hábiles"

Usa funciones MySQL:
- `fn_es_dia_habil(fecha)` → BOOLEAN
- `fn_agregar_dias_habiles(fecha, n)` → DATE
- `fn_contar_dias_habiles(fecha_ini, fecha_fin)` → INT

Columnas de la vista `llamadas_QN` usadas:
```
id_CTransferencia, hora_inicio, hora_fin,
division, area, nidMQ, etiquetas
```

### 3.5 Análisis de Colgadas
**Origen del script:** "Análisis colgadas, AGOSTO/2025"

CTE `todos_los_menu` → análisis de llamadas que completaron el menú
pero la llamada fue colgada sin transferir.

### 3.6 Análisis cMENU_ERROR (Menús con número de teléfono)
**Origen del script:** "Análisis Menu con numero"

Detección: `cMenu REGEXP '^[0-9]+'` — registros donde `cMenu` contiene
un número de teléfono en lugar de un nombre de menú (anomalía de datos).

Naming del script de producción: `q_cMENU_ERROR.sql`

### 3.7 Menús que Redirigen por Centro de Transferencia
**Origen del script:** "Análisis de Menús que Redirigen por Centro de Transferencia"

Usa columnas adicionales de la vista:
```
etiquetas, nidMQ, id_CTransferencia
```

Naming del script de producción: `q_menu_centro_transferecia_010925.sql`

---

## 4. Divergencia crítica: referencia vs realidad (PROVEN)

| Dimensión | Referencia (temp-holding) | Realidad (scripts SQL) |
|---|---|---|
| **Base de datos** | PostgreSQL "BD Analytics" | MySQL — tablas limpias |
| **Concepto de reporte** | Agentes, Colas, Campañas (call center genérico) | IVR: Transfer/Menu/Opción, DID, Centros |
| **Filtro de datos** | `segmento_id` (OP/FI/VT/SP) | `cDID_800Transfer` (19020084, 19028031, 19020001) |
| **Abandono** | Campo `status = 'ABANDONED'` | `cMenu IS NULL OR TRIM(cMenu) = ''` |
| **Períodos** | Fechas arbitrarias + `DATE_TRUNC` | `quarter_name` = 'Q01_25', 'Q02_25', 'Q03_25' |
| **Vistas/tablas** | `vista_agentes`, `vista_colas`, `vista_campanas` | Tablas limpias por reporte (a definir) |
| **TMO / métricas** | `AVG(duracion)` directo | No existe campo `duracion` — se calcula de `hora_inicio`/`hora_fin` |

**GAP G-23 (NUEVO):** Los 14 UCs de MOD_Reports de la referencia están
completamente desalineados con los reportes reales de IACT. Los conceptos
"Agentes", "Colas" y "Campañas" no existen en el IVR real.

---

## 5. Catálogo de reportes reales — estado y naming (INFERRED + PROVEN parcial)

Basado en scripts SQL de producción y confirmación del equipo:

Catálogo de tablas limpias (PROVEN — confirmado por el equipo, 2026-05-02):

| Reporte | Naming script producción | Tabla limpia | SP ETL (INFERRED) |
|---|---|---|---|
| Transfer/Menú/Opción | `q_menu_centro_transferecia_010925.sql` | `rpt_menu_centro` | `sp_etl_menu_centro` |
| Clientes únicos por DID | — | `rpt_clientes_unicos` | `sp_etl_clientes_unicos` |
| Llamadas abandonadas | — | `rpt_llamadas_abandonadas` | `sp_etl_llamadas_abandonadas` |
| Centros transferencia + días hábiles | — | `rpt_centros_transferencia` | `sp_etl_centros_transferencia` |
| Análisis colgadas | — | `rpt_colgadas` | `sp_etl_colgadas` |
| Menús con número (error) | `q_cMENU_ERROR.sql` | `rpt_cMENU_ERROR` | `sp_etl_cMENU_ERROR` |
| Menús redirigidos | — | `rpt_menu_redirigidos` | `sp_etl_menu_redirigidos` |

**Notas confirmadas:**
- Prefijo `rpt_` confirmado para todas las tablas limpias
- `rpt_menu_redirigidos` es tabla **separada** de `rpt_menu_centro`
- Scope 1 = 7 reportes. Reportes futuros en open clause (fuera de Scope 1)
- Naming de tablas confirmado por el equipo (P-02, P-09, P-10, P-11: cerradas)

---

## 6. Columnas conocidas por reporte (PROVEN de scripts SQL)

### Reporte 1: Transfer/Menu/Opción

Columnas que vendrán de la vista `llamadas_QN`:
```
fecha          DATE
hora_inicio    TIME
hora_fin       TIME
id_CTransferencia  VARCHAR  -- normalización de cDID_Centro_Transferencia
id_8T          VARCHAR  -- zona geográfica
menu           VARCHAR  -- cMenu normalizado
opcion         VARCHAR  -- cOpcion
division       VARCHAR
area           VARCHAR
nidMQ          VARCHAR
etiquetas      VARCHAR
cDID_800Transfer  VARCHAR  -- DID de entrada
quarter_name   VARCHAR(10)  -- 'Q01_25', 'Q02_25', 'Q03_25'
```

### Reporte 2: Clientes Únicos

Columnas de la tabla limpia:
```
quarter_name   VARCHAR(10)
cDID_800Transfer  VARCHAR
clientes_unicos  INT  -- COUNT(DISTINCT cTelefono_Digitado)
```

### Reporte 3: Llamadas Abandonadas

Columnas de la tabla limpia:
```
quarter_name    VARCHAR(10)
cMenu           VARCHAR
total_llamadas  INT
abandono        INT
pct_abandono    DECIMAL(5,2)
```

### Reporte 6: cMENU_ERROR

Columnas de la tabla limpia:
```
quarter_name    VARCHAR(10)
cMenu           VARCHAR  -- el valor numérico/telefónico en cMenu
tipo_error      ENUM('numero_telefono', 'numerico', 'otro')
total           INT
```

---

## 7. UCs de Pipeline en la referencia (PROVEN)

Fuente: `temp-holding/GENERACION_DOCUMENTACION/TMP_COMPLETO_IACT_2026-01-13_2/UC_PIP_*.rst`

| UC | Nombre | FRs en referencia |
|---|---|---|
| UC_PIP_01 (UC_050) | Supervisar ETL | FR-050.01: estado actual, FR-050.02: métricas ejecución, FR-050.03: auto-actualizar |
| UC_PIP_02 (UC_051) | Consultar Errores ETL | FR-051.01: listar errores, FR-051.02: detalle error, FR-051.03: exportar log |
| UC_PIP_03 (UC_052) | Consultar Disponibilidad | FR-052.01: fecha último dato, FR-052.02: completitud de datos |
| UC_PIP_04 (UC_053) | Solicitar Reintento (Reiniciar ETL) | FR-053.01: verificar ETL no activo, FR-053.02: iniciar ETL manual, FR-053.03: registrar ejecución manual |

**Nota:** Estos 4 UCs siguen siendo válidos en CONCEPTO aunque deben ser
reescritos para la arquitectura MySQL-internal. Ver `etl-architecture-correction.md`.

---

## 8. Gaps adicionales identificados en esta revisión

| Gap | Descripción | Impacto |
|---|---|---|
| G-23 | Los 14 UC_RPT de la referencia usan conceptos genéricos (Agentes/Colas/Campañas) incompatibles con IACT real | Reescritura completa de MOD_Reports UC |
| G-24 | ~~Las tablas limpias no tienen naming definitivo~~ | **CERRADO** — naming confirmado 2026-05-02 (ver sección 5) |
| G-25 | ~~El número total de reportes reales no está confirmado~~ | **CERRADO** — 7 reportes Scope 1 confirmados 2026-05-02 |
| G-26 | No existe documentación de cómo se calculan `hora_inicio`/`hora_fin` en la vista `llamadas_QN` | Impacta el cálculo de duración de llamadas en reportes |
| G-27 | Los UCs de referencia usan `segmento_id` como filtro principal; el real usa `cDID_800Transfer` — conceptos distintos | Impacta todo el modelo de RBAC de reportes |

---

## 9. Conclusión: lo que existe vs lo que se necesita

### Lo que existe en la referencia (temp-holding)

- 14 UCs de MOD_Reports basados en arquitectura Python/PostgreSQL genérica
- 4 UCs de MOD_Pipeline basados en la misma arquitectura incorrecta
- FRs numerados (FR-050..053 para pipeline, FR-017..030 para reports)
- Conceptos completamente desalineados con el IVR real

### Lo que se necesita crear desde cero

1. **Catálogo de tablas limpias** — nombre, schema, SP que las genera (P-02, P-09..P-11)
2. **UCs de MOD_Reports reales** — basados en los 7+ reportes IVR identificados
3. **ETL tracking table** — para el módulo de monitoreo (P-01)
4. **UCs de MOD_Pipeline corregidos** — con arquitectura MySQL-internal

### Lo que se puede reutilizar de la referencia

- **Estructura de UCs** (14 secciones, formato RST) — el template es válido
- **FRs de exportación** (CSV, Excel, PDF) — los UC_RPT_04..06 son reutilizables
- **FRs de programación de reportes** — UC_RPT_07..08 son reutilizables
- **RBAC básico** (RPT-001..014 como funciones) — las funciones existen, solo cambia el contenido
- **Reglas de negocio de rango temporal** (máx 2 años, CNST-006) — siguen vigentes

---

## 10. Orden de acciones recomendado

Antes de escribir cualquier UC real de MOD_Reports, confirmar con el equipo:

1. **P-09:** ¿El reporte de menús redirigidos es tabla separada o parte del Transfer/Menu/Opción?
2. **P-10:** ¿Hay más reportes planificados? Lista completa.
3. **P-11:** ¿Naming final de tablas limpias?
4. **P-02:** ¿Prefijo `rpt_` o sin prefijo?

Una vez confirmados → crear `source/databases/mysql-clean-tables.rst` con el
catálogo completo, luego reescribir los UCs de MOD_Reports.

---

## 11. Schemas confirmados desde datos reales (PROVEN — 2026-05-02)

Fuente: reportes en formato Excel/tabular compartidos por el equipo el 2026-05-02.
Los schemas de secciones 6 son INFERRED de scripts SQL. Esta sección los corrige
y amplía con columnas observadas en los datos reales.

### 11.1 rpt_centros_transferencia (PROVEN)

Fuente: `DID_Centro_Transferencia_280825.xlsx`

```
trimestre             VARCHAR(10)   -- 'Q01_25', 'Q02_25', 'Q03_25'
fecha                 INT o VARCHAR -- YYYYMM: 202501, 202502, ..., 202509
                                    -- NO es tipo DATE (ver D-15)
800_transfer          VARCHAR       -- 'Nacional', 'Puebla'
centro_transferencia  VARCHAR       -- DID destino, o sentinel:
                                    --   'CLIENTE_COLGO'
                                    --   'CASO_ERROR_CEROS'  (ver 11.5)
                                    --   'CASO_NULL'
menu                  VARCHAR       -- e.g. 'RES-FallaInternet', 'cliente_colgo',
                                    --   'SIN_MENU', 'CASO_NULL', 'VACIO'
opcion                VARCHAR       -- e.g. 'DEFAULT', 'SIN_OPCION', 'TELVICOBRA',
                                    --   'CASO_NULL', 'VACIO'
total_llamadas        INT
porcentaje            DECIMAL(15,7)
misma_linea           INT
linea_diferente       INT
no_digito_telefono    INT
```

Corrección al schema INFERRED de sección 6: la tabla real tiene 11 columnas, NO 3.
La sección 6 (Reporte 4/centros) no existía con schema completo — este es el primero.

### 11.2 rpt_clientes_unicos (PROVEN)

Fuente: reporte `clientes_unicos` compartido por el equipo.

```
trimestre         VARCHAR(10)  -- 'Q01_25', 'Q02_25', 'Q03_25'
cDID_800Transfer  VARCHAR      -- 'nacional_A', 'nacional_B', 'puebla'
                               -- NOTA: Nacional aparece como DOS filas separadas
                               -- (ver D-17: nacional_A y nacional_B son DIDs distintos)
clientes_unicos   INT          -- COUNT(DISTINCT cTelefono_Digitado)
```

**Volumen de la tabla:** 8 filas para Q01+Q02+Q03 2025 (tabla muy pequeña).
Suma de `clientes_unicos` para todos los trimestres: **9,617,998** clientes únicos.

Corrección al schema INFERRED de sección 6 (Reporte 2): el campo `quarter_name` se
llamaba así en el script SQL, pero en la tabla limpia real la columna es `trimestre`.
Pendiente confirmar naming definitivo de esta columna con el equipo.

### 11.3 Reporte llamadas_cmenu (PROVEN — tabla destino pendiente de mapeo)

Fuente: reporte `llamadas_cmenu` compartido por el equipo.

```
cDID_800Transfer  VARCHAR    -- 'Nacional', 'Puebla'
                             -- Nacional aparece DOS veces (nacional_A + nacional_B
                             -- están sumados o son filas separadas — confirmar)
trimestre         VARCHAR    -- 'Q01_25', 'Q02_25', 'Q03_25'
cMenu             VARCHAR    -- nombre del menú (mayúsculas en este reporte):
                             -- 'CLIENTE_COLGO', 'RES-FALLAINTERNET',
                             -- 'DESBORDE_CABECERA', 'VACIO', 'SIN_OPCION',
                             -- 'RES-MADT-DETALLE', 'RES-SALDOOPAGOS',
                             -- 'SINOPCION_CABECERA', 'DESBORDE_PROMOCIONAL',
                             -- 'RES-FALLASLINEA', 'MARQUE3', 'RES_FALLA_STOP',
                             -- 'MASI_REPITEBOLETA', 'NOTMX_SINOP',
                             -- 'NUMERO TELMEX', 'ANI', 'KIPSOLCOM',
                             -- 'TMX_SOMO', 'SALDOCABECERA', 'SALDOS3_OTRA',
                             -- 'SALDOS1_PAGAR', 'MENUSALDOSCABECERA',
                             -- 'telefono_cMenu', 'NOTMX-SEGUIMIENTOINSTALACION'
total_llamadas    INT
```

**Volumen total:** suma `total_llamadas` = **34,101,981** llamadas en Q01+Q02+Q03 2025.

**G-28 (NUEVO):** La tabla destino para este reporte en el catálogo D-02 no está clara.
`rpt_cMENU_ERROR` es específicamente para menus con número de teléfono como anomalía
(script `q_cMENU_ERROR.sql`). Este reporte muestra TODOS los menús incluyendo menús
normales como `CLIENTE_COLGO`. Puede ser:
- Una vista/aggregación de `rpt_menu_centro`
- O un reporte distinto fuera del catálogo D-02 actual
- O el reportee que da origen a `rpt_menu_centro` en su forma simplificada

**Pendiente confirmar con el equipo:** ¿A qué tabla `rpt_*` del catálogo D-02 mapea
el reporte `llamadas_cmenu`? ¿Es el origen de `rpt_menu_centro` o una tabla nueva?

### 11.4 Menús observados en datos reales — catálogo (PROVEN)

De los datos de `llamadas_cmenu`, menús reales identificados en producción Q01-Q03 2025:

| cMenu (mayúsculas en reporte) | Tipo |
|---|---|
| `CLIENTE_COLGO` | Llamada colgada por cliente antes de menú |
| `RES-FALLAINTERNET` / `RES-FallaInternet` | Menú de falla de internet |
| `DESBORDE_CABECERA` | Desborde de cabecera |
| `NOTMX-SEGUIMIENTOINSTALACION` | Seguimiento de instalación (NTX) |
| `VACIO` | Valor vacío (sentinel) |
| `SIN_MENU` | Sin menú seleccionado |
| `RES-MADT-DETALLE` | Menú MADT detalle |
| `RES-SALDOOPAGOS` | Saldos y pagos |
| `SINOPCION_CABECERA` | Sin opción en cabecera |
| `DESBORDE_PROMOCIONAL` | Desborde de promocional |
| `RES-FALLASLINEA` | Fallas de línea |
| `MARQUE3` | Marque 3 |
| `RES_FALLA_STOP` | Falla stop |
| `MASI_REPITEBOLETA` | MASI repite boleta |
| `NOTMX_SINOP` | NTX sin opción |
| `NUMERO TELMEX` | Número Telmex |
| `ANI` | ANI (Automatic Number Identification) |
| `KIPSOLCOM` | Kipsolcom |
| `TMX_SOMO` | TMX SOMO |
| `SALDOCABECERA` | Saldo cabecera |
| `SALDOS3_OTRA` | Saldos S3 otro |
| `SALDOS1_PAGAR` | Saldos S1 a pagar |
| `MENUSALDOSCABECERA` | Menú saldos cabecera |
| `telefono_cMenu` | Sentinel: número de teléfono como cMenu (anomalía — ver `rpt_cMENU_ERROR`) |

**Nota sobre casing:** el mismo menú puede aparecer con casing diferente en reportes
distintos (e.g. `RES-FallaInternet` vs `RES-FALLAINTERNET`). Los SPs de ETL deben
normalizar el casing o el análisis debe ser case-insensitive.

### 11.5 Sentinels de calidad de datos (PROVEN)

En los datos reales de producción existen valores sentinel que representan condiciones
de error o datos faltantes en dimensiones de las tablas limpias:

| Sentinel | Aparece en | Significado |
|---|---|---|
| `CASO_ERROR_CEROS` | `centro_transferencia`, `menu`, `opcion` | El campo raw (`cDID_Centro_Transferencia`) era 0 o inválido |
| `CASO_NULL` | `centro_transferencia`, `menu`, `opcion` | El campo raw era NULL |
| `VACIO` | `menu`, `opcion`, `cMenu` | El campo raw era cadena vacía |
| `CLIENTE_COLGO` | `centro_transferencia` | El cliente colgó antes de que se completara la transferencia |
| `SIN_MENU` | `menu` | No hubo selección de menú (cliente no interactuó) |
| `SIN_OPCION` | `opcion` | No hubo selección de opción |

**Distribución de `CASO_ERROR_CEROS`:** Aparece en datos de Q02_25 y Q03_25,
NO en Q01_25. Esto es consistente con el problema conocido en `dFecha` para
`tbl_historico_t3_2025` (mencionado por el equipo). La degradación de datos
comenzó en Q2 2025, no desde el inicio.

**G-29 (NUEVO):** La causa exacta del problema `dFecha` en `tbl_historico_t3_2025`
(y posiblemente `t2_2025`) no está documentada formalmente. El equipo mencionó
"un problema en el campo de fecha que estaba mal". Evidencia indirecta:
`CASO_ERROR_CEROS` surge en Q02/Q03 pero no en Q01. Pendiente documentación
formal del defecto en campo `dFecha`.

### 11.6 Volumen de datos — brutos vs agregados (PROVEN)

| Nivel | Tabla/Fuente | Filas estimadas Q01-Q03 2025 |
|---|---|---|
| Bruto | `tbl_historico_t1_2025` + `t2_2025` + `t3_2025` | **~34.1M** llamadas totales |
| Agregado | `rpt_clientes_unicos` | 8 filas (tabla mínima) |
| Agregado | `rpt_centros_transferencia` (Q03 Puebla) | ~cientos de filas por trimestre/segmento |
| Agregado | `rpt_llamadas_cmenu` (si separada) | ~20-30 filas por trimestre/segmento |

**Implicación para D-07 (PROVEN):** Las tablas limpias almacenan datos AGREGADOS,
no registros individuales de llamadas. TRUNCATE+INSERT sobre unas pocas centenas
de filas es trivialmente rápido. La preocupación de eficiencia no aplica a las
tablas limpias — aplica (si hubiera que hacerlo) solo sobre las tablas brutas,
que el ETL NO toca con TRUNCATE. D-07 queda CONFIRMADO como correcto y eficiente.

---

## 12. Gaps adicionales identificados (acumulado)

| Gap | Descripción | Estado |
|---|---|---|
| G-23 | 14 UC_RPT de referencia usan conceptos genéricos incompatibles con IACT real | Abierto |
| G-24 | ~~Naming de tablas limpias~~ | **CERRADO** — D-01/D-02 confirmados |
| G-25 | ~~Total de reportes reales~~ | **CERRADO** — 7 reportes Scope 1 confirmados |
| G-26 | Cómo se calculan `hora_inicio`/`hora_fin` en vista `llamadas_QN` | Abierto |
| G-27 | UCs usan `segmento_id`; real usa `cDID_800Transfer` — conceptos distintos | Abierto |
| G-28 | Mapeo del reporte `llamadas_cmenu` al catálogo rpt_* (¿rpt_menu_centro o nuevo?) | **Abierto — confirmar con equipo** |
| G-29 | Causa exacta del problema `dFecha` en `tbl_historico_t2/t3_2025` no documentada | **Abierto — confirmar con equipo** |
