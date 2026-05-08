```yml
project: IACT-docs
work_package: 2026-05-05-08-24-00-domain-model-residual-spanish-pass
created_at: 2026-05-05 08:24:00
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-08-17-04-cnst-033-system-design-view-pass
target: Eliminar identificadores castellanos residuales del domain-model (ETLEjecucion, ETLLog, EstadoEjecucion)
```

# WP — Domain Model Residual Spanish Pass

## Trigger

Hallazgo D-05 del WP ``cnst-033-system-design-view-pass``:
``etl-ejecucion.rst`` y ``etl-log.rst`` violan CNST-033:

- Nombre de archivo en castellano (``ejecucion``).
- Clase ``ETLEjecucion`` (acrónimo + castellano).
- Atributos castellanos (``tabla_origen``, ``iniciado_en``,
  ``estado``, ``mensaje_error``, ``ejecutado_por``,
  ``registros_base``).
- Métodos castellanos (``es_exitosa``, ``es_fallida``,
  ``duracion_segundos``).
- Enum ``EstadoEjecucion`` con valores castellanos.

## Alcance

| Antes | Después |
|-------|---------|
| ``etl-ejecucion.rst`` / ``ETLEjecucion`` | ``pipeline-execution.rst`` / ``PipelineExecution`` |
| ``etl-log.rst`` / ``ETLLog`` | ``pipeline-log.rst`` / ``PipelineLog`` |
| ``EstadoEjecucion`` | ``ExecutionStatus`` |
| Atributos: ``tabla_origen``, ``trimestre``, ``iniciado_en``, ``finalizado_en``, ``estado``, ``registros_base``, ``mensaje_error``, ``ejecutado_por`` | ``source_table``, ``period``, ``started_at``, ``finished_at``, ``status``, ``base_records``, ``error_message``, ``executed_by`` |
| Métodos: ``es_exitosa()``, ``es_fallida()``, ``duracion_segundos()`` | ``is_successful()``, ``is_failed()``, ``duration_seconds()`` |
| Enum values: ``en_ejecucion``, ``exitoso``, ``fallido`` | ``IN_PROGRESS``, ``SUCCEEDED``, ``FAILED`` |

## Justificación

CNST-033 §8.2 explícito: ``etl → pipeline``. Aplicado
de forma estricta. Renombrar a ``Pipeline*`` también
alinea con la convención del corpus (``ServicioETL``
ya se renombra a ``PipelineService`` en el WP
predecesor).

## Riesgos

- ETLEjecucion: 128 referencias en source/.
- ETLLog: 45 referencias en source/.
- Total ~173 ocurrencias a corregir.
- Mitigación: sweep mecanizado.

## Decisiones tomadas

Ver ``decisions-log.md``.
