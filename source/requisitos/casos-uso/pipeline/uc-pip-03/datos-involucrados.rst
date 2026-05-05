.. _uc-pip-03-parte-07:

================================
Parte 7 — Datos involucrados
================================

7.1 Entidades
=============

- **PipelineExecution** — registro de la ultima ejecucion exitosa del
  Servicio ETL por trimestre. Determina la frescura de los datos.
- **DisponibilidadDatos** — proyeccion de lectura calculada a
  partir de PipelineExecution y el conteo de la Base Analitica IVR.

7.2 Modelo PipelineExecution (subset relevante)
==========================================

::

   PipelineExecution:
     trimestre        : codigo del trimestre (ej: Q3_25)
     finished_at    : timestamp de la ultima actualizacion
     estado           : exitoso  (filtro de este UC)
     base_records   : filas en Base Analitica IVR tras el ETL

7.3 Proyeccion DisponibilidadDatos
====================================

No es una entidad persistida. Es calculada en tiempo de consulta:

::

   DisponibilidadDatos:
     trimestre              : codigo del trimestre
     ultima_actualizacion   : timestamp de finished_at
     registros_disponibles  : base_records de la ultima ejecucion
     minutos_desde_etl      : diferencia desde ultima_actualizacion
     estado_frescura        : fresco | degradado | vencido

Umbrales de frescura (configurables):

- ``fresco``:   ``minutos_desde_etl`` < 720 (12 horas)
- ``degradado``: 720 <= ``minutos_desde_etl`` < 1440 (24 horas)
- ``vencido``:  ``minutos_desde_etl`` >= 1440

7.4 Indices de consulta
=======================

- ``PipelineExecution(estado, trimestre, started_at DESC)`` —
  para obtener la ultima ejecucion exitosa por trimestre.
