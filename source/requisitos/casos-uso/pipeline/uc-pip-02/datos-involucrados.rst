.. _uc-pip-02-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades
=============

- **PipelineExecution** — registro de una ejecucion del Servicio ETL.
  Solo los registros con ``estado = 'fallido'`` son relevantes
  para este UC.

7.2 Modelo PipelineExecution (subset relevante)
==========================================

::

   PipelineExecution:
     id               : identificador unico de la ejecucion
     source_table     : nombre de la tabla fuente procesada
     trimestre        : codigo del trimestre (ej: Q3_25)
     started_at      : timestamp de inicio de la ejecucion
     finished_at    : timestamp de finalizacion
     estado           : fallido  (filtro de este UC)
     error_message    : descripcion del error capturado
     executed_by    : 'scheduler' | 'manual'

7.3 Indices de consulta
=======================

- ``PipelineExecution(estado, started_at DESC)`` — para listar
  ejecuciones fallidas ordenadas por fecha descendente.
- ``PipelineExecution(trimestre)`` — para filtrar por trimestre.

7.4 Notas de contenido
=======================

El campo ``error_message`` contiene el mensaje de excepcion o
el codigo de error retornado por el Servicio ETL. No contiene
stack traces del sistema interno ni datos de clientes.
