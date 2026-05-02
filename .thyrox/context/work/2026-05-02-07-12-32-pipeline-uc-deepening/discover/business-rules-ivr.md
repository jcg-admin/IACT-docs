```yml
created_at: 2026-05-02 09:45:00
updated_at: 2026-05-02 10:30:00
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.1.0
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
— es un valor semánticamente válido y distinto de `SIN_MENU`. No se mapea a
ningún sentinel.

```sql
-- Desborde_Cabecera NO cae en estas reglas de normalización:
WHEN cMenu IS NULL         THEN 'SIN_MENU'    -- NULL
WHEN TRIM(cMenu) = ''      THEN 'SIN_MENU'    -- vacío
WHEN cMenu = 'sin cMenu'   THEN 'SIN_MENU'    -- string sin valor
-- 'Desborde_Cabecera' → pasa al ELSE → se almacena como 'Desborde_Cabecera'
ELSE cMenu
```

**Impacto en reportes:**
- `sp_rpt_llamadas_abandonadas` — `Desborde_Cabecera` no es un abandono; debe
  excluirse del conteo de abandonos junto con `SIN_MENU`/`VACIO`, o tratarse
  como categoría propia. **P-16: confirmar tratamiento.**
- `sp_rpt_menu_redirigidos` — Llamadas con `Desborde_Cabecera` SÍ fueron
  redirigidas, pero por etiqueta, no por opción de menú. **P-17: confirmar.**

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

**P-19:** ¿`Desborde_Promocional` se incluye o excluye en `sp_rpt_llamadas_abandonadas`?
**P-20:** ¿`Desborde_Promocional` entra en `sp_rpt_menu_redirigidos`?

---

## BR-MENU-002 — Catálogo real de valores cMenu por segmento

Datos observados desde datos reales compartidos por el equipo (período: Q3 2025).

### Nacional — 2,567,201 llamadas totales

| cMenu | Total | % | Clasificación |
|---|---|---|---|
| *(vacío)* | 238,049 | 9.3% | → `SIN_MENU` |
| `cliente_colgo` | 444,438 | 17.3% | Abandono — mayor grupo |
| `Desborde_Cabecera` | 336,919 | 13.1% | Enrutamiento por etiqueta (BR-ROUTING-002) |
| `NOTMX-SeguimientoInstalacion` | 264,883 | 10.3% | Menú de servicio |
| `RES_FALLA_STOP` | 214,894 | 8.4% | Menú de servicio |
| `RES-FallaInternet` | 162,925 | 6.3% | Menú de servicio |
| `RES-MADT-Detalle` | 132,330 | 5.2% | Menú de servicio |
| `RES-SaldooPagos` | 108,867 | 4.2% | Menú de servicio |
| `SinOpcion_Cabecera` | 97,513 | 3.8% | Sin opción en cabecera |
| `Desborde_Promocional` | 79,994 | 3.1% | Enrutamiento promocional (BR-ROUTING-003) |
| *(otros ~33 menús)* | ~525,389 | 20.5% | Menús de servicio específicos |

### Puebla — 132,473 llamadas totales

| cMenu | Total | % | Clasificación |
|---|---|---|---|
| `Numero Telmex` | 16,909 | 12.8% | Identificación por número |
| `cliente_colgo` | 12,075 | 9.1% | Abandono |
| `Desborde_Cabecera` | 11,682 | 8.8% | Enrutamiento por etiqueta |
| `RES-ContratacionInfinitum_2024` | 11,691 | 8.8% | Menú de servicio (versión 2024) |
| *(vacío)* | 11,592 | 8.8% | → `SIN_MENU` |
| `RES-Fallas_2024` | 10,115 | 7.6% | Menú de servicio (versión 2024) |
| `RES_FALLA_STOP` | 9,738 | 7.4% | Menú de servicio |
| `SinOpcion_Cabecera` | 9,346 | 7.1% | Sin opción en cabecera |
| `RES-SaldosPagos_2024` | 7,945 | 6.0% | Menú de servicio (versión 2024) |
| *(otros ~17 menús)* | ~43,380 | 32.7% | Menús de servicio específicos |

### Hallazgos del catálogo

**Los menús no son universales entre segmentos.** Nacional ~43 valores, Puebla ~25.
Solo ~15 son comunes. Los SPs de reporte filtran por `segmento` — comportamiento correcto.

**Puebla usa sufijo `_2024` en sus menús.** `RES-ContratacionInfinitum_2024`,
`RES-Fallas_2024`, `RES-SaldosPagos_2024`, `RES-SegInst_2024`. Nacional tiene
equivalentes sin sufijo. Los menús evolucionan: en 2025/2026 pueden aparecer
`_2025`. El diseño de `base_ivr_detalle` almacena el nombre literal — no requiere
cambios cuando aparecen nuevos nombres.

**`SinOpcion_Cabecera` no es un sentinel.** Es un estado válido del menú (cliente
llegó a la cabecera pero no presionó opción). Se almacena tal cual.

**`ANI` como valor de cMenu.** 2,887 Nacional, 2,181 Puebla. La llamada fue
identificada por ANI antes de navegar cualquier menú. Se almacena como `'ANI'`.

**Proporción Nacional:Puebla ≈ 19:1.** nacional_A + nacional_B dominan ~95%
del total consolidado. Los porcentajes de reportes globales reflejan Nacional.

---

## BR-MENU-003 — Definición de llamadas abandonadas

La definición de "abandono" es más amplia que `SIN_MENU`/`VACIO`. El SP actual
`sp_rpt_llamadas_abandonadas` usa solo esos dos valores, pero `cliente_colgo`
es el grupo más grande de Nacional (444K = 17.3% del total).

| cMenu | Volumen Nacional | Volumen Puebla | ¿Abandono? |
|---|---|---|---|
| *(vacío)* | 238,049 | 11,592 | Sí → `SIN_MENU` |
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

---

## Preguntas abiertas derivadas de estas BRs

| # | Pregunta | Impacto |
|---|---|---|
| P-16 | `Desborde_Cabecera` en `sp_rpt_llamadas_abandonadas`: ¿excluir, contar o categoría propia? | Lógica del SP |
| P-17 | `Desborde_Cabecera` en `sp_rpt_menu_redirigidos`: ¿incluir o filtrar? | Lógica del SP |
| P-18 | ¿Cuándo completa migración NK90 → IPVR? | Normalización LENGTH > 10 tendrá revisión post-migración |
| P-19 | `Desborde_Promocional` en `sp_rpt_llamadas_abandonadas`: ¿incluir o excluir? | Lógica del SP |
| P-20 | `Desborde_Promocional` en `sp_rpt_menu_redirigidos`: ¿incluir o filtrar? | Lógica del SP |
| P-21 | **¿Cuál es la definición oficial de "llamada abandonada"?** `cliente_colgo` (444K Nacional) no está en el SP actual. Diferencia entre definición mínima y amplia es ~18 puntos porcentuales. | Reescritura del SP si la definición es amplia |
