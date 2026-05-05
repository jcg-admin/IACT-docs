```yml
created_at: 2026-05-02 06:00:00
project: IACT-docs
work_package: 2026-05-02-05-32-56-arq-mod-cajones
phase: Phase 11 — TRACK
author: NestorMonroy
status: Completado
```

# Changelog — arq-mod-cajones

## Added

- `modulos/auth/` — 7 spec files (index, responsabilidades, dependencias,
  componentes, restricciones, casos-uso, diagramas)
- `modulos/user-identity/` — 7 spec files
- `modulos/rbac-core/` — 8 spec files (incluye enforcers.rst)
- `modulos/etl-monitoring/` — 7 spec files
- `modulos/vis-reports/` — 7 spec files
- `modulos/alerts/` — 7 spec files
- `modulos/audit/` — 8 spec files (incluye retencion.rst)
- `modulos/sys-logs/` — 8 spec files (incluye metricas.rst)

## Removed

- `modulos/arq-mod-001-auth.rst` — reemplazado por `auth/`
- `modulos/arq-mod-002-user-identity.rst` — reemplazado por `user-identity/`
- `modulos/arq-mod-003-rbac-core.rst` — reemplazado por `rbac-core/`
- `modulos/arq-mod-004-etl-monitoring.rst` — reemplazado por `etl-monitoring/`
- `modulos/arq-mod-005-vis-reports.rst` — reemplazado por `vis-reports/`
- `modulos/arq-mod-006-alerts.rst` — reemplazado por `alerts/`
- `modulos/arq-mod-007-audit.rst` — reemplazado por `audit/`
- `modulos/arq-mod-008-sys-logs.rst` — reemplazado por `sys-logs/`

## Changed

- `modulos/index.rst` — toctree apunta a `{nombre}/index` en lugar de
  archivos planos; tabla de mapeo módulo↔UC usa `:ref:` para enlaces a módulos

## Decisiones de Diseño

**D-01: Split por concern, no por sección numerada**

El split sigue concerns arquitectónicos (responsabilidades, dependencias,
componentes, restricciones, casos-uso, diagramas) — no los números de sección
del documento original. Esto permite agregar/reorganizar secciones sin
renumerar archivos.

**D-02: Archivos extra para módulos con contenido propio**

rbac-core → `enforcers.rst` (tabla de middleware/decoradores)
audit → `retencion.rst` (política de retención 2-5 años)
sys-logs → `metricas.rst` (catálogo histogram/gauge/counter)

**D-03: Labels :ref: en cada index.rst de módulo**

Cada `{módulo}/index.rst` define `.. _arq-mod-NNN:` como label de referencia.
Los archivos de spec dentro del módulo pueden usar `:ref:arq-mod-NNN:` para
referenciar otros módulos. Esto permite trazabilidad bidireccional sin
acoplar rutas de archivo.

**D-04: Transición (----) al inicio de archivo causa ERROR en docutils**

Una transición RST (----) inmediatamente después del título del documento
(sin contenido previo en el body de la sección) genera "Document or section
may not begin with a transition". Fix: eliminar el ---- inicial en archivos
sin :contents: previo.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main` con bump de versión.
Entrada candidata: "Reorganize architecture modules into subdirectory cajones"
