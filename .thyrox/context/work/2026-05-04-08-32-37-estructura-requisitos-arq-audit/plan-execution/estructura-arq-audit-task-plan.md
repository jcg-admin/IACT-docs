```yml
created_at: 2026-05-04 10:54:18
project: IACT-docs
work_package: 2026-05-04-08-32-37-estructura-requisitos-arq-audit
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Activo
```

# Task Plan — Reestructuración source/arquitectura-tecnica/

Estrategia de referencia: `strategy/estructura-requisitos-arq-audit-strategy.md`
Análisis de base: `discover/estructura-requisitos-arq-audit-analysis.md`

---

## BLOQUE A — Use Case View (H-14)

**Objetivo:** `use-case-view/` queda con 13 archivos módulo-indexados
(los `mod-*.rst` de `uc-module-view/`). `uc-module-view/` queda eliminado.

- [x] [T-001] Verificar el estado actual de `uc-module-view/` (listar los 13 mod-*.rst
  y `rbac-funciones-por-modulo.rst`). Confirmar que `use-case-view/` no tiene
  ningún `mod-*.rst` ya.
  `Dependencias: ninguna`

- [x] [T-002] Copiar los 13 archivos `mod-*.rst` de `uc-module-view/` a `use-case-view/`.
  Verificar que los diagramas PlantUML en cada archivo cumplen STD-011 (aliases
  descriptivos). Corregir aliases si no cumplen.
  `Dependencias: T-001`

- [x] [T-003] Evaluar `uc-module-view/rbac-funciones-por-modulo.rst` — decidir si mueve
  a `arquitectura-tecnica/rbac/` o `requisitos/reglas-negocio/rbac/`.
  Mover al destino decidido. Actualizar referencias cruzadas.
  `Dependencias: T-001`

- [x] [T-004] Actualizar `use-case-view/index.rst`: reemplazar el toctree actual
  (81 per-UC) por toctree con los 13 `mod-*.rst`. Actualizar descripción del view.
  `Dependencias: T-002`

- [x] [T-005] Eliminar los 80 archivos per-UC de `use-case-view/` (solo los individuales,
  NO los mod-*.rst recién copiados). Verificar que no quedan referencias
  a los archivos eliminados antes de borrar.
  `Dependencias: T-004`

- [x] [T-006] Eliminar el directorio `uc-module-view/` completo (ya integrado en T-002).
  Buscar referencias cruzadas a `uc-module-view/` en todo el corpus y actualizar
  a las nuevas rutas en `use-case-view/`.
  `Dependencias: T-002, T-003, T-005`

- [x] [T-007] Verificar build: `make html` debe dar 0 WARNING/ERROR relacionados
  con `use-case-view/` o `uc-module-view/`.
  `Dependencias: T-006`

---

## BLOQUE B — Domain Model (H-07 + H-09)

**Objetivo:** `domain-model/` tiene `overview.rst` + un archivo por clase (26 archivos).
Sin prefijo "bounded-context". `bounded-contexts/` eliminado.
Los 160 per-UC reubicados en UC specs o eliminados si duplicados.

**Clases por BC (fuente: bounded-context-*.rst):**
- Auth (3): User, Session, InternalMailbox
- RBAC (6): Function, FunctionGroup, AccessGroup, Assignment,
  ExceptionalPermission, SeparationRule
- Calls (2): Call, Campaign
- Reports (5): Report, Metric, ExportJob, ScheduledReport, SavedView
- Pipeline ETL (1): ETLEjecucion
- Alerts (3): Alert, Threshold, Subscription
- Audit (1): AuditEvent
- Logs (5): ApplicationLog, ETLLog, InfrastructureLog, SystemHealth, TechnicalMetric

- [x] [T-008] Auditar los 160 archivos per-UC de `domain-model/` (80 `{uc}-domain-model.rst`
  + 80 `{uc}-estado.rst`). Para cada UC verificar si ya existe un diagrama equivalente
  en `requisitos/casos-uso/{dominio}/{uc}/diagramas-uml/`.
  Generar lista: (a) duplicados directos, (b) a migrar, (c) ya cubiertos.
  `Dependencias: ninguna`

- [x] [T-009] Crear los 26 archivos de clase en `domain-model/` extrayendo cada clase
  del bounded-context correspondiente. Naming: kebab-case del nombre de la clase
  (User → `user.rst`, ExceptionalPermission → `exceptional-permission.rst`).
  Cada archivo: metadata, título = nombre de la clase, diagrama PlantUML con
  solo esa clase + sus enums + relaciones directas. Aplicar STD-011.
  `Dependencias: ninguna`

- [x] [T-010] Mover `bounded-contexts/overview.rst` a `domain-model/overview.rst`.
  Actualizar referencias (`modelo-dominio-iact.rst` apuntaba a
  `bounded-contexts/overview`).
  `Dependencias: ninguna`

- [x] [T-011] Actualizar `domain-model/index.rst`: toctree con `overview.rst` +
  los 26 archivos de clase organizados por BC en secciones. Describir el
  Domain Model view correctamente (25 entidades canónicas en 7 BCs).
  `Dependencias: T-009, T-010`

- [x] [T-012] Eliminar `arquitectura-tecnica/bounded-contexts/` completo
  (ya integrado — overview en T-010, clases en T-009). Actualizar cualquier
  referencia cruzada remanente.
  `Dependencias: T-009, T-010, T-011`

- [x] [T-013] Para los archivos per-UC de `domain-model/` sin equivalente en UC specs:
  mover `{uc}-estado.rst` a `requisitos/casos-uso/{dominio}/{uc}/diagramas-uml/`.
  Eliminar duplicados confirmados en T-008.
  `Dependencias: T-008, T-011`

- [x] [T-013b] Verificar build sin errores relacionados con `domain-model/`
  y `bounded-contexts/`.
  `Dependencias: T-012, T-013`

---

## BLOQUE C — Deploy View (H-10)

**Objetivo:** `deploy-view/` tiene 3 archivos canónicos (estándar, auth-cache, etl).
Los 77 redundantes, eliminados.

- [x] [T-014] Crear `deploy-view/deploy-estandar.rst` — diagrama canónico tipo
  `Client → WebServer(App) → DB` (variante de los 71 idénticos).
  Metadata correcta, alias STD-011, caption descriptivo.
  `Dependencias: ninguna`

- [x] [T-015] Crear `deploy-view/deploy-auth-cache.rst` — diagrama con nodo cache
  (variante de los 5 de auth/sesiones).
  `Dependencias: ninguna`

- [x] [T-016] Crear `deploy-view/deploy-etl.rst` — diagrama con disparador ETL y SP call
  (variante de los 4 ETL).
  `Dependencias: ninguna`

- [x] [T-017] Actualizar `deploy-view/index.rst`: toctree con 3 canónicos + descripción
  del Deploy View real (entorno, nodos, interconexiones). Eliminar referencia
  a los 80 per-UC en el índice.
  `Dependencias: T-014, T-015, T-016`

- [x] [T-018] Eliminar los 80 archivos per-UC de `deploy-view/`. Verificar 0 referencias
  cruzadas externas antes de eliminar.
  `Dependencias: T-017`

- [x] [T-019] Verificar build: 0 warnings relacionados con `deploy-view/`.
  `Dependencias: T-018`

---

## BLOQUE D — Design View (H-11)

**Objetivo:** `design-view/` tiene 12 archivos módulo-indexados canónicos.
Los 148 boilerplate per-UC, eliminados.

- [x] [T-020] Para cada uno de los 12 módulos crear `design-view/mod-{nombre}.rst`
  con diagrama de secuencia canónico del módulo (patrón real de interacción,
  con SvcNode específico, pasos de dominio reales, no el genérico
  Iface→SvcNode→Store genérico de 4 líneas). Aplicar STD-011.
  Módulos: auth, access, permissions, admin, alerts, audit, etl-monitoring,
  sys-logs, user-identity, vis-reports, operator-calls, supervision.
  `Dependencias: ninguna`

- [x] [T-021] Actualizar `design-view/index.rst`: toctree con 12 canónicos,
  descripción del Design View (patrones de interacción por módulo).
  `Dependencias: T-020`

- [x] [T-022] Eliminar los 160 archivos per-UC de `design-view/`
  (`{uc}-secuencia.rst` y `{uc}-comunicacion.rst`). Verificar 0 refs externas.
  `Dependencias: T-021`

- [x] [T-023] Verificar build: 0 warnings relacionados con `design-view/`.
  `Dependencias: T-022`

---

## BLOQUE E — Implementation View (H-12)

**Objetivo:** `implementation-view/` tiene 12 archivos `mod-*.rst` por módulo.
Los 68 redundantes, eliminados.

- [x] [T-024] Para cada uno de los 12 módulos extraer el diagrama único real
  (ya verificado por hash MD5 en H-12) y crear
  `implementation-view/mod-{nombre}.rst` con ese diagrama.
  Fuente: uno cualquiera de los per-UC del mismo módulo.
  `Dependencias: ninguna`

- [x] [T-025] Actualizar `implementation-view/index.rst`: toctree con 12 canónicos.
  `Dependencias: T-024`

- [x] [T-026] Eliminar los 80 archivos per-UC de `implementation-view/`.
  Verificar 0 refs externas antes de borrar.
  `Dependencias: T-025`

- [x] [T-027] Verificar build: 0 warnings relacionados con `implementation-view/`.
  `Dependencias: T-026`

---

## BLOQUE F — Process View (H-15)

**Objetivo:** Los 81 diagramas UC-flow reclasificados como UC behavior.
`process-view/` contiene 4-6 diagramas de concurrencia real IACT.

- [x] [T-028] Crear `process-view/proc-etl-pipeline.rst` — diagrama de actividad/secuencia
  del pipeline ETL concurrente: disparador → cola → worker → retry →
  notificación. Mostrar paralelismo, condiciones de fallo seguro (P-04).
  `Dependencias: ninguna`

- [x] [T-029] Crear `process-view/proc-alertas-paralelas.rst` — diagrama de concurrencia
  de procesamiento de alertas: múltiples alertas evaluadas en paralelo,
  mecanismo de deduplicación.
  `Dependencias: ninguna`

- [x] [T-030] Crear `process-view/proc-sesiones-jwt.rst` — diagrama de sincronización
  de sesiones JWT: refresh, invalidación, concurrencia multi-sesión.
  `Dependencias: ninguna`

- [x] [T-031] Crear `process-view/proc-dashboard-concurrencia.rst` — diagrama de
  concurrencia de consultas de dashboard de alto volumen: pool de conexiones,
  cache de resultados, timeouts.
  `Dependencias: ninguna`

- [x] [T-032] Actualizar `process-view/index.rst`: toctree con los 4 diagramas reales.
  Describir el Process View (concurrencia, paralelismo, mecanismos de sincronización).
  `Dependencias: T-028, T-029, T-030, T-031`

- [x] [T-033] Los 80 archivos per-UC de `process-view/` (UC activity diagrams)
  deben reclasificarse. Verificar si algún UC spec en
  `requisitos/casos-uso/{dominio}/{uc}/diagramas-uml/` ya tiene diagrama de
  actividad equivalente. Listar los que necesitan migración.
  `Dependencias: ninguna`

- [x] [T-034] Mover los archivos per-UC de `process-view/` sin equivalente en UC specs
  a `requisitos/casos-uso/{dominio}/{uc}/diagramas-uml/diagrama-actividad.rst`.
  `Dependencias: T-033`

- [x] [T-035] Eliminar los archivos per-UC de `process-view/` que ya tienen equivalente
  en UC specs (duplicados). Eliminar los que se migraron en T-034.
  `Dependencias: T-032, T-034`

- [x] [T-036] Verificar build: 0 warnings relacionados con `process-view/`.
  `Dependencias: T-035`

---

## BLOQUE G — RBAC textual (H-08)

**Objetivo:** Los 4 archivos BR de `rbac/modelo-rbac-iact/` en `requisitos/reglas-negocio/`.
RACI en `normativa/gobernanza/`.

- [x] [T-037] Crear `source/requisitos/reglas-negocio/rbac/` (si no existe).
  Mover `catalogo-funciones.rst`, `sod.rst`, `grupos-funciones.rst`, `mapeo-uc.rst`
  a ese directorio. Actualizar `requisitos/reglas-negocio/index.rst`.
  `Dependencias: ninguna`

- [x] [T-038] Mover `arquitectura-tecnica/rbac/raci-rbac-iact/` completo a
  `source/normativa/gobernanza/raci-rbac/`. Actualizar referencias en
  `normativa/gobernanza/index.rst`.
  `Dependencias: ninguna`

- [x] [T-039] Buscar y actualizar las 38 referencias cruzadas (`:doc:`) que apuntan
  a los archivos movidos en T-037 y T-038. Usar grep para encontrarlas todas.
  `Dependencias: T-037, T-038`

- [x] [T-040] Actualizar `arquitectura-tecnica/rbac/modelo-rbac-iact/index.rst` para
  reflejar los archivos que permanecen (ARCH decision: implementacion.rst,
  arquitectura.rst, resumen.rst, permisos-temporales.rst, modelo-datos.rst)
  y agregar referencia cruzada a los movidos.
  `Dependencias: T-037`

- [x] [T-041] Verificar build: 0 warnings relacionados con `rbac/`.
  `Dependencias: T-039, T-040`

---

## BLOQUE H — Eliminación de modulos/casos-uso.rst redundantes (H-13)

**Objetivo:** Los `casos-uso.rst` per-módulo en `modulos/` eliminados (duplican `requisitos/`).

- [x] [T-042] Verificar que la información de los 8 `casos-uso.rst` en
  `arquitectura-tecnica/modulos/*/casos-uso.rst` está cubierta en
  `requisitos/casos-uso/{dominio}/index.rst`. Listar diferencias si hay.
  `Dependencias: ninguna`

- [x] [T-043] Actualizar los `modulos/*/index.rst` para eliminar la referencia a
  `casos-uso.rst` de cada módulo (si estaban en toctree).
  `Dependencias: T-042`

- [x] [T-044] Eliminar los 8 `casos-uso.rst` redundantes de `modulos/`.
  `Dependencias: T-043`

- [x] [T-045] Verificar build: 0 warnings post-eliminación.
  `Dependencias: T-044`

---

## BLOQUE I — Validación final

- [x] [T-046] Ejecutar `bash .claude/scripts/validate-phase-completion.sh`.
  Verificar: working tree clean, remote sync, build 0/0/0.
  `Dependencias: T-007, T-013, T-019, T-023, T-027, T-036, T-041, T-045`

- [x] [T-047] Actualizar `now.md`: stage → `track`, phase → `Phase 11 — TRACK/EVALUATE`.
  `Dependencias: T-046`

- [x] [T-048] Crear `track/estructura-arq-audit-changelog.md` con resumen de cambios:
  archivos eliminados, archivos creados, referencias actualizadas.
  `Dependencias: T-046`

---

## Resumen de impacto estimado

| Bloque | H resueltos | Archivos eliminados (aprox.) | Archivos creados (aprox.) |
|--------|-------------|------------------------------|---------------------------|
| A — Use Case View | H-14 | ~81 (per-UC + uc-module-view) | 0 (ya existen en uc-module-view) |
| B — Domain Model | H-07, H-09 | ~169 (per-UC + 9 bounded-context files) | 27 (overview + 26 por clase) |
| C — Deploy View | H-10 | 77 | 3 |
| D — Design View | H-11 | 148 | 12 |
| E — Implementation View | H-12 | 68 | 12 |
| F — Process View | H-15 | ~75 (reclasificados/eliminados) | 4 |
| G — RBAC textual | H-08, SD-04 | 0 (movidos) | 0 (mismos archivos) |
| H — casos-uso redundantes | H-13 parcial | 8 | 0 |
| **Total** | **8 H resueltos** | **~617** | **~31** |

El net de ~586 archivos menos en `arquitectura-tecnica/` refleja la eliminación
de duplicados y boilerplate que no aportaban información arquitectónica real.
