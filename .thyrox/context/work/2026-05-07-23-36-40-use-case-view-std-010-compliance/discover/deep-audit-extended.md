```yml
created_at: 2026-05-07 23:50:00
project: IACT-docs
work_package: 2026-05-07-23-36-40-use-case-view-std-010-compliance
phase: Phase 1 — DISCOVER (extended)
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Deep Audit (Extended)
```

# Audit profundo extendido — use-case-view

> Análisis exhaustivo de `source/arquitectura-tecnica/use-case-view/`
> en multiples dimensiones: STD-010, STD-011, alineación con
> casos-uso, integridad de cross-refs, completitud de metadata.

## 1. Universo

- **85 archivos UC** (`uc-*.rst`)
- **14 archivos index** (cluster index + global indices)
- **Total: 99 archivos `.rst`**
- 13 modulos: access, admin, alerts, audit, auth, caller,
  logs, operator, permissions, pipeline, reports,
  supervision, users.

## 2. STD-010 violaciones consolidadas

### 2.1 Tabla maestra de violaciones (32 ediciones identificadas)

| Cat | Subcat | Refs | Archivos |
|---|---|---|---|
| A.1 | PostgreSQL/Postgres FTS (BD) | 2 | 2 |
| A.2 | Redis (cache) | 0 | — |
| A.3 | Elasticsearch (search) | 1 | 1 |
| A.4 | Apache/mod_wsgi (web) | 0 | — |
| A.5 | **Django** (framework) | 2 | 2 |
| B.1 | Cron/APScheduler (async) | 11 | 6 |
| B.2 | Celery/RabbitMQ (queue) | 0 | — |
| C.1 | concepto rol/role | 10 | 7 |
| D.1 | actor "User" generico | 2 | 2 |
| **Total** | | **28** | **~18 unicos** |

### 2.2 Nuevas violaciones encontradas (no en audit inicial)

#### A.5: Django (framework) — 2 refs

**`admin/index.rst:229`:**

```
en v5.6.x** (TD-RBAC-03). Solo via Django RunPython data
```

**Cambio propuesto:**

```
en v5.6.x** (TD-RBAC-03). Solo via migraciones de datos
del Servicio de Aplicacion (segun TD-RBAC-03).
```

**`admin/uc-adm-02-gestionar-catalogo-de-funciones.rst:21`:**

```
74+ funciones actuales se administran via migraciones Django; este UC
```

**Cambio propuesto:**

```
74+ funciones actuales se administran via migraciones de datos
del Servicio de Aplicacion; este UC
```

### 2.3 Casos limite — debate normativo

#### FTS / FTS bounded — vocabulario de dominio?

`FTS` aparece 8+ veces como nombre de **funcionalidad del UC**
(no como tecnologia). Ejemplos:

- `usecase "UC_LOG_03\nBuscar Logs (FTS)" as UC_LOG_03`
- `usecase "Ejecutar bounded FTS" as FTS_QUERY`

**Decision propuesta:** preservar como vocabulario de dominio
(FTS es un termino de capacidad funcional, no de tecnologia
concreta). Esta lectura aplica el mismo principio que JWT
(STD-010 §3.3 exempt como vocabulario de dominio).

Solo es violacion cuando se cita el **producto** ("Elasticsearch",
"Postgres FTS"). Eso ya esta en Cat-A.3.

#### HMAC — vocabulario de dominio?

`HMAC` aparece en uc-aud-04 (3 refs) como **algoritmo
estandarizado** de firma. STD-010 §3.3 lista PBKDF2 y argon2
como prohibidos pero usa "el algoritmo de derivacion de clave"
como canonico.

**Decision propuesta:** HMAC esta en gris. Por consistencia
con SHA-256 (que aparece en otros docs sin ser violacion),
preservar HMAC. PERO el caption "Firmar HMAC" se podria
suavizar a "Firmar con MAC seguro" o similar.

**Recomendacion:** dejar HMAC como esta. Es vocabulario
estandar de seguridad ampliamente entendido y compatible
con la regla "JWT como vocabulario de dominio".

#### `Sodrulerepo` (heredado del WP previo)

Detectado en WP `endpoint-sod-rules-rename` y ya fue corregido
para uc-acc-05. Verificar si quedan instancias en use-case-view:

(no detectadas en este audit — uc-acc-05 use-case-view no
referencia sod identifiers, solo el endpoint que ya esta
canonico).

## 3. Estados desalineados con casos-uso (NUEVO HALLAZGO CRITICO)

### 3.1 Resumen

**18 UCs en use-case-view tienen estado DIFERENTE al de casos-uso.**

| Cluster | UCs afectados | use-case-view | casos-uso |
|---|---|---|---|
| operator | 10 (uc-opr-01..10) | Reservado | Fuera del scope |
| caller | 5 (uc-cli-01..05) | Vigente | Fuera del scope |
| supervision | 3 (uc-sup-01..03) | Reservado | Fuera del scope |

### 3.2 Origen del problema

WP previo `2026-05-07-04-50-49-std-012-prefix-normalization`
reclasifico explicitamente OPR/SUP/CLI a `Fuera del scope`
en casos-uso (cambio mencionado en su changelog: "18 UCs
reclasificados de Vigente/Reservado a Fuera del scope").

**Pero el cambio NO se propago a use-case-view.** Los archivos
en use-case-view conservan estados antiguos (Vigente/Reservado).

Esto es deuda heredada del WP std-012 que NO fue detectada
durante el WP `uml-diagrams-deep-audit` (que se enfoco en
los 92 archivos recreados, no en los archivos hermanos en
use-case-view).

### 3.3 Impacto

**Severidad: alta.** El estado declarado en metadata es
contractual con el modelo del proyecto. Una vista (use-case-view)
contradice a otra (casos-uso) — el lector tiene 2 fuentes
de verdad inconsistentes.

### 3.4 Accion requerida

Sincronizar `:estado: Fuera del scope` (o el valor canonico
adoptado en STD-007 si existe) en los 18 archivos de
use-case-view.

**Caveat:** verificar tambien `:version:` — todos en use-case-view
estan en 1.0.0. Tras un cambio de estado, la version deberia
bumparse. Patron observado: el archivo permanece en version
del momento de creacion del cambio.

## 4. STD-011 (aliases auto-documentados) compliance

### 4.1 Patron observado

La gran mayoria de archivos en use-case-view siguen el patron:

```plantuml
actor "view_reports" as view_reports
actor "manage_alerts" as manage_alerts
```

(codename = alias, auto-documentado) — **OK**.

Excepciones legitimas:

```plantuml
actor "User\n<<authenticated>>" as AuthUser
actor "Caller\n<<external>>" as Caller
```

— estos son actores no-RBAC (genericos / externos) y el
alias mnemónico es adecuado.

### 4.2 Casos a revisar

`actor "Cron expiracion" as Cron_expiracion <<sistema_externo>>`
en multiples archivos (Cat-B). Tras el rename a "Planificador",
el alias debe mantener la auto-documentacion:

```plantuml
actor "Planificador expiracion" as Planificador_expiracion <<sistema>>
```

## 5. Cross-refs `:doc:` integridad

| Métrica | Valor |
|---|---|
| Total `:doc:` refs | 937 |
| Refs únicas | 194 |
| Refs rotas | **0** ✅ |

## 6. Metadata completitud

| Campo | Status |
|---|---|
| `:estado:` en todos los UCs | ✅ 85/85 |
| `:modulo:` en todos los UCs | ⚠ no verificado en este audit (script con bug) |
| `:version:` en todos los UCs | ✅ 85/85 (todas 1.0.0) |
| `:fecha_creacion:` | ✅ presente |
| `:autor:` | ✅ presente |

## 7. Distribución de estados (use-case-view)

| Estado | Cantidad | Cluster |
|---|---|---|
| Vigente | 72 | todos los Vigente reales |
| Reservado | 13 | operator (10) + supervision (3) |
| **Total** | **85** | |

Tras alinear con casos-uso (sección 3), la distribucion
seria:

| Estado | Cantidad |
|---|---|
| Vigente | 67 (= 72 - 5 caller) |
| Reservado | 0 (los 13 son re-categorizados) |
| Fuera del scope | 18 (10 operator + 5 caller + 3 supervision) |

Y agregando los 3 placeholders de uc-usr-05/06/07
(WP `users-alignment`):

| Estado | Cantidad |
|---|---|
| Vigente | 67 |
| Reservado | 3 (uc-usr-05/06/07) |
| Fuera del scope | 18 |
| **Total** | **88** (= casos-uso paridad) |

## 8. Decision points para Phase 5/8

Tras el audit profundo, el alcance del WP debe expandirse.

### Opcion A: Expandir WP std-010-compliance

Incluir en este WP:

- 28 ediciones de vocabulario (Cat-A/B/C/D)
- 18 alineaciones de estado (operator/caller/supervision)
- Total: ~46 ediciones en ~36 archivos

**Pro:** un solo WP cierra todo el debt de use-case-view
detectado en este audit.

**Con:** WP grande (estimado 3-5 horas).

### Opcion B: WP separado para state realignment

Crear `use-case-view-state-realignment`:

- 18 alineaciones de estado.

Mantener WP std-010-compliance solo para vocabulario:

- 28 ediciones.

**Pro:** WPs atomicos, scope claro.

**Con:** orquestacion de mas WPs en cola.

### Opcion C: Estado solo + dejar STD-010 ya analizado

Cerrar este WP std-010-compliance con audit completo
(sin EXECUTE), abrir WP nuevo solo de state alignment, y
diferir el remediation STD-010 hasta que el ejecutor lo
priorice.

**Pro:** state alignment es deuda heredada con prioridad,
STD-010 es mejora.

**Con:** retrasa la aplicacion de STD-010.

## 9. Recomendacion

**Opcion A (expandir WP).** Razones:

1. Ambas correcciones son sobre el mismo dominio
   (`use-case-view/`).
2. Hacer un solo build clean serial al cierre es mas
   eficiente que 2 separados (~20-30 min cada uno).
3. La revision por archivo en EXECUTE puede consolidarse
   (un mismo archivo puede tener vocabulario + estado, se
   corrige en un commit).

## 10. Próximo paso

Documentar este audit (este artefacto) + commit. Esperar
aprobacion del ejecutor sobre Opcion A/B/C antes de Phase
5 STRATEGY.

## Refs

- STD-010 v1.0.0
- STD-011 v1.0.0 (aliases auto-documentados)
- STD-007 (estados validos del proyecto)
- WP std-012-prefix-normalization (origen de la
  reclasificacion OPR/SUP/CLI a Fuera del scope)
- A-005 (eliminacion concepto role en backend)
- discover/std-010-audit.md (audit inicial v1.0.0)
