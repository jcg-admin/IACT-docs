```yml
created_at: 2026-05-02 09:45:00
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
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
  como categoría propia según criterio del equipo. **P-16: confirmar tratamiento.**
- `sp_rpt_menu_redirigidos` — Llamadas con `Desborde_Cabecera` SÍ fueron
  redirigidas, pero por etiqueta, no por opción de menú. Incluirlas puede
  distorsionar el reporte. **P-17: confirmar si se incluyen o filtran.**

---

## Resumen de impacto en tablas base

| BR | Campo raw afectado | Campo en base_ivr_detalle | Tratamiento |
|---|---|---|---|
| BR-CLIENT-001 | `cTelefono_Origen`, `cTelefono_Digitado` | `misma_linea`, `linea_diferente`, `no_digito_telefono` | SUM de comparaciones |
| BR-ROUTING-001 | `cDID_Centro_Transferencia` (NK90) | `centro_transferencia` | LEFT(..., LENGTH-10) cuando len > 10 |
| BR-MENU-001 | `cMenu`, `cOpcion`, `cDID_Centro_Transferencia` | `menu`, `opcion`, `centro_transferencia` | Grain natural del GROUP BY |
| BR-ROUTING-002 | `cMenu = 'Desborde_Cabecera'`, `cEtiquetacliente` | `menu = 'Desborde_Cabecera'` | Sin normalización; contexto requiere `cEtiquetacliente` |

---

## Preguntas abiertas derivadas de estas BRs

| # | Pregunta | Impacto |
|---|---|---|
| P-16 | `Desborde_Cabecera` en `sp_rpt_llamadas_abandonadas`: ¿se excluye, se cuenta como abandono o categoría propia? | Lógica del SP de reporte |
| P-17 | `Desborde_Cabecera` en `sp_rpt_menu_redirigidos`: ¿se incluye o se filtra? | Lógica del SP de reporte |
| P-18 | Post-migración IPVR: ¿cuándo se espera que NK90 deje de concatenar teléfono en `cDID_Centro_Transferencia`? | La normalización LENGTH > 10 tendrá fecha de caducidad |
