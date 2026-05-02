```yml
created_at: 2026-05-02 09:45:00
updated_at: 2026-05-02 15:00:00
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.4.0
```

# Reglas de Negocio — Sistema IVR IACT

Reglas confirmadas directamente por el equipo. Documentan comportamiento real
del IVR de producción. Estas BRs son insumo para el diseño de ETL SPs y
Reporting SPs.

---

## BR-CLIENT-001 — Identificación del cliente por teléfono

**Contexto:** Cada llamada registra hasta dos teléfonos:
- `cTelefono_Origen` — ANI (Automatic Number Identification): el número desde
  el que llama el cliente. Capturado automáticamente por la red telefónica.
- `cTelefono_Digitado` — número que el cliente ingresa manualmente en el menú
  IVR cuando el sistema lo solicita. Puede ser NULL (75.3% de los registros).

**Regla:**

| Condición | Clasificación | Campo en base_ivr_detalle |
|---|---|---|
| `cTelefono_Origen = cTelefono_Digitado` | Misma línea — el cliente llamó desde su número registrado y lo confirmó | `misma_linea` |
| `cTelefono_Origen != cTelefono_Digitado` | Línea diferente — el cliente llamó desde otro número | `linea_diferente` |
| `cTelefono_Digitado IS NULL` | No digitó teléfono — el cliente no ingresó número en el IVR | `no_digito_telefono` |

**Implementación SQL (inline en sp_etl_base_detalle):**

```sql
SUM(cTelefono_Origen = cTelefono_Digitado)   AS misma_linea,
SUM(cTelefono_Origen != cTelefono_Digitado)  AS linea_diferente,
SUM(cTelefono_Digitado IS NULL)              AS no_digito_telefono
```

**Nota de consistencia:** Las tres métricas son mutuamente excluyentes y su
suma es igual a `COUNT(*)`:
- Cuando `cTelefono_Digitado IS NULL`: `misma_linea` = 0, `linea_diferente` = 0,
  `no_digito_telefono` = 1.
- Cuando `cTelefono_Digitado IS NOT NULL`: exactamente uno de `misma_linea` o
  `linea_diferente` es 1, y `no_digito_telefono` = 0.

**Impacto en reportes:**
- `sp_rpt_centros_transferencia` — columnas `misma_linea`, `linea_diferente`,
  `no_digito_telefono` mapeadas directamente de `base_ivr_detalle`.
- `sp_rpt_clientes_unicos` — usa `COUNT(DISTINCT cTelefono_Digitado)` en
  `base_ivr_clientes`. Solo cuenta llamadas donde el cliente sí digitó.

---

## BR-ROUTING-001 — Enrutamiento NK90: concatenación de centro y teléfono

**Contexto:** La infraestructura de enrutamiento actual (**NK90**) está en proceso
de migración a **IPVR**. Durante esta convivencia, NK90 registra el campo
`cDID_Centro_Transferencia` concatenando el número de enrutamiento (VDN) con
el `cTelefono_Digitado` del cliente.

**Comportamiento:**

```
cDID_Centro_Transferencia = [numero_enrutamiento][cTelefono_Digitado]
```

**Ejemplo real:**

| Campo | Valor |
|---|---|
| `cTelefono_Origen` | `4433772577` |
| `cTelefono_Digitado` | `4433150875` |
| `cDID_Centro_Transferencia` | `13090044433150875` |

Descomposición: `1309004` (7 dígitos) + `4433150875` (10 dígitos) = `13090044433150875` (17 dígitos)

**Regla de normalización:**

Cuando `LENGTH(cDID_Centro_Transferencia) > 10`, los últimos 10 dígitos son el
`cTelefono_Digitado` concatenado por NK90. El identificador real del centro es
`LEFT(cDID_Centro_Transferencia, LENGTH(cDID_Centro_Transferencia) - 10)`.

```sql
WHEN LENGTH(cDID_Centro_Transferencia) > 10
    THEN LEFT(cDID_Centro_Transferencia,
         LENGTH(cDID_Centro_Transferencia) - 10)
```

**Identificadores de centro conocidos (post-normalización):**

```
'13090044433150875' → '1309004'   (NK90, 7 dígitos)
'3090049535342699'  → '309004'    (NK90, 6 dígitos)
'15070013'          → '15070013'  (8 dígitos, sin concatenación)
```

**Nota de migración:** Una vez completada la migración a IPVR, `cDID_Centro_Transferencia`
debería dejar de concatenar el teléfono. Esta BR y la normalización LENGTH > 10
deberán revisarse post-migración. Los registros de las tablas históricas
`tbl_historico_*` seguirán teniendo el valor NK90 concatenado — la normalización
es permanente para datos ya almacenados.

**Impacto en ETL:**
La regla ya está implementada inline en `sp_etl_base_detalle` como parte del
CASE de normalización de `cDID_Centro_Transferencia`. Es la 4ª condición
del CASE (antes del ELSE).

---

## BR-MENU-001 — Opciones de menú que redirigen a un centro

**Contexto:** Cada `cDID_Centro_Transferencia` (VDN) puede recibir llamadas
provenientes de múltiples combinaciones de `cMenu`+`cOpcion`. Para conocer
qué opciones de menú redirigen a un centro dado:

```sql
SELECT
    cDID_Centro_Transferencia,
    GROUP_CONCAT(
        DISTINCT CONCAT(cMenu, ':', cOpcion)
        SEPARATOR ', '
    ) AS menus_que_redirigen
FROM   tbl_historico_tN_YYYY
WHERE  cDID_Centro_Transferencia IS NOT NULL
GROUP BY cDID_Centro_Transferencia;
```

**Ejemplo — centro 15070013:**

```
RES-MADT-Detalle:DEFAULT
RES-FallaInternet:ADEUDO22222
RES-Aparatos:DEFAULT
RES-ContratacionInfinitum:DEFAULT
RES-ContratacionInfinitum_2024:DEFAULT
RES-StartGo:DEFAULT
```

**Interpretación:** Un mismo centro puede ser destino de múltiples flujos de
navegación IVR. Esto explica por qué en `base_ivr_detalle` un
`centro_transferencia` puede aparecer con múltiples combinaciones de
`menu`+`opcion` — es el comportamiento esperado, no una anomalía.

**Relevancia para reportes:**
- `sp_rpt_menu_centro` — la columna `pct_dentro_centro` calcula el porcentaje
  de cada menu+opcion dentro del total de llamadas que llegaron a ese centro.
- `sp_rpt_menu_redirigidos` — lista los menús que redirigieron, con su centro destino.

---

## BR-ROUTING-002 — Desborde_Cabecera: enrutamiento por etiqueta de cliente

**Contexto:** Cuando `cMenu = 'Desborde_Cabecera'`, la llamada NO fue enrutada
por la navegación normal del menú IVR. Fue enrutada por la etiqueta de cliente
almacenada en `cEtiquetacliente`.

**Comportamiento:**

```
cMenu = 'Desborde_Cabecera'
    → el enrutamiento fue dirigido por cEtiquetacliente
    → el cliente tiene una etiqueta activa que determina su destino
```

**Relación con cEtiquetacliente:**
El campo `cEtiquetacliente` es un CSV de hasta 6 posiciones con las etiquetas
asignadas al cliente (ej: `'ADEUDO22222,,,,,'`). La función `fn_extraer_etiqueta`
lo parsea por posición. Cuando hay `Desborde_Cabecera`, la etiqueta activa
en la posición correspondiente es la que determinó el destino.

**Tratamiento en base_ivr_detalle:**
`Desborde_Cabecera` se almacena como valor de `menu` sin normalización adicional
— es un valor semánticamente válido y distinto de `VACIO`. No se mapea a
ningún sentinel.

```sql
-- Desborde_Cabecera NO cae en estas reglas de normalización:
WHEN cMenu IS NULL         THEN 'VACIO'    -- NULL
WHEN TRIM(cMenu) = ''      THEN 'VACIO'    -- vacío
WHEN cMenu = 'sin cMenu'   THEN 'VACIO'    -- string sin valor
-- 'Desborde_Cabecera' → pasa al ELSE → se almacena como 'Desborde_Cabecera'
ELSE cMenu
```

**Impacto en reportes (D-16, D-17 resueltas):**
- `sp_rpt_llamadas_abandonadas` — **EXCLUIR** `Desborde_Cabecera`. Es una llamada
  enrutada, no abandonada.
- `sp_rpt_menu_redirigidos` — **INCLUIR** `Desborde_Cabecera`. Es exactamente
  un evento de redirección.

---

## BR-ROUTING-003 — Desborde_Promocional: enrutamiento por evento promocional

**Confirmado desde datos reales:** Aparece en ambos segmentos.

| Segmento | Volumen | % del total |
|---|---|---|
| Nacional | 79,994 | 3.1% |
| Puebla | 3,519 | 2.7% |

**Comportamiento:** Similar a `Desborde_Cabecera` pero disparado por un evento
promocional activo, no por `cEtiquetacliente`. La llamada fue enrutada
automáticamente sin navegar el menú estándar.

**Tratamiento en base_ivr_detalle:** Almacenado como `'Desborde_Promocional'` en
`menu` sin normalización (pasa al ELSE del CASE — correcto).

**D-19 (resuelta):** `Desborde_Promocional` → **EXCLUIR** de `sp_rpt_llamadas_abandonadas`.
**D-20 (resuelta):** `Desborde_Promocional` → **INCLUIR** en `sp_rpt_menu_redirigidos`.

---

## BR-MENU-002 — Catálogo real de valores cMenu por segmento

Datos confirmados desde dataset granular Q1-Q3 2025 compartido por el equipo.

### Volúmenes totales por trimestre y segmento — Q1-Q3 2025 (PROVEN)

> Fuente: datos de producción compartidos directamente por el equipo.
> nacional_A = DID 19028031 · nacional_B = DID 19020001 · Puebla = DID 19020084

| Trimestre | Segmento | Total llamadas (aprox) | CLIENTE_COLGO (top abandono) |
|---|---|---|---|
| Q01_25 | Nacional (A+B combinado) | ~11,640,000 | 2,507,905 (21.6%) |
| Q01_25 | Puebla | ~525,000 | 117,215 (22.3%) |
| Q02_25 | Nacional A | ~13,600,000 | 1,867,260 (13.7%) |
| Q02_25 | Nacional B | ~4,700,000 | 885,171 (18.8%) |
| Q02_25 | Puebla | ~734,000 | ~123,000 (16.8%) |
| Q03_25 | Nacional A | ~8,800,000 | 1,478,963 (16.8%) |
| Q03_25 | Nacional B | ~95,000 | 30,201 (31.8%) |
| Q03_25 | Puebla | ~409,000 | ~52,000 (12.7%) |

> **Nota Q01_25 Nacional:** El dataset de Q01 no separa nacional_A de nacional_B —
> aparecen combinados con `800_transfer = 'Nacional'`. Solo Q02 y Q03 muestran la
> separación. Ver D-23 para consolidación en reportes.

> **Nota Q03_25 Nacional B:** Volumen dramáticamente reducido vs Q02 (~95K en Sep vs
> ~4.7M en Q02). Probable evento operativo o migración de tráfico. Pendiente confirmar.

### Nacional — Top cMenu (combinado nacional_A + B, Q3 2025 referencia)

| cMenu | Total Q3 (aprox) | Clasificación |
|---|---|---|
| `cliente_colgo` | ~1,509,164 (combina A+B) | Abandono — mayor grupo |
| `Desborde_Cabecera` | ~variable por mes | Enrutamiento por etiqueta (BR-ROUTING-002) |
| `NOTMX-SeguimientoInstalacion` | segundo en volumen | Menú de servicio |
| `RES_FALLA_STOP` | alto volumen (Q02 onward) | Menú de servicio |
| `VACIO` | ~800K-900K / trimestre | Generado por ETL desde cMenu vacío/NULL (~9%) — convención unificada (D-24) |
| `SinOpcion_Cabecera` | ~3-4% | Estado válido — sin opción en cabecera |
| `Desborde_Promocional` | ~1-3% | Enrutamiento promocional (BR-ROUTING-003) |
| `Marque3` | ~1% | Menú de tecla 3 |
| `NoTMX_SinOp` | desde Q02 | Sin opción en flujo NOTMX |
| `MASI_RepiteBoleta` | desde Q02 | Reimpresión de boleta |

### Puebla — Top cMenu (Q3 2025 referencia)

| cMenu | Aprox | Clasificación |
|---|---|---|
| `cliente_colgo` | ~52K (Q03) | Abandono |
| `RES-ContratacionInfinitum_2024` | alto | Menú de servicio (versión 2024) |
| `VACIO` | ~8.8% | Generado por ETL desde vacío/NULL (D-24) |
| `Numero Telmex` | persistente desde Q02 | Menú de identificación por número (BR-DATA-001) |
| `RES-Fallas_2024` | variable | Menú de servicio (versión 2024) |
| `SinOpcion_Cabecera` | ~7% | Estado válido |
| `ANI` | desde Q02 | Identificación por ANI antes del menú |
| `SaldoCabecera` | nuevo en Q03 | Balance en cabecera |
| *(CASO_ERROR_CEROS)* | ~20K-30K/mes en Q02-Q03 | Sentinel de error DID ceros (ver etl-job-flow-design.md) |

### Hallazgos del catálogo

**Los menús no son universales entre segmentos.** Nacional ~50+ valores distintos,
Puebla ~30. Solo ~15 son comunes. Los SPs de reporte filtran por `segmento`.

**Puebla usa sufijo `_2024` en sus menús.** `RES-ContratacionInfinitum_2024`,
`RES-Fallas_2024`, `RES-SaldosPagos_2024`, `RES-SegInst_2024`. Nacional tiene
equivalentes sin sufijo. Los menús evolucionan trimestralmente. El diseño de
`base_ivr_detalle` almacena el nombre literal — no requiere cambios cuando
aparecen nuevos nombres.

**El catálogo IVR cambia entre trimestres.** Q02 introdujo `RES_FALLA_STOP`,
`MASI_RepiteBoleta`, `NoTMX_SinOp`, renombres de IDs `QJA_DAT_ROJA`,
`QJA_VSI_ROJA` (antes `QJA_AB_DAT_1`, `QJA_AB_VSI_1`). Q03 introdujo
`SaldoCabecera`, `Saldos1_Pagar`, `Saldos3_Otra`, `MenuSaldosCabecera`,
`KIPSOLCOM`. El ETL absorbe cambios automáticamente (ELSE cMenu).

**`SinOpcion_Cabecera` no es un sentinel.** Es un estado válido del menú.

**`ANI` como valor de cMenu.** La llamada fue identificada por ANI antes de
navegar cualquier menú. `misma_linea = total_llamadas` en estos registros
(confirma que ANI = el número que llama es el mismo reconocido). Se almacena `'ANI'`.

**Proporción Nacional:Puebla ≈ 22:1 en Q03** (8.9M Nacional vs ~409K Puebla).
Los porcentajes de reportes globales reflejan Nacional de forma dominante.

**`CASO_ERROR_CEROS` en Puebla Q02-Q03.** ~20K-30K registros/mes en Puebla donde
`cDID_Centro_Transferencia` es todo ceros. Sentinel ya documentado en etl-job-flow-design.md.
Impacto: representa ~3-4% del total Puebla. Necesita investigación de causa raíz (P-22).

**Variantes de VDN en Q02-Q03.** Aparecen `2309004`, `230806646350495` como
centro_transferencia — son variantes de `1309004`/`130806646350495` con prefijo
diferente. Volumen pequeño. Confirmar si son DIDs nuevos o errores de datos (P-23).

---

## BR-MENU-003 — Definición de llamadas abandonadas

La definición de "abandono" es más amplia que solo `VACIO`. El SP actual
`sp_rpt_llamadas_abandonadas` usa solo ese valor, pero `cliente_colgo`
es el grupo más grande de Nacional (444K = 17.3% del total).

| cMenu | Volumen Nacional | Volumen Puebla | ¿Abandono? |
|---|---|---|---|
| *(vacío)* | 238,049 | 11,592 | Sí → `VACIO` |
| `cliente_colgo` | 444,438 | 12,075 | **Sí — mayor grupo, NO está en SP actual** |
| `SinOpcion_Cabecera` | 97,513 | 9,346 | Parcial — sin opción pero llegó al menú |
| `ANI` | 2,887 | 2,181 | Pendiente definición |
| `Opción Invalida` | 77 | 185 | Parcial |
| `Desborde_Cabecera` | 336,919 | 11,682 | No — fue enrutado (P-16) |
| `Desborde_Promocional` | 79,994 | 3,519 | No — fue enrutado (P-19) |

**P-21 (ABIERTA — URGENTE):** ¿Cuál es la definición oficial de "llamada abandonada"?
El SP actual captura ~8-9% del total. Con `cliente_colgo` incluido, captaría ~26-27%.
La diferencia es significativa para las métricas del negocio.

---

## BR-DATA-001 — Anomalía telefono_cMenu: números de teléfono en campo cMenu

**Descripción:** En producción aparecen números de teléfono en el campo `cMenu` de
`tbl_historico_*`. Esto no es comportamiento esperado del IVR. Se identifican dos
formas distintas:

### Forma A — "Numero Telmex" (Puebla, desde Q02_25)

El IVR registra `cMenu = 'Numero Telmex'` cuando el cliente ingresa su número Telmex
como método de identificación. **NO es una anomalía de datos** — es un menú IVR
válido específico de Puebla. El nombre del menú es literalmente "Numero Telmex".

| Trimestre | Segmento | Volumen | Nota |
|---|---|---|---|
| Q02_25 | Puebla | ~26K-43K/mes | Nuevo desde Q02; opcion = `SIN_OPCION` |
| Q03_25 | Puebla | ~13K-17K/mes | Continúa |
| Q03_25 | Nacional | ~18K/mes Sep | Aparece en Nacional desde Q03 (Sep 2025) |

**Tratamiento en ETL:** Se almacena como `'Numero Telmex'` en `menu` (ELSE del CASE
— correcto). **No requiere normalización especial.**

**Distinción importante:** `misma_linea + linea_diferente` suma al total (no todos
son `no_digito_telefono`), lo que confirma que los clientes sí tienen `cTelefono_Digitado`
al usar este menú.

### Forma B — Número de teléfono literal como cMenu (Nacional, Q03_25)

El IVR almacena directamente el número de teléfono en `cMenu`. Esto SÍ es una
anomalía — el número del cliente aparece donde debería estar el nombre del menú.

**Ejemplos confirmados (Q03_25 Nacional 202509):**

| cMenu (valor raw) | Total | Nota |
|---|---|---|
| `25519465555` | < 500 | Teléfono literal en cMenu |
| `25511027599` | < 500 | Teléfono literal en cMenu |
| `28183512172` | < 500 | Teléfono literal en cMenu |
| `MENU_10_NUMEROS` | ~130 | Nombre de menú para entrada de 10 dígitos |
| `MENU_11_NUMEROS` | ~20 | Nombre de menú para entrada de 11 dígitos |

**Volumen total:** < 500 registros por trimestre. **Impacto mínimo en métricas.**

**Tratamiento en ETL:** `sp_rpt_cMENU_ERROR` ya captura estos casos via
`WHERE menu REGEXP '^[0-9]+'`. Los valores `MENU_10_NUMEROS` y `MENU_11_NUMEROS`
(con prefijo alfabético) no caen en este filtro — se almacenan como menús válidos.

**Tratamiento en base_ivr_detalle:** Los números literales pasan al ELSE del CASE
de normalización → se almacenan tal cual en `menu`. `sp_rpt_cMENU_ERROR` los
identifica y reporta como anomalía de calidad.

---

## Resumen de impacto en tablas base

| BR | Campo raw afectado | Campo en base_ivr_detalle | Tratamiento |
|---|---|---|---|
| BR-CLIENT-001 | `cTelefono_Origen`, `cTelefono_Digitado` | `misma_linea`, `linea_diferente`, `no_digito_telefono` | SUM de comparaciones |
| BR-ROUTING-001 | `cDID_Centro_Transferencia` (NK90) | `centro_transferencia` | LEFT(..., LENGTH-10) cuando len > 10 |
| BR-MENU-001 | `cMenu`, `cOpcion`, `cDID_Centro_Transferencia` | `menu`, `opcion`, `centro_transferencia` | Grain natural del GROUP BY |
| BR-ROUTING-002 | `cMenu = 'Desborde_Cabecera'` | `menu = 'Desborde_Cabecera'` | Sin normalización |
| BR-ROUTING-003 | `cMenu = 'Desborde_Promocional'` | `menu = 'Desborde_Promocional'` | Sin normalización |
| BR-MENU-002 | `cMenu` (catálogo completo) | `menu` (nombre literal) | Almacenamiento directo; menús evolucionan |
| BR-MENU-003 | `cMenu` (tipos de abandono) | `menu` | Impacta lógica de `sp_rpt_llamadas_abandonadas` |
| BR-DATA-001 | `cMenu` con valor numérico o 'Numero Telmex' | `menu` | Forma A: menú válido; Forma B: `sp_rpt_cMENU_ERROR` |

---

## Decisiones derivadas (resueltas por análisis de datos)

### D-16 / D-17 — `Desborde_Cabecera` en SPs de reporte

**`Desborde_Cabecera` = llamada enrutada a cola de desborde (overflow).** El IVR transfirió
la llamada a un agente alternativo cuando la cola principal estaba saturada. La llamada SÍ
fue atendida por el sistema — no es un abandono.

| SP | Decisión | Justificación |
|---|---|---|
| `sp_rpt_llamadas_abandonadas` | **EXCLUIR** | La llamada fue enrutada, no abandonada |
| `sp_rpt_menu_redirigidos` | **INCLUIR** | Es exactamente un evento de redirección |

```sql
-- sp_rpt_llamadas_abandonadas: Desborde_Cabecera NO entra
WHERE menu IN ('VACIO','cliente_colgo','SinOpcion_Cabecera')
  AND menu NOT IN ('Desborde_Cabecera','Desborde_Promocional')

-- sp_rpt_menu_redirigidos: Desborde_Cabecera SÍ entra
WHERE menu IN ('Desborde_Cabecera','Desborde_Promocional', ...)
```

### D-19 / D-20 — `Desborde_Promocional` en SPs de reporte

Misma lógica que D-16/D-17. `Desborde_Promocional` = desborde hacia cola promocional.
La llamada fue enrutada, no abandonada.

| SP | Decisión |
|---|---|
| `sp_rpt_llamadas_abandonadas` | **EXCLUIR** |
| `sp_rpt_menu_redirigidos` | **INCLUIR** |

### D-21 — Definición de "llamada abandonada"

**`cliente_colgo` ES una llamada abandonada.** "cliente_colgo" = el cliente colgó mientras
estaba en el menú IVR sin completar la transacción ni llegar a un agente. Semánticamente:
el cliente inició la llamada, navegó el IVR, y abandonó antes de resolver su necesidad.

**El SP `sp_rpt_llamadas_abandonadas` está incompleto.** Solo captura `VACIO`
(nunca llegó a un menú). Con `cliente_colgo` incluido, la cobertura sube de ~8-9% a ~26-27%.

**Definición correcta para el SP:**

```sql
WHERE menu IN (
    'VACIO',             -- nunca llegó a menú (NULL/vacío/sin cMenu)
    'cliente_colgo',     -- llegó al menú y colgó → abandono explícito
    'SinOpcion_Cabecera' -- llegó al menú pero no eligió opción → abandono implícito
)
```

`SinOpcion_Cabecera` (~97K Nacional / 9K Puebla) es abandono implícito: el cliente llegó
a la cabecera pero no pulsó ninguna tecla. Incluirlo es consistente con la definición amplia.

**Volúmenes bajo definición correcta (Q3 2025 Nacional A ~8.8M):**

| cMenu | Volumen aprox | Tipo abandono |
|---|---|---|
| `VACIO` | ~792K-900K | Nunca llegó al menú |
| `cliente_colgo` | ~1,479K | Llegó y colgó |
| `SinOpcion_Cabecera` | ~97K | Llegó pero no eligió |
| **Total abandonos** | **~2,370K-2,480K** | **~27-28% del total** |

---

## Decisiones y preguntas cerradas

| # | Resolución |
|---|---|
| P-16 / D-16 | `Desborde_Cabecera` → **EXCLUIR** de abandonadas, **INCLUIR** en redirigidos |
| P-17 / D-17 | Ídem P-16 |
| P-18 | No relevante para el reporte — la normalización `LENGTH > 10` cubre todos los casos independientemente de la migración |
| P-19 / D-19 | `Desborde_Promocional` → **EXCLUIR** de abandonadas |
| P-20 / D-20 | `Desborde_Promocional` → **INCLUIR** en redirigidos |
| P-21 / D-21 | Definición correcta de abandono: `VACIO` + `cliente_colgo` + `SinOpcion_Cabecera` |
| P-22 | No relevante — `CASO_ERROR_CEROS` es un sentinel; el reporte lo muestra tal cual sin filtrar |
| P-23 | No relevante — VDNs con prefijo `2...` se almacenan y muestran como vienen; sin filtro adicional |
| P-24 / D-24 | **Convención unificada: `VACIO`** — igual al script de análisis histórico. `SIN_MENU` eliminado del ETL. |
