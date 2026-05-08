.. _uc-pip-04-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades escritas
======================

- **PipelineExecution** — nuevo registro creado por el Disparador ETL
  al iniciar el reintento. Campos adicionales respecto al flujo
  normal:

::

   PipelineExecution (nuevo registro de reintento):
     estado           : IN_PROGRESS  (al inicio)
     executed_by    : 'manual'
     source_table     : nombre de la tabla fuente del trimestre
     trimestre        : trimestre que se esta reprocesando

- **RegistroAuditoria** — evento de auditoria generado por el
  sistema al ejecutar el reintento. Registra quien solicito
  el reprocesamiento y en que condiciones.

7.2 Restricciones de escritura
================================

- Solo puede existir una PipelineExecution con ``estado = 'IN_PROGRESS'``
  a la vez. El Disparador ETL rechaza el reintento si detecta
  una ejecucion activa.
- El campo ``executed_by = 'manual'`` distingue los reintentos
  manuales de las ejecuciones programadas por el scheduler.
