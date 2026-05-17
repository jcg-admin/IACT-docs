```yml
created_at: 2026-05-05 08:18:00
project: IACT-docs
work_package: 2026-05-05-08-17-04-cnst-033-system-design-view-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Inventario completo — identificadores castellanos

Generado por sweep automatizado. Filtrado: PascalCase con
stems castellanos (``Servicio``, ``Repositorio``,
``Interfaz``, ``Almacen``, ``Cola``, ``Reporte``,
``Aplicacion``, ``Auditoria``, ``Alerta``, ``Usuario``,
``Sesion``, etc.) en
``source/arquitectura-tecnica/{system-view,design-view,modulos}/``.

## Tabla completa

| Identificador | Ocurrencias | Archivos |
|---------------|-------------|----------|
| ``AlmacenDatos`` | 87 | 13 |
| ``RepositorioUser`` | 33 | 3 |
| ``InterfazAdmin`` | 31 | 4 |
| ``ServicioETL`` | 27 | 2 |
| ``ServicioSupervision`` | 21 | 1 |
| ``ServicioLlamadas`` | 18 | 2 |
| ``ServicioAlertas`` | 18 | 1 |
| ``Reporte`` | 17 | 5 |
| ``Aplicacion`` | 17 | 17 |
| ``InterfazSupervision`` | 16 | 1 |
| ``Almacen`` | 14 | 10 |
| ``ServicioAdmin`` | 14 | 1 |
| ``RepositorioAssignment`` | 14 | 2 |
| ``ServicioExportacion`` | 14 | 2 |
| ``RepositorioCall`` | 14 | 2 |
| ``InterfazAuditoria`` | 13 | 1 |
| ``ServicioAuth`` | 13 | 2 |
| ``InterfazLogs`` | 13 | 1 |
| ``RepositorioETLEjecucion`` | 13 | 1 |
| ``InterfazPipeline`` | 13 | 1 |
| ``RepositorioAlert`` | 13 | 1 |
| ``InterfazMonitor`` | 13 | 1 |
| ``InterfazAgente`` | 13 | 1 |
| ``InterfazReportes`` | 13 | 1 |
| ``ServicioPermisos`` | 12 | 1 |
| ``ServicioAcceso`` | 12 | 1 |
| ``ServicioUsuarios`` | 12 | 1 |
| ``ServicioRBAC`` | 9 | 1 |
| ``Usuario`` | 8 | 8 |
| ``Repositorio`` | 8 | 7 |
| ``InterfazWeb`` | 8 | 1 |
| ``RepositorioExceptionalPerm`` | 7 | 1 |
| ``ServicioAuditoria`` | 7 | 1 |
| ``RepositorioAuditEvent`` | 7 | 1 |
| ``Auditoria`` | 7 | 7 |
| ``ServicioLogs`` | 7 | 1 |
| ``RepositorioApplicationLog`` | 7 | 1 |
| ``RepositorioSession`` | 7 | 1 |
| ``RepositorioIVR`` | 7 | 1 |
| ``RepositorioReport`` | 7 | 1 |
| ``Sesion`` | 5 | 5 |
| ``ColaProcesamiento`` | 5 | 1 |
| ``ServicioDeOrigen`` | 5 | 1 |
| ``Alerta`` | 4 | 4 |
| ``AuditoriaAcceso`` | 3 | 1 |
| ``Interfaz`` | 3 | 1 |
| ``ReporteLlamadasAbandonadas`` | 2 | 1 |
| ``ReporteTransferencias`` | 2 | 1 |
| ``Servicio`` | 2 | 2 |
| ``Operador`` | 2 | 2 |
| ``Llamada`` | 1 | 1 |
| ``Cliente`` | 1 | 1 |

**Total identificadores únicos:** 52
**Total archivos afectados:** 17 (estimado tras
deduplicación)

## Archivos afectados

```
source/arquitectura-tecnica/system-view/
├── clases-sistema-iact.rst

source/arquitectura-tecnica/design-view/
├── seq-access.rst
├── seq-admin.rst
├── seq-alerts.rst
├── seq-audit.rst
├── seq-auth.rst
├── seq-caller.rst
├── seq-logs.rst
├── seq-operator.rst
├── seq-permissions.rst
├── seq-pipeline.rst
├── seq-reports.rst
├── seq-supervision.rst
└── seq-users.rst

source/arquitectura-tecnica/modulos/
└── ... (3 archivos por confirmar)
```

## Categorías

Por agrupación de stems:

| Categoría | Identificadores | Total ocurrencias |
|-----------|-----------------|--------------------|
| ``Interfaz*`` (UI tier) | 11 | 154 |
| ``Servicio*`` (App tier) | 14 | 197 |
| ``Repositorio*`` (Data tier) | 11 | 124 |
| ``Almacen*`` (Persistence) | 2 | 101 |
| ``Cola*`` (Queue) | 1 | 5 |
| ``Reporte*`` (DTO) | 3 | 21 |
| Entidades singulares (``Usuario``, ``Sesion``, etc.) | 10 | 49 |

## Hallazgo

**``Aplicacion`` aparece en los 17 archivos** — es el
identificador más universal. Probablemente representa el
tier de aplicación genérico ("Application"). Es seguro
renombrar de forma masiva.

**``AlmacenDatos`` con 87 ocurrencias en 13 archivos** —
es el participante database de los sequence diagrams.
Convertir a ``Database`` mantiene la especificidad
``<<postgresql>>``.
