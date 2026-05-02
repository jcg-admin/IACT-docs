```yml
created_at: 2026-05-02 07:28:08
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Schema Real del IVR — Análisis desde scripts SQL de producción

> **HALLAZGO DISRUPTIVO:** El schema real del MySQL IVR es fundamentalmente diferente
> al schema pedagógico documentado en PARTE_0/PARTE_6. Ver sección 1.

## Fuentes (PROVEN)

Scripts SQL reales proporcionados por el equipo:
1. `Script_Transfer_Menu_Opcion.sql` — Análisis detallado de transfer, menu y opción
2. `Script_Clientes_Unicos_DID_Trimestre.sql` — Clientes únicos por DID y trimestre
3. `Script_Llamadas_Abandonadas.sql` — Análisis de llamadas abandonadas
4. `Script_Centros_Transferencia.sql` — Análisis de centros de transferencia
5. `Script_Centros_Dias_Habiles.sql` — Centros con análisis de días hábiles

---

## 1. Corrección crítica — schema pedagógico vs schema real

El análisis previo (`ivr-schema-analysis.md`) documentó un schema **PEDAGÓGICO** extraído
de PARTE_6 (material de enseñanza), no el schema de producción.

| Aspecto | Schema pedagógico (PARTE_6) | Schema REAL (scripts producción) |
|---|---|---|
| Nombre tabla | `ivr_calls` (fictional) | `tbl_historico_tN_YYYY` (real) |
| Particionamiento | Lógico: columnas `quarter`+`year` | **Físico: tablas separadas por trimestre** |
| Campo fecha | `call_date` | `dFecha` |
| Campo organización | `segment` ('OP', 'MG') | `cDID_800Transfer` (numérico: 19020084) |
| Campo estado llamada | `status` ('COMPLETED', 'ABANDONED') | **No existe campo status — abandono se infiere de `cMenu`** |
| Duración | `duration_seconds` | `hora_inicio` + `hora_fin` (calculado) |
| Sesión | `session_id` FK → `ivr_sessions` | No evidencia de tabla sessions |
| IVR navigation | No documentado | `cMenu` + `cOpcion` |
| Teléfonos | No documentado | `cTelefono_Origen` + `cTelefono_Digitado` |
| Centro de destino | No documentado | `cDID_Centro_Transferencia` (requiere normalización) |

---

## 2. Tablas reales del MySQL IVR (PROVEN)

### 2.1 Convención de nombres

```
tbl_historico_t{N}_{YYYY}

donde:
  N    = número de trimestre (1, 2, 3, 4)
  YYYY = año (2025, 2026, ...)
```

**Tablas confirmadas por scripts:**
- `tbl_historico_t1_2025` — Q1 2025 (2025-01-01 a 2025-03-31)
- `tbl_historico_t2_2025` — Q2 2025 (2025-04-01 a 2025-06-30)
- `tbl_historico_t3_2025` — Q3 2025 (2025-07-01 a 2025-09-30)

**Implicación para el ETL:** El ETL extrae de `tbl_historico_tN_YYYY` por trimestre, no de
una tabla única con `WHERE quarter = 'QN'`. El particionamiento es FÍSICO, no lógico.

### 2.2 Columnas confirmadas en tbl_historico_tN_YYYY

| Columna | Tipo | Descripción | Script fuente |
|---|---|---|---|
| `dFecha` | DATE | Fecha de la interacción IVR | Todos los scripts (WHERE dFecha >= ...) |
| `cDID_800Transfer` | BIGINT/VARCHAR | Número DID de entrada (800 number) | Todos — filtro principal |
| `cDID_Centro_Transferencia` | VARCHAR | Centro de transferencia destino (formato variable — requiere normalización) | Script 1, Script 4 |
| `cMenu` | VARCHAR | Menú IVR seleccionado/recorrido | Script 1, Script 3 |
| `cOpcion` | VARCHAR | Opción específica dentro del menú | Script 1 |
| `cTelefono_Origen` | VARCHAR | Número telefónico del llamante (CLI) | Script 1, Script 2 |
| `cTelefono_Digitado` | VARCHAR | Número telefónico digitado por el usuario en el IVR | Script 1 |

### 2.3 Columnas inferidas de la vista `llamadas_QN`

En el último script (Script 5) se referencia una vista/tabla derivada `llamadas_Q3` con columnas:

| Columna | Tipo inferido | Descripción |
|---|---|---|
| `id_CTransferencia` | VARCHAR | ID normalizado del centro de transferencia |
| `fecha` | DATE | Fecha (equivalente a `dFecha`) |
| `hora_inicio` | TIME | Hora de inicio de la llamada |
| `hora_fin` | TIME | Hora de fin de la llamada |
| `numero_entrada` | VARCHAR | Número de entrada (equivalente a `cTelefono_Origen` o `cDID_800Transfer`) |
| `menu` | VARCHAR | Menú (simplificado de `cMenu`) |
| `opcion` | VARCHAR | Opción (simplificada de `cOpcion`) |

**INFERRED:** `llamadas_Q3` es probablemente una VIEW o tabla agregada que normaliza
`tbl_historico_t3_2025`. Podría existir también `llamadas_Q1`, `llamadas_Q2`.

**Columnas completas de `llamadas_QN` — confirmadas por múltiples scripts:**

| Columna | Tipo inferido | Descripción | Script |
|---|---|---|---|
| `id_CTransferencia` | VARCHAR | ID normalizado del centro de transferencia (VDN) | Scripts 4,5,6 |
| `fecha` | DATE | Fecha de la llamada | Scripts 4,5 |
| `hora_inicio` | DATETIME/TIME | Hora de inicio de la llamada | Script 6 |
| `hora_fin` | DATETIME/TIME | Hora de fin de la llamada | Script 6 |
| `numero_entrada` / `numero_digitado` | VARCHAR | Número del llamante / digitado | Scripts 4,6 |
| `menu` | VARCHAR | Menú IVR (normalizado de `cMenu`) | Scripts 4,5,6 |
| `opcion` | VARCHAR | Opción dentro del menú (normalizado de `cOpcion`) | Scripts 4,5,6 |
| `id_8T` | VARCHAR | Zona geográfica — identificador de zona | Script 6 |
| `division` | VARCHAR | División organizacional | Script 6 |
| `area` | VARCHAR | Área organizacional | Script 6 |
| `nidMQ` | VARCHAR/INT | ID de integración con mensajería (¿WhatsApp/email?) | Script 6 |
| `etiquetas` | VARCHAR | Etiquetas/tags asociados a la llamada | Script 6 |

---

## 3. Valores de referencia — DIDs y organizaciones (PROVEN)

De los scripts, los DIDs de las organizaciones son:

| Variable | Valor | Organización |
|---|---|---|
| `@OPuebla` | `19020084` | Centro Puebla |
| `@ONacionalA` / `@ONacional` | `19028031` | Centro Nacional (línea A) |
| `@ONacionalB` | `19020001` | Centro Nacional (línea B) |

**Los "segmentos" en el sistema real son por DID de entrada (Puebla/Nacional),
no por 'OP'/'MG'/'FI'/'VT' como en el material pedagógico.**

---

---

## 3b. Lógica de "llamadas colgadas" vs "menú con número" (PROVEN)

Del script "Análisis colgadas" y "Análisis menu con numero":

**Llamadas colgadas/abandonadas** — identificadas cuando `cMenu` es:
```sql
cMenu IS NULL
OR TRIM(cMenu) = ''
OR cMenu IN ('', 'sin cMenu')
```

**Anomalías de menú** — cuando `cMenu` contiene un número de teléfono:
```sql
-- cMenu contiene número puro (probablemente error de sistema)
cMenu REGEXP '^[0-9]+$'
-- O cuando el menú es igual al teléfono digitado
cTelefono_Digitado = cMenu AND cTelefono_Origen = cMenu
```

Esto sugiere que cuando el IVR falla en registrar el menú navegado, guarda el número
de teléfono en el campo `cMenu`.

---

## 4. Lógica de "llamadas abandonadas" (PROVEN / INFERRED)

**Hallazgo crítico:** NO existe columna `status` = 'ABANDONED'. El abandono se infiere
del estado del menú IVR.

Del Script 3 (Llamadas Abandonadas), el campo clave es `cMenu`:

```sql
-- Categorización de cMenu en llamadas abandonadas:
CASE 
    WHEN TRIM(cMenu) IS NULL OR TRIM(cMenu) = '' THEN 'vacio'
    WHEN cMenu = 'sin cMenu' THEN 'vacio'
    ELSE UPPER(TRIM(cMenu))
END as menu_limpio
```

Una llamada "abandonada" se identifica por el valor de `cMenu` que indica que el cliente
colgó antes de completar el flujo IVR (valores como 'vacio', 'cliente_colgo', etc.).

**INFERRED:** El concepto de `status = 'ABANDONED'` del material pedagógico mapea en la
realidad a llamadas donde `cMenu` es vacío o tiene un valor de abandono específico.

---

## 5. Normalización de cDID_Centro_Transferencia (PROVEN)

Este campo requiere lógica de limpieza compleja (Script 1 y Script 4):

```sql
CASE
    WHEN TRIM(cDID_Centro_Transferencia) IS NULL OR TRIM(cDID_Centro_Transferencia) = '' 
        THEN 'CASO_NULL'
    WHEN cDID_Centro_Transferencia = 'cliente_colgo' 
        THEN 'CLIENTE_COLGO'
    WHEN cDID_Centro_Transferencia REGEXP '^0+$' 
        THEN 'CASO_ERROR_CEROS'
    WHEN cDID_Centro_Transferencia REGEXP '^[^0-9]' 
        THEN 'ERROR_CARACTER_INICIAL'
    WHEN LENGTH(cDID_Centro_Transferencia) <= 10 
        THEN cDID_Centro_Transferencia
    WHEN LENGTH(cDID_Centro_Transferencia) > 10 
        THEN LEFT(cDID_Centro_Transferencia, LENGTH(cDID_Centro_Transferencia) - 10)
    ELSE 'FORMATO_ESPECIAL'
END AS centro_transferencia
```

**Implicación para ETL:** El ETL debe aplicar esta lógica de normalización en la fase
Transform antes de cargar en `analytics_calls`.

El valor `'cliente_colgo'` en `cDID_Centro_Transferencia` confirma que es otro
indicador de llamada terminada por el cliente (abandono).

---

## 6. Funciones de negocio en BD (PROVEN)

El Script 5 referencia funciones definidas en la base de datos:

| Función | Parámetros | Descripción |
|---|---|---|
| `fn_es_dia_habil(fecha)` | DATE | Retorna BOOLEAN — ¿es día hábil? |
| `fn_agregar_dias_habiles(fecha, n)` | DATE, INT | Agrega N días hábiles a una fecha |
| `fn_contar_dias_habiles(fecha_ini, fecha_fin)` | DATE, DATE | Cuenta días hábiles entre dos fechas |

**Implicación:** La BD IVR tiene lógica de negocio embebida en funciones MySQL. El ETL
debe considerar si necesita replicar esta lógica en Analytics o puede consumirla directamente.

---

## 7. Lógica de segmentación temporal (PROVEN)

Del Script 2, los rangos por trimestre para 2025:

| Trimestre | Inicio | Fin |
|---|---|---|
| Q1_25 | 2025-01-01 | 2025-03-31 |
| Q2_25 | 2025-04-01 | 2025-06-30 |
| Q3_25 | 2025-07-01 | 2025-09-30 |

**Nombres de trimestre en sistema:** `'Q01_25'`, `'Q02_25'`, `'Q03_25'`
(formato: `Q{NN}_{YY}` — dos dígitos para el número y dos para el año)

**Implicación para DataAvailability:** El campo `period_value` en el modelo DataAvailability
debe usar el formato `'Q01_25'` (no `'Q3-2024'` como se asumió en el análisis pedagógico).

---

## 8. Clasificación de centros y SLA (PROVEN)

Del Script 5, la lógica de clasificación de centros:

```sql
-- Clasificación por patrón de uso del centro
CASE 
    WHEN llamadas_dias_habiles / total >= 0.8 THEN 'CENTRO_EMPRESARIAL'
    WHEN llamadas_fines_semana / total >= 0.4 THEN 'CENTRO_MIXTO'
    ELSE 'CENTRO_PERSONAL'
END as patron_uso_centro

-- Clasificación por volumen y actividad
CASE 
    WHEN COUNT(*) >= 20 AND dias_habiles_desde_hoy <= 1 THEN 'CENTRO_CRITICO_ACTIVO'
    WHEN COUNT(*) >= 20 AND dias_habiles_desde_hoy > 3 THEN 'CENTRO_ALTO_VOLUMEN_INACTIVO'
    WHEN COUNT(*) >= 10 THEN 'CENTRO_VOLUMEN_MEDIO'
    ELSE 'CENTRO_BAJO_VOLUMEN'
END as clasificacion_centro

-- Estados SLA
WHEN dias_habiles <= 0 THEN 'DENTRO_SLA_HOY'
WHEN dias_habiles <= 3 THEN 'DENTRO_SLA_3_DIAS'
WHEN dias_habiles <= 5 THEN 'FUERA_SLA_CRITICO'
ELSE 'FUERA_SLA_ESCALAMIENTO'
```

**Implicación para reportes:** Los reportes de IACT deben incluir estas métricas de SLA.
Esto sugiere que `analytics_calls` debe preservar información de centros de transferencia
y fechas para calcular días hábiles.

---

## 9. Métricas calculadas por el ETL (INFERRED)

A partir de los scripts, las métricas que el ETL debe calcular en la fase Transform:

| Métrica | Fórmula | Destino en Analytics |
|---|---|---|
| `clientes_unicos` | `COUNT(DISTINCT cTelefono_Origen)` por DID+trimestre | `analytics_calls` o tabla separada |
| `total_llamadas` | `COUNT(*)` por agrupación | `analytics_calls` |
| `porcentaje` | `COUNT(*) / total_trimestre * 100` | Calculado en reporting, no almacenado |
| `llamadas_dias_habiles` | `COUNT WHERE fn_es_dia_habil(dFecha)` | `analytics_calls` o flag |
| `duracion_promedio` | `AVG(hora_fin - hora_inicio) WHERE duración > 0` | `analytics_calls` |
| `misma_linea` | `COUNT WHERE cTelefono_Origen = cTelefono_Digitado` | Posible campo en Analytics |
| `linea_diferente` | `COUNT WHERE cTelefono_Origen != cTelefono_Digitado` | Posible campo en Analytics |

---

## 10. Gaps documentales derivados del schema real (INFERRED)

**Actualizando gaps G-01..G-06 de ivr-schema-analysis.md:**

| # | Gap original | Corrección / nuevo gap |
|---|---|---|
| G-01 | "Schema completo de `ivr_calls` no documentado" | **Corregir:** la tabla real es `tbl_historico_tN_YYYY`. Crear `source/databases/ivr-schema-real.rst` |
| G-02 | "`analytics_calls` no tiene schema documentado" | Sigue siendo válido — pendiente |
| G-03 | "`analytics_centers` no documentada" | Sigue siendo válido |
| G-04 | "Lógica PARCIAL/COMPLETO no especificada" | Sigue siendo válido |
| G-05 | "No hay BR para trimestre completo = todos los segmentos" | **Actualizar:** "trimestre completo = todos los DIDs activos para ese tN_YYYY" |
| G-06 | "Patrón extracción por quarter+year no en etl-pipeline.rst" | **Actualizar:** extracción es por `tbl_historico_tN_YYYY` (tabla separada) |
| **G-16** | Schema real diverge del schema pedagógico — docs en source/ usan nombres ficticios | **NUEVO — Alto** |
| **G-17** | `DataAvailability.period_value` formato incorrecto — debe ser `'Q01_25'` no `'Q3-2024'` | **NUEVO — Alto** |
| **G-18** | Funciones `fn_es_dia_habil`, `fn_agregar_dias_habiles`, `fn_contar_dias_habiles` no documentadas | **NUEVO — Medio** |
| **G-19** | Columnas IVR reales (`dFecha`, `cMenu`, `cOpcion`, `cTelefono_*`, `cDID_*`) no aparecen en ningún doc de source/ | **NUEVO — Alto** |
| **G-20** | La vista/tabla `llamadas_QN` no está documentada — posible capa intermedia del ETL | **NUEVO — Alto** |
| **G-21** | Lógica de normalización de `cDID_Centro_Transferencia` no documentada | **NUEVO — Medio** |
| **G-22** | Clasificaciones de centros (EMPRESARIAL/MIXTO/PERSONAL) y SLA no están en ningún UC | **NUEVO — Medio** |

---

## 11. Implicaciones para UC_PIP deepening

### UC_PIP_01 (Ver Estado Pipeline)
- El "estado" que muestra debe incluir qué tablas `tbl_historico_tN_YYYY` han sido procesadas
- Un ETLExecution corresponde a procesar una tabla completa, no un `WHERE quarter = 'QN'`

### UC_PIP_02 (Ver Errores ETL)
- Los errores pueden ser de la fase Extract (leer `tbl_historico_tN_YYYY`) o de Transform
  (normalizar `cDID_Centro_Transferencia`, calcular métricas)

### UC_PIP_03 (Consultar Disponibilidad de Datos)
- `DataAvailability.period_value` debe usar formato `'Q01_25'` (no `'Q3-2024'`)
- Un trimestre está COMPLETO cuando `tbl_historico_tN_YYYY` fue procesada exitosamente
  para todos los DIDs activos

### UC_PIP_04 (Solicitar Reintento)
- Un reintento implica re-procesar una `tbl_historico_tN_YYYY` completa
- La lógica de idempotencia debe considerar que la tabla origen puede haber sido actualizada

---

## 12. Tabla de mapping ETL — real a Analytics

El ETL mapea de la estructura real a la estructura Analytics:

| Campo IVR real | Columna Analytics (inferido) | Transformación |
|---|---|---|
| `tbl_historico_tN_YYYY` (tabla) | `analytics_calls.quarter` + `.year` | Inferido del nombre de tabla |
| `dFecha` | `analytics_calls.call_date` | Directo |
| `cDID_800Transfer` | `analytics_calls.center_id` (via `analytics_centers`) | Lookup/normalización |
| `cDID_Centro_Transferencia` (normalizado) | `analytics_calls.transfer_center_id` (?) | Lógica de limpieza |
| `cMenu` + `cOpcion` | `analytics_calls.metric_type` (?) | Clasificación IVR |
| `cTelefono_Origen` | `analytics_calls.caller_phone` (?) | Directo |
| Calculado (abandono por cMenu) | `analytics_calls.status` equivalente | Lógica derivada |
| `hora_fin - hora_inicio` | `analytics_calls.call_duration` | Cálculo |

**Nota:** Las columnas con `(?)` son inferidas — no confirmadas por documentación existente.

---

## Resumen ejecutivo

1. **El schema real del IVR usa tablas `tbl_historico_tN_YYYY`** (separadas por trimestre),
   no una tabla `ivr_calls` con columna `quarter`.

2. **El campo "abandono" se infiere de `cMenu`** (valor vacío o `'cliente_colgo'`),
   no de un campo `status`.

3. **La segmentación es por DID** (`cDID_800Transfer`: Puebla=19020084, Nacional=19028031/19020001),
   no por 'OP'/'MG' como en el material pedagógico.

4. **El ETL debe aplicar lógica de normalización compleja** sobre `cDID_Centro_Transferencia`
   antes de cargar en Analytics.

5. **Existen funciones de negocio embebidas** (`fn_es_dia_habil`, `fn_agregar_dias_habiles`)
   que el ETL o Analytics debe replicar/consumir.

6. **El formato de trimestre en el sistema es `'Q01_25'`** (Q + dos dígitos + año abreviado).

7. **La vista `llamadas_QN` tiene al menos 13 columnas** incluyendo `id_8T` (zona geográfica),
   `division`, `area`, `nidMQ` (mensajería), `etiquetas` — estructura mucho más rica que
   `tbl_historico_tN_YYYY`.

8. **Integración con mensajería** (`nidMQ`) sugiere que algunas llamadas IVR se complementan
   con WhatsApp u otro canal — campo relevante para el ETL y para reportes.
