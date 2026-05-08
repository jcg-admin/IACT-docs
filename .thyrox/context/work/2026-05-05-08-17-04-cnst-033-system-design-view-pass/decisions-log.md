```yml
created_at: 2026-05-05 08:25:00
updated_at: 2026-05-05 08:25:00
project: IACT-docs
work_package: 2026-05-05-08-17-04-cnst-033-system-design-view-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Decisions Log — CNST-033 System & Design View Pass

----

## D-01 — Mapear a clases canónicas existentes, no inventar

**Contexto:** la v1.0.0 de ``translation-table.md``
inventaba nombres nuevos (``UserRepository``,
``AuthService``, ``WebFrontend``) sin consultar el
catálogo canónico de domain-model.

**Hallazgo:** muchos identificadores castellanos
(``ServicioAuditoria``, ``RepositorioAlert``,
``Usuario``, ``Sesion``, ``Reporte``, ``Llamada``) ya
tienen su clase canónica en
``source/arquitectura-tecnica/domain-model/``.

**Decisión:** la traducción procede en 3 tipos:

- **Tipo 1**: mapear a clase canónica existente
  (``Usuario`` → ``User``, ``RepositorioAlert`` →
  ``AlertRepo``, etc.). NO inventar nombre nuevo.
- **Tipo 2**: rol arquitectónico de tier sin clase
  canónica (``AlmacenDatos`` → ``Database``,
  ``Aplicacion`` → ``Application``,
  ``ColaProcesamiento`` → ``ProcessingQueue``).
- **Tipo 3**: identificador sin clase canónica pero
  rol claro (``ServicioAuth`` → ``AuthService``).
  Marcar como hallazgo para WP futuro de
  completar domain-model.

**Justificación:** alinear el naming en design-view con
el dominio canónico evita duplicación conceptual y
mantiene un único punto de verdad. Inventar nombres
crea drift terminológico vs el resto de la
documentación.

----

## D-02 — Sufijo Repo (no Repository) para alinear con corpus

**Contexto:** la v1.0.0 proponía sufijo ``Repository``.
El corpus canónico usa ``Repo`` (``AlertRepo``,
``AssignmentRepo``, ``AuditRepo``,
``ExceptionalPermissionRepo``, ``ScheduledReportRepo``).

**Decisión:** sufijo ``Repo``. Sin excepciones.

**Justificación:** consistencia con corpus existente.
PEP-8 y CNST-033 §3.1/§4.2 favorecen brevedad cuando no
hay ambigüedad. ``Repo`` es el estándar local.

----

## D-03 — Frontend (no UI) para tier de presentación

**Contexto:** ``Interfaz<X>`` puede mapearse a ``UI`` o
``Frontend``. La v1.0.0 oscilaba entre ambos.

**Decisión:** ``Frontend`` con sufijo. ``WebFrontend``,
``AdminFrontend``, ``ReportsFrontend``, etc.

**Justificación:**

- ``UI`` (User Interface) es ambiguo en software:
  también significa "user interface library/framework".
- ``Frontend`` es inequívoco: la app cliente que
  consume la API.
- ``Interfaz`` traducido literal a ``Interface`` choca
  con el concepto de **contrato** (interface en
  programación). ``Frontend`` evita ambigüedad.

----

## D-04 — ServicioETL → PipelineService (§8.2)

**Contexto:** CNST-033 §8.2 dice ``etl → pipeline``.

**Decisión:** ``ServicioETL`` → ``PipelineService``.

**Excepción:** ``etl-ejecucion`` y ``etl-log`` en
domain-model conservan ``Etl`` (PascalCase) en este WP
porque están **fuera de scope** (corregirlos requiere
renombrar archivos del domain-model). Se registra
hallazgo para WP futuro.

----

## D-05 — Hallazgos para WPs futuros

**Hallazgos descubiertos durante DISCOVER que NO se
abordan aquí:**

1. **``etl-ejecucion.rst`` y ``etl-log.rst``** usan
   ``ejecucion`` (castellano) en kebab-case del archivo
   y ``EtlEjecucion`` en clase. Viola CNST-033 §3.1 (SQL
   snake_case inglés) implícitamente.
   → WP futuro ``domain-model-residual-spanish-pass``.

2. **Servicios faltantes en domain-model**:
   ``AuthService``, ``UserService``, ``AccessService``,
   ``LogService``, ``AlertService``, ``CallService``,
   ``SupervisionService``, ``AdminService``,
   ``PipelineService`` aparecen en design-view pero NO
   tienen archivo en domain-model. Posiblemente faltan
   o están materializados como otras clases (e.g.
   ``AlertHook`` ≈ ``AlertService``).
   → WP futuro ``domain-model-services-completion-pass``.

3. **Repos faltantes en domain-model**:
   ``UserRepo``, ``CallRepo``, ``ReportRepo``,
   ``SessionRepo``, ``ApplicationLogRepo``,
   ``EtlExecutionRepo``, ``IvrRepo`` aparecen en
   design-view pero faltan en domain-model.
   → WP futuro
   ``domain-model-repositories-completion-pass``.

**Justificación:** mantener el WP actual acotado al
sweep de identificadores en design-view + system-view.
Los hallazgos del domain-model no se mezclan con la
traducción para preservar trazabilidad.

----

## D-06 — Sweep mecanizado en commit atómico (igual D-06 del WP predecesor)

**Decisión:** mismo patrón del WP predecesor — un solo
commit que renombra todo. Pre-render PlantUML antes de
commitear para validar que diagramas funcionan.

----

## D-07 — Reporte<X> compuestos → DTOs específicos

**Contexto:** ``ReporteLlamadasAbandonadas`` y
``ReporteTransferencias`` aparecen como class boxes en
diagrams. Son DTOs devueltos por los XxxReportService.

**Decisión:**

- ``ReporteLlamadasAbandonadas`` → ``AbandonmentReport``
  (DTO devuelto por ``AbandonmentReportService.get``).
- ``ReporteTransferencias`` → ``TransferReport``
  (DTO devuelto por ``TransferReportService.get``).

Estos nombres ya aparecen en los archivos
domain-model como tipos de retorno de los servicios.

----

## Pendientes de decisión

(ninguno antes de SP-01 — el inventario está completo y
la tabla v2.0.0 es la fuente canónica.)

Pendientes operativos:

- Confirmar con ejecutor antes de SP-02 (análisis de
  colisiones).
- Confirmar con ejecutor antes del sweep mecanizado
  (SP-03).
