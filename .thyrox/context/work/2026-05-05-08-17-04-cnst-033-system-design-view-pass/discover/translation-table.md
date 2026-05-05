```yml
created_at: 2026-05-05 08:18:30
updated_at: 2026-05-05 08:24:00
project: IACT-docs
work_package: 2026-05-05-08-17-04-cnst-033-system-design-view-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 2.0.0
```

# Tabla canónica de traducción (revisada)

**Cambio v2.0.0:** la versión 1.0.0 inventaba nombres
nuevos (``UserRepository``, ``AuthService``,
``WebFrontend``). Esto era **incorrecto**: la mayoría de
los identificadores castellanos en design-view tienen
**clase canónica ya existente** en
``source/arquitectura-tecnica/domain-model/``.

**Regla revisada:**

1. **Tipo 1 — Si existe clase canónica:** usar el nombre
   canónico exacto. NO inventar.
2. **Tipo 2 — Si es rol de tier sin clase canónica:**
   usar label de tier idiomático (Database, Frontend,
   ProcessingQueue, etc.).

## Catálogo canónico consultado

``ls source/arquitectura-tecnica/domain-model/*.rst`` →
68 archivos. Stems en PascalCase derivados de los
nombres de archivo kebab-case (e.g. ``audit-repo.rst`` →
``AuditRepo``).

## Tipo 1 — Mapeo a clase canónica existente

| Castellano | Canónico (existe) | Archivo domain-model |
|------------|-------------------|----------------------|
| ``Usuario`` | ``User`` | user.rst |
| ``Sesion`` | ``Session`` | session.rst |
| ``Llamada`` | ``Call`` | call.rst |
| ``Alerta`` | ``Alert`` | alert.rst |
| ``Reporte`` | ``Report`` | report.rst |
| ``RepositorioAlert`` | ``AlertRepo`` | alert-repo.rst |
| ``RepositorioAssignment`` | ``AssignmentRepo`` | assignment-repo.rst |
| ``RepositorioExceptionalPerm`` | ``ExceptionalPermissionRepo`` | exceptional-permission-repo.rst |
| ``RepositorioAuditEvent`` | ``AuditRepo`` | audit-repo.rst (opera sobre AuditEvent) |
| ``ServicioAuditoria`` | ``AuditService`` | audit-service.rst |
| ``ServicioPermisos`` | ``PermissionService`` | permission-service.rst |
| ``ServicioExportacion`` | ``ExportWorker`` | export-worker.rst |
| ``ServicioRBAC`` | ``RbacRepo`` | rbac-repo.rst (es repo, no service) |
| ``ReporteLlamadasAbandonadas`` | ``AbandonmentReport`` | DTO devuelto por AbandonmentReportService |
| ``ReporteTransferencias`` | ``TransferReport`` | DTO devuelto por TransferReportService |
| ``Cliente`` (caller IVR) | ``Caller`` | (concepto — sin clase entity) |

## Tipo 2 — Roles de tier sin clase canónica

Estos identificadores representan **roles arquitectónicos
genéricos** en sequence diagrams. NO existen como clase en
domain-model — son labels de stratification (Frontend,
Application, Database, Queue).

| Castellano | Inglés (label de tier) | Justificación |
|------------|------------------------|----------------|
| ``AlmacenDatos`` | ``Database`` | participant ``database`` con stereotype ``<<postgresql>>`` |
| ``Almacen`` (bare) | ``Datastore`` | genérico |
| ``Aplicacion`` | ``Application`` | tier name canónico |
| ``ColaProcesamiento`` | ``ProcessingQueue`` | tier queue |
| ``ServicioDeOrigen`` | ``SourceSystem`` | sistema externo (IVR origen) |
| ``Operador`` | ``Operator`` | actor |
| ``Repositorio`` (bare) | ``Repository`` | rol genérico |
| ``Servicio`` (bare) | ``Service`` | rol genérico |
| ``Interfaz`` (bare) | ``Frontend`` | rol genérico |

## Tipo 3 — Sin clase canónica pero entidad clara

Identificadores que no tienen su archivo en domain-model
pero refieren a entidades/servicios ya conceptualizados:

| Castellano | Inglés | Justificación |
|------------|--------|---------------|
| ``Auditoria`` | ``Audit`` | dominio conceptual (sin clase entity) |
| ``AuditoriaAcceso`` | ``AccessAudit`` | dominio compuesto |

## Frontends por área funcional

Los ``Interfaz<X>`` no tienen clase canónica — son
**actores frontend** que invocan los servicios. Mapear
con sufijo ``Frontend`` per convención DDD para UI tier.

| Castellano | Inglés | Justificación |
|------------|--------|---------------|
| ``InterfazWeb`` | ``WebFrontend`` | UI genérico |
| ``InterfazAdmin`` | ``AdminFrontend`` | UI admin |
| ``InterfazReportes`` | ``ReportsFrontend`` | UI reportes |
| ``InterfazAuditoria`` | ``AuditFrontend`` | UI auditoría |
| ``InterfazLogs`` | ``LogsFrontend`` | UI logs |
| ``InterfazPipeline`` | ``PipelineFrontend`` | UI pipeline |
| ``InterfazMonitor`` | ``MonitorFrontend`` | UI monitoreo |
| ``InterfazAgente`` | ``AgentFrontend`` | UI agente |
| ``InterfazSupervision`` | ``SupervisionFrontend`` | UI supervisión |

## Servicios sin clase canónica

Aparecen como participantes en sequence diagrams pero
**no tienen su archivo en domain-model**. Posibles
causas:

- Son roles arquitectónicos sin materialización como
  clase única (``ServicioAuth`` orquesta varios:
  ``Session``, ``User``).
- Faltan en domain-model — hallazgo para WP futuro.

| Castellano | Inglés (rol) | ¿Falta clase canónica? |
|------------|--------------|------------------------|
| ``ServicioAuth`` | ``AuthService`` | SÍ — registrar hallazgo |
| ``ServicioUsuarios`` | ``UserService`` | SÍ |
| ``ServicioAcceso`` | ``AccessService`` | SÍ |
| ``ServicioLogs`` | ``LogService`` | SÍ |
| ``ServicioAlertas`` | ``AlertService`` | SÍ — existe AlertHook pero es ≠ |
| ``ServicioETL`` | ``PipelineService`` | SÍ — §8.2 |
| ``ServicioLlamadas`` | ``CallService`` | SÍ |
| ``ServicioSupervision`` | ``SupervisionService`` | SÍ |
| ``ServicioAdmin`` | ``AdminService`` | SÍ |

**Decisión propuesta para Tipo "Servicios sin canónico":**
en este WP usar el nombre inglés del rol
(``AuthService``, ``UserService``, etc.). Registrar
hallazgo en ``track/`` para WP futuro
``domain-model-completion-pass`` que materialice los
servicios faltantes como clase canónica.

## Repositorios sin clase canónica

| Castellano | Inglés (rol) | ¿Falta clase? |
|------------|--------------|---------------|
| ``RepositorioUser`` | ``UserRepo`` | SÍ — no existe user-repo.rst |
| ``RepositorioCall`` | ``CallRepo`` | SÍ |
| ``RepositorioReport`` | ``ReportRepo`` | SÍ |
| ``RepositorioSession`` | ``SessionRepo`` | SÍ |
| ``RepositorioApplicationLog`` | ``ApplicationLogRepo`` | SÍ |
| ``RepositorioETLEjecucion`` | ``EtlExecutionRepo`` | SÍ — §8.2 dudoso (ETL es entidad concreta acá: ``etl-ejecucion`` ya existe en español en el domain-model) |
| ``RepositorioIVR`` | ``IvrRepo`` | SÍ |

**Convención:** usar sufijo ``Repo`` (no ``Repository``)
para alinear con los repos canónicos existentes
(``AlertRepo``, ``AssignmentRepo``, ``AuditRepo``,
``ScheduledReportRepo``).

## Hallazgo crítico — naming en castellano en domain-model

``etl-ejecucion.rst`` y ``etl-log.rst`` usan **kebab-case
en castellano** (``ejecucion`` debería ser
``execution``). La clase derivada ``EtlEjecucion`` viola
CNST-033.

**Decisión:** este hallazgo queda **fuera de scope** de
este WP (que ataca design-view, no domain-model).
Registrar para WP futuro
``domain-model-residual-spanish-pass``.

## Anti-pattern resuelto

La v1.0.0 de esta tabla proponía ``UserRepository`` y
similares con sufijo ``Repository`` completo. Era
inconsistente con el corpus existente que usa ``Repo``
(``AlertRepo``, ``AssignmentRepo``).

**Lección:** consultar el corpus canónico ANTES de
proponer naming convention.
