```yml
created_at: 2026-05-02 05:32:56
project: IACT-docs
work_package: 2026-05-02-05-32-56-arq-mod-cajones
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Activo
```

# Task Plan — Reestructuración arq-mod-* en cajones

## Principio

Cada `arq-mod-N-nombre.rst` se convierte en un directorio `nombre/` con
archivos spec separados. El archivo plano original se elimina y el
directorio toma su lugar en el toctree del `index.rst` padre.

Archivos por módulo:
- `index.rst` — propósito + alcance + toctree interno + cross-refs (:doc:)
- `responsabilidades.rst` — puede / no puede (tablas list-table)
- `dependencias.rst` — depende de / requerido por (list-table + :doc: refs)
- `componentes.rst` — componentes técnicos, modelos de datos, APIs expuestas
- `restricciones.rst` — CNSTs aplicables (list-table + :doc: refs a normativa)
- `casos-uso.rst` — UCs asociados + FRs derivados (list-table + :doc: refs)
- `diagramas.rst` — todos los PlantUML del módulo (ya escritos en Task Plan 1)

Reglas:
- Toda referencia a otro doc RST → `:doc:`ruta/relativa``
- Toda referencia a sección con etiqueta → `:ref:`etiqueta``
- Tablas → `.. list-table::` (ya en uso, mantener)
- Diagramas → `.. uml::` con `:caption:`
- NO crear referencias desde/hacia `.thyrox/`, `temp-holding/`, `source/base-cognitiva/`

---

## T-001 — auth/ (arq-mod-001)

Crear `modulos/auth/` con 7 archivos desde `arq-mod-001-auth.rst`:

- [ ] `auth/index.rst` — propósito, alcance, toctree, :doc: a casos-uso/auth/index
- [ ] `auth/responsabilidades.rst` — sección 3 PUEDE/NO PUEDE
- [ ] `auth/dependencias.rst` — sección 4 depende de / requerido por con :doc: refs
- [ ] `auth/componentes.rst` — sección 5 (componentes + APIs + modelos + código)
- [ ] `auth/restricciones.rst` — sección 6 CNSTs con :doc: a normativa/
- [ ] `auth/casos-uso.rst` — secciones 7+8 (UCs + FRs) con :doc: a casos-uso/auth/
- [ ] `auth/diagramas.rst` — secciones 9+11 PlantUML (secuencia + componentes)
- [ ] Eliminar `arq-mod-001-auth.rst`
- [ ] Actualizar `modulos/index.rst` toctree → `auth/index`

## T-002 — user-identity/ (arq-mod-002)

Crear `modulos/user-identity/` con 7 archivos:

- [ ] `user-identity/index.rst` — propósito, alcance, toctree, :doc: a casos-uso/users/index
- [ ] `user-identity/responsabilidades.rst`
- [ ] `user-identity/dependencias.rst` — con :doc: refs
- [ ] `user-identity/componentes.rst`
- [ ] `user-identity/restricciones.rst`
- [ ] `user-identity/casos-uso.rst` — con :doc: a casos-uso/users/
- [ ] `user-identity/diagramas.rst` — estado ciclo de vida usuario (BR-009)
- [ ] Eliminar `arq-mod-002-user-identity.rst`
- [ ] Actualizar toctree → `user-identity/index`

## T-003 — rbac-core/ (arq-mod-003)

Crear `modulos/rbac-core/` con 8 archivos (tiene sección extra: enforcers):

- [ ] `rbac-core/index.rst` — propósito, alcance, :doc: a casos-uso/access/ + casos-uso/permissions/
- [ ] `rbac-core/responsabilidades.rst`
- [ ] `rbac-core/enforcers.rst` — sección 4 enforcers de seguridad
- [ ] `rbac-core/dependencias.rst`
- [ ] `rbac-core/componentes.rst`
- [ ] `rbac-core/restricciones.rst`
- [ ] `rbac-core/casos-uso.rst` — con :doc: a casos-uso/access/ y casos-uso/permissions/
- [ ] `rbac-core/diagramas.rst` — precedencia de permisos + SoD (UML-11 × 2)
- [ ] Eliminar `arq-mod-003-rbac-core.rst`
- [ ] Actualizar toctree → `rbac-core/index`

## T-004 — etl-monitoring/ (arq-mod-004)

Crear `modulos/etl-monitoring/` con 7 archivos:

- [ ] `etl-monitoring/index.rst` — :doc: a casos-uso/pipeline/index
- [ ] `etl-monitoring/responsabilidades.rst`
- [ ] `etl-monitoring/dependencias.rst`
- [ ] `etl-monitoring/componentes.rst`
- [ ] `etl-monitoring/restricciones.rst`
- [ ] `etl-monitoring/casos-uso.rst` — con :doc: a casos-uso/pipeline/
- [ ] `etl-monitoring/diagramas.rst` — secuencia ETL con Actor Tiempo
- [ ] Eliminar `arq-mod-004-etl-monitoring.rst`
- [ ] Actualizar toctree → `etl-monitoring/index`

## T-005 — vis-reports/ (arq-mod-005)

Crear `modulos/vis-reports/` con 7 archivos:

- [ ] `vis-reports/index.rst` — :doc: a casos-uso/reports/index
- [ ] `vis-reports/responsabilidades.rst`
- [ ] `vis-reports/dependencias.rst`
- [ ] `vis-reports/componentes.rst`
- [ ] `vis-reports/restricciones.rst`
- [ ] `vis-reports/casos-uso.rst` — con :doc: a casos-uso/reports/
- [ ] `vis-reports/diagramas.rst` — actividad flujo de acceso/exportación
- [ ] Eliminar `arq-mod-005-vis-reports.rst`
- [ ] Actualizar toctree → `vis-reports/index`

## T-006 — alerts/ (arq-mod-006)

Crear `modulos/alerts/` con 7 archivos:

- [ ] `alerts/index.rst` — :doc: a casos-uso/alerts/index
- [ ] `alerts/responsabilidades.rst`
- [ ] `alerts/dependencias.rst`
- [ ] `alerts/componentes.rst` — InternalMessage model + AlertConfig + AlertInstance
- [ ] `alerts/restricciones.rst` — CNST_001 no-email
- [ ] `alerts/casos-uso.rst` — con :doc: a casos-uso/alerts/
- [ ] `alerts/diagramas.rst` — estado ciclo de vida alerta (CNST_001)
- [ ] Eliminar `arq-mod-006-alerts.rst`
- [ ] Actualizar toctree → `alerts/index`

## T-007 — audit/ (arq-mod-007)

Crear `modulos/audit/` con 8 archivos (tiene sección extra: retención/compliance):

- [ ] `audit/index.rst` — :doc: a casos-uso/audit/index
- [ ] `audit/responsabilidades.rst`
- [ ] `audit/dependencias.rst`
- [ ] `audit/componentes.rst` — AuditLog model + decorador + APIs
- [ ] `audit/restricciones.rst`
- [ ] `audit/casos-uso.rst` — con :doc: a casos-uso/audit/
- [ ] `audit/retencion.rst` — sección 12 retención y compliance (política 2-5 años)
- [ ] `audit/diagramas.rst` — secuencia emisión de evento
- [ ] Eliminar `arq-mod-007-audit.rst`
- [ ] Actualizar toctree → `audit/index`

## T-008 — sys-logs/ (arq-mod-008)

Crear `modulos/sys-logs/` con 8 archivos (tiene sección extra: métricas técnicas):

- [ ] `sys-logs/index.rst` — :doc: a casos-uso/logs/index
- [ ] `sys-logs/responsabilidades.rst`
- [ ] `sys-logs/dependencias.rst`
- [ ] `sys-logs/componentes.rst` — health check view + APIs + config logging
- [ ] `sys-logs/restricciones.rst`
- [ ] `sys-logs/casos-uso.rst` — con :doc: a casos-uso/logs/
- [ ] `sys-logs/metricas.rst` — sección 12 métricas técnicas (histogram, gauge, counter)
- [ ] `sys-logs/diagramas.rst` — actividad health check con Actor Tiempo
- [ ] Eliminar `arq-mod-008-sys-logs.rst`
- [ ] Actualizar toctree → `sys-logs/index`

---

## T-009 — Actualizar modulos/index.rst

- [ ] Reescribir toctree con las 8 entradas `{nombre}/index`
- [ ] Agregar :doc: refs a los módulos desde la tabla de mapeo módulo↔UC
- [ ] Verificar que todos los módulos tienen `.. _arq-mod-NNN:` como etiqueta para :ref:

## T-010 — Build y validación

- [ ] `.venv/bin/sphinx-build -b html source build/html`
- [ ] 0 warnings
- [ ] Verificar que todos los :doc: y :ref: resuelven (no broken references)

## T-011 — Commit y push

- [ ] Commit por lote o consolidado
- [ ] Push a `feature/arquitectura-tecnica-content`
