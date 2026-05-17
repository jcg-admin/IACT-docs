```yml
created_at: 2026-05-08 21:50:00
project: IACT-docs
work_package: 2026-05-08-21-28-42-process-deploy-view-rename
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — process-deploy-view-rename

## [1.0.0] — 2026-05-08

### Resumen

Rename retroactivo de archivos en `process-view/` y `deploy-view/`
de naming basado en tipo de artefacto (`proc-*`, `deploy-*`) a
naming basado en contenido. Aplica el mismo principio CLEAN_CODE
§6.2 que motivo el rename retroactivo de DesignView en el WP
anterior. Sin migracion estructural — la estructura flat era
correcta porque ProcessView se organiza por patron de
concurrencia (no por modulo) y DeployView por variante de
topologia (no por modulo).

### Renamed (7 git mv)

#### ProcessView (4 archivos)

| Antes | Despues |
|---|---|
| `proc-alertas-paralelas.rst` | `alert-evaluation-concurrency.rst` |
| `proc-dashboard-concurrencia.rst` | `realtime-dashboard-concurrency.rst` |
| `proc-etl-pipeline.rst` | `etl-pipeline-concurrency.rst` |
| `proc-sesiones-jwt.rst` | `jwt-session-synchronization.rst` |

#### DeployView (3 archivos)

| Antes | Despues |
|---|---|
| `deploy-estandar.rst` | `standard-topology.rst` |
| `deploy-auth-cache.rst` | `auth-cache-topology.rst` |
| `deploy-etl.rst` | `etl-pipeline-topology.rst` |

### Cross-refs migration

- `process-view/index.rst` toctree actualizado (4 entries)
- `deploy-view/index.rst` toctree actualizado (3 entries)
- `implementation-view/impl-caller.rst` ref externa
  re-targeteada de `process-view/proc-etl-pipeline` a
  `process-view/etl-pipeline-concurrency`

### Verification

- 0 cross-refs huerfanas (verificado por
  `grep -rE ":doc:.*proc-|deploy-(estandar|auth-cache|etl)\``)
- 0 warnings en archivos renombrados de mi WP
- Build strict sphinx detecto 180 warnings PRE-EXISTENTES en
  archivos NO tocados por este WP (resumen-salud-assembler,
  perspectivas/, rbac/, etc.) — issues de title-overline,
  bullet-list-unindent que el cache de doctrees del Sphinx
  habia enmascarado en builds previos. Estos warnings son
  deuda historica del corpus, no consecuencia de este WP.
  Documentados como hallazgo H-01.

### Hallazgos (H-XX)

- **H-01 (corpus-wide):** 180 warnings docutils pre-existentes
  en ~150+ archivos no tocados por este WP. Categorias:
  - Title underline too short: 149
  - Title overline too short: 9
  - Bullet/Block quote unindent: 21
  - Other: 1
  Surface-detected al hacer `find ... -exec sed ... {} +`
  porque actualizo mtimes y forzo re-procesamiento de archivos
  cacheados por Sphinx. Recomendacion: WP futuro
  `corpus-docutils-cleanup` para limpiar deuda historica.
- **H-02 (modulos/ overlap):** analisis preliminar concluyo
  que `arquitectura-tecnica/modulos/` contiene contenido
  COMPLEMENTARIO a DesignView/ImplementationView (proposito,
  responsabilidades, dependencias, restricciones del modulo),
  no duplicacion. Coexistencia legitima. system-view rename
  puede proceder independientemente del analisis de modulos.

### Commits del WP

1. (este commit) — todo el batch del WP

### Refs

- WP `design-view-restructure` + `implementation-view-restructure`
  precedentes — pattern de rename validado.
- CLEAN_CODE_NAMING_PRINCIPLES.md §6.2.
