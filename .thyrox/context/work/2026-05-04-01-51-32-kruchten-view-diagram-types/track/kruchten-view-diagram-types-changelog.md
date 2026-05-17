```yml
created_at: 2026-05-04 01:51:32
updated_at: 2026-05-04 01:51:32
project: IACT-docs
work_package: 2026-05-04-01-51-32-kruchten-view-diagram-types
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: En progreso
```

# Changelog — kruchten-view-diagram-types

## Added

- `discover/kruchten-view-diagram-types-analysis.md` — analisis de
  cobertura de diagramas por vista, gap analysis, patrones canonicos.
- `discover/decisions.md` — 6 decisiones autonomas (D-KRUCHTEN-001..006).
- `add-diagrams.py` — script de implementacion para agregar diagramas
  faltantes y corregir nombres de participantes/nodos.

## Changed

- **Restructura de directorios Kruchten** (D-KRUCHTEN-001, D-KRUCHTEN-002):
  - 480 archivos movidos de `arquitectura-tecnica/uc/{View}/uc-{mod}-{nn}.rst`
    a `arquitectura-tecnica/{View}/{mod}-{nn}.rst`
  - `arquitectura-tecnica/uc/index.rst` → `arquitectura-tecnica/vistas-kruchten.rst`
  - `arquitectura-tecnica/index.rst`: ruta actualizada de `uc/index` a `vistas-kruchten`
  - Metadata `subdominio` en todos los archivos: `uc/{View}` → `{View}`
  - Metadata `version` en los 6 index.rst: `1.0.0` → `1.1.0`
  - Toctrees en los 6 index.rst: entradas `uc-{mod}-{nn}` → `{mod}-{nn}`

## Status de promocion a CHANGELOG.md raiz

Pendiente — se promovera en merge a main.
