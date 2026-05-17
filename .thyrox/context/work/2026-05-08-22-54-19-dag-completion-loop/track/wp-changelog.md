```yml
created_at: 2026-05-08 23:10:00
project: IACT-docs
work_package: 2026-05-08-22-54-19-dag-completion-loop
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — dag-completion-loop

## [1.0.0] — 2026-05-08

### Resumen

Loop ejecutorio multi-iteracion que cierra los criterios de
**naming y estructura** del DAG arquitectonico. Aplica
CLEAN_CODE §6.2 a archivos pendientes de WPs anteriores
(implementation-view excepciones + modulos/diagramas/) y
documenta formalmente la coexistencia de `modulos/` con
DesignView/ImplementationView.

### Renamed (16 git mv)

#### Implementation-view (3) — T2

| Antes | Despues |
|---|---|
| `impl-caller.rst` | `caller-ivr-adapter.rst` |
| `impl-operator.rst` | `operator-extension-point.rst` |
| `impl-supervision.rst` | `supervision-extension-point.rst` |

#### modulos/*/diagramas/* (12) — T3

| Antes | Despues |
|---|---|
| `componentes-mod-{logs,operator,supervision,audit,pipeline,reports,alerts}.rst` | `{modulo}/diagramas/layer-structure.rst` (1 por modulo) |
| `secuencia-creacion-usuario.rst` | `user-creation-flow.rst` |
| `secuencia-sp-rpt-flujo-completo.rst` | `sp-rpt-execution-flow.rst` |
| `secuencia-disparo-alerta-br016.rst` | `alert-trigger-flow.rst` |
| `secuencia-consulta-logs-sistema.rst` | `log-query-flow.rst` |
| `secuencia-atencion-llamada-entrante.rst` | `inbound-call-flow.rst` |

#### rbac/diagramas (1)

| Antes | Despues |
|---|---|
| `clases-entidades-rbac.rst` | `entity-model.rst` |

### Added

- `modulos/coexistence-with-design-implementation-view.rst` —
  documenta formalmente la decision (H-02 del WP previo
  process-deploy-view-rename) sobre 3 dimensiones distintas,
  audiencias distintas, sin duplicacion. Agregado al toctree
  de `modulos/index.rst` en seccion "Decisiones transversales".

### Fixed

- `bootstrap-grupos-predefinidos.rst:271` — title underline
  too short (deuda historica surfaceada por mtime bumps de
  sed durante rename).

### Decisiones del ejecutor

- **T1** (revertida): `process-view`, `deploy-view`,
  `system-view` mantienen estructura flat. La decision del
  WP `process-deploy-view-rename` era correcta — esas vistas
  no se organizan por modulos.
- **T2** (aplicada): `impl-*` renombrados a content-based.
- **T3** (aplicada): 13 archivos renombrados a content-based.

### Verification

- Build strict EXIT=0, 0 warnings.
- 0 cross-refs huerfanas (verificado por grep tras cada
  iteracion).
- 6 de 7 criterios de la checklist DAG pasan juntos en una
  pasada (C7 linkcheck no medido, no bloqueante).

### Hallazgos para WPs siguientes

Auditoria post-cierre revela 3 gaps de **contenido** (no de
naming) que bloquean el PR de consolidacion:

- **H-CONTENT-1:** design-view incompleto en 4 modulos
  (`admin`, `audit`, `logs`, `users`). Solo tienen
  bounded-context + interaction-pattern; falta lifecycle/flow.
- **H-CONTENT-2:** implementation-view incompleto en TODOS
  los 10 modulos in-scope. Solo tienen `layer-structure.rst`,
  faltan diagramas de interaccion a nivel de implementacion.
- **H-CONTENT-3:** modulos/ con naming inconsistente respecto
  a design-view/implementation-view. 5 dirs con prefijo de
  dominio (`sys-`, `etl-`, `vis-`, `user-`, `rbac-`). 1 dir
  realmente ausente (`admin`). 1 split pendiente (`rbac-core`
  → `permissions` + `access`).

Tres WPs siguientes (orden 1 → 3 → 2):

1. `WP-CONTENT-1` — design-view fill (4 modulos).
2. `WP-CONTENT-3` — modulos/ rename + split + admin.
3. `WP-CONTENT-2` — implementation-view fill (10 modulos).

### Refs

- WP `etl-ivr-flow-v2-doc` precedente.
- CLEAN_CODE_NAMING_PRINCIPLES.md §6.2.
- `modulos/coexistence-with-design-implementation-view.rst`.
