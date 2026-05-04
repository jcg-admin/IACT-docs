```yml
created_at: 2026-05-04 02:16:24
project: IACT-docs
work_package: 2026-05-04-02-11-54-uml-alias-naming-fix
phase: Phase 11 — TRACK
author: NestorMonroy
status: En progreso
```

# Changelog — uml-alias-naming-fix

---

## Added

- `source/normativa/estandares/std-011-alias-diagramas-uml.rst` — STD_011 v1.0.0:
  estándar que formaliza D-ALIAS-001..003; define alias auto-documentados para
  todos los diagramas PlantUML del proyecto IACT.

- `.thyrox/context/work/2026-05-04-02-11-54-uml-alias-naming-fix/discover/uml-alias-naming-analysis.md` —
  análisis de violaciones en `diagramas-uml-sistema.rst` y UCs.

- `.thyrox/context/work/2026-05-04-02-11-54-uml-alias-naming-fix/discover/decisions.md` —
  decisiones D-ALIAS-001, D-ALIAS-002, D-ALIAS-003.

- `source/normativa/estandares/index.rst` — STD_011 agregado al toctree.

## Changed

- `source/arquitectura-tecnica/diagramas-uml-sistema.rst` — corregidos 13 aliases
  crípticos (`as RVG`, `as QSG`, `as PAG`, `as UAG`, `as AUG`, `as SCH`,
  `as USR`, `as AE`, `as DE`, `as SR`, `as SRP`, `as FAIL`, `as USR` object)
  → aliases auto-documentados conforme D-ALIAS-001..003.

- `source/arquitectura-tecnica/diagramas-uc-por-modulo.rst` — corregidos aliases
  crípticos en diagramas UC por módulo.

- `source/requisitos/casos-uso/**/diagramas-uml.rst` — sweep de aliases `as U`,
  `as F`, `as A`, `as B` etc. en ~80 UCs.

## Status de promoción a CHANGELOG.md raíz

Pendiente hasta merge a `main`. Entradas a promover:
- STD_011 (normativa/estandares)
- Correcciones de alias en diagramas de arquitectura y UCs
