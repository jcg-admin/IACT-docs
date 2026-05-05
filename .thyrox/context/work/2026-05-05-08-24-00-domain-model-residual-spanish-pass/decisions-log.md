```yml
created_at: 2026-05-05 08:24:00
updated_at: 2026-05-05 08:24:00
project: IACT-docs
work_package: 2026-05-05-08-24-00-domain-model-residual-spanish-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Decisions Log — Residual Spanish Pass

## D-01 — ETL → Pipeline (CNST-033 §8.2 estricto)

**Cita literal CNST-033 §8.2:** ``etl / estado_etl → pipeline (sin acronimo)``.

**Decisión:** todo ``ETL`` / ``Etl`` / ``etl`` en
identificadores se traduce a ``Pipeline`` / ``pipeline``.

- ``ETLEjecucion`` → ``PipelineExecution``
- ``ETLLog`` → ``PipelineLog``
- ``etl-ejecucion.rst`` → ``pipeline-execution.rst``
- ``etl-log.rst`` → ``pipeline-log.rst``
- ``etl_runs`` (tabla SQL) → ``pipeline_runs``

**Excepción:** la sigla ``ETL`` en **prosa narrativa**
(no en código/identificadores) puede mantenerse como
sigla del dominio cuando el contexto es genérico
("proceso ETL"). En todo identificador de código se
aplica la traducción.

## D-02 — Casing PEP-8 para acrónimos embebidos

``ETLLog`` → ``PipelineLog`` (no ``ETL_Log`` ni
``ETLLOG``). PascalCase canónico.

Los identificadores que contienen ``IVR`` mantienen el
casing ``Ivr`` (PEP-8): ``IvrRepo``, no ``IVRRepo``
(per D-04 del WP predecesor).

## D-03 — Sweep mecanizado en commit atómico

Mismo patrón D-06 del predecesor: rename + content
sweep en un commit. Pre-render PlantUML para validar.

## D-04 — Bounded context

``etl-ejecucion.rst`` declara
``:bounded_context: PipelineETL`` (ya en inglés
parcial). ``etl-log.rst`` declara ``:bounded_context: Logs``.

**Decisión:** unificar ``PipelineETL`` → ``Pipeline``
(eliminar redundancia "Pipeline ETL" que es tautología
post-D-01). ``Logs`` se mantiene.
