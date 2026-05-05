```yml
created_at: 2026-05-04 20:02:46
project: THYROX
work_package: 2026-05-04-20-02-46-broken-refs-diagramas-tiempo
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
```

# Changelog — WP broken-refs-diagramas-tiempo (R-08)

## Added

- `discover/broken-refs-diagramas-tiempo-analysis.md` — análisis de causa
  raíz de las 6 refs rotas en `diagramas-tiempo.rst`.
- `track/broken-refs-diagramas-tiempo-changelog.md` — este changelog.
- `logs/build-after-fix-2026-05-04-20-02-46.txt` — log de build incremental
  post-fix para verificar ausencia de warnings R-08.

## Fixed

- `source/requisitos/_metodologia-aplicacion/diagramas-tiempo.rst` — 6
  `:doc:` refs con bare names reemplazadas por rutas absolutas
  `/requisitos/_metodologia-aplicacion/{nombre}/index`. Targets verificados
  existentes (R-08).

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a `main`. La entrada de CHANGELOG.md raíz se construirá
desde este archivo al hacer merge con bump de versión.
