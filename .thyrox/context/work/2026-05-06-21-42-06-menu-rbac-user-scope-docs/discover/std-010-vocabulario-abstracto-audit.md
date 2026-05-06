```yml
created_at: 2026-05-06 23:50:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# STD-010 Vocabulario Abstracto — Auditoría de cumplimiento

## Trigger

Ejecutor planteó: *"sin embargo todo lo de tecnología
adicional se tiene prohibido mencionarlo como por ejemplo
celery, puedes analizar si existe alguna normativa sobre
eso"* + ejemplos del principio "máquina de gaseosa"
(React Form → Interfaz de Acceso, Celery → Procesador
Asíncrono, etc.).

## Sección 1 — Normativa identificada

**Existe normativa formal y vigente:**

`source/normativa/estandares/std-010-vocabulario-abstracto.rst`
(v1.0.0, 2026-05-04, status Aprobado).

### Regla central de STD-010

> *"Los documentos de requisitos describen LO QUE HACE el
> sistema, no CÓMO LO IMPLEMENTA. Los nombres de
> bibliotecas, frameworks, algoritmos concretos y
> excepciones de lenguaje pertenecen a
> ``implementacion-tecnica.rst`` y a
> ``source/arquitectura-tecnica/``."*

### Origen del principio

- **D-ETL-005** (WP `source-corrections-pipeline`):
  decisión original "soda machine rule".
- **D-KRUCHTEN-004** (WP `kruchten-view-diagram-types`):
  aplicación a participantes de diagramas Kruchten.
- STD-010 lo formaliza como estándar normativo
  (2026-05-04).

## Sección 2 — Ámbito de aplicación de STD-010

| Archivo / directorio | STD-010 aplica |
|---|---|
| `source/requisitos/casos-uso/**/flujo-principal.rst` | Sí |
| `source/requisitos/casos-uso/**/criterios-aceptacion.rst` | Sí |
| `source/requisitos/casos-uso/**/datos-involucrados.rst` | Sí |
| `source/requisitos/casos-uso/**/diagramas-uml.rst` (participantes) | Sí |
| `source/requisitos/casos-uso/**/requisitos-no-funcionales.rst` | Sí |
| `source/requisitos/casos-uso/**/excepciones.rst` | Sí |
| `source/requisitos/casos-uso/**/implementacion-tecnica.rst` | **NO** — libre |
| `source/arquitectura-tecnica/**` | **NO** — libre |
| `source/backend/**` | NO listado — libre por implicación |
| `.thyrox/context/work/**` (WP artifacts) | No listado — interno |

**Implicación:** los WP discovery artifacts no están bajo
STD-010, pero las decisiones que ahí se toman propagan al
Phase 7 DESIGN y eventualmente a `source/requisitos/`. Los
términos prohibidos deben **filtrarse** en la transición
WP → narrativa UC.

## Sección 3 — Tabla de mapeo aplicable a este WP

Vocabulario relevante para el diseño MenuItem extraído de
STD-010 §3:

| Tecnológico (PROHIBIDO en UC) | Canónico (CORRECTO) |
|---|---|
| `Redis` | el servicio de cache / la cache de sesiones |
| `MySQL` / `MariaDB` | el repositorio / Almacén de Datos |
| `Celery` | el Procesador Asíncrono |
| `RabbitMQ` | el Broker de Mensajes |
| `APScheduler` / `Cron` | el Planificador de Tareas |
| `bcrypt` | el algoritmo de hash seguro de contraseñas |
| `simplejwt` | el Servicio de Autenticación |
| `React` / `Frontend (React)` | la Interfaz de Usuario |
| `Redux Toolkit` | el Gestor de Estado |
| `Django API` (en participantes) | Servicio de Aplicación |
| `OperationalError` | error del repositorio |

### Regla para diagramas UML (STD-010 §4)

```
' CORRECTO en source/requisitos/
participant "Interfaz de Acceso" as Iface
participant "Servicio de Autenticacion" as Svc
database   "Almacen de Datos" as Store

' PROHIBIDO en source/requisitos/
participant "Frontend\n(React)" as F
participant "Django API" as API
database   "MariaDB" as DB
```

**Actores en diagramas UC** (excepción explícita): SÍ usan
el `codename` de la `Function` del catálogo RBAC
(D-DIAG-001), no nombres institucionales:

```
' CORRECTO
actor "view_reports"      as view_reports
actor "manage_menu_catalog" as manage_menu_catalog

' PROHIBIDO
actor "Administrador" as A
```

## Sección 4 — Auditoría de violaciones en este WP

Búsqueda en artefactos del WP de términos prohibidos:

```bash
grep -nE "Celery|Redis|bcrypt|mod_wsgi|MariaDB|simplejwt" \
  .thyrox/context/work/2026-05-06-21-42-06-menu-rbac-user-scope-docs/discover/*.md
```

### Hallazgos

| # | Archivo | Línea(s) | Término | Severidad |
|---|---|---|---|---|
| V-1 | `final-decisions-p1-p4-and-pending-items.md` | 21, 243, 247, 263, 266, 282, 305, 322, 346, 350 | `Redis` | Media (WP interno) |
| V-2 | `final-decisions-p1-p4-and-pending-items.md` | 417, 492 | `Celery beat` | **Alta** (propagable a UC) |
| V-3 | `menuitem-design-corrections-v2.md` | 162, 194, 195 | `Redis GET / SET` | Media (WP interno) |

### Análisis de severidad

**V-1 y V-3 (Redis en WP discovery):**
STD-010 no aplica directamente al directorio
`.thyrox/context/work/`, así que las menciones en
**razonamiento técnico interno del WP** son tolerables. La
decisión técnica concreta (Redis como motor de cache) vive
en `source/arquitectura-tecnica/` o
`implementacion-tecnica.rst` — ámbitos donde STD-010
permite el nombre tecnológico.

**V-2 (Celery beat job):** **Crítico.** La sección 4 de
``final-decisions-p1-p4-and-pending-items.md`` propone:

> *"Job de monitoreo (Celery beat)"* + código
> ``@celery_app.task`` para ``check_deprecated_menu_items``.

Si esto propaga a la narrativa UC en Phase 7 DESIGN
(probablemente como `UC_MEN_xx — Monitorear MenuItems
deprecados`), sería violación directa de STD-010 §3.5.

## Sección 5 — Reformulación canónica para Phase 7

### V-1 / V-3 (Redis)

En **WP discovery** (donde estamos): aceptable mantener
"Redis" como decisión de implementación documentada.

En **UC narrativa** (Phase 7, `source/requisitos/`):
reformular como:

| Antes (WP) | Después (UC) |
|---|---|
| "Cache lookup `caps:user:{id}` Redis call ≤ 2ms" | "Lookup en el servicio de cache ≤ 2ms" |
| "Si Redis falla durante invalidación..." | "Si el servicio de cache falla durante invalidación..." |
| "Redis es SPOF" | "el servicio de cache no debe ser punto único de falla del UC" |

La decisión "el servicio de cache es Redis" vive en
`source/arquitectura-tecnica/decisiones-tecnologia.rst`
(o equivalente) y en `implementacion-tecnica.rst` del UC.

### V-2 (Celery beat)

En UC narrativa, reformular:

| Antes (WP) | Después (UC) |
|---|---|
| "Job Celery diario `check_deprecated_menu_items`" | "El Planificador de Tareas ejecuta diariamente la verificación de MenuItems deprecados" |
| "@celery_app.task" + código | (mover a `implementacion-tecnica.rst` del UC) |
| "Celery beat" | "el Planificador de Tareas" |

La narrativa UC describe la **responsabilidad** ("verificar
diariamente MenuItems en estado DEPRECATED y notificar al
actor `system_admin`"), no el motor concreto.

## Sección 6 — Excepciones aplicables

STD-010 §5 permite tecnología explícita en:

1. `implementacion-tecnica.rst` por UC.
2. Identificadores de datos concretos (nombres de tabla,
   campos, stored procedures) — vocabulario de dominio.
3. Criterios de rendimiento atados a algoritmo específico
   (e.g., "P50 ≤ 250ms incluyendo verificación bcrypt"),
   en notas técnicas.

Para el diseño de MenuItem:

- ✅ Permitido en `implementacion-tecnica.rst` del UC:
  "El servicio de cache se implementa con Redis 7+, TTL
  300s, key pattern `caps:user:{id}`".
- ✅ Permitido en `arquitectura-tecnica/`: "El Planificador
  de Tareas se implementa con Celery beat".
- ❌ Prohibido en `flujo-principal.rst` /
  `criterios-aceptacion.rst` / `diagramas-uml.rst`.

## Sección 7 — Cláusula de cumplimiento para Phase 7

Cuando se generen los 9 artefactos UC listados en
``final-decisions-p1-p4-and-pending-items.md`` §6, aplicar
este filtro de paso:

1. **Pre-commit grep** (de STD-010 §6):
   ```bash
   grep -rE "bcrypt|React|MySQL|MariaDB|Celery|mod_wsgi|simplejwt|OperationalError|Pillow|Redis" \
     source/requisitos/casos-uso/menu/ \
     --include="*.rst" \
     --exclude="implementacion-tecnica.rst"
   ```
   Resultado vacío = conforme.

2. **Participantes de diagramas UML** del UC siguen STD-010
   §4: `Interfaz de Acceso`, `Servicio de Aplicación`,
   `Almacén de Datos`, `Servicio de Cache`, `Procesador
   Asíncrono`. Actores = `codename` de `Function` (no
   nombres como "Administrador").

3. **Datos del modelo** (`MenuItem`, `Function`,
   `AccessGroup`, `FunctionGroupMembership`,
   `UserAccessGroupAssignment`) son vocabulario de
   dominio del catálogo RBAC v5.6.0 — permitidos en
   narrativa.

4. **Decisiones de tecnología concreta** (Redis 7+, Celery
   beat, índices PostgreSQL específicos) se mueven a:
   - `source/arquitectura-tecnica/` (nivel sistema), y/o
   - `implementacion-tecnica.rst` por UC.

## Sección 8 — Alineación con observación del ejecutor sobre nombres de clase

Ejecutor también señaló: *"los nombres de las clases tienen
que estar en inglés (no mezclar Cupon con
PaymentTransaction)"*. STD-010 §3.2 menciona ``Almacén de
Datos`` (español) como término canónico de narrativa, no
como nombre de clase de implementación.

**Distinción vigente en el corpus:**

| Capa | Idioma | Ejemplo |
|---|---|---|
| Narrativa UC (STD-010) | Español | "el Almacén de Datos", "el Procesador Asíncrono" |
| Modelo de dominio (clases) | Inglés | `MenuItem`, `Function`, `AccessGroup`, `UserCapabilityResolver` |
| Identificadores RBAC (codenames) | Inglés snake_case | `view_reports`, `manage_menu_catalog` |
| Identificadores DB legacy heredados | Español | `pipeline_runs.estado`, `tbl_historico_tN_YYYY` |

El diseño MenuItem ya cumple: todas las clases propuestas
están en inglés (`MenuItem`, `Function`,
`UserCapabilityResolver`, `FunctionGroupMembership`).

> **Nota:** la auditoría del corpus completo para detectar
> mezcla de idiomas (`Cupon` vs `PaymentTransaction`)
> excede el scope de este WP. Se sugiere abrir WP separado
> *naming-class-language-audit* si el ejecutor quiere
> revisar todo el corpus.

## Sección 9 — Acciones en este WP

| # | Acción | Cuándo |
|---|---|---|
| A-1 | Mantener artefactos discover actuales (Redis/Celery citables como decisión interna) | — |
| A-2 | En Phase 5 STRATEGY, agregar sección "STD-010 compliance" que documente el filtro de paso WP → UC | Phase 5 |
| A-3 | En Phase 7 DESIGN, generar cada UC con: `flujo-principal.rst` (canónico) + `implementacion-tecnica.rst` (libre) | Phase 7 |
| A-4 | Pre-commit del Phase 7: ejecutar el grep de STD-010 §6 sobre `source/requisitos/casos-uso/menu/` antes de cada commit | Phase 7 ongoing |
| A-5 | Diagramas UML del UC: participantes en términos canónicos; actores = `codename` de Function | Phase 7 |
| A-6 | Decisión "Redis 7+ TTL 300s" se documenta en `arquitectura-tecnica/cache-strategy.rst` (nuevo o existente), no en flujo principal del UC | Phase 7 |
| A-7 | Decisión "Celery beat para `check_deprecated_menu_items`" se documenta en `arquitectura-tecnica/scheduled-tasks.rst` (nuevo o existente), no en flujo principal del UC | Phase 7 |

## Sección 10 — Conclusión

1. **Sí existe normativa formal:** STD-010 v1.0.0
   (2026-05-04), aprobado.
2. **Las violaciones detectadas en el WP son de severidad
   media** y no rompen STD-010 directamente (los WP
   discovery artifacts no están en el ámbito de aplicación).
3. **El riesgo crítico** es la propagación de
   `Celery`/`Redis` desde el WP a la narrativa UC en
   Phase 7. La cláusula de cumplimiento de §7 mitiga ese
   riesgo.
4. **El diseño MenuItem es canónico** en cuanto a:
   nombres de clases (inglés), codenames de Function
   (snake_case inglés), y vocabulario de dominio
   (`MenuItem`, `Function`, `AccessGroup`).
5. **Acción mínima:** integrar A-2..A-7 en el plan de
   Phase 7 DESIGN antes de generar artefactos UC.

## Refs

- STD-010: :doc:`/normativa/estandares/std-010-vocabulario-abstracto`.
- D-ETL-005 (origen del principio): WP histórico
  ``source-corrections-pipeline``.
- D-KRUCHTEN-004 (aplicación a Kruchten views): WP
  histórico ``kruchten-view-diagram-types``.
- Ejemplo visual del principio:
  :doc:`/requisitos/_metodologia-aplicacion/casos-uso-diagramas/ejemplo-visual-maquina-de-gaseosas-referencia-generica`.
- Decisiones afectadas en este WP:
  ``discover/final-decisions-p1-p4-and-pending-items.md``
  (V-1, V-2), ``discover/menuitem-design-corrections-v2.md``
  (V-3).
