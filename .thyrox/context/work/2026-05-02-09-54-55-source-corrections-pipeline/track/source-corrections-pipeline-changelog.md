```yml
created_at: 2026-05-02 09:54:55
project: IACT-docs
work_package: 2026-05-02-09-54-55-source-corrections-pipeline
author: NestorMonroy
```

# WP Changelog — source-corrections-pipeline

## Added

- discover/source-corrections-pipeline-analysis.md — gap analysis
  completo entre source/ y la arquitectura real descubierta en el WP
  previo (pipeline-uc-deepening). 6 gaps documentados:
  - Gap 1: etl-pipeline.rst describe Python classes → realidad son SPs
  - Gap 2: modelo-dual.rst pone analytics en PostgreSQL → realidad es MariaDB
  - Gap 3: vis-reports DailyMetrics Django model → no existe, son CALL sp_rpt_*
  - Gap 4: br-016 sin implementación concreta de abandono (VACIO/cliente_colgo/SinOpcion_Cabecera)
  - Gap 5: UC-PIP-01..04 datos-involucrados e implementacion-tecnica incorrectos
  - 10 archivos a editar, 3 preguntas abiertas antes de editar.

## Status de promoción a CHANGELOG.md raíz
Pendiente — el WP está en Phase 1 DISCOVER.
