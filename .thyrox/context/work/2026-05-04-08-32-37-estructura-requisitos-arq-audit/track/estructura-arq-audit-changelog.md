```yml
created_at: 2026-05-04 14:30:00
project: IACT-docs
work_package: 2026-05-04-08-32-37-estructura-requisitos-arq-audit
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Borrador
```

# Changelog — WP estructura-requisitos-arq-audit

## Added

- `source/arquitectura-tecnica/use-case-view/mod-*.rst` — 13 canonical UC module diagrams replacing 80 per-UC entries (Bloque A)
- `source/arquitectura-tecnica/domain-model/` — 36 files: index, overview, 8 bc-*.rst BC diagrams, 26 canonical class files with full attributes/methods/enums per DT-01 (Bloque B)
- `source/arquitectura-tecnica/deploy-view/deploy-estandar.rst`, `deploy-auth-cache.rst`, `deploy-etl.rst` — 3 canonical deployment variants (Bloque C)
- `source/arquitectura-tecnica/design-view/mod-*.rst` — 12 canonical sequence diagrams with STD-011 CamelCase participants and canonical class names (Bloque D)
- `source/arquitectura-tecnica/implementation-view/mod-*.rst` — 12 canonical component diagrams with 5-layer stack per module (Bloque E)
- `source/arquitectura-tecnica/process-view/proc-*.rst` — 4 canonical concurrency patterns: ETL pipeline, alertas paralelas, sesiones JWT, dashboard (Bloque F)
- `source/requisitos/reglas-negocio/rbac/` — new directory with index + 4 RBAC business spec files moved from arquitectura-tecnica (Bloque G)
- `source/normativa/gobernanza/raci-rbac/` — RACI matrices moved from arquitectura-tecnica (Bloque G)

## Changed

- `source/arquitectura-tecnica/use-case-view/index.rst` v2.0.0 — toctree from 80 per-UC entries to 13 mod-*.rst (Bloque A)
- `source/arquitectura-tecnica/domain-model/index.rst` v2.0.0 — BC-organized toctree, 26 canonical classes (Bloque B)
- `source/arquitectura-tecnica/modelo-dominio-iact.rst` — updated toctree from bounded-contexts/bounded-context-* to domain-model/bc-* (Bloque B)
- `source/arquitectura-tecnica/deploy-view/index.rst` v2.0.0 — 3 variant entries (Bloque C)
- `source/arquitectura-tecnica/design-view/index.rst` v2.0.0 — 12 canonical module entries (Bloque D)
- `source/arquitectura-tecnica/implementation-view/index.rst` v2.0.0 — 12 canonical module entries (Bloque E)
- `source/arquitectura-tecnica/process-view/index.rst` v2.0.0 — 4 canonical concurrency entries (Bloque F)
- `source/arquitectura-tecnica/rbac/modelo-rbac-iact/index.rst` — toctree updated (removed moved files, kept ARCH files), cross-refs added (Bloque G, T-040)
- `source/arquitectura-tecnica/rbac/index.rst` — raci-rbac-iact toctree entry replaced with seealso cross-ref to new location (T-046 fix)
- `source/normativa/gobernanza/index.rst` — added RACI RBAC toctree section (Bloque G)
- `source/requisitos/reglas-negocio/index.rst` — added RBAC toctree section (Bloque G)
- 8x `source/arquitectura-tecnica/modulos/*/index.rst` — removed `casos-uso` toctree entries (Bloque H)
- 4 traceability fixes applied (trazabilidad-decisiones.md):
  - `modulos/user-identity/diagramas/clases-modulo-identidad.rst` — canonical attributes (CRITICAL)
  - `modulos/alerts/diagramas/ciclo-vida-alerta.rst` — AlertState enum (HIGH)
  - `uc-auth-01/datos-involucrados.rst` — removed closed_at/close_reason (MEDIUM)
  - `uc-perm-06/diagramas-uml/diagrama-de-cascade.rst` — removed AccessGroupFunction (MEDIUM)

## Removed

- `source/arquitectura-tecnica/uc-module-view/` — 15 files (Bloque A)
- `source/arquitectura-tecnica/use-case-view/` — 80 per-UC entries (Bloque A)
- `source/arquitectura-tecnica/bounded-contexts/` — 10 files (Bloque B)
- `source/arquitectura-tecnica/domain-model/` — 160 per-UC class files (Bloque B)
- `source/arquitectura-tecnica/deploy-view/` — 80 per-UC deploy files (Bloque C)
- `source/arquitectura-tecnica/design-view/` — 160 per-UC files (80 secuencia + 80 comunicacion) (Bloque D)
- `source/arquitectura-tecnica/implementation-view/` — 80 per-UC files (Bloque E)
- `source/arquitectura-tecnica/process-view/` — 80 per-UC files (Bloque F)
- 8x `source/arquitectura-tecnica/modulos/*/casos-uso.rst` — redundant UC lists (Bloque H)

## Build status

```
make html
build succeeded.
WARN: 15 (pre-existing toc.not_included for _metodologia-aplicacion/ and uml-system-view/)
WP-introduced warnings: 0
```

## Status de promocion a CHANGELOG.md raiz

Cambios candidatos para siguiente merge a main:
- Restructura architecture views (use-case, domain-model, deploy, design, implementation, process)
- Domain reclassification: RBAC business specs → requisitos, RACI → normativa
- Traceability fixes: canonical class attributes in 4 diagrams
