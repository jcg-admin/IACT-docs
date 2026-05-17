```yml
project: IACT-docs
work_package: 2026-05-08-22-54-19-dag-completion-loop
created_at: 2026-05-08 22:54:19
current_phase: Phase 10 — IMPLEMENT (loop ejecutorio)
author: NestorMonroy
status: Borrador
```

# WP — DAG completion loop

## Objetivo

Completar el DAG de vistas arquitectonicas hasta que **los 7
criterios de la checklist pasen juntos en una sola pasada**.
Loop ejecutorio multi-iteracion con build strict entre cada
iteracion.

## Contexto

Decisiones del ejecutor (3 tensiones resueltas):

- **T1** — process-view / deploy-view / system-view → restructurar en directorios (19 archivos planos a directorios). Reemplaza la decision del WP `process-deploy-view-rename` que cerro con flat como correcto.
- **T2** — `impl-caller/operator/supervision.rst` → renombrar para eliminar prefijo `impl-`.
- **T3** — `modulos/*/diagramas/*` (13 archivos `componentes-*`, `secuencia-*`, `clases-*`) → renombrar a content-based.

## Plan de loop

| Iter | Trabajo | Criterios validados |
|------|---------|---------------------|
| 1 | process-view restructure (4 archivos → 4 dirs/index.rst) | 1, 2, 6 |
| 2 | deploy-view restructure (3 archivos → 3 dirs) | 1, 2, 6 |
| 3 | system-view restructure (12 archivos → 12 dirs) | 1, 2, 6 |
| 4 | implementation-view rename `impl-*.rst` (3) | 1, 2, 6 |
| 5 | modulos/*/diagramas/* rename (13) | 2, 6 |
| 6 | modulos/ coexistencia documentada | 5, 6 |
| 7 | uml-14/relaciones-dependencia-iact.rst | 4, 6 |
| 8 | verificacion final — 7 criterios juntos | 1..7 |

## Criterio de salida

Los 7 criterios devuelven el valor esperado en una pasada
secuencial al final, sin que ninguna iteracion previa haya
sido revertida por una posterior.

## Refs

- WP previo: `2026-05-08-21-46-06-etl-ivr-flow-v2-doc/track/deferred-supervisor-rename.md` (Alternativa 2 aplicada).
- WP previo: `2026-05-08-21-28-42-process-deploy-view-rename` (decision flat — REVERTIDA por T1).
