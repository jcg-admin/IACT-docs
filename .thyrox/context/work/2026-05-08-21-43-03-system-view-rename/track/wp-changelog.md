```yml
created_at: 2026-05-08 21:55:00
project: IACT-docs
work_package: 2026-05-08-21-43-03-system-view-rename
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — system-view-rename

## [1.0.0] — 2026-05-08

### Resumen

Rename retroactivo de los 12 archivos planos en
`source/arquitectura-tecnica/system-view/` de naming heterogeneo
(prefix de tipo de diagrama UML + sufijo `-sistema-iact`) a
naming basado en contenido. Aplica el mismo principio
CLEAN_CODE §6.2 ya validado en DesignView, ImplementationView,
ProcessView y DeployView.

### Renamed (12 git mv)

| Antes | Despues | Contenido real |
|---|---|---|
| `casos-uso-sistema-iact.rst` | `system-functional-scope.rst` | UC overview del sistema |
| `clases-sistema-iact.rst` | `domain-overview.rst` | Vista global de entidades |
| `componentes-sistema-iact.rst` | `component-overview.rst` | Componentes alto nivel |
| `comunicacion-sistema-iact.rst` | `object-collaboration.rst` | Collaboration diagram |
| `maquina-estados-sistema-iact.rst` | `system-session-lifecycle.rst` | FSM sesion sistema-wide |
| `secuencia-sistema-iact.rst` | `system-interaction-overview.rst` | Sequencia canonica sistema |
| `despliegue-sistema-iact.rst` | `system-deployment.rst` | Topologia despliegue |
| `despliegue-multicliente.rst` | `multi-tenant-topology.rst` | Variante multi-cliente |
| `submaquina-etl.rst` | `etl-execution-lifecycle.rst` | FSM ejecucion ETL |
| `submaquina-reporte.rst` | `ivr-report-query-lifecycle.rst` | FSM consulta reporte IVR |
| `actividad-autenticacion.rst` | `authentication-flow.rst` | Flujo authn |
| `actividad-flujo-principal.rst` | `main-rbac-flow.rst` | Flujo principal por grupo RBAC |

### Cross-refs migration

- `system-view/index.rst` toctree actualizado (12 entries)
- 1 ref textual narrativa en
  `requisitos/reglas-negocio/rbac/catalogo-funciones.rst:788`
  re-targeteada (`despliegue-multicliente.rst` →
  `multi-tenant-topology.rst`)
- 0 cross-refs `:doc:` externas a archivos individuales (solo
  al index del system-view, que no se afecta)

### Verification

- 0 cross-refs huerfanas (verified por grep)
- 0 warnings nuevos en mis archivos renombrados
- 180 warnings docutils PRE-EXISTENTES en archivos no tocados
  por este WP (mismo patron del WP anterior — cache PlantUML
  vacio post-commit `3ebebeab`). No bloqueantes para este WP.

### Auditoria de operational-view

Verificado: `operational-view/` (4 archivos:
`system-administration`, `system-configuration`,
`system-installation`, `system-support`) **ya cumple
CLEAN_CODE** — naming content-based, no requiere rename.

### Refs

- WPs precedentes: design-view-restructure,
  implementation-view-restructure, process-deploy-view-rename.
- CLEAN_CODE_NAMING_PRINCIPLES.md §6.2.
- WP plantuml-cache-investigation (causa de los 180 warnings
  pre-existentes).
