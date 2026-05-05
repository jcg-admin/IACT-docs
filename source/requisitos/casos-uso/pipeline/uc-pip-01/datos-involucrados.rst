.. _uc-pip-01-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades
=============

- **PipelineExecution** — registro de una ejecucion del Servicio ETL.
- **ResumenSalud** — proyeccion de lectura construida a partir de
  los ultimos registros de PipelineExecution.

7.2 Modelo PipelineExecution
=======================

::

   PipelineExecution:
     id               : identificador unico de la ejecucion
     source_table     : nombre de la tabla fuente procesada
     trimestre        : codigo del trimestre (ej: Q3_25)
     started_at      : timestamp de inicio de la ejecucion
     finished_at    : timestamp de finalizacion (nulo si aun corre)
     estado           : IN_PROGRESS | exitoso | fallido
     base_records   : filas en Base Analitica IVR tras el ETL
     error_message    : descripcion del error (nulo si exitoso)
     executed_by    : 'scheduler' | 'manual'

7.3 Indices de consulta
=======================

- ``PipelineExecution(estado, started_at DESC)`` — para obtener
  las ultimas ejecuciones por estado.
- ``PipelineExecution(trimestre)`` — para filtrar por trimestre.

7.4 Proyeccion ResumenSalud
============================

El ResumenSalud no es una entidad persistida. Es una proyeccion
de lectura calculada en tiempo de consulta a partir de los
registros de PipelineExecution:

::

   ResumenSalud:
     ultima_ejecucion_exitosa : PipelineExecution o nulo
     ejecucion_en_curso       : PipelineExecution o nulo
     ultima_ejecucion_fallida : PipelineExecution o nulo
     total_exitosas_24h       : entero
     total_fallidas_24h       : entero
     estado_general           : ok | degradado | critico
