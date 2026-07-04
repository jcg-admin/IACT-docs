```yml
created_at: 2026-07-03 22:15:30
project: IACT-docs
work_package: 2026-07-03-22-15-30-auditar-implementacion-ucs-api-ui
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
```

# WP Changelog — auditar-implementacion-ucs-api-ui

## Added

- Iniciativa `source/gestion/pm/iniciativas/auditar-implementacion-ucs-api-ui/`
  con index, alcance, deep-analisis, matriz (88 filas, generada
  programáticamente) y tareas-y-progreso (T-001..T-008 completadas).
- WP con discover analysis, risk register y evidencia grep-validada
  (`analyze/evidencia/matriz-uc-api-ui.md`).

## Added (extensión de sesión — pedido del ejecutor)

- `analyze/ramas-y-prs/estado-ramas-prs-multirepo.md` — análisis
  verificado de PRs abiertos (5, todos dependabot) y ramas por repo,
  con SHAs de respaldo de las ramas eliminadas.

## Fixed

- 3 iniciativas huérfanas de toctree registradas en
  `gestion/pm/iniciativas/index.rst`
  (`auditar-conformidad-uc-codigo-vs-docs`,
  `auditoria-cross-stack-falsos-positivos-y-ghost-sp`,
  `documentar-uc-adm-01-05`) — eliminan 3 de los 21 warnings
  pre-existentes del strict build.

## Build (evidencia)

- Strict build completo (`sphinx -W`):
  `track/build-logs/sphinx-strict-auditar-implementacion-ucs-2026-07-03T22-28-59.log`
  → `EXIT=1`, 21 warnings, **0 originados por los archivos de esta
  iniciativa** (grep del log por `auditar-implementacion-ucs-api-ui`
  = 0 hits). Deuda pre-existente: 4 sintaxis RST, 3 toctree huérfanos
  (corregidos arriba), 3 highlighting, render PlantUML fallando en el
  entorno de la sesión.
- Rebuild estricto incremental post-fix:
  `track/build-logs/sphinx-strict-incremental-toctree-fix-2026-07-04T00-02-35.log`
  → `EXIT=1` con solo 2 warnings, ambos avisos de infraestructura de
  `plantuml_cached` ("not safe for parallel writing" / "doing serial
  write") que se emiten en todo build `-W -j auto`. Los 3 huérfanos de
  toctree quedaron resueltos (0 hits `toc.not_included`).
- `make html` canónico: **bloqueado en este entorno** — el guard
  `check-bootstrap` exige `tools/plantuml.jar` y el proxy de la sesión
  retorna 403 al descargarlo de GitHub releases
  (`make-html-canonico-2026-07-04T00-11-*.log`). Esto también explica
  los 4 warnings "error while running plantuml" del build completo.
  Verificación canónica pendiente en un entorno con bootstrap completo.

## Changed

- `source/gestion/pm/iniciativas/index.rst` — registrada la nueva
  iniciativa bajo "Iniciativas cerradas" (orden alfabético) y
  `:ultimo_cambio:` actualizado.
- `.thyrox/context/focus.md` y `now.md` — estado de sesión.

## Aceptado / no fixeado

- Eliminación de las 28 ramas `feature/*` mergeadas de iact-docs:
  **bloqueada por el entorno** (HTTP 403 al push de deleción). Comando
  listo en `analyze/ramas-y-prs/estado-ramas-prs-multirepo.md` para
  ejecutar desde un clon con permisos.

- F-03..F-07 quedan como iniciativas derivadas **propuestas**; su
  apertura es decisión del ejecutor (I-011).
- La auditoría no incluye tests por UC ni IACT-db (out-of-scope
  declarado en el alcance).

## Status de promoción a CHANGELOG.md raíz

- Al merge a `main` con bump: promover una entrada "Added — auditoría
  de implementación UC docs→api/ui (88 UCs, 0 gaps, hallazgos
  F-01..F-07)".
