```yml
project: IACT-docs
work_package: 2026-05-05-08-17-04-cnst-033-system-design-view-pass
created_at: 2026-05-05 08:17:04
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-08-03-31-rbac-vocabulary-cnst-033-pass
target: Aplicar CNST-033 a todos los identificadores en system-view, design-view y modulos
```

# WP — CNST-033 System & Design View Pass

## Trigger

El WP predecesor (``rbac-vocabulary-cnst-033-pass``) cerró
las 5 violaciones derivadas de D-11 pero registró en su
changelog (sección "Aceptado / no fixeado") que **otros
identificadores castellanos** quedaban fuera de scope:

> Otros identificadores castellanos en seq-reports.rst y
> system-view/ (``InterfazReportes``, ``RepositorioReport``,
> ``AlmacenDatos``, ``ColaProcesamiento``, etc.) — quedan
> fuera del scope de este WP. Se registra como hallazgo
> para WP futuro ``cnst-033-system-design-view-pass``.

## Alcance — inventario inicial

Inventario automatizado encontró **~50 identificadores
únicos** en castellano distribuidos en **17 archivos**:

- 13 archivos en ``source/arquitectura-tecnica/design-view/``
  (sequencia diagrams: seq-access, seq-admin, seq-alerts,
  seq-audit, seq-auth, seq-caller, seq-logs, seq-operator,
  seq-permissions, seq-pipeline, seq-reports,
  seq-supervision, seq-users)
- 1 archivo en ``source/arquitectura-tecnica/system-view/``
  (clases-sistema-iact)
- 3 archivos en ``source/arquitectura-tecnica/modulos/``

Identificadores con mayor frecuencia (top 20):

| # | Identificador | Ocurrencias | Archivos |
|---|---------------|-------------|----------|
| 1 | ``AlmacenDatos`` | 87 | 13 |
| 2 | ``RepositorioUser`` | 33 | 3 |
| 3 | ``InterfazAdmin`` | 31 | 4 |
| 4 | ``ServicioETL`` | 27 | 2 |
| 5 | ``ServicioSupervision`` | 21 | 1 |
| 6 | ``ServicioLlamadas`` | 18 | 2 |
| 7 | ``ServicioAlertas`` | 18 | 1 |
| 8 | ``Reporte`` | 17 | 5 |
| 9 | ``Aplicacion`` | 17 | 17 |
| 10 | ``InterfazSupervision`` | 16 | 1 |
| 11 | ``Almacen`` | 14 | 10 |
| 12 | ``ServicioAdmin`` | 14 | 1 |
| 13 | ``RepositorioAssignment`` | 14 | 2 |
| 14 | ``ServicioExportacion`` | 14 | 2 |
| 15 | ``RepositorioCall`` | 14 | 2 |
| 16 | ``InterfazAuditoria`` | 13 | 1 |
| 17 | ``ServicioAuth`` | 13 | 2 |
| 18 | ``InterfazLogs`` | 13 | 1 |
| 19 | ``RepositorioETLEjecucion`` | 13 | 1 |
| 20 | ``InterfazPipeline`` | 13 | 1 |

(Inventario completo en
``discover/spanish-identifiers-inventory.md``.)

## Estrategia de traducción

CNST-033 §4.2 establece que los nombres de clase
**describen dominio, no mecanismo**. Pero estos
identificadores están en diagramas de **secuencia**, donde
los participantes representan **roles arquitectónicos**
(stratification: Frontend → API → Repository → Datastore),
NO clases concretas del domain-model.

**Decisión propuesta — categorización del vocabulario:**

| Patrón castellano | Inglés propuesto | Justificación |
|-------------------|------------------|---------------|
| ``Interfaz<X>`` | ``<X>UI`` o ``<X>Frontend`` | rol UI tier |
| ``Servicio<X>`` | ``<X>Service`` | rol application tier (DDD) |
| ``Repositorio<X>`` | ``<X>Repository`` | rol data access tier |
| ``Almacen<X>`` / ``AlmacenDatos`` | ``Datastore`` o ``Database`` | rol persistence tier |
| ``Cola<X>`` / ``ColaProcesamiento`` | ``ProcessingQueue`` | rol queue tier |
| ``Manejador<X>`` | ``<X>Handler`` | rol mediator |
| ``Gestor<X>`` | ``<X>Manager`` (raro — preferir verbo) | rol coordinator |
| ``Reporte<X>`` (clase) | ``<X>Report`` | DTO |
| ``Aplicacion`` | ``Application`` | tier name |
| ``Sesion`` | ``Session`` | entidad |
| ``Auditoria`` | ``Audit`` | dominio |
| ``Alerta`` | ``Alert`` | dominio |
| ``Usuario`` | ``User`` | entidad |

**Excepción declarada:** ``IACT`` y ``IVR`` se mantienen
como acrónimos del dominio (per D-04 del WP predecesor).

## Áreas a revisar

1. **R-design-view-seq**: 13 archivos seq-*.rst — sweep
   amplio, todos los participantes castellanos.
2. **R-system-view-clases**: clases-sistema-iact.rst —
   class boxes en castellano (``Aplicacion``, ``Reporte``,
   etc.).
3. **R-modulos**: modulos/vis-reports/ y otros — sweep
   focalizado.
4. **R-conflictos**: validar que ``Service``,
   ``Repository``, ``UI``/``Frontend`` no introduzcan
   colisiones con clases canónicas del domain-model
   (e.g. ``UserRepository`` vs ``RBACRepo`` ya existente).
5. **R-orden-de-relaciones**: validar que las flechas
   en sequence diagrams mantienen sentido tras el
   renombrado.
6. **R-prerender**: post-sweep, todos los diagramas
   deben renderizar sin error.

## Output esperado

- ``discover/spanish-identifiers-inventory.md`` —
  inventario completo (todos los ~50 identificadores
  con conteo y archivos).
- ``discover/translation-table.md`` — tabla de mapeo
  castellano→inglés con justificación CNST-033 por fila.
- ``decisions-log.md`` — D-NN por categoría de
  identificador (no por identificador individual —
  serían demasiados).
- ``analyze/conflict-check.md`` — validación de que el
  inglés propuesto no colisiona con identificadores
  canónicos.
- ``track/{wp}-changelog.md`` — registro por archivo.

## Riesgos

- **R1**: scope amplio (~50 identificadores, ~17
  archivos) — riesgo de cambios masivos no triviales.
  Mitigación: sweep mecanizado con tabla canónica
  (translation-table.md) revisada antes de ejecutar.
- **R2**: colisiones con domain-model — algunos
  identificadores propuestos (``UserRepository``)
  podrían chocar con clases canónicas
  (``RBACRepo``, ``AssignmentRepo``). Mitigación:
  análisis de colisiones antes de aplicar.
- **R3**: pérdida de semántica al traducir —
  ``InterfazAdmin`` puede ser "admin frontend" o
  "admin UI" según contexto. Mitigación: revisar
  cada identificador en contexto antes del sweep.
- **R4**: ``ServicioETL`` y ``Pipeline`` —
  CNST-033 §8.2 dice ``etl → pipeline``. ¿Renombramos
  ``ServicioETL`` a ``PipelineService``?
  Decisión pendiente.

## Stopping points

- **SP-01**: tras inventario completo y tabla de
  traducción (validar mapping antes de ejecutar).
- **SP-02**: tras análisis de colisiones (validar que
  no rompemos identificadores canónicos del
  domain-model).
- **SP-03**: tras sweep del primer archivo
  (validar que el patrón mecanizado funciona).
- **SP-04**: pre-merge — pre-render 0 errores.

## Predecesores

- ``2026-05-05-08-03-31-rbac-vocabulary-cnst-033-pass``
  — cerró las 5 violaciones de D-11.
- ``2026-05-05-07-40-30-arq-tecnica-uml-rigor-pass`` —
  pasada UML que descubrió la cadena de violaciones.

## Decisiones pendientes del ejecutor

1. **CNST-033 §8.2 sobre "ETL → pipeline"**: ¿se aplica
   a ``ServicioETL``? Inclinación inicial:
   ``ServicioETL`` → ``PipelineService`` (siguiendo §8.2
   literalmente). Validar si el corpus existente usa
   "Pipeline" como término de dominio.
2. **Política de "Almacen"**: ¿``Datastore`` (genérico)
   o ``Database`` (específico)? Los diagramas usan
   ``database AlmacenDatos`` con stereotipo
   ``<<postgresql>>`` — concreto. Inclinación:
   ``Database`` para mantener especificidad.
